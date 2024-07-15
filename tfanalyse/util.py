import json
import os


def _check_exists(path: str) -> bool:
    return os.path.exists(path)


def is_json(string: str) -> bool:
    try:
        json.loads(string)
    except json.JSONDecodeError:
        return False
    return True


def pretty_print_json(json_str: str) -> None:
    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError:
        secho("Invalid JSON.", fg="red")
        return
    secho(json.dumps(parsed, indent=2))
