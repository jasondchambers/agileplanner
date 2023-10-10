import yaml
from datetime import date
from .person import Person

class Team:
    def __init__(self, name:str, file_path) -> None:
        self.name = name
        self.file_path = file_path
        self.person_list = []
    
    def add_person(self, person: Person) -> None:
        self.person_list.append(person)
    
    def add_list(self, list_of_people:list[Person]) -> None:
        self.person_list += list_of_people

    def load_from_yaml_as_string(self, yaml_string:str):
        data = yaml.safe_load(yaml_string)
        return self.load_yaml(data)

    def load_from_yaml_file(self):
        with open(self.file_path, 'r') as file:
            data = yaml.safe_load(file)
            return self.load_yaml(data)

    def load_yaml(self,data):
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
        persons = []
        for person in self.person_list:
            persons.append(person.to_yaml())
        team_data = {
            'name': self.name,
            'persons': persons
        }
        data = {'team' :team_data}

        with open(self.file_path, 'w') as file:
            yaml.safe_dump(data, file, sort_keys=False)

    def __str__(self) -> str:
        return f'Team: {self.name} [ {self.person_list}]'

class Organization:

    def __init__(self, org_name:str) -> None:
        self.org_name = org_name

    def generate_team(self,teams: list[Team]) -> Team:
        org_team  = Team(self.org_name, "NONE")
        for team in teams:
             org_team.add_list(team.person_list)
        return org_team

        
