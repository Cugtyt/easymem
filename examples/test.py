"""Sample for EasyMem."""  # noqa: INP001

from dataclasses import dataclass, field
from datetime import datetime

from easymem import BasicMemMessage, EasyMem


@dataclass
class MyMemMessage(BasicMemMessage):
    """Custom message class for EasyMem."""

    date: datetime = field(
        default_factory=datetime.now,
        metadata={"description": "The date of the message."},
    )


async def main() -> None:  # noqa: D103
    mem = await EasyMem.create(message_type=MyMemMessage)
    await mem.insert(content="Hello, world!")
    print(await mem.query("Hello"))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
