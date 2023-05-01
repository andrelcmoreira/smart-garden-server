from dataclasses import dataclass

@dataclass
class Config:
    """
    Configuration model.

    """
    id: str
    group: str = ''
    interval: str
