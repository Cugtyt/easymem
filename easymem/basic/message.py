"""Basic memory message class."""

from typing import Annotated

from pydantic import ConfigDict, Field

from easymem.base.message import MemMessageBase
from easymem.basic.msearch.date import BasicDateMassiveSearch
from easymem.basic.msearch.text import BasicTextMassiveSearch


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
