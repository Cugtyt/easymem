"""Massive search types for EasyMem."""

from abc import ABC, abstractmethod
from typing import Generic, ParamSpec, TypeVar

from pydantic import BaseModel

MassiveSearchP = ParamSpec("MassiveSearchP")
MassiveSearchR_co = TypeVar("MassiveSearchR_co", covariant=True)


class MassiveSearchSpecBase(
    ABC,
    Generic[MassiveSearchP, MassiveSearchR_co],
):
    """Base class for massive search spec."""

    @abstractmethod
    async def search_task(
        self,
        *args: MassiveSearchP.args,
        **kwargs: MassiveSearchP.kwargs,
    ) -> MassiveSearchR_co:
        """Build the massive search output."""

    @classmethod
    @abstractmethod
    def build_format_model(cls) -> type[BaseModel]:
        """Build the massive search format model."""
