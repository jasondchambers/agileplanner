"""HolidaySchedulePort."""
from datetime import date
from abc import ABC, abstractmethod

class HolidaySchedulePort(ABC):
    # pylint: disable=too-few-public-methods
    """Interface for a holiday schedule. A holiday schedule is a list of dates that 
    are holidays for a given location."""

    @abstractmethod
    def falls_on_holiday(self,some_date: date,location: str) -> bool:
        """Returns true if the date falls on a holiday for the given location."""
