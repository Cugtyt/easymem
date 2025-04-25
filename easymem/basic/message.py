"""Basic memory message class."""

from dataclasses import dataclass
from typing import Annotated, TypeVar

from pydantic import ConfigDict, Field

from easymem.base.message import MemMessageBase
from easymem.basic.msearch.date import BasicDateMassiveSearch
from easymem.basic.msearch.text import BasicTextMassiveSearch


@dataclass(slots=True)
class BasicMemMessage(MemMessageBase):
    """Basic memory message class."""

    model_config = ConfigDict(extra="ignore")

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
            description="The date of the message.",
            examples=[
                "2023-10-01",
                "2023-10-02",
            ],
        ),
        BasicDateMassiveSearch,
    ]


BasicMemMessageT = TypeVar("BasicMemMessageT", bound=BasicMemMessage)
