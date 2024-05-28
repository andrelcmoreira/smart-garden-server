from dataclasses import dataclass


@dataclass
class User:
    """
    User model.

    """
    username: str
    passwd: str
