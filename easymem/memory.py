"""EasyMem."""

from typing import Any

from pydantic import BaseModel, ConfigDict

from easymem.db import MemoryDB
from easymem.ext import QdrantMemoryDB
from easymem.message import BasicMemMessage
from easymem.records import BasicMemoryRecord


class EasyMem(BaseModel):
    """EasyMem class."""

    model_config = ConfigDict(extra="ignore")

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

    async def query(self, query: str) -> list[BasicMemoryRecord]:
        """Query the indexes."""
        return await self.db.query(query)
