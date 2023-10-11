"""Scheduler."""
import copy
from typing import NamedTuple
from enum import Enum
from .teamcapacity import TeamCapacity
from .epic import EpicType, Epic


class EpicStateDuringScheduling(Enum):
    """Class representing the various states of an epic during scheduling."""
    NOT_STARTED = 1
    IN_PROGRESS = 2
    DONE = 3


class EpicScheduleStatus(Enum):
    """Class representing the outcome of a scheduled epic."""
    NO_CAPACITY_TO_START = 1
    NO_CAPACITY_TO_COMPLETE = 2
    OK = 3


class ScheduleResult(NamedTuple):
    """Class representing the result of scheduling an epic."""
    epic_schedule_status: EpicScheduleStatus
    epic_key: str
    epic_type: EpicType
    epic_estimated_size: int
    start_date: str
    end_date: str
    epic_remaining: int

    def __str__(self):
        # pylint: disable-next=line-too-long
        return f'{self.epic_key} {self.epic_estimated_size} {self.epic_type} {self.epic_schedule_status}: starts {self.start_date} and ends {self.end_date} with {self.epic_remaining} remaining'


class TeamScheduler:
    """Class for scheduling epics givwn the capacity for a team."""
    def __init__(self, team_capacity: TeamCapacity, assigned_epics: set[Epic]):
        # self.capacity_data = copy.deepcopy(team_capacity.total_capacity_data)
        self.detailed_capacity_data = copy.deepcopy(
            team_capacity.detailed_capacity_data)
        self.assigned_epics = assigned_epics

    def build_schedule(self):
        """Builds a schedule for the assigned epics."""
        schedule_results: list[ScheduleResult] = []
        for epic in self.assigned_epics:
            result = self.schedule_epic(epic)
            schedule_results.append(result)
        return schedule_results

    def who_has_capacity(self, day, category_of_work):
        """Returns a list of persons who have capacity for the category of work on the given day."""
        l = []
        for person_name in self.detailed_capacity_data[day].keys():
            remaining_capacity = sum(
                self.detailed_capacity_data[day][person_name][category_of_work])
            if remaining_capacity > 0:
                l.append(person_name)
        return l

    def apply_capacity(self, day, category_of_work, person_name, epic_remaining):
        """Applies capacity for the category of work on the given day for the given person."""
        person_has_available = sum(
            self.detailed_capacity_data[day][person_name][category_of_work])
        if person_has_available > 0:
            subtract_capacity = min(epic_remaining, person_has_available)
            epic_remaining -= subtract_capacity
            for c in EpicType:
                self.detailed_capacity_data[day][person_name][c.name].append(
                    -subtract_capacity)
        return epic_remaining

    def schedule_epic(self, epic) -> ScheduleResult:
        """Schedules an epic."""
        epic_size = epic.estimated_size
        epic_state = EpicStateDuringScheduling.NOT_STARTED
        epic_remaining = epic_size
        epic_start_date = "WILL NOT START"
        epic_end_date = "WILL NOT COMPLETE IN TIME"
        for day in self.detailed_capacity_data.keys():
            if epic_state == EpicStateDuringScheduling.DONE:
                break
            list_of_persons = self.who_has_capacity(day, epic.epic_type.name)
            for person in list_of_persons:
                if epic_state == EpicStateDuringScheduling.NOT_STARTED:
                    epic_start_date = day
                    epic_state = EpicStateDuringScheduling.IN_PROGRESS
                if epic_remaining > 0:
                    epic_remaining = self.apply_capacity(
                        day, epic.epic_type.name, person, epic_remaining)
            if epic_remaining == 0:
                epic_end_date = day
                epic_state = EpicStateDuringScheduling.DONE
        epic_schedule_status = EpicScheduleStatus.OK
        if epic_state == EpicStateDuringScheduling.NOT_STARTED:
            epic_schedule_status = EpicScheduleStatus.NO_CAPACITY_TO_START
        elif epic_state == EpicStateDuringScheduling.IN_PROGRESS:
            epic_schedule_status = EpicScheduleStatus.NO_CAPACITY_TO_COMPLETE
        return ScheduleResult(
            epic_schedule_status=epic_schedule_status,
            epic_key=epic.key,
            epic_type=epic.epic_type,
            epic_estimated_size=epic.estimated_size,
            start_date=epic_start_date,
            end_date=epic_end_date,
            epic_remaining=epic_remaining
        )
