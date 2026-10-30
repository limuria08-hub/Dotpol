"""P2.04 exact vote arithmetic: no turnout invention or official-winner inference."""
import pytest
from fastapi.testclient import TestClient

from app import create_app
from dotpol_platform.store import Store, InvalidInput, NotFound
from dotpol_platform.election_results import initialize, import_results, COLUMNS
from dotpol_platform.election_metrics import analyze_import, compare_imports, _percent

HEADER = ",".join(COLUMNS) + "\n"


def fixture(store, project, name, body):
    source = store.import_source(project, name, "csv", HEADER + body, origin="synthetic-demo")
    data = import_results(store, project, source["id"])
    return data["import"]["id"], source["id"]


def test_exact_shares_and_margin_with_incomplete_source(tmp_path):
    db = Store(tmp_path / "data.sqlite3")
    initialize(db)
    project = db.create_project("Public aggregate analysis")["id"]
    import_id, source_id = fixture(
        db, project, "partial.csv",
        "General Election,2024,North,Version 1,One,Party A,600,1000\n"
        "General Election,2024,North,Version 1,Two,Party B,300,1000\n",
    )
    result = analyze_import(db, project, import_id)
    assert result["method"] == "dotpol-election-metrics-v1"
    assert not result["official_result"] and not result["source_verified"]
    assert result["contest_count"] == 1
    contest = result["contests"][0]
    assert contest["declared_valid_votes"] == 1000
    assert contest["sum_imported_candidate_votes"] == 900
    assert contest["unrepresented_votes"] == 100
    assert not contest["matches_declared_total"]
    assert [r["vote_share_pct"] for r in contest["candidates"]] == ["60.0000", "30.0000"]
    assert contest["margin_over_next_candidate_votes"] == 300
    assert contest["margin_over_next_candidate_pct_points"] == "30.0000"
    assert contest["official_winner"] is None
    assert contest["turnout_pct"] is None
    assert "no registered-elector" in contest["turnout_reason"]
    assert [r["source_line"] for r in contest["candidates"]] == [2, 3]
    assert contest["provenance"]["source_id"] == source_id


def test_tie_and_single_candidate_do_not_fabricate_winners(tmp_path):
    db = Store(tmp_path / "d.sqlite3")
    initialize(db)
    p = db.create_project("Tests")["id"]
    tie, _ = fixture(
        db, p, "tie.csv",
        "General,2024,A,B1,Alice,A,450,900\n"
        "General,2024,A,B1,Bob,B,450,900\n",
    )
    c = analyze_import(db, p, tie)["contests"][0]
    assert c["lead_is_tied"] and len(c["leading_result_ids"]) == 2
    assert c["margin_over_next_candidate_votes"] == 0
    assert c["margin_over_next_candidate_pct_points"] == "0.0000"
    assert c["official_winner"] is None
    single, _ = fixture(db, p, "single.csv", "Other,2024,B,B1,Only,X,100,100\n")
    c = analyze_import(db, p, single)["contests"][0]
    assert c["margin_over_next_candidate_votes"] is None
    assert c["margin_over_next_candidate_pct_points"] is None
    assert c["candidates"][0]["vote_share_pct"] == "100.0000"
    assert c["official_winner"] is None


def test_exact_rounding_does_not_use_binary_float():
    assert _percent(1, 3) == "33.3333"
    assert _percent(1, 6) == "16.6667"
    assert _percent(0, 10) == "0.0000"
    with pytest.raises(InvalidInput):
        _percent(1, 0)


def test_guarded_historical_swings_same_user_declared_boundary(tmp_path):
    db = Store(tmp_path / "d.sqlite3")
    initialize(db)
    p = db.create_project("Comparison")["id"]
    before, _ = fixture(
        db, p, "before.csv",
        "General Election,2022,North,V1,Alpha,Party A,600,1000\n"
        "General Election,2022,North,V1,Beta,Party B,400,1000\n",
    )
    after, _ = fixture(
        db, p, "after.csv",
        "General Election,2024,North,V1,Alpha New,Party A,450,900\n"
        "General Election,2024,North,V1,Gamma,Party C,450,900\n",
    )
    out = compare_imports(db, p, before, after)
    assert len(out["comparisons"]) == 1 and not out["skipped"]
    c = out["comparisons"][0]
    assert c["earlier_year"] == 2022 and c["later_year"] == 2024
    assert c["boundary_match_type"] == "same_user_declared_boundary_label_only"
    assert c["officially_comparable"] is False
    changes = {x["party_id"]: x for x in c["party_share_changes"]}
    parties = {x["party_id"]: x["name"] for x in (
        __import__("dotpol_platform.political_identity", fromlist=["list_entities"])
        .list_entities(db, p, "party")
    )}
    named = {parties[pid]: row for pid, row in changes.items()}
    assert named["Party A"]["earlier_share_pct"] == "60.0000"
    assert named["Party A"]["later_share_pct"] == "50.0000"
    assert named["Party A"]["share_change_pct_points"] == "-10.0000"
    assert not named["Party B"]["comparable"]
    assert named["Party B"]["later_votes"] is None
    assert named["Party B"]["share_change_pct_points"] is None
    assert not named["Party C"]["comparable"]
    assert named["Party C"]["earlier_votes"] is None
    with pytest.raises(InvalidInput):
        compare_imports(db, p, after, before)


def test_changed_boundary_prevents_swings(tmp_path):
    db = Store(tmp_path / "d.sqlite3")
    initialize(db)
    p = db.create_project("Boundaries")["id"]
    older, _ = fixture(db, p, "older.csv", "General,2022,North,Map 2022,A,X,50,50\n")
    newer, _ = fixture(db, p, "newer.csv", "General,2024,North,Map 2024,B,X,60,60\n")
    out = compare_imports(db, p, older, newer)
    assert out["comparisons"] == []
    assert len(out["skipped"]) == 2
    assert all("ambiguous one-to-one" in x["reason"] for x in out["skipped"])


def test_source_withdrawal_cross_project_and_same_import_denied(tmp_path):
    db = Store(tmp_path / "d.sqlite3")
    initialize(db)
    p = db.create_project("P")["id"]
    other = db.create_project("Other")["id"]
    import_id, sid = fixture(db, p, "one.csv", "General,2024,Seat,V1,A,X,10,10\n")
    with pytest.raises(NotFound):
        analyze_import(db, other, import_id)
    with pytest.raises(InvalidInput):
        compare_imports(db, p, import_id, import_id)
    db.withdraw(p, sid)
    with pytest.raises(InvalidInput, match="withdrawn"):
        analyze_import(db, p, import_id)


def test_local_api_reuses_source_registry_and_protects_comparison(tmp_path):
    c = TestClient(create_app(tmp_path / "local.sqlite3"))
    headers = {"X-Dotpol-Local": "1"}
    p = c.post("/api/projects", json={"title": "Research"}, headers=headers).json()["id"]
    old, new = [], []
    for name, year, votes in [("old.csv", 2022, [70, 30]), ("new.csv", 2024, [60, 40])]:
        contents = HEADER + (
            f"General,{year},Seat,V1,A,Party A,{votes[0]},100\n"
            f"General,{year},Seat,V1,B,Party B,{votes[1]},100\n"
        )
        source = c.post(f"/api/projects/{p}/sources", json={
            "name": name, "kind": "csv", "content": contents,
            "origin": "synthetic-demo",
        }, headers=headers)
        assert source.status_code == 201, source.text
        item = c.post(f"/api/projects/{p}/election-results/import", headers=headers,
                      json={"source_id": source.json()["id"]})
        assert item.status_code == 201, item.text
        old.append(item.json()["import"]["id"])
    metrics = c.get(f"/api/projects/{p}/election-results/imports/{old[0]}/metrics")
    assert metrics.status_code == 200, metrics.text
    assert metrics.json()["contests"][0]["candidates"][0]["vote_share_pct"] == "70.0000"
    url = f"/api/projects/{p}/election-results/compare"
    body = {"earlier_import_id": old[0], "later_import_id": old[1]}
    assert c.post(url, json=body).status_code == 403
    assert c.post(url, json=body, headers={**headers, "Origin":"https://evil.invalid"}).status_code == 403
    response = c.post(url, json=body, headers=headers)
    assert response.status_code == 200, response.text
    assert len(response.json()["comparisons"]) == 1
    assert len(response.json()["comparisons"][0]["party_share_changes"]) == 2
    assert c.post(url, json={"earlier_import_id":"bad","later_import_id":old[1]}, headers=headers).status_code == 422
