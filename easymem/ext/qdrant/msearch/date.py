"""Date Massive Search."""

from datetime import UTC, datetime

from qdrant_client.models import DatetimeRange, FieldCondition

from easymem.ext.qdrant.msearch.base import QdrantMassiveSearch
from easymem.massivesearch.datetime import DateMassiveSearchSpecBase


class QdrantDateMassiveSearch(QdrantMassiveSearch, DateMassiveSearchSpecBase):
    """Date massive search for Qdrant."""

    def build(self, key: str) -> FieldCondition:
        """Build the massive search output."""
        return FieldCondition(
            key=key,
            range=DatetimeRange(
                gte=datetime.strptime(self.start_date, "%Y-%m-%d").replace(
                    tzinfo=UTC,
                ),
                lte=datetime.strptime(self.end_date, "%Y-%m-%d").replace(
                    tzinfo=UTC,
                ),
            ),
        )
