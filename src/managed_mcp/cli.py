"""CLI for Managed MCP."""
from pathlib import Path
from typing import Annotated

from typer import Argument, Typer

cli = Typer(name="managed-mcp", help="Managed MCP CLI for dynamically creating MCP servers.")

@cli.command(name="run", help="Run the Managed MCP server.")
def run(tool_dir: Annotated[str, Path, Argument(..., help="Path to the directory containing MCP tools.", exists=True)]):
    """Run the Managed MCP server with the specified tool directory."""
    from managed_mcp.main import ManagedMCP
    ManagedMCP(tools_dir=tool_dir).run()