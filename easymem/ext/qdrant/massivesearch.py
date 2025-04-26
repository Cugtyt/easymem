"""Massive search types for QdrantEasyMem."""

from abc import ABC, abstractmethod

from qdrant_client.models import Condition


class QdrantMassiveSearchProtocol(ABC):
    """Qdrant massive search protocol."""

    @abstractmethod
    async def search_task(self, key: str) -> Condition:
        """Qdrant massive search task."""
