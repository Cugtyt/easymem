"""Qdrant Database Interface."""

from dataclasses import asdict, dataclass
from typing import Any

from qdrant_client import AsyncQdrantClient

from easymem.db import MemoryDB
from easymem.message import BasicMemMessage


@dataclass
class QdrantMemoryDB(MemoryDB):
    """Qdrant database class for EasyMem."""

    client_kwargs: dict[str, Any] | None = None

    async def connect(self) -> None:
        """Connect to the database."""
        if not self.client_kwargs:
            self.client_kwargs = {"location": ":memory:"}

        self.client = AsyncQdrantClient(**self.client_kwargs)

    async def add(self, message: BasicMemMessage) -> None:
        """Add a message to the database."""
        metadata = {k: v for k, v in asdict(message).items() if k != "content"}
        await self.client.add(
            collection_name=self.collection_name,
            documents=[message.content],
            metadata=[metadata],
        )

    async def query(self, query: str) -> list[dict]:
        """Query the database."""
        if not query:
            msg = "Query must be a non-empty string."
            raise ValueError(msg)

        results = await self.client.query(
            collection_name=self.collection_name,
            query_text=query,
            limit=self.limit,
        )
        return [
            {
                "id": result.id,
                "content": result.document,
                "score": result.score,
                **result.metadata,
            }
            for result in results
        ]
