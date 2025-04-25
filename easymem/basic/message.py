"""Basic memory message class."""

from dataclasses import dataclass
from typing import Annotated, TypeVar

from pydantic import Field

from easymem.base.message import MemMessageBase
from easymem.basic.msearch.date import BasicDateMassiveSearch
from easymem.basic.msearch.text import BasicTextMassiveSearch


@dataclass(slots=True)
class BasicMemMessage(MemMessageBase):
    """Basic memory message class."""

    content: Annotated[
        str,
        Field(
            ...,
            description="The content of the message.",
            examples=[
                "I love programming in Python!",
                "The weather is great today.",
            ],
        ),
        BasicTextMassiveSearch,
    ]

    date: Annotated[
        str,
        Field(
            ...,
            description=(
                "The date of the message; data starts from 2000-01-01, "
                "current date is 2025-05-01."
            ),
            examples=[
                "2023-10-01",
                "2023-10-02",
            ],
        ),
        BasicDateMassiveSearch,
    ]


BasicMemMessageT = TypeVar("BasicMemMessageT", bound=BasicMemMessage)
