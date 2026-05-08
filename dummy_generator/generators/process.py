import random
import uuid
from datetime import datetime, timedelta

from dummy_generator.db.interface import DBRepository
from dummy_generator.generators.base import BaseGenerator
from dummy_generator.models.schemas import ProcessStatus

_STAGES = ["설계", "제조", "검사", "출하"]
_STATUSES = ["대기", "진행중", "완료"]


class ProcessGenerator(BaseGenerator):
    COLLECTION = "process_status"

    def __init__(self, db: DBRepository, order_ids: list[str] | None = None):
        super().__init__(db)
        self._order_ids = order_ids or []

    def _make_one(self) -> ProcessStatus:
        updated_at = datetime.now() - timedelta(hours=random.randint(0, 720))
        order_id = (
            random.choice(self._order_ids) if self._order_ids else str(uuid.uuid4())
        )
        return ProcessStatus(
            id=str(uuid.uuid4()),
            order_id=order_id,
            stage=random.choice(_STAGES),
            status=random.choice(_STATUSES),
            updated_at=updated_at.isoformat(),
        )
