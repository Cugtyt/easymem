"""Vector Massive Search."""

from qdrant_client.models import FieldCondition

from easymem.ext.qdrant.msearch.base import QdrantMassiveSearch
from easymem.massivesearch.vector import VectorMassiveSearchSpecBase


class QdrantVectorMassiveSearch(QdrantMassiveSearch, VectorMassiveSearchSpecBase):
    """Vector massive search for Qdrant."""

    def search_task(self, key: str) -> FieldCondition:
        """Build the massive search output.

        This one will be ignored in Qdrant as it support vector search natively.
        """
        return FieldCondition(key=key)
