"""Massive search types for Qdrant."""

from abc import abstractmethod

from qdrant_client.models import FieldCondition

from easymem.base.massivesearch import MassiveSearchSpecBase


class QdrantMassiveSearch(MassiveSearchSpecBase):
    """Base class for massive search spec."""

    @abstractmethod
    def search_task(self, key: str) -> FieldCondition:
        """Build the massive search output."""
