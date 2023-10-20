"""Feature."""
from typing import Any
import yaml
from .epic import Epic, EpicType

class Feature:
    """Class representing a feature."""

    def __init__(self, key:str) -> None:
        self.key = key
        self.epic_list: list[Epic] = []

    def add_epic(self, epic: Epic) -> None:
        """Adds an epic to the feature."""
        self.epic_list.append(epic)

    def to_yaml(self) -> dict[str, Any]:
        """Converts the feature to a yaml."""
        return {
            'key': self.key,
            'epics': [epic.to_yaml() for epic in self.epic_list]
        }

class Features:
    """Class representing a list of features."""

    def __init__(self, file_path: str) -> None:
        self.feature_list: list[Feature] = []
        self.file_path = file_path

    def add_feature(self, feature: Feature) -> None:
        """Adds a feature to the list."""
        self.feature_list.append(feature)

    def load_from_yaml_as_string(self, yaml_string:str) -> 'Features':
        """Loads features from a yaml string."""
        data = yaml.safe_load(yaml_string)
        return self.load_yaml(data)

    def load_from_yaml_file(self) -> 'Features':
        """Loads features from a yaml file."""
        with open(self.file_path, 'r', encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return self.load_yaml(data)

    def load_yaml(self,data:Any) -> 'Features':
        """Loads features from a yaml."""
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
        """Gets a list of all epics in the features."""
        l:list[Epic] = []
        for feature in self.feature_list:
            l = l + feature.epic_list
        return l

    def to_yaml(self):
        """Writes the features to yaml file."""
        features_data:list[dict[str, Any]] = []
        for feature in self.feature_list:
            features_data.append(feature.to_yaml())
        data: Any = {'features' :features_data}

        with open(self.file_path, 'w', encoding="utf-8") as file:
            yaml.dump(data, file, sort_keys=False)
