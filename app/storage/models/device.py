from dataclasses import dataclass

@dataclass
class Device:
    dev_id: str
    serial: str
    group: str
    desc: str
