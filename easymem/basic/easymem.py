"""Basic EasyMem module."""

from uuid import UUID

import numpy as np

from easymem.base.easymem import EasyMemBase
from easymem.basic.message import BasicMemMessage
from easymem.basic.model import AzureOpenAIClient
from easymem.basic.record import BasicMemResult


class BasicEasyMem(EasyMemBase[BasicMemMessage, BasicMemResult]):
    """Basic EasyMem class."""

    def __init__(self) -> None:
        """Initialize the database."""
        self.memory: np.ndarray = np.empty((0, 3), dtype=object)
        self.model = AzureOpenAIClient()
        self.format_model = BasicMemMessage.build_msearch_format_model()

    async def connect(self) -> None:
        """Connect to the database."""

    async def add(self, message: BasicMemMessage) -> None:
        """Add a message to the database."""
        message_id = str(UUID())
        self.memory = np.append(
            self.memory,
            np.array([[message_id, message.content, message.date]], dtype=object),
            axis=0,
        )

    async def massivequery(self, query: str) -> list[BasicMemResult]:
        """Massive search in the database."""
        self.model.response(query, )
