from abc import ABC, abstractmethod
from dataclasses import asdict

from dummy_generator.db.interface import DBRepository


class BaseGenerator(ABC):
    COLLECTION: str = ""

    def __init__(self, db: DBRepository):
        self._db = db

    @abstractmethod
    def _make_one(self) -> object:
        ...

    def generate(self, n: int) -> list[dict]:
        records = [asdict(self._make_one()) for _ in range(n)]
        for record in records:
            self._db.save(self.COLLECTION, record)
        return records
