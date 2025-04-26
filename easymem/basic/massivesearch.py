"""Massive search types for BasicEasyMem."""

from abc import abstractmethod

import numpy as np

from easymem.base.massivesearch import MassiveSearchProtocol


class BasicMassiveSearchProtocol(MassiveSearchProtocol):
    """Basic massive search protocol."""

    @abstractmethod
    async def search_task(self, col: int, data: np.ndarray) -> np.ndarray:
        """Structural contract for basic massive search."""
