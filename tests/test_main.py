import pytest
from managed_mcp.main import ManagedMCP

def test_managed_mcp_initialization(mocker):
    # Mock the tool manager
    MockToolManager = mocker.patch("managed_mcp.main.ManagedToolManager")
    mock_tool_manager_instance = MockToolManager.return_value

    # Initialize ManagedMCP
    ManagedMCP(tools_dir="mock_tools")

    # Assert ManagedToolManager is initialized with the correct directory
    MockToolManager.assert_called_once_with(tool_dir="mock_tools")

    # Assert load_tools is called
    mock_tool_manager_instance.load_tools.assert_called_once()