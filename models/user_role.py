from enum import Enum, auto


class UserRole(Enum):
    guest = auto()
    normal = auto()
    admin = auto()
