"""Qdrant Database Interface."""

from dataclasses import dataclass
from typing import Any

from qdrant_client import AsyncQdrantClient

from easymem.db import MemoryDB
from easymem.massivesearch.base import MassiveSearchSpecBase
from easymem.message import BasicMemMessage
from easymem.records import BasicMemoryRecord


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
        if not self.client:
            msg = "QdrantMemoryDB is not connected. Call connect() first."
            raise RuntimeError(msg)

        metadata = {k: v for k, v in message.model_dump().items() if k != "content"}
        await self.client.add(
            collection_name=self.collection_name,
            documents=[message.content],
            metadata=[metadata],
        )

    async def query(self, query: str) -> list[BasicMemoryRecord]:
        """Query the database."""
        if not query:
            msg = "Query must be a non-empty string."
            raise ValueError(msg)

        if not self.client:
            msg = "QdrantMemoryDB is not connected. Call connect() first."
            raise RuntimeError(msg)

        results = await self.client.query(
            collection_name=self.collection_name,
            query_text=query,
            limit=self.limit,
        )
        return [
            self.record_type(
                id=result.id,
                score=result.score,
                message=self.message_type(
                    **{**result.metadata, "content": result.document},
                ),
                **result.metadata,
            )
            for result in results
        ]

    async def massive_search(
        self,
        query: dict[str, MassiveSearchSpecBase],
    ) -> list[BasicMemoryRecord]:
        """Massive search in the database."""
        if not self.client:
            msg = "QdrantMemoryDB is not connected. Call connect() first."
            raise RuntimeError(msg)
