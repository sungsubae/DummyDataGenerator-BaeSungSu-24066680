from dataclasses import asdict

from dummy_generator.models.schemas import Customer, Inventory, ProcessStatus, SampleOrder


def test_customer_serializes_to_dict():
    c = Customer(id="1", name="홍길동", company="S-Semi", contact="010-0000-0000", email="a@b.com")
    d = asdict(c)
    assert d == {"id": "1", "name": "홍길동", "company": "S-Semi",
                 "contact": "010-0000-0000", "email": "a@b.com"}


def test_sample_order_fields():
    o = SampleOrder(id="2", customer_id="c1", sample_type="DRAM-DDR5",
                    quantity=500, due_date="2026-06-01", status="주문접수")
    assert o.sample_type == "DRAM-DDR5"
    assert o.quantity == 500
    assert o.status == "주문접수"


def test_inventory_fields():
    inv = Inventory(id="3", sample_type="NAND-Flash-3D",
                    quantity=5000, unit="개", location="창고-A1")
    assert inv.location == "창고-A1"
    assert inv.unit == "개"


def test_process_status_fields():
    ps = ProcessStatus(id="4", order_id="o1", stage="제조",
                       status="진행중", updated_at="2026-05-01T10:00:00")
    assert ps.stage == "제조"
    assert ps.status == "진행중"


def test_all_schemas_are_dataclasses():
    for cls in (Customer, SampleOrder, Inventory, ProcessStatus):
        obj = asdict(cls(**{f.name: "x" for f in cls.__dataclass_fields__.values()}))
        assert isinstance(obj, dict)
