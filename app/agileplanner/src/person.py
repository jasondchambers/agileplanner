"""Person class."""""
from datetime import date
from typing import Any, NamedTuple

class Person(NamedTuple):
    """Class representing a person."""
    name: str
    start_date: date
    end_date: date
    front_end: bool
    back_end: bool
    qe: bool
    devops: bool
    documentation: bool
    reserve_capacity: float
    location: str
    out_of_office_dates: list[date]

    def is_out_of_office(self,some_date: date) -> bool:
        """Returns true if the person is out of office on the given date."""
        return some_date in self.out_of_office_dates
    
    def is_not_active(self, some_date: date) -> bool:
        """Returns true if the person is not active on the given date."""
        return self.start_date > some_date or self.end_date < some_date

    def is_not_available(self, some_date: date) -> bool:
        """Returns true if the person is not available on the given date."""
        return self.is_out_of_office(some_date) or self.is_not_active(some_date)

    def to_yaml(self) -> dict[str, Any]:
        """Converts the person to yaml."""
        return {
            'name': self.name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'front_end': self.front_end,
            'back_end': self.back_end,
            'qe': self.qe,
            'devops': self.devops,
            'documentation': self.documentation,
            'reserve_capacity': self.reserve_capacity,
            'location': self.location,
            'out_of_office_dates': [d.isoformat() for d in self.out_of_office_dates],
        }

    def __str__(self) -> str:
        return f'Person: {self.name} {self.start_date} {self.end_date} {self.location}'
