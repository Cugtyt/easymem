"""Massive search types for QdrantEasyMem."""

from abc import abstractmethod

from qdrant_client.models import Condition

from easymem.base.massivesearch import MassiveSearchProtocol


class QdrantMassiveSearchProtocol(MassiveSearchProtocol):
    """Qdrant massive search protocol."""

    @abstractmethod
    async def search_task(self, key: str) -> Condition:
        """Qdrant massive search task."""
