from dataclasses import dataclass

@dataclass
class Device:
    id: str
    serial: str
    model: str
    desc: str = ''
    group: str = ''
