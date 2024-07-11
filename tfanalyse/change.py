from dataclasses import dataclass
from enum import Enum


@dataclass
class Change:
    address: str
    type: str
    name: str
    action: "Action"

    @classmethod
    def from_entry(cls, entry: dict) -> "Change":
        return Change(
            address=entry["address"],
            type=entry["type"],
            name=entry["name"],
            action=Action[entry["change"]["actions"][0].upper().replace("-", "")],
        )


class Action(Enum):
    CREATE = "green"
    UPDATE = "yellow"
    DELETE = "red"
    NOOP = "white"
