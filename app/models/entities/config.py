from dataclasses import dataclass


@dataclass
class Config:
    '''
    Configuration model.

    '''
    id: str
    interval: str
    group: str = ''
