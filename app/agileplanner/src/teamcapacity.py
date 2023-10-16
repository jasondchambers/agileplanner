"""TeamCapacity."""
import pandas as pd
from .team import Team
from .holiday import HolidaySchedulePort
from .person import Person
from .epic import EpicType
from .timeperiod import TimePeriod

class TeamCapacity():
    # pylint: disable=line-too-long, too-many-instance-attributes
    """Class representing the capacity for a team."""
    def __init__(self,  team: Team, time_period:TimePeriod, holiday_schedule:HolidaySchedulePort) -> None:
        if time_period.is_valid() is False:
            raise ValueError('Invalid time period')
        self.team = team
        self.start_date = time_period.start_date
        self.end_date = time_period.end_date
        self.date_range = pd.date_range(time_period.start_date,time_period.end_date, freq="D")
        self.holiday_schedule = holiday_schedule
        self.total_capacity_data = {}
        self.leading_static_column_headings = [
            'Team',
            'Person',
            'Location',
            'Start Date',
            'End Date',
            'Front End',
            'Back End',
            'QE',
            'Documentation',
            'DevOps',
            'Reserve Capacity'
        ]
        self.daily_column_headings = [dt.strftime('%Y-%m-%d') for dt in self.date_range]
        self.trailing_static_column_headings = [
            'Total'
        ]
        self.data = {}
        all_column_headings = self.leading_static_column_headings + self.daily_column_headings + self.trailing_static_column_headings 
        for column_heading in all_column_headings:
            self.data[column_heading] = []
        self.detailed_capacity_data = {}
        self.df = None

    def is_person_unavailable(self,person):
        """Returns true if the person is unavailable for the time period."""
        if person.start_date > self.end_date:
            return True
        if person.end_date < self.start_date:
            return True
        return False

    def populate_leading_static_columns_for_person(self,person:Person):
        """Populates the leading static columns for a person."""
        self.data['Team'].append(self.team.name)
        self.data['Person'].append(person.name)
        self.data['Location'].append(person.location)
        self.data['Start Date'].append(person.start_date.isoformat())
        self.data['End Date'].append(person.end_date.isoformat())
        self.data['Front End'].append('T' if person.front_end else 'F')
        self.data['Back End'].append('T' if person.back_end else 'F')
        self.data['QE'].append('T' if person.qe else 'F')
        self.data['DevOps'].append('T' if person.devops else 'F')
        self.data['Documentation'].append('T' if person.documentation else 'F')
        self.data['Reserve Capacity'].append(person.reserve_capacity)

    def populate_daily_columns_with_zeros_for_person(self,person):
        """Populates the daily columns with zeros for a person."""
        for daily_column in self.daily_column_headings:
            self.data[daily_column].append(0)
            self.populate_detailed_capacity(daily_column,person,0)
        self.data['Total'].append(0)

    def populate_detailed_capacity(self,for_day,person,capacity_for_person_for_this_day):
        """Populates the detailed capacity for a person for a given day."""
        detailed_capacity_data_for_day = self.detailed_capacity_data.setdefault(for_day, {})
        detailed_capacity_data_for_day_for_person = detailed_capacity_data_for_day.setdefault(person.name, {}) 
        detailed_capacity_data_for_day_for_person[EpicType.FRONTEND.name] = [
            capacity_for_person_for_this_day if person.front_end else 0]
        detailed_capacity_data_for_day_for_person[EpicType.BACKEND.name] = [
            capacity_for_person_for_this_day if person.back_end else 0]
        detailed_capacity_data_for_day_for_person[EpicType.QE.name] = [
            capacity_for_person_for_this_day if person.qe else 0]
        detailed_capacity_data_for_day_for_person[EpicType.DEVOPS.name] = [
            capacity_for_person_for_this_day if person.devops else 0]
        detailed_capacity_data_for_day_for_person[EpicType.DOCUMENTATION.name] = [
            capacity_for_person_for_this_day if person.documentation else 0]

    def its_the_weekend(self,dayofweek):
        """Returns true if the given day of the week is a weekend."""
        return dayofweek > 4

    def its_a_holiday(self, some_date, location):
        """Returns true if the given date is a holiday."""
        return self.holiday_schedule.falls_on_holiday(some_date,location)

    def populate_daily_columns_for_person(self,person):
        """Populates the daily columns for a person."""
        total = 0
        for dt in self.date_range:
            daily_column = dt.strftime('%Y-%m-%d')
            if (person.is_not_available(dt.date()) or
                 self.its_the_weekend(dt.dayofweek) or
                 self.its_a_holiday(dt.date(),person.location)):
                self.data[daily_column].append(0)
                self.populate_detailed_capacity(daily_column,person,0)
            else:
                capacity_for_person_for_this_day = (1.0-person.reserve_capacity) * 1.0
                self.data[daily_column].append(capacity_for_person_for_this_day)
                self.populate_detailed_capacity(daily_column,person,capacity_for_person_for_this_day)
                total += capacity_for_person_for_this_day 
        self.data['Total'].append(total)

    def populate_total_row(self):
        """Populates the total row."""
        for leading_static_column in self.leading_static_column_headings:
            if leading_static_column == 'Team':
                self.data[leading_static_column].append(self.team.name)
            elif leading_static_column == 'Person':
                self.data[leading_static_column].append('Total')
            else:
                self.data[leading_static_column].append('-')
        for dt in self.date_range:
            daily_column = dt.strftime('%Y-%m-%d')
            daily_total = sum(self.data[daily_column])
            self.data[daily_column].append(daily_total)
            self.total_capacity_data[daily_column] = [daily_total] 
        team_total = sum(self.data['Total'])
        self.data['Total'].append(team_total)

    def calculate(self):
        """Calculates the capacity for the team."""
        for person in self.team.person_list:
            self.populate_leading_static_columns_for_person(person)
            if self.is_person_unavailable(person):
                self.populate_daily_columns_with_zeros_for_person(person)
            else:
                self.populate_daily_columns_for_person(person)
        self.populate_total_row()
        self.df = pd.DataFrame(self.data)

    def get_df(self) -> pd.DataFrame:
        """Returns the capacity data as a pandas dataframe."""
        return self.df
