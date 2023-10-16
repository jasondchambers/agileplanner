"""TimePeriod."""
from datetime import date
from typing import NamedTuple

class TimePeriod(NamedTuple):
    """Class representing a time period."""
    name: str
    start_date: date
    end_date: date

    def is_valid(self) -> bool:
        """Returns true if the time period is valid."""
        if self.start_date > self.end_date:
            return False
        if (self.end_date - self.start_date).days > (365 *3):
            return False
        return True

    def __str__(self) -> str:
        return f'Person: {self.name} {self.start_date} {self.end_date}'
