from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass
class Change:
    """
    Represents a subset of a .resource_changes[] entry from a Terraform plan JSON.
    """

    address: str
    type: str
    name: str
    action: Action

    @classmethod
    def from_entry(cls, entry: dict) -> Change:
        return Change(
            address=entry["address"],
            type=entry["type"],
            name=entry["name"],
            action=Action.from_entry(entry),
        )


class Action(Enum):
    """
    Represents a Terraform plan change action.
    Value is the colour to display the action in.
    """

    CREATE = "green"
    UPDATE = "yellow"
    DELETE = "red"
    NOOP = "white"

    @classmethod
    def from_entry(cls, entry: dict) -> Action:
        return Action[entry["change"]["actions"][0].upper().replace("-", "")]
