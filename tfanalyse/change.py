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
    change_action: ChangeAction
    properties_before: dict
    properties_after: dict

    @classmethod
    def from_entry(cls, entry: dict) -> Change:
        return Change(
            address=entry["address"],
            type=entry["type"],
            name=entry["name"],
            change_action=ChangeAction.from_entry(entry),
            properties_before=entry["change"]["before"],
            properties_after=entry["change"]["after"],
        )

    def diff_properties(self) -> dict[str, tuple[str | None, str | None]]:
        """
        Return a dictionary of properties that have changed.
        Structure is key -> (old_value, new_value)
        """
        return {
            key: (self.properties_before.get(key), self.properties_after.get(key))
            for key in set(self.properties_before) | set(self.properties_after)
            if self.properties_before.get(key) != self.properties_after.get(key)
        }


class ChangeAction(Enum):
    """
    Represents a Terraform plan change action.
    Value is the colour to display the action in.
    """

    CREATE = "green"
    UPDATE = "yellow"
    DESTROY = "red"
    NOOP = "white"

    @classmethod
    def from_entry(cls, entry: dict) -> ChangeAction:
        return ChangeAction[
            entry["change"]["actions"][0]
            .upper()
            .replace("-", "")
            .replace("DELETE", "DESTROY")
        ]
