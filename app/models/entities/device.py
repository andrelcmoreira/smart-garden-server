from dataclasses import dataclass


@dataclass
class Device:
    """
    Device model.

    """
    serial: str
    model: str
    id: str = ''
    desc: str = ''
