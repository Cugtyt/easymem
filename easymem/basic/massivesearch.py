"""Massive search types for BasicEasyMem."""

from abc import ABC, abstractmethod

import numpy as np


class BasicMassiveSearchProtocol(ABC):
    """Basic massive search protocol."""

    @abstractmethod
    async def search_task(self, col: int, data: np.ndarray) -> np.ndarray:
        """Structural contract for basic massive search."""
