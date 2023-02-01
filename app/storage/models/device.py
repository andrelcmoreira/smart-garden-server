from dataclasses import dataclass

@dataclass
class Device:
    id: str
    serial: str
    group: str
    desc: str
