from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class DefaultAuth:
    token: str


@dataclass
class Provider:
    name: str
    appid: int
    version: int
    steamid: Optional[str]
    timestamp: int