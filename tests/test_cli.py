from typer.testing import CliRunner
from managed_mcp.cli import cli

runner = CliRunner()

def test_run_command(mocker):
    # Mock the ManagedMCP class
    mock_managed_mcp = mocker.patch("managed_mcp.main.ManagedMCP")
    
    # Run the CLI command
    result = runner.invoke(cli, ["example/dummy_tool"])

    # Assertions
    assert result.exit_code == 0
    mock_managed_mcp.assert_called_once_with(tools_dir="example/dummy_tool")
    mock_managed_mcp.return_value.run.assert_called_once()