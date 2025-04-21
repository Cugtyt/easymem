"""EasyMem."""

from dataclasses import dataclass, fields
from typing import Any

from easymem.db import MemoryDB
from easymem.ext import QdrantMemoryDB
from easymem.message import BasicMemMessage
from easymem.records import MemoryRecord


@dataclass
class EasyMem:
    """EasyMem class."""

    message_type: type[BasicMemMessage]
    db: MemoryDB

    @classmethod
    async def create(
        cls,
        message_type: type[BasicMemMessage] = BasicMemMessage,
        db: MemoryDB | None = None,
    ) -> "EasyMem":
        """Initialize EasyMem."""
        if not issubclass(message_type, BasicMemMessage):
            msg = f"{message_type} must be a subclass of BasicMemMessage."
            raise TypeError(msg)
        if db and not isinstance(db, MemoryDB):
            msg = f"{db} must be an instance of MemoryDB."
            raise TypeError(msg)

        if db is None:
            db = QdrantMemoryDB()
        await db.connect()

        return cls(message_type=message_type, db=db)

    async def insert(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Insert data into indexes."""
        await self.db.add(self.message_type(**kwargs))

    async def query(self, query: str) -> list[MemoryRecord]:
        """Query the indexes."""
        allowed = {f.name for f in fields(self.message_type)}
        results = await self.db.query(query)

        records: list[MemoryRecord] = []
        for result in results:
            msg_kwargs = {k: v for k, v in result.items() if k in allowed}
            records.append(
                MemoryRecord(
                    id=result["id"],
                    message=self.message_type(**msg_kwargs),
                    score=result["score"],
                ),
            )
        return records
