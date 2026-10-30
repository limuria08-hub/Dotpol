"""P2.04 neutral, reproducible election arithmetic on existing P2.01 result rows.

No prediction, persuasion, voter profiling, external lookup, or alternate DB.
Calculations are derived solely from a user's *unverified* source-declared
totals, never presented as official results or actual turnout.
"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP, localcontext

from .election_results import get_import
from .political_identity import get_entity
from .store import InvalidInput, Store

METHOD = "dotpol-election-metrics-v1"
FOUR_DP = Decimal("0.0001")


def _percent(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        raise InvalidInput("Cannot calculate a percentage without a positive denominator")
    # Decimal avoids platform-dependent float rounding and exact-vote drift.
    with localcontext() as ctx:
        ctx.prec = 40
        percent = (Decimal(numerator) * 100 / Decimal(denominator)).quantize(
            FOUR_DP, rounding=ROUND_HALF_UP
        )
    return format(percent, ".4f")


def _contest_metrics(rows: list[dict], provenance: dict) -> dict:
    """Calculate one contest only; inputs are already validated P2.01 rows."""
    rows = sorted(rows, key=lambda x: (x["source_line"], x["id"]))
    first = rows[0]
    denominator = first["total_valid_votes"]
    counted = sum(row["votes"] for row in rows)
    if counted > denominator or any(row["total_valid_votes"] != denominator for row in rows):
        raise InvalidInput("Stored candidate rows have inconsistent declared totals")
    parties: dict[str, int] = defaultdict(int)
    candidate_metrics = []
    for row in rows:
        parties[row["party_id"]] += row["votes"]
        candidate_metrics.append({
            "result_id": row["id"], "candidate_name": row["candidate_name"],
            "party_id": row["party_id"], "source_line": row["source_line"],
            "votes": row["votes"], "vote_share_pct": _percent(row["votes"], denominator),
        })
    ranked = sorted(rows, key=lambda x: (-x["votes"], x["source_line"], x["id"]))
    highest = ranked[0]["votes"]
    tied_leaders = [row["id"] for row in ranked if row["votes"] == highest]
    # A leader is NOT an official election winner; the source may be incomplete.
    runner = ranked[1] if len(ranked) > 1 else None
    margin_votes = highest - runner["votes"] if runner is not None else None
    unrepresented = denominator - counted
    return {
        "election_id": first["election_id"],
        "constituency_id": first["constituency_id"],
        "boundary_version_id": first["boundary_version_id"],
        "year": first["year"],
        "declared_valid_votes": denominator,
        "sum_imported_candidate_votes": counted,
        "unrepresented_votes": unrepresented,
        "matches_declared_total": unrepresented == 0,
        "candidate_count": len(rows),
        "candidates": candidate_metrics,
        "party_groups": [
            {"party_id": party, "votes": votes, "vote_share_pct": _percent(votes, denominator)}
            for party, votes in sorted(parties.items())
        ],
        "leading_result_ids": tied_leaders,
        "leading_votes": highest,
        "lead_is_tied": len(tied_leaders) > 1,
        "margin_over_next_candidate_votes": margin_votes,
        "margin_over_next_candidate_pct_points":
            _percent(margin_votes, denominator) if margin_votes is not None else None,
        "official_winner": None,
        "turnout_pct": None,
        "turnout_reason": "The source has no registered-elector or ballots-cast denominator.",
        "provenance": provenance,
        "cautions": [
            "All figures derive from uploaded CSV, not independently verified official returns.",
            "Leading candidate is descriptive only, not a certified winner.",
            "Declared totals do not establish complete or independently verified ballot records.",
            "Party labels, source dates and electoral boundaries are not officially reconciled.",
        ],
    }


def analyze_import(store: Store, project_id: str, import_id: str) -> dict:
    """Read an existing P2.01 import; never silently use withdrawn evidence."""
    data = get_import(store, project_id, import_id)
    meta = data["import"]
    if meta["source_status"] != "active":
        raise InvalidInput("Cannot derive new election metrics from a withdrawn source")
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in data["rows"]:
        key = (
            row["election_id"], row["constituency_id"],
            row["boundary_version_id"], row["year"],
        )
        grouped[key].append(row)
    provenance = {
        "project_id": project_id, "import_id": import_id,
        "source_id": meta["source_id"], "source_sha256": meta["source_sha256"],
        "source_name": meta["source_name"], "source_status": meta["source_status"],
        "source_verification": "user-uploaded-unverified",
        "schema_version": meta["schema_version"], "imported_at": meta["imported_at"],
    }
    contests = [_contest_metrics(rows, provenance) for _, rows in sorted(grouped.items())]
    return {
        "method": METHOD, "project_id": project_id, "import_id": import_id,
        "source_verified": False, "official_result": False,
        "contest_count": len(contests), "contests": contests,
        "calculation": {
            "vote_share_pct": "100 * candidate_votes / source_declared_total_valid_votes",
            "party_share_pct": "100 * sum(group_votes) / source_declared_total_valid_votes",
            "lead_margin_pct_points": "100 * (top_votes - second_votes) / source_declared_total_valid_votes",
            "rounding": "Decimal ROUND_HALF_UP to 4 places; never floating point",
            "turnout": "unavailable (registered electors / ballots cast absent)",
        },
    }


def _election_family(store: Store, project_id: str, election_id: str, year: int) -> str:
    label = get_entity(store, project_id, election_id)["name"]
    suffix = f" ({year})"
    # The importer creates its P1 election ID using this convention.
    if not label.endswith(suffix):
        raise InvalidInput("Election label cannot be compared across years")
    return label[:-len(suffix)].casefold()


def compare_imports(store: Store, project_id: str, earlier_id: str,
                    later_id: str) -> dict:
    """Descriptive party share change only where declared boundaries match.

    Does not assume a missing party received zero votes. Labels are user
    declared; same boundary label is not proof of matching actual geometry.
    """
    if earlier_id == later_id:
        raise InvalidInput("Historical comparison requires two distinct imports")
    earlier = analyze_import(store, project_id, earlier_id)
    later = analyze_import(store, project_id, later_id)
    before = {}
    after = {}
    for contest in earlier["contests"]:
        key = (contest["constituency_id"], contest["boundary_version_id"])
        before.setdefault(key, []).append(contest)
    for contest in later["contests"]:
        key = (contest["constituency_id"], contest["boundary_version_id"])
        after.setdefault(key, []).append(contest)
    comparisons = []
    skipped = []
    for key in sorted(set(before) | set(after)):
        old = before.get(key, [])
        new = after.get(key, [])
        if len(old) != 1 or len(new) != 1:
            skipped.append({
                "constituency_id": key[0], "boundary_version_id": key[1],
                "reason": "Missing or ambiguous one-to-one contest match; no change inferred.",
            })
            continue
        old, new = old[0], new[0]
        if old["year"] >= new["year"]:
            raise InvalidInput("Historical comparison requires strictly increasing election years")
        if _election_family(store, project_id, old["election_id"], old["year"]) != _election_family(
            store, project_id, new["election_id"], new["year"]
        ):
            skipped.append({
                "constituency_id": key[0], "boundary_version_id": key[1],
                "reason": "Election labels differ; contest cannot be assumed comparable.",
            })
            continue
        previous = {x["party_id"]: x for x in old["party_groups"]}
        current = {x["party_id"]: x for x in new["party_groups"]}
        changes = []
        for party in sorted(set(previous) | set(current)):
            x, y = previous.get(party), current.get(party)
            # Absent party != zero-vote party. Do not impute.
            comparable = x is not None and y is not None
            if comparable:
                with localcontext() as ctx:
                    ctx.prec = 40
                    change = (
                        (Decimal(y["votes"]) * 100 / Decimal(new["declared_valid_votes"]))
                        - (Decimal(x["votes"]) * 100 / Decimal(old["declared_valid_votes"]))
                    ).quantize(FOUR_DP, rounding=ROUND_HALF_UP)
                change_str = format(change, ".4f")
            else:
                change_str = None
            changes.append({
                "party_id": party,
                "earlier_votes": x["votes"] if x is not None else None,
                "later_votes": y["votes"] if y is not None else None,
                "earlier_share_pct": x["vote_share_pct"] if x is not None else None,
                "later_share_pct": y["vote_share_pct"] if y is not None else None,
                "share_change_pct_points": change_str,
                "comparable": comparable,
            })
        comparisons.append({
            "constituency_id": key[0], "boundary_version_id": key[1],
            "earlier_year": old["year"], "later_year": new["year"],
            "earlier_import_id": earlier_id, "later_import_id": later_id,
            "earlier_source_sha256": old["provenance"]["source_sha256"],
            "later_source_sha256": new["provenance"]["source_sha256"],
            "party_share_changes": changes,
            "boundary_match_type": "same_user_declared_boundary_label_only",
            "officially_comparable": False,
        })
    return {
        "method": METHOD, "project_id": project_id,
        "source_verified": False,
        "comparisons": comparisons, "skipped": skipped,
        "caution": "Historical change is descriptive; source completeness, party aliases and physical boundary equality are not verified.",
    }
