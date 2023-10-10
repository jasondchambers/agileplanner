# Instead of having hard-coded holidays, have a callback 
from datetime import date
from abc import ABC, abstractmethod

class HolidaySchedulePort(ABC):
    @abstractmethod
    def falls_on_holiday(self,some_date: date,location: str) -> bool:
        pass