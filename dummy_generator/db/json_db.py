import json
from pathlib import Path


class JsonDB:
    """JSON 파일 기반 DBRepository 구현체."""

    def __init__(self, data_dir: str = "data"):
        self._root = Path(data_dir)
        self._root.mkdir(parents=True, exist_ok=True)

    def _path(self, collection: str) -> Path:
        return self._root / f"{collection}.json"

    def _load(self, collection: str) -> list[dict]:
        path = self._path(collection)
        if not path.exists():
            return []
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _dump(self, collection: str, records: list[dict]) -> None:
        with open(self._path(collection), "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    def save(self, collection: str, record: dict) -> None:
        records = self._load(collection)
        records.append(record)
        self._dump(collection, records)

    def find_all(self, collection: str) -> list[dict]:
        return self._load(collection)

    def find_by_id(self, collection: str, record_id: str) -> dict | None:
        return next((r for r in self._load(collection) if r.get("id") == record_id), None)

    def clear(self, collection: str) -> None:
        self._dump(collection, [])

    def count(self, collection: str) -> int:
        return len(self._load(collection))
