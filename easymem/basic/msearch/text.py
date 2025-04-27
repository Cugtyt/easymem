"""Basic text Massive Search."""

from dataclasses import dataclass
from typing import Annotated

from easymem.base import MassiveSearchField
from easymem.basic.massivesearch import BasicMassiveSearchProtocol


@dataclass(slots=True)
class BasicTextMassiveSearch(BasicMassiveSearchProtocol):
    """Basic text massive search."""

    keyword: Annotated[
        list[str],
        MassiveSearchField(
            description=(
                "Keywords for the text search. "
                "This should be a list of strings."
                "The keywords are used to filter the results."
            ),
            examples=[
                ["Python", "programming"],
                ["weather", "great"],
            ],
        ),
    ]

    async def search_task(self, col: int, data: list[tuple]) -> list[tuple]:
        """Search for messages containing the keywords."""
        if not self.keyword:
            return data

        result = []
        for row in data:
            text = row[col]
            if any(kw.lower() in text.lower() for kw in self.keyword):
                result.append(row)
        return result
