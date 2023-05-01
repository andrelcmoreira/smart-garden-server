from dataclasses import dataclass

@dataclass
class Device:
    """
    Device model.

    """
    id: str
    serial: str
    model: str
    desc: str = ''
