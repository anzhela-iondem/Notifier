from typing import Optional
from dataclasses import dataclass


@dataclass
class EnvItemEntity:
    key: str
    value: str


@dataclass
class EventEntity:
    event_type: str
    body: str
    to: Optional[str] = None
