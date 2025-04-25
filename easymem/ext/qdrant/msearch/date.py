"""Qdrant datetime massive search module for EasyMem."""

from datetime import datetime
from typing import Annotated

from pydantic import Field
from qdrant_client.models import Condition, DatetimeRange, FieldCondition

from easymem.base.massivesearch import MassiveSearchSpecBase


class QdrantDatetimeMassiveSearch(MassiveSearchSpecBase):
    """Qdrant date massive search module for EasyMem."""

    start_datetime: Annotated[
        str,
        Field(
            ...,
            description=(
                "Start datetime for the date range search. "
                "This should be in the format YYYY-MM-DDTHH:MM:SSZ."
                "The datetime is inclusive."
            ),
        ),
    ]

    end_datetime: Annotated[
        str,
        Field(
            ...,
            description=(
                "End datetime for the date range search. "
                "This should be in the format YYYY-MM-DDTHH:MM:SSZ."
                "The datetime is inclusive."
            ),
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
