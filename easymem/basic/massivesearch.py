"""Massive search types for BasicEasyMem."""

from abc import ABC, abstractmethod


class BasicMassiveSearchProtocol(ABC):
    """Basic massive search protocol."""

    @abstractmethod
    async def search_task(self, col: int, data: list[tuple]) -> list[tuple]:
        """Structural contract for basic massive search."""
