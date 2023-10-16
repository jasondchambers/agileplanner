"""Unit tests for teamcapacity.py"""
import unittest
from datetime import date
from ..src.team import Team
from ..src.teamcapacity import TeamCapacity
from ..src.holiday import HolidaySchedulePort
from ..src.timeperiod import TimePeriod

class HolidayScheduleForTesting(HolidaySchedulePort):
    """HolidaySchedulePort implementation for testing."""
    # overriding abstract method
    def falls_on_holiday(self,some_date: date,location: str) -> bool:
        return False

class TestTeamCapacity(unittest.TestCase):
    """Test TeamCapacity class"""

    def test_impossible_time_period(self):
        """Test that an impossible time period raises an exception"""
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
            end_date=date(1990,10,25)
        )
        team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        self.assertRaises(ValueError, TeamCapacity,
            team1,
            time_period,
            HolidayScheduleForTesting())

    def test_period_greater_than_three_years(self):
        """Test that a very long time period raises an exception"""
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
            end_date=date(2026,10,25)
        )
        team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        self.assertRaises(ValueError, TeamCapacity,
            team1,
            time_period,
            HolidayScheduleForTesting())

    #def test_time_period_of_one_day(self): TODO
        #"""Tests a time period of one day."""
        #team1_document = """
        #team:
          #name: Team1
          #persons:
          #- name: Freddy UIDev
            #start_date: '2023-01-01'
            #end_date: '2030-12-31'
            #front_end: True
            #back_end: True
            #qe: False
            #devops: False
            #documentation: False
            #reserve_capacity: 0.0
            #location: US
            #out_of_office_dates: []
        #"""
        #time_period = TimePeriod(
            #name='test_period',
            #start_date=date(2023,10,25),
            #end_date=date(2023,10,25)
        #)
        #team1 = Team('Team1', 'team1.yaml').load_from_yaml_as_string(team1_document)
        #team1_capacity = TeamCapacity(
            #team1,
            #time_period,
            #HolidayScheduleForTesting())
        #team1_capacity.calculate()
        #df = team1_capacity.get_df()
        #self.assertEqual(df.shape[0],1) 
