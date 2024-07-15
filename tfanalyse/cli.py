import json
import subprocess

import click
from click import secho

from tfanalyse.change import Change, ChangeAction
from tfanalyse.util import _check_exists

"""
Main CLI entrypoint for tfanalyse.
Note that functions such as _load() and _summarise() exist primarily so they can be called from other places
in the code without the click decorator being applied.
"""


@click.command()
@click.argument("plan")
@click.option("--show-no-op", is_flag=True, default=False, help="Show no-op changes.")
@click.option(
    "--destroy-only", is_flag=True, default=False, help="Show only deletion changes."
)
@click.option(
    "--update-only", is_flag=True, default=False, help="Show only update changes."
)
def tfanalyse(
    plan: str, show_no_op: bool, destroy_only: bool, update_only: bool
) -> None:
    """
    Summarise Terraform plan changes.
    """
    parsed_plan = _load(plan, False)
    changes = _parse_changes(parsed_plan)
    _summarise(changes, destroy_only, show_no_op, update_only)


def _summarise(
    changes: list[Change], destroy_only: bool, show_no_op: bool, update_only: bool
):
    """
    Summarise Terraform plan changes.
    """
    # For every change in the plan, print the action and address
    for change in changes:
        # Perform filtering based on flags
        if not show_no_op and change.change_action == ChangeAction.NOOP:
            continue
        if destroy_only and change.change_action != ChangeAction.DESTROY:
            continue
        if update_only and change.change_action != ChangeAction.UPDATE:
            continue
        secho(change.change_action.name, fg=change.change_action.value, nl=False)
        secho(f" {change.address}")
        # Print updated properties
        if change.change_action == ChangeAction.UPDATE:
            for key, (old, new) in change.diff_properties().items():
                secho(f"  {key}: {old} -> {new}", fg="yellow")


def _load(plan: str, print_plan: bool) -> dict:
    """
    Load a Terraform plan file into a Python dictionary.
    Optionally pretty-print plan JSON.
    :param plan: Path to plan file, likely generated by running `terraform plan -out=plan.tfplan`.
    :param print_plan: Whether to print the plan JSON.
    :return:
    """
    if not _check_exists(plan):
        secho(f"Plan file {plan} does not exist.", fg="red")
        exit(1)
    try:
        output = subprocess.run(
            ["terraform", "show", "-json", plan], check=True, capture_output=True
        )
    except subprocess.CalledProcessError as e:
        secho("Failed to load Terraform plan.", fg="red")
        secho(f"\n{e.stderr.decode()}", fg="red")
        exit(1)
    parsed_plan = json.loads(output.stdout)
    if print_plan:
        secho(json.dumps(parsed_plan, indent=2))
    return parsed_plan


def _parse_changes(parsed_plan: dict) -> list[Change]:
    """
    Parse Terraform plan changes to the dedicated dataclass.
    :param parsed_plan: The plan dictionary.
    :return: list of Change class instances.
    """
    return [Change.from_entry(entry) for entry in parsed_plan["resource_changes"]]
