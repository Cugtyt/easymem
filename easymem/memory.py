"""EasyMem."""

from dataclasses import fields
from typing import Any

from easymem.db import MemoryDB
from easymem.ext import QdrantMemoryDB
from easymem.message import BasicMemMessage
from easymem.records import MemoryRecord


class EasyMem:
    """EasyMem class."""

    async def build(
        self,
        message_type: type[BasicMemMessage] = BasicMemMessage,
        db: MemoryDB | None = None,
    ) -> None:
        """Initialize EasyMem."""
        if not issubclass(message_type, BasicMemMessage):
            msg = f"{message_type} must be a subclass of BasicMemMessage."
            raise TypeError(msg)
        if "__dataclass_fields__" not in message_type.__dict__:
            msg = f"{message_type} must be a dataclass."
            raise TypeError(msg)
        self.message_type: type[BasicMemMessage] = message_type
        self.db: MemoryDB = db or QdrantMemoryDB()
        await self.db.connect()

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
