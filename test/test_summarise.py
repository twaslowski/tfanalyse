import pytest

from tfanalyse.change import Change, ChangeAction
from tfanalyse.cli import _summarise


@pytest.fixture()
def changes():
    return [
        Change(
            address="module.foo.aws_instance.bar",
            type="aws_instance",
            name="bar",
            change_action=ChangeAction.CREATE,
            properties_before={},
            properties_after={"ami": "ami-12345678"},
        )
    ]


def test_should_output_one_change(changes, capsys):
    _summarise(changes, False, False, False)
    captured = capsys.readouterr()
    assert "CREATE module.foo.aws_instance.bar" in captured.out


def test_should_output_modification_details_on_modified_resource(changes, capsys):
    changes[0].change_action = ChangeAction.UPDATE
    _summarise(changes, False, False, False)
    captured = capsys.readouterr()
    assert "ami: None -> ami-12345678" in captured.out


def test_should_output_only_deletion_changes(changes, capsys):
    _summarise(changes, True, False, False)
    captured = capsys.readouterr()
    assert "aws_instance" not in captured.out


def test_should_output_only_modification_changes(changes, capsys):
    _summarise(changes, False, False, True)
    captured = capsys.readouterr()
    assert "aws_instance" not in captured.out
