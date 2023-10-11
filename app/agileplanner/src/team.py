"""Team."""
from datetime import date
import yaml
from .person import Person

class Team:
    """Class representing a team."""
    def __init__(self, name:str, file_path) -> None:
        self.name = name
        self.file_path = file_path
        self.person_list = []

    def add_person(self, person: Person) -> None:
        """Adds a person to the team."""
        self.person_list.append(person)

    def add_list(self, list_of_people:list[Person]) -> None:
        """Adds a list of people to the team."""
        self.person_list += list_of_people

    def load_from_yaml_as_string(self, yaml_string:str):
        """Loads a team from a yaml string."""
        data = yaml.safe_load(yaml_string)
        return self.load_yaml(data)

    def load_from_yaml_file(self):
        """Loads a team from a yaml file."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return self.load_yaml(data)

    def load_yaml(self,data):
        # pylint: disable=line-too-long
        """Loads a team from yaml."""
        team_data = data['team']
        self.name = team_data['name']
        self.person_list = []
        for person_data in team_data['persons']:
            person = Person(
                name=person_data['name'],
                start_date=date.fromisoformat(person_data['start_date']),
                end_date=date.fromisoformat(person_data['end_date']),
                front_end=person_data['front_end'],
                back_end=person_data['back_end'],
                qe=person_data['qe'],
                devops=person_data['devops'],
                documentation=person_data['documentation'],
                reserve_capacity=float(person_data['reserve_capacity']),
                location=person_data['location'],
                out_of_office_dates=[date.fromisoformat(d) for d in person_data['out_of_office_dates']],
            )
            self.person_list.append(person)
        return self

    def to_yaml(self):
        """Writes the team to a yaml file."""
        persons = []
        for person in self.person_list:
            persons.append(person.to_yaml())
        team_data = {
            'name': self.name,
            'persons': persons
        }
        data = {'team' :team_data}

        with open(self.file_path, 'w', encoding='utf-8') as file:
            yaml.safe_dump(data, file, sort_keys=False)

    def __str__(self) -> str:
        return f'Team: {self.name} [ {self.person_list}]'

class Organization:
    """Class representing an organization."""

    def __init__(self, org_name:str) -> None:
        self.org_name = org_name

    def generate_team(self,teams: list[Team]) -> Team:
        """Generates a single team from a list of teams that represent the organization."""
        org_team  = Team(self.org_name, "NONE")
        for team in teams:
            org_team.add_list(team.person_list)
        return org_team
