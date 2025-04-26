"""Massive search types for EasyMem."""

from abc import abstractmethod
from typing import Generic, ParamSpec, TypeVar

from pydantic import BaseModel, ConfigDict

MassiveSearchP = ParamSpec("MassiveSearchP")
MassiveSearchR_co = TypeVar("MassiveSearchR_co", covariant=True)


class MassiveSearchProtocol(
    BaseModel,
    Generic[MassiveSearchP, MassiveSearchR_co],
):
    """Base class for massive search spec."""

    model_config = ConfigDict(extra="ignore")

    @abstractmethod
    async def search_task(
        self,
        *args: MassiveSearchP.args,
        **kwargs: MassiveSearchP.kwargs,
    ) -> MassiveSearchR_co:
        """Build the massive search output."""
