"""Epic."""
from enum import Enum
from typing import Any, NamedTuple

class EpicType(Enum):
    """Class representing the various types of supported epics."""
    FRONTEND = 1
    BACKEND = 2
    QE = 3
    DEVOPS = 4
    DOCUMENTATION = 5

class Epic(NamedTuple):
    """Class representing an epic."""
    key: str
    estimated_size: int
    epic_type: EpicType

    def to_yaml(self) -> dict[str, Any]:
        """Converts the epic to a yaml object."""
        return {
            'key': self.key,
            'estimated_size': self.estimated_size,
            'epic_type' : self.epic_type.name
        }
