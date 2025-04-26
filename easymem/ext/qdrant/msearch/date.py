"""Qdrant datetime massive search module for EasyMem."""

from dataclasses import dataclass
from datetime import datetime
from typing import Annotated

from qdrant_client.models import Condition, DatetimeRange, FieldCondition

from easymem.base.massivesearch import MassiveSearchField
from easymem.ext.qdrant.massivesearch import QdrantMassiveSearchProtocol


@dataclass(slots=True)
class QdrantDatetimeMassiveSearch(QdrantMassiveSearchProtocol):
    """Qdrant date massive search module for EasyMem."""

    start_datetime: Annotated[
        str,
        MassiveSearchField(
            description=(
                "Start datetime for the date range search. "
                "This should be in the format YYYY-MM-DDTHH:MM:SSZ."
                "The datetime is inclusive."
            ),
            examples=[
                "2023-10-01T00:00:00Z",
                "2023-10-02T12:30:00Z",
            ],
        ),
    ]

    end_datetime: Annotated[
        str,
        MassiveSearchField(
            description=(
                "End datetime for the date range search. "
                "This should be in the format YYYY-MM-DDTHH:MM:SSZ."
                "The datetime is inclusive."
            ),
            examples=[
                "2023-10-01T00:00:00Z",
                "2023-10-02T12:30:00Z",
            ],
        ),
    ]

    async def search_task(self, key: str) -> Condition:
        """Search for messages within the datetime range."""
        start = datetime.fromisoformat(self.start_datetime)
        end = datetime.fromisoformat(self.end_datetime)
        return FieldCondition(
            key=key,
            range=DatetimeRange(
                gte=start,
                lte=end,
            ),
        )
