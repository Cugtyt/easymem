"""Vector Massive Search."""

from qdrant_client.models import Filter

from easymem.massivesearch.vector import VectorMassiveSearchSpecBase


class QdrantVectorMassiveSearchSpecBase(VectorMassiveSearchSpecBase):
    """Vector massive search for Qdrant."""

    def build(self, key: str) -> Filter:  # noqa: ARG002
        """Build the massive search output.

        This one will be ignored in Qdrant as it support vector search natively.
        """
        return Filter()
