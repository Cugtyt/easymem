"""Date Massive Search."""

from pydantic import Field

from easymem.massivesearch.base import MassiveSearchSpecBase


class DateMassiveSearchSpecBase(MassiveSearchSpecBase):
    """Date massive search spec."""

    start_date: str = Field(
        ...,
        description=(
            "Start date for the date range search. "
            "This should be in the format YYYY-MM-DD."
            "The date is inclusive."
        ),
    )
    end_date: str = Field(
        ...,
        description=(
            "End date for the date range search. "
            "This should be in the format YYYY-MM-DD."
            "The date is inclusive."
        ),
    )
