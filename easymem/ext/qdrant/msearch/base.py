"""Massive search types for Qdrant."""

from abc import abstractmethod

from qdrant_client.models import FieldCondition

from easymem.massivesearch.base import MassiveSearchSpecBase


class QdrantMassiveSearch(MassiveSearchSpecBase):
    """Base class for massive search spec."""

    @abstractmethod
    def build(self, key: str) -> FieldCondition:
        """Build the massive search output."""
