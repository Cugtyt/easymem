"""Basic text Massive Search."""

from typing import Annotated

import numpy as np
from pydantic import BaseModel, Field


class BasicTextMassiveSearch(BaseModel):
    """Basic text massive search spec."""

    keyword: Annotated[
        list[str],
        Field(
            ...,
            description=(
                "Keywords for the text search. "
                "This should be a list of strings."
                "The keywords are used to filter the results."
            ),
        ),
    ]

    async def search_task(self, col: int, data: np.ndarray) -> np.ndarray:
        """Search for messages containing the keywords."""
        if not self.keyword:
            return data

        text_column = data[:, col].astype(str)

        mask = np.array([any(k in text for k in self.keyword) for text in text_column])
        return data[mask]
