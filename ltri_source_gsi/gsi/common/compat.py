from enum import Enum
from typing import Dict
import dataclasses
from pydantic.dataclasses import dataclass

# pydantic versions of the la4 machine serializer


class RunningEnum(Enum):
    RUNNING = "RUNNING"
    NOTRUNNING = "NOTRUNNING"

@dataclass
class Machine:
    name: str
    iname: str

    id: str
    desc: str

    speed: str = "TENTHS"
    running: RunningEnum = RunningEnum.RUNNING

@dataclass
class MachineDict:
    machines: Dict[str, Machine]
    speed_enum: Dict[str, float] = dataclasses.field(default_factory=lambda: {"TENTHS": .1})