from dataclasses import dataclass

@dataclass
class Device:
    dev_id: str
    serial: str
    group: str
    desc: str

    def __str__(self):
        return "{ 'id': %s, 'serial': %s, 'group': %s, 'desc': %s }" % (
            self.dev_id, self.serial, self.group, self.desc
        )
