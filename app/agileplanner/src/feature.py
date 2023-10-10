import yaml
from .epic import Epic, EpicType

class Feature:

    def __init__(self, key:str) -> None:
        self.key = key
        self.epic_list: list[Epic] = []
    
    def add_epic(self, epic: Epic) -> None:
        self.epic_list.append(epic)

    def to_yaml(self):
        return {
            'key': self.key,
            'epics': [epic.to_yaml() for epic in self.epic_list]
        }

class Features:

    def __init__(self, file_path) -> None:
        self.feature_list: list[Feature] = []
        self.file_path = file_path
    
    def add_feature(self, feature: Feature) -> None:
        self.feature_list.append(feature)

    def load_from_yaml_as_string(self, yaml_string:str):
        data = yaml.safe_load(yaml_string)
        return self.load_yaml(data)

    def load_from_yaml_file(self):
        with open(self.file_path, 'r') as file:
            data = yaml.safe_load(file)
            return self.load_yaml(data)

    def load_yaml(self,data):
        for feature_data in data['features']:
            feature = Feature(feature_data['key'])
            for epic_data in feature_data['epics']:
                epic = Epic(
                    epic_data['key'], 
                    epic_data['estimated_size'],
                    EpicType[epic_data['epic_type']])
                feature.add_epic(epic)
            self.feature_list.append(feature)
        return self

    def get_epics(self) -> list[Epic]:
        l = []
        for feature in self.feature_list:
            l = l + feature.epic_list
        return l

    def to_yaml(self):
        features = []
        for feature in self.feature_list:
            features.append(feature.to_yaml())
        data = {'features' :features}

        with open(self.file_path, 'w') as file:
            yaml.dump(data, file, sort_keys=False)
