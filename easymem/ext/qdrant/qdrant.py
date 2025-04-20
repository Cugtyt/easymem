"""Qdrant Database Interface."""

from dataclasses import asdict
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from easymem.db import MemoryDB
from easymem.message import BasicMemMessage


class QdrantMemoryDB(MemoryDB):
    """Qdrant database class for EasyMem."""

    client_kwargs: dict[str, Any]
    vector_kwargs: dict[str, Any]

    def connect(self) -> None:
        """Connect to the database."""
        if not self.client_kwargs:
            self.client_kwargs = {"location": ":memory"}
        if not self.vector_kwargs:
            self.vector_kwargs = {"size": 128, "distance": Distance.DOT}

        self.client = QdrantClient(**self.client_kwargs)
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(**self.vector_kwargs),
        )

    def add(self, mid: str, message: BasicMemMessage) -> None:
        """Add a message to the database."""
        metadata = {k: v for k, v in asdict(message).items() if k != "content"}
        self.client.add(
            collection_name=self.collection_name,
            documents=[message.content],
            metadata=[metadata],
            ids=[mid],
        )

    def query(self, query: str) -> list[dict]:
        """Query the database."""
        if not query:
            msg = "Query must be a non-empty string."
            raise ValueError(msg)

        results = self.client.query(
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
