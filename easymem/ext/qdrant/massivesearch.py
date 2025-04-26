"""Massive search types for QdrantEasyMem."""

from abc import abstractmethod
from typing import Protocol, runtime_checkable

from qdrant_client.models import Condition


@runtime_checkable
class QdrantMassiveSearchProtocol(Protocol):
    """Qdrant massive search protocol."""

    @abstractmethod
    async def search_task(self, key: str) -> Condition:
        """Qdrant massive search task."""
