"""Sample for EasyMem."""  # noqa: INP001

from easymem.basic.easymem import BasicEasyMem
from easymem.basic.message import BasicMemMessage


async def main() -> None:
    mem = BasicEasyMem()
    await mem.connect()
    await mem.add(BasicMemMessage(content="Hello", date="2023-10-01"))
    await mem.add(BasicMemMessage(content="World", date="2023-10-02"))
    await mem.add(BasicMemMessage(content="Python", date="2023-10-03"))
    await mem.massivequery("find Hello")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
