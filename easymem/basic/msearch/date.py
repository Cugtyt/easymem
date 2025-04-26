"""Basic Date Massive Search."""

from dataclasses import dataclass
from typing import Annotated

import numpy as np

from easymem.base.massivesearch import MassiveSearchField
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

    async def search_task(self, col: int, data: np.ndarray) -> np.ndarray:
        """Search for messages within the date range."""
        start_date = np.datetime64(self.start_date)
        end_date = np.datetime64(self.end_date)

        date_column = data[:, col].astype(np.datetime64)

        mask = (date_column >= start_date) & (date_column <= end_date)
        return data[mask]
