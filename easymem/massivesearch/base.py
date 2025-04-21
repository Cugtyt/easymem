"""Massive search types for EasyMem."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class MassiveSearchSpecBase(ABC, BaseModel):
    """Base class for massive search spec."""

    @abstractmethod
    def build(self, key: str) -> Any:  # noqa: ANN401
        """Build the massive search output."""
