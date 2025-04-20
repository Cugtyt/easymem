"""EasyMem."""

import uuid
from typing import Any

from easymem.db import MemoryDB
from easymem.ext import QdrantMemoryDB
from easymem.message import BasicMemMessage
from easymem.records import MemoryRecord


class EasyMem:
    """EasyMem class."""

    def __init__(
        self,
        message_type: type[BasicMemMessage] = BasicMemMessage,
        db: MemoryDB | None = None,
    ) -> None:
        """Initialize EasyMem."""
        self.message_type: type[BasicMemMessage] = message_type
        self.db: MemoryDB = db or QdrantMemoryDB()
        self.db.connect()

    def insert(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Insert data into indexes."""
        mid = str(uuid.uuid4())
        self.db.add(
            mid,
            self.message_type(**kwargs),
        )

    def query(self, query: str) -> list[MemoryRecord]:
        """Query the indexes."""
        results = self.db.query(query)
        return [
            MemoryRecord(
                id=result["id"],
                message=self.message_type(**result),
                score=result["score"],
            )
            for result in results
        ]
