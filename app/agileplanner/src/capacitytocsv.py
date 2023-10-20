"""Functions for generating capacity sheets for teams and organizations."""
from .team import Team, Organization
from .teamcapacity import TeamCapacity
from .timeperiod import TimePeriod
from .holiday import HolidaySchedulePort

def generate_capacity_sheet_for_team(
        team: Team, time_period: TimePeriod,
        holiday_schedule: HolidaySchedulePort) -> TeamCapacity:
    """
    Generates a capacity sheet for a given team and time period.

    Args:
        team (Team): The team for which to generate the capacity sheet.
        time_period (TimePeriod): The time period for which to generate the capacity sheet.
        holiday_schedule (HolidaySchedulePort): The holiday schedule to use .

    Returns:
        TeamCapacity: The generated capacity sheet.
    """
    team_capacity = TeamCapacity(
        team,
        time_period,
        holiday_schedule=holiday_schedule,
    )
    team_capacity.calculate()
    df = team_capacity.get_df()
    csv_name: str = team.name + "_" + time_period.name + ".csv"
    df.to_csv(csv_name)
    return team_capacity

def generate_capacity_sheet_for_org(
        org_name: str,
        teams: list[Team],
        time_period: TimePeriod,
        holiday_schedule: HolidaySchedulePort) -> TeamCapacity:
    """ Generates a capacity sheet for a given organization and time period."""
    org = Organization(org_name)
    org_team = org.generate_team(teams)
    return generate_capacity_sheet_for_team(
        org_team, time_period, holiday_schedule=holiday_schedule
    )
