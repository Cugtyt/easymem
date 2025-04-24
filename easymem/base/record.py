"""Base memory record classes."""

from abc import ABC
from typing import TypeVar

from pydantic import BaseModel, ConfigDict

from easymem.base.message import MemMessageBase


class MemQueryResultBase(BaseModel, ABC):
    """Base memory record class."""

    model_config = ConfigDict(extra="ignore")

    message: MemMessageBase


MemQueryResultRecordT = TypeVar("MemQueryResultRecordT", bound=MemQueryResultBase)
