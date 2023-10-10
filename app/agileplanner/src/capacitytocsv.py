import pandas as pd
from .team import Team, Organization
from .teamcapacity import TeamCapacity
from .timeperiod import TimePeriod
from .holiday import HolidaySchedulePort

def generate_capacity_sheet_for_team(team: Team, time_period: TimePeriod, holiday_schedule:HolidaySchedulePort) -> TeamCapacity:
    team_capacity = TeamCapacity(team, time_period.start_date, time_period.end_date, holiday_schedule=holiday_schedule)
    team_capacity.calculate()
    df = team_capacity.get_df()
    csv_name = team.name+'_'+time_period.name+'.csv'
    df.to_csv(csv_name)
    return team_capacity

def generate_capacity_sheet_for_org(org_name:str, teams: list[Team], time_period: TimePeriod, holiday_schedule:HolidaySchedulePort) -> TeamCapacity:
    org = Organization(org_name)
    org_team = org.generate_team(teams)
    return generate_capacity_sheet_for_team(org_team, time_period, holiday_schedule=holiday_schedule)