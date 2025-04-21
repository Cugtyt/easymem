"""Sample for EasyMem."""  # noqa: INP001

from datetime import datetime

from pydantic import Field

from easymem import BasicMemMessage, EasyMem


class MyMemMessage(BasicMemMessage):
    """Custom message class for EasyMem."""

    date: datetime = Field(
        default_factory=datetime.now,
        description="The date of the message.",
    )


async def main() -> None:  # noqa: D103
    mem = await EasyMem.create(message_type=MyMemMessage)
    await mem.insert(content="Hello, world!")
    print(await mem.query("Hello"))  # noqa: T201


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
