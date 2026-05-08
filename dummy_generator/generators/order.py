import random
import uuid
from datetime import date, timedelta

from dummy_generator.db.interface import DBRepository
from dummy_generator.generators.base import BaseGenerator
from dummy_generator.models.schemas import SampleOrder

_SAMPLE_TYPES = [
    "DRAM-DDR5", "DRAM-DDR4", "NAND-Flash-3D", "NAND-Flash-2D",
    "Logic-IC-7nm", "Logic-IC-14nm", "Power-IC-600V", "Power-IC-200V",
    "MOSFET-N채널", "MOSFET-P채널", "SiC-MOSFET", "GaN-HEMT",
]
_STATUSES = ["주문접수", "생산중", "검사중", "출하완료"]


class OrderGenerator(BaseGenerator):
    COLLECTION = "orders"

    def __init__(self, db: DBRepository, customer_ids: list[str] | None = None):
        super().__init__(db)
        self._customer_ids = customer_ids or []

    def _make_one(self) -> SampleOrder:
        due_date = date.today() + timedelta(days=random.randint(7, 90))
        customer_id = (
            random.choice(self._customer_ids) if self._customer_ids else str(uuid.uuid4())
        )
        return SampleOrder(
            id=str(uuid.uuid4()),
            customer_id=customer_id,
            sample_type=random.choice(_SAMPLE_TYPES),
            quantity=random.randint(10, 10000),
            due_date=due_date.isoformat(),
            status=random.choice(_STATUSES),
        )
