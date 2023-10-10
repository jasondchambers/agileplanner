from enum import Enum
from typing import NamedTuple

class EpicType(Enum):
    FRONTEND = 1
    BACKEND = 2
    QE = 3
    DEVOPS = 4
    DOCUMENTATION = 5

class Epic(NamedTuple):
    key: str
    estimated_size: int
    epic_type: EpicType

    def to_yaml(self):
        return {
            'key': self.key,
            'estimated_size': self.estimated_size,
            'epic_type' : self.epic_type.name
        }

