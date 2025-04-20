"""Sample for EasyMem."""  # noqa: INP001

from datetime import datetime

from easymem import BasicMemMessage, EasyMem


class MyMemMessage(BasicMemMessage):
    """Custom message class for EasyMem."""

    date: datetime


mem = EasyMem(message_type=MyMemMessage)
