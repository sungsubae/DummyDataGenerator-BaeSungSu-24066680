import pytest

from dummy_generator.db.json_db import JsonDB
from dummy_generator.generators.customer import CustomerGenerator
from dummy_generator.generators.inventory import InventoryGenerator
from dummy_generator.generators.order import OrderGenerator
from dummy_generator.generators.process import ProcessGenerator


@pytest.fixture
def db(tmp_path):
    return JsonDB(data_dir=str(tmp_path))


# ── CustomerGenerator ─────────────────────────────────────────────────────────

class TestCustomerGenerator:
    def test_generate_returns_correct_count(self, db):
        records = CustomerGenerator(db).generate(5)
        assert len(records) == 5

    def test_records_saved_to_db(self, db):
        CustomerGenerator(db).generate(3)
        assert db.count("customers") == 3

    def test_record_has_required_fields(self, db):
        r = CustomerGenerator(db).generate(1)[0]
        assert all(k in r for k in ["id", "name", "company", "contact", "email"])

    def test_ids_are_unique(self, db):
        records = CustomerGenerator(db).generate(10)
        ids = [r["id"] for r in records]
        assert len(set(ids)) == 10


# ── OrderGenerator ────────────────────────────────────────────────────────────

class TestOrderGenerator:
    def test_customer_ids_assigned_from_pool(self, db):
        cids = ["cid-1", "cid-2"]
        records = OrderGenerator(db, cids).generate(20)
        assert all(r["customer_id"] in cids for r in records)

    def test_records_saved_to_db(self, db):
        OrderGenerator(db, ["cid-1"]).generate(4)
        assert db.count("orders") == 4

    def test_status_values_are_valid(self, db):
        valid = {"주문접수", "생산중", "검사중", "출하완료"}
        records = OrderGenerator(db, ["cid-1"]).generate(30)
        assert all(r["status"] in valid for r in records)

    def test_quantity_in_range(self, db):
        records = OrderGenerator(db, ["cid-1"]).generate(30)
        assert all(10 <= r["quantity"] <= 10000 for r in records)

    def test_without_customer_ids_still_generates(self, db):
        records = OrderGenerator(db).generate(3)
        assert len(records) == 3


# ── InventoryGenerator ────────────────────────────────────────────────────────

class TestInventoryGenerator:
    def test_generate_returns_correct_count(self, db):
        records = InventoryGenerator(db).generate(7)
        assert len(records) == 7

    def test_record_has_required_fields(self, db):
        r = InventoryGenerator(db).generate(1)[0]
        assert all(k in r for k in ["id", "sample_type", "quantity", "unit", "location"])

    def test_quantity_non_negative(self, db):
        records = InventoryGenerator(db).generate(30)
        assert all(r["quantity"] >= 0 for r in records)


# ── ProcessGenerator ──────────────────────────────────────────────────────────

class TestProcessGenerator:
    def test_order_ids_assigned_from_pool(self, db):
        oids = ["oid-1", "oid-2"]
        records = ProcessGenerator(db, oids).generate(20)
        assert all(r["order_id"] in oids for r in records)

    def test_stage_values_are_valid(self, db):
        valid = {"설계", "제조", "검사", "출하"}
        records = ProcessGenerator(db, ["oid-1"]).generate(30)
        assert all(r["stage"] in valid for r in records)

    def test_status_values_are_valid(self, db):
        valid = {"대기", "진행중", "완료"}
        records = ProcessGenerator(db, ["oid-1"]).generate(30)
        assert all(r["status"] in valid for r in records)

    def test_records_saved_to_db(self, db):
        ProcessGenerator(db, ["oid-1"]).generate(5)
        assert db.count("process_status") == 5

    def test_without_order_ids_still_generates(self, db):
        records = ProcessGenerator(db).generate(3)
        assert len(records) == 3
