"""Unit tests for scheduler.py"""
import unittest
from datetime import date
from ..src.scheduler import TeamScheduler, EpicScheduleStatus
from ..src.epic import Epic, EpicType
from ..src.teamcapacity import TeamCapacity
from ..src.team import Team
from ..src.timeperiod import TimePeriod
from ..src.holiday import HolidaySchedulePort

class HolidayScheduleForTesting(HolidaySchedulePort):
    """HolidaySchedulePort implementation for testing."""
    # overriding abstract method
    def falls_on_holiday(self,some_date: date,location: str) -> bool:
        return False

class TestTeamScheduler(unittest.TestCase):
    """Tests for TeamScheduler"""

    def test_schedule_epic_team_unavailable(self):
        """Tests scheduling an epic when the team is unavailable."""
        team1_document = """
        team:
          name: Team1
          persons:
          - name: Freddy UIDev
            start_date: '2023-01-01'
            end_date: '2023-01-31'
            front_end: True
            back_end: True
            qe: False
            devops: False
            documentation: False
            reserve_capacity: 0.0
            location: US
            out_of_office_dates: []
        """
        time_period = TimePeriod(
            name='test_period',
            start_date=date(2023,10,25),
            end_date=date(2023,11,7)
        )
        e1 = Epic(
            key='csesc-1050',
            estimated_size=2,
            epic_type=EpicType.FRONTEND
        )
        team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        team1_capacity = TeamCapacity(
            team1,
            time_period,
            HolidayScheduleForTesting())
        team1_capacity.calculate()
        scheduler = TeamScheduler(team1_capacity,[e1])
        schedule_results = scheduler.build_schedule()
        self.assertEqual(len(schedule_results), 1)
        self.assertEqual(schedule_results[0].start_date, 'WILL NOT START')
        self.assertEqual(schedule_results[0].end_date, 'WILL NOT COMPLETE IN TIME')

    def test_schedule_epic_that_fits(self):
        """Tests scheduling an epic that fits."""
        team1_document = """
        team:
          name: Team1
          persons:
          - name: Freddy UIDev
            start_date: '2023-01-01'
            end_date: '2030-12-31'
            front_end: True
            back_end: True
            qe: False
            devops: False
            documentation: False
            reserve_capacity: 0.0
            location: US
            out_of_office_dates: []
        """
        time_period = TimePeriod(
            name='test_period',
            start_date=date(2023,10,25),
            end_date=date(2023,11,7)
        )
        e1 = Epic(
            key='csesc-1050',
            estimated_size=2,
            epic_type=EpicType.FRONTEND
        )
        team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        team1_capacity = TeamCapacity(
            team1, 
            time_period,
            HolidayScheduleForTesting())
        team1_capacity.calculate()
        scheduler = TeamScheduler(team1_capacity,[e1])
        schedule_results = scheduler.build_schedule()
        self.assertEqual(len(schedule_results), 1)
        self.assertEqual(schedule_results[0].start_date, '2023-10-25')
        self.assertEqual(schedule_results[0].end_date, '2023-10-26')
        self.assertEqual(schedule_results[0].epic_schedule_status, EpicScheduleStatus.OK)

    def test_schedule_epic_but_team_doesnt_have_skill_match(self):
        """Tests scheduling an epic when the team doesn't have a skill match."""
        team1_document = """
        team:
          name: Team1
          persons:
          - name: Freddy UIDev
            start_date: '2023-01-01'
            end_date: '2030-12-31'
            front_end: True
            back_end: True
            qe: False
            devops: False
            documentation: False
            reserve_capacity: 0.0
            location: US
            out_of_office_dates: []
        """
        time_period = TimePeriod(
            name='test_period',
            start_date=date(2023,10,25),
            end_date=date(2023,11,7)
        )
        e1 = Epic(
            key='csesc-1050',
            estimated_size=2,
            epic_type=EpicType.DOCUMENTATION
        )
        team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        team1_capacity = TeamCapacity(
            team1,
            time_period,
            HolidayScheduleForTesting())
        team1_capacity.calculate()
        scheduler = TeamScheduler(team1_capacity,[e1])
        schedule_results = scheduler.build_schedule()
        self.assertEqual(len(schedule_results), 1)
        self.assertEqual(schedule_results[0].start_date, 'WILL NOT START')
        self.assertEqual(schedule_results[0].end_date, 'WILL NOT COMPLETE IN TIME')
        self.assertEqual(schedule_results[0].epic_schedule_status, EpicScheduleStatus.NO_CAPACITY_TO_START)

    def test_schedule_epic_make_sure_person_is_not_over_allocated(self):
        """Tests scheduling an epic when the person is over allocated."""
        team1_document = """
        team:
          name: Team1
          persons:
          - name: Freddy Can Do It All
            start_date: '2023-01-01'
            end_date: '2030-12-31'
            front_end: True
            back_end: True
            qe: False
            devops: False
            documentation: False
            reserve_capacity: 0.0
            location: US
            out_of_office_dates: []
        """
        time_period = TimePeriod(
            name='test_period',
            start_date=date(2023,10,25),
            end_date=date(2023,11,7)
        )
        e1 = Epic(
            key='csesc-1050',
            estimated_size=2,
            epic_type=EpicType.FRONTEND
        )
        e2 = Epic(
            key='csesc-1051',
            estimated_size=2,
            epic_type=EpicType.BACKEND
        )
        team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        team1_capacity = TeamCapacity(
            team1,
            time_period,
            HolidayScheduleForTesting())
        team1_capacity.calculate()
        scheduler = TeamScheduler(team1_capacity,[e1,e2])
        schedule_results = scheduler.build_schedule()
        self.assertEqual(len(schedule_results), 2)
        self.assertEqual(schedule_results[0].epic_key, 'csesc-1050')
        self.assertEqual(schedule_results[0].start_date, '2023-10-25')
        self.assertEqual(schedule_results[0].end_date, '2023-10-26')
        self.assertEqual(schedule_results[0].epic_schedule_status, EpicScheduleStatus.OK)
        self.assertEqual(schedule_results[1].epic_key, 'csesc-1051')
        self.assertEqual(schedule_results[1].start_date, '2023-10-27')
        self.assertEqual(schedule_results[1].end_date, '2023-10-30')
        self.assertEqual(schedule_results[1].epic_schedule_status, EpicScheduleStatus.OK)

    def test_schedule_epic_that_fits_with_team_of_two_but_only_one_has_skill_match(self):
        """Tests scheduling an epic that fits with a team of two but only one has a skill match."""
        team1_document = """
        team:
          name: Team1
          persons:
          - name: Freddy UIDev
            start_date: '2023-01-01'
            end_date: '2030-12-31'
            front_end: True
            back_end: True
            qe: False
            devops: False
            documentation: False
            reserve_capacity: 0.0
            location: US
            out_of_office_dates: []
          - name: Bobby BackendDev
            start_date: '2023-01-01'
            end_date: '2030-12-31'
            front_end: False
            back_end: True
            qe: False
            devops: False
            documentation: False
            reserve_capacity: 0.0
            location: US
            out_of_office_dates: []
        """
        time_period = TimePeriod(
            name='test_period',
            start_date=date(2023,10,25),
            end_date=date(2023,11,7)
        )
        e1 = Epic(
            key='csesc-1050',
            estimated_size=2,
            epic_type=EpicType.FRONTEND
        )
        team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        team1_capacity = TeamCapacity(
            team1,
            time_period,
            HolidayScheduleForTesting())
        team1_capacity.calculate()
        scheduler = TeamScheduler(team1_capacity,[e1])
        schedule_results = scheduler.build_schedule()
        self.assertEqual(len(schedule_results), 1)
        self.assertEqual(schedule_results[0].start_date, '2023-10-25')
        self.assertEqual(schedule_results[0].end_date, '2023-10-26')
        self.assertEqual(schedule_results[0].epic_schedule_status, EpicScheduleStatus.OK)

    def test_schedule_epic_that_fits_with_team_of_two(self):
        """Tests scheduling an epic that fits with a team of two."""
        team1_document = """
        team:
          name: Team1
          persons:
          - name: Freddy UIDev
            start_date: '2023-01-01'
            end_date: '2030-12-31'
            front_end: True
            back_end: True
            qe: False
            devops: False
            documentation: False
            reserve_capacity: 0.0
            location: US
            out_of_office_dates: []
          - name: Bobby UIDev
            start_date: '2023-01-01'
            end_date: '2030-12-31'
            front_end: True
            back_end: True
            qe: False
            devops: False
            documentation: False
            reserve_capacity: 0.0
            location: US
            out_of_office_dates: []
        """
        time_period = TimePeriod(
            name='test_period',
            start_date=date(2023,10,25),
            end_date=date(2023,11,7)
        )
        e1 = Epic(
            key='csesc-1050',
            estimated_size=2,
            epic_type=EpicType.FRONTEND
        )
        team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        team1_capacity = TeamCapacity(
            team1,
            time_period,
            HolidayScheduleForTesting())
        team1_capacity.calculate()
        scheduler = TeamScheduler(team1_capacity,[e1])
        schedule_results = scheduler.build_schedule()
        self.assertEqual(len(schedule_results), 1)
        self.assertEqual(schedule_results[0].start_date, '2023-10-25')
        self.assertEqual(schedule_results[0].end_date, '2023-10-25')
        self.assertEqual(schedule_results[0].epic_schedule_status, EpicScheduleStatus.OK)

    def test_schedule_two_epics_that_fit(self):
        """Tests scheduling two epics that fit."""
        team1_document = """
        team:
          name: Team1
          persons:
          - name: Freddy UIDev
            start_date: '2023-01-01'
            end_date: '2030-12-31'
            front_end: True
            back_end: False
            qe: False
            devops: False
            documentation: False
            reserve_capacity: 0.0
            location: US
            out_of_office_dates: []
        """
        time_period = TimePeriod(
            name='test_period',
            start_date=date(2023,10,25),
            end_date=date(2023,11,7)
        )
        e1 = Epic(
            key='csesc-1050',
            estimated_size=2,
            epic_type=EpicType.FRONTEND
        )
        e2 = Epic(
            key='csesc-1051',
            estimated_size=2,
            epic_type=EpicType.FRONTEND
        )
        team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        team1_capacity = TeamCapacity(
            team1,
            time_period,
            HolidayScheduleForTesting())
        team1_capacity.calculate()
        scheduler = TeamScheduler(team1_capacity,[e1,e2])
        schedule_results = scheduler.build_schedule()
        self.assertEqual(len(schedule_results), 2)
        self.assertEqual(schedule_results[0].epic_key, 'csesc-1050')
        self.assertEqual(schedule_results[0].start_date, '2023-10-25')
        self.assertEqual(schedule_results[0].end_date, '2023-10-26')
        self.assertEqual(schedule_results[0].epic_schedule_status, EpicScheduleStatus.OK)
        self.assertEqual(schedule_results[1].epic_key, 'csesc-1051')
        self.assertEqual(schedule_results[1].start_date, '2023-10-27')
        self.assertEqual(schedule_results[1].end_date, '2023-10-30')
        self.assertEqual(schedule_results[1].epic_schedule_status, EpicScheduleStatus.OK)

    def test_schedule_second_epic_wont_fit(self):
        # pylint: disable=line-too-long
        """Tests scheduling a second epic that won't fit."""
        team1_document = """
        team:
          name: Team1
          persons:
          - name: Freddy UIDev
            start_date: '2023-01-01'
            end_date: '2030-12-31'
            front_end: True
            back_end: False
            qe: False
            devops: False
            documentation: False
            reserve_capacity: 0.0
            location: US
            out_of_office_dates: []
        """
        time_period = TimePeriod(
            name='test_period',
            start_date=date(2023,10,25),
            end_date=date(2023,11,3)
        )
        e1 = Epic(
            key='csesc-1050',
            estimated_size=2,
            epic_type=EpicType.FRONTEND
        )
        e2 = Epic(
            key='csesc-1051',
            estimated_size=10,
            epic_type=EpicType.FRONTEND
        )
        team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        team1_capacity = TeamCapacity(
            team1,
            time_period,
            HolidayScheduleForTesting())
        team1_capacity.calculate()
        scheduler = TeamScheduler(team1_capacity,[e1,e2])
        schedule_results = scheduler.build_schedule()
        self.assertEqual(len(schedule_results), 2)
        self.assertEqual(schedule_results[0].epic_key, 'csesc-1050')
        self.assertEqual(schedule_results[0].start_date, '2023-10-25')
        self.assertEqual(schedule_results[0].end_date, '2023-10-26')
        self.assertEqual(schedule_results[0].epic_remaining, 0)
        self.assertEqual(schedule_results[0].epic_schedule_status, EpicScheduleStatus.OK)
        self.assertEqual(schedule_results[1].epic_key, 'csesc-1051')
        self.assertEqual(schedule_results[1].start_date, '2023-10-27')
        self.assertEqual(schedule_results[1].end_date, 'WILL NOT COMPLETE IN TIME')
        self.assertEqual(schedule_results[1].epic_remaining, 4)
        self.assertEqual(schedule_results[1].epic_schedule_status, EpicScheduleStatus.NO_CAPACITY_TO_COMPLETE)

    def test_schedule_third_epic_wont_start(self):
        # pylint: disable=line-too-long
        """Tests scheduling a third epic that won't start."""
        team1_document = """
        team:
          name: Team1
          persons:
          - name: Freddy UIDev
            start_date: '2023-01-01'
            end_date: '2030-12-31'
            front_end: True
            back_end: False
            qe: False
            devops: False
            documentation: False
            reserve_capacity: 0.0
            location: US
            out_of_office_dates: []
        """
        time_period = TimePeriod(
            name='test_period',
            start_date=date(2023,10,25),
            end_date=date(2023,10,30)
        )
        e1 = Epic(
            key='csesc-1050',
            estimated_size=2,
            epic_type=EpicType.FRONTEND
        )
        e2 = Epic(
            key='csesc-1051',
            estimated_size=2,
            epic_type=EpicType.FRONTEND
        )
        e3 = Epic(
            key='csesc-1052',
            estimated_size=2,
            epic_type=EpicType.FRONTEND
        )
        team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        team1_capacity = TeamCapacity(
            team1,
            time_period,
            HolidayScheduleForTesting())
        team1_capacity.calculate()
        scheduler = TeamScheduler(team1_capacity,[e1,e2,e3])
        schedule_results = scheduler.build_schedule()
        self.assertEqual(len(schedule_results), 3)
        self.assertEqual(schedule_results[0].epic_key, 'csesc-1050')
        self.assertEqual(schedule_results[0].start_date, '2023-10-25')
        self.assertEqual(schedule_results[0].end_date, '2023-10-26')
        self.assertEqual(schedule_results[0].epic_remaining, 0)
        self.assertEqual(schedule_results[0].epic_schedule_status, EpicScheduleStatus.OK)
        self.assertEqual(schedule_results[1].epic_key, 'csesc-1051')
        self.assertEqual(schedule_results[1].start_date, '2023-10-27')
        self.assertEqual(schedule_results[1].end_date, '2023-10-30')
        self.assertEqual(schedule_results[1].epic_remaining, 0)
        self.assertEqual(schedule_results[1].epic_schedule_status, EpicScheduleStatus.OK)
        self.assertEqual(schedule_results[2].epic_key, 'csesc-1052')
        self.assertEqual(schedule_results[2].start_date, 'WILL NOT START')
        self.assertEqual(schedule_results[2].end_date, 'WILL NOT COMPLETE IN TIME')
        self.assertEqual(schedule_results[2].epic_remaining, 2)
        self.assertEqual(schedule_results[2].epic_schedule_status, EpicScheduleStatus.NO_CAPACITY_TO_START)