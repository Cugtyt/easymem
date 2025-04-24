"""Sample for EasyMem."""  # noqa: INP001

# from datetime import datetime

# from pydantic import Field

# from easymem import BasicMemMessage, EasyMem


# class MyMemMessage(BasicMemMessage):
#     """Custom message class for EasyMem."""

#     date: datetime = Field(
#         default_factory=datetime.now,
#         description="The date of the message.",
#     )


# async def main() -> None:
#     mem = await EasyMem.create(message_type=MyMemMessage)
#     await mem.insert(content="Hello, world!")
#     print(await mem.query("Hello"))


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(main())

from typing import Annotated, get_type_hints

from pydantic import BaseModel, Field


class MyModel(BaseModel):
    config: str = Field(
        ...,
        description="The config of the model.",
        examples=[
            "example1",
            "example2",
        ],
    )


class Test(BaseModel):
    a: Annotated[
        str,
        Field(description="A string field.", examples=["example1", "example2"]),
        MyModel,
    ]


print(get_type_hints(Test, include_extras=True)['a'].__metadata__[1])
