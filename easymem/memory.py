"""EasyMem."""

from typing import Any

from pydantic import BaseModel, ConfigDict

from easymem.base.easymem import EasyMemBase
from easymem.base.record import MemQueryResultBase
from easymem.ext import QdrantMemoryDB
from easymem.message import BasicMemMessage


class EasyMem(BaseModel):
    """EasyMem class."""

    model_config = ConfigDict(extra="ignore")

    message_type: type[BasicMemMessage]
    db: EasyMemBase
    massive_search_format_model: type[BaseModel]

    @classmethod
    async def create(
        cls,
        message_type: type[BasicMemMessage] = BasicMemMessage,
        db: EasyMemBase | None = None,
    ) -> "EasyMem":
        """Initialize EasyMem."""
        if not issubclass(message_type, BasicMemMessage):
            msg = f"{message_type} must be a subclass of BasicMemMessage."
            raise TypeError(msg)
        if db and not isinstance(db, EasyMemBase):
            msg = f"{db} must be an instance of MemoryDB."
            raise TypeError(msg)

        if db is None:
            db = QdrantMemoryDB()
        await db.connect()

        return cls(message_type=message_type, db=db)

    async def insert(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Insert data into indexes."""
        await self.db.add(self.message_type(**kwargs))

    async def query(self, query: str) -> list[MemQueryResultBase]:
        """Query the indexes."""
        return await self.db.query(query)

    async def massivequery(self, query: str) -> list[MemQueryResultBase]:
        """Massive query the indexes."""
        return await self.db.massivequery(query)
