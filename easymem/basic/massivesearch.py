"""Massive search types for BasicEasyMem."""

from abc import abstractmethod
from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class BasicMassiveSearchProtocol(Protocol):
    """Basic massive search protocol."""

    @abstractmethod
    async def search_task(self, col: int, data: np.ndarray) -> np.ndarray:
        """Structural contract for basic massive search."""
