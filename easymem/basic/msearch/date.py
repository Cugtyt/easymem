"""Basic Date Massive Search."""

from dataclasses import dataclass
from typing import Annotated

from easymem.base import MassiveSearchField
from easymem.basic.massivesearch import BasicMassiveSearchProtocol


@dataclass(slots=True)
class BasicDateMassiveSearch(BasicMassiveSearchProtocol):
    """Basic date massive search."""

    start_date: Annotated[
        str,
        MassiveSearchField(
            description=(
                "Start date for the date range search. "
                "This should be in the format YYYY-MM-DD."
                "The date is inclusive."
            ),
            examples=[
                "2023-10-01",
                "2023-10-02",
            ],
        ),
    ]
    end_date: Annotated[
        str,
        MassiveSearchField(
            description=(
                "End date for the date range search. "
                "This should be in the format YYYY-MM-DD."
                "The date is inclusive."
            ),
            examples=[
                "2023-10-01",
                "2023-10-02",
            ],
        ),
    ]

    async def search_task(self, col: int, data: list[tuple]) -> list[tuple]:
        """Search for messages within the date range."""
        if not self.start_date and not self.end_date:
            return data

        result = []
        for row in data:
            date = row[col]
            if self.start_date <= date <= self.end_date:
                result.append(row)
        return result
