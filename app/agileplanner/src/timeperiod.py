"""TimePeriod."""
from datetime import date
from typing import NamedTuple

class TimePeriod(NamedTuple):
    """Class representing a time period."""
    name: str
    start_date: date
    end_date: date

    def __str__(self) -> str:
        return f'Person: {self.name} {self.start_date} {self.end_date}'
