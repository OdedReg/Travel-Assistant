from pydantic import BaseModel, Field


class Date(BaseModel):
    """
    A class to represent a date with Pydantic validation.

    Attributes:
        day (int): The day of the month, from 1 to 31.
        month (int): The month of the year, from 1 to 12.
        year (int): The year, from 2025 to 2050.
    """
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2025, le=2050)