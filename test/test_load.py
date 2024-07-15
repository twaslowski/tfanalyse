from click.testing import CliRunner

from tfanalyse.cli import tfanalyse


def test_load_command_with_nonexistent_file():
    runner = CliRunner()
    result = runner.invoke(tfanalyse, ["nonexistent.tfplan"])
    assert result.exit_code == 1
    assert "Plan file nonexistent.tfplan does not exist." in result.output


def test_load_command_with_invalid_file():
    runner = CliRunner()
    result = runner.invoke(tfanalyse, ["test/resources/invalid_plan.tfplan"])
    assert result.exit_code == 1
    assert "Failed to load Terraform plan" in result.output
