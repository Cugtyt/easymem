"""Date Massive Search."""

from datetime import datetime
from qdrant_client.models import DatetimeRange, FieldCondition, Filter

from easymem.massivesearch.datetime import DateMassiveSearchSpecBase


class QdrantDateMassiveSearch(DateMassiveSearchSpecBase):
    """Date massive search for Qdrant."""

    def build(self, key: str) -> Filter:
        """Build the massive search output."""
        return Filter(
            must=[
                FieldCondition(
                    key=key,
                    range=DatetimeRange(
                        # Qdrant uses RFC 3339 format for datetime
                        gte=
                        lte=
                    ),
                ),
            ],
        )
