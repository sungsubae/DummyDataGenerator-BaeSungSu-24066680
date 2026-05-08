import pytest

from dummy_generator.db.interface import DBRepository
from dummy_generator.db.json_db import JsonDB


@pytest.fixture
def db(tmp_path):
    return JsonDB(data_dir=str(tmp_path))


def test_implements_protocol(db):
    assert isinstance(db, DBRepository)


def test_save_and_find_all(db):
    db.save("col", {"id": "1", "val": "a"})
    result = db.find_all("col")
    assert len(result) == 1
    assert result[0]["val"] == "a"


def test_multiple_saves_accumulate(db):
    for i in range(3):
        db.save("col", {"id": str(i)})
    assert db.count("col") == 3


def test_find_by_id_found(db):
    db.save("col", {"id": "abc", "val": "x"})
    r = db.find_by_id("col", "abc")
    assert r is not None
    assert r["val"] == "x"


def test_find_by_id_not_found(db):
    assert db.find_by_id("col", "missing") is None


def test_clear_empties_collection(db):
    db.save("col", {"id": "1"})
    db.clear("col")
    assert db.find_all("col") == []
    assert db.count("col") == 0


def test_empty_collection_returns_defaults(db):
    assert db.find_all("nonexistent") == []
    assert db.count("nonexistent") == 0
    assert db.find_by_id("nonexistent", "x") is None


def test_data_persists_across_instances(tmp_path):
    db1 = JsonDB(data_dir=str(tmp_path))
    db1.save("col", {"id": "1", "val": "persist"})

    db2 = JsonDB(data_dir=str(tmp_path))
    assert db2.count("col") == 1
    assert db2.find_by_id("col", "1")["val"] == "persist"
