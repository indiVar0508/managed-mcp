"""ManagedMCP: A class to auto create MCP tools from specified directory."""
from mcp.server.fastmcp import FastMCP

from managed_mcp.managed_tool_manager import ManagedToolManager


class ManagedMCP(FastMCP):
    """ManagedMCP is a class that manages tools defined in a specified directory."""

    def __init__(self, *, tools_dir: str, **kwargs):  # noqa: D107
        super().__init__(**kwargs)
        self._tool_manager = ManagedToolManager(tool_dir=tools_dir)
        self._tool_manager.load_tools()
