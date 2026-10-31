"""P2.01 normalized candidate-result imports: reproducible, neutral and source-linked."""
import pytest
from fastapi.testclient import TestClient

from app import create_app
from dotpol_platform.store import Store, InvalidInput, NotFound
from dotpol_platform.election_results import (
    COLUMNS, initialize, import_results, list_imports, get_import,
)
from dotpol_platform.political_identity import list_entities

HEADER = ",".join(COLUMNS) + "\n"
NORMAL = HEADER + (
    "General Election,2024,North Seat,2024-boundary,Asha,Party A,600,1000\n"
    "General Election,2024,North Seat,2024-boundary,Bala,Party B,350,1000\n"
    "General Election,2024,North Seat,2024-boundary,NOTA,None of the above,50,1000\n"
    "General Election,2024,South Seat,2024-boundary,Carla,Party A,200,700\n"
    "General Election,2024,South Seat,2024-boundary,Daya,Party B,300,700\n"
)


def setup(tmp_path):
    store = Store(tmp_path / "local.sqlite3")
    initialize(store)
    project = store.create_project("Synthetic election research")["id"]
    source = store.import_source(project, "results.csv", "csv", NORMAL, "synthetic-demo")
    return store, project, source


def test_atomic_import_links_exact_csv_lines_and_reuses_canonical_ids(tmp_path):
    db, project, source = setup(tmp_path)
    result = import_results(db, project, source["id"])
    rows = result["rows"]
    assert len(rows) == 5
    assert [r["source_line"] for r in rows] == [2, 3, 4, 5, 6]
    assert all(r["import_id"] == result["import"]["id"] for r in rows)
    assert result["import"]["source_sha256"] == source["sha256"]
    assert result["import"]["status"] == "user-uploaded-unverified"
    assert result["quality"]["official_status"] == "not-verified-from-primary-source"
    assert result["quality"]["source_verified"] is False
    contests = result["quality"]["contests"]
    assert len(contests) == 2
    north, south = contests
    assert north["reported_votes"] == 1000
    assert north["complete_against_declared_total"] is True
    assert south["reported_votes"] == 500
    assert south["unrepresented_votes"] == 200
    assert south["complete_against_declared_total"] is False
    assert rows[0]["party_id"] == rows[3]["party_id"]
    assert rows[0]["constituency_id"] == rows[1]["constituency_id"]
    assert rows[0]["election_id"] == rows[3]["election_id"]
    assert len(list_entities(db, project, "party")) == 3
    assert len(list_entities(db, project, "election")) == 1
    assert len(list_entities(db, project, "constituency")) == 2
    assert all(e["status"] == "user-declared-unverified" for e in list_entities(db,project))
    assert get_import(Store(db.db_path), project, result["import"]["id"]) == result
    with pytest.raises(InvalidInput, match="already imported"):
        import_results(db, project, source["id"])


@pytest.mark.parametrize("data", [
    HEADER,
    "candidate,party,votes\nA,B,2\n",
    HEADER + "E,2024,C,B,V,P,1,10,EXTRA\n",
    HEADER + "E,2024,C,B,V,P,not-a-number,10\n",
    HEADER + "E,2024,C,B,V,P,-1,10\n",
    HEADER + "E,2024,C,B,V,P,11,10\n",
    HEADER + "E,2024,C,B,V,P,1,0\n",
    HEADER + "E,2024,C,B,V,P,2,10\nE,2024,C,B,V,Q,3,10\n",
    HEADER + "E,2024,C,B,V,P,2,10\nE,2024,C,B,W,Q,3,11\n",
    HEADER + "E,2024,C,B1,V,P,2,10\nE,2024,C,B2,W,Q,3,10\n",
    HEADER + "E,2024,C,B,V,P,9,10\nE,2024,C,B,W,Q,9,10\n",
    HEADER + "E,2024,C,B,V,P,2,10\nE,2024,C,B,v,Q,3,10\n",
    HEADER + "E,2024,C,B,V,P,2,10\nE,2024,C,B\n",
    HEADER + "E,0000,C,B,V,P,2,10\n",
    HEADER + "E,2024,C,B,V,P,9223372036854775808,9223372036854775808\n",
])
def test_invalid_dataset_rolls_back_results_and_identity_rows(tmp_path, data):
    db=Store(tmp_path/"local.sqlite3")
    initialize(db)
    p=db.create_project("P")["id"]
    s=db.import_source(p,"test.csv","csv",data)
    with pytest.raises(InvalidInput):
        import_results(db,p,s["id"])
    assert list_imports(db,p) == []
    assert list_entities(db,p) == []


def test_cross_project_sources_and_source_withdrawal(tmp_path):
    db,p,source=setup(tmp_path)
    other=db.create_project("Other")["id"]
    with pytest.raises(NotFound):
        import_results(db,other,source["id"])
    saved=import_results(db,p,source["id"])
    assert list_imports(db,other)==[]
    with pytest.raises(NotFound):
        get_import(db,other,saved["import"]["id"])
    db.withdraw(p,source["id"])
    assert get_import(db,p,saved["import"]["id"])["import"]["source_status"]=="withdrawn"
    with pytest.raises(InvalidInput):
        import_results(db,p,source["id"])


def test_api_uses_existing_local_security_and_returns_unverified_status(tmp_path):
    client=TestClient(create_app(tmp_path/"api.sqlite3"))
    headers={"X-Dotpol-Local":"1"}
    p=client.post("/api/projects",headers=headers,json={"title":"Election test"}).json()["id"]
    source=client.post(f"/api/projects/{p}/sources",headers=headers,json={
        "name":"election.csv","kind":"csv","content":NORMAL,"origin":"synthetic-demo"
    })
    assert source.status_code==201
    url=f"/api/projects/{p}/election-results/import"
    assert client.post(url,json={"source_id":source.json()["id"]}).status_code==403
    assert client.post(url,headers={**headers,"Origin":"https://evil.invalid"},
                       json={"source_id":source.json()["id"]}).status_code==403
    out=client.post(url,headers=headers,json={"source_id":source.json()["id"]})
    assert out.status_code==201,out.text
    saved=out.json()
    assert saved["quality"]["source_verified"] is False
    assert saved["import"]["schema_version"]=="dotpol-candidate-results-v1"
    assert client.get(f"/api/projects/{p}/election-results/imports").json()[0]["id"]==saved["import"]["id"]
    assert client.get(f"/api/projects/{p}/election-results/imports/{saved['import']['id']}").json()==saved


def test_same_label_different_projects_have_different_canonical_ids(tmp_path):
    db=Store(tmp_path/"db.sqlite3");initialize(db)
    projects=[db.create_project(label)["id"] for label in ("A","B")]
    ids=[]
    for p in projects:
        s=db.import_source(p,"election.csv","csv",NORMAL)
        data=import_results(db,p,s["id"])
        ids.append(data["rows"][0]["election_id"])
    assert ids[0]!=ids[1]
