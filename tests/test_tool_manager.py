import os
import re
import pytest
import tempfile
from pathlib import Path
from managed_mcp.tool_manager import ToolManager

def test_detect_tools_valid_directory(tmp_path):
    # Create Python files with functions
    file1 = Path(tmp_path) / "file1.py"
    file1.write_text("def tool_example(): pass\ndef another_function(): pass \n\nclass ManagedTool:\n    def tool_method(self): pass")

    file2 = Path(tmp_path) / "file2.py"
    file2.write_text("def tool_another(): pass\n\ndef tool_another1(): pass\n\ndef _tool_another1(): pass")
    # Run the function
    result = ToolManager.detect_tools(tmp_path)
    assert list(map(list, result.values())) == [["tool_example"], ["tool_another", "tool_another1"]]
    for module_path in result.keys():
        for expected_pattern in {re.compile("file1"), re.compile("file2")}:
            if expected_pattern.match(module_path) is not None:
                break
        else:
            raise AssertionError(f"Module path {list(result.keys())} does not match expected pattern {expected_pattern}")


def test_detect_tools_no_tool_functions(tmp_path):
    # Create Python files without tool_ functions
    file1 = Path(tmp_path) / "file1.py"
    file1.write_text("def example(): pass\ndef another_function(): pass")
    tool_manager = ToolManager(tool_dir=str(tmp_path))
    # Run the function
    result = tool_manager.detect_tools(tmp_path)
    assert result == {}

def test_detect_tools_invalid_directory():
    # Run the function with an invalid directory
    with pytest.raises(ValueError, match="Invalid tool directory: non_existent_directory"):
        # Attempt to create a ToolManager with a non-existent directory
        ToolManager("non_existent_directory")


def test_detect_tool_from_invalid_directory():
    # Attempt to create a ToolManager with a non-existent directory
    assert ToolManager(".").detect_tools("non_existent_directory") == {}
    

def test_load_tools():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a Python file with a tool function
        tool_file_path = os.path.join(temp_dir, "tool_example.py")
        with open(tool_file_path, "w") as tool_file:
            tool_file.write("def tool_sample():\n    return 'Sample Tool'\n")
        tools = ToolManager(temp_dir).load()
        assert "tool_sample" in tools
        assert hasattr(tools["tool_sample"], "__call__")
        assert tools["tool_sample"]() == "Sample Tool"

def test_load_tools_overwrite():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a Python file with a tool function
        tool_file_path = os.path.join(temp_dir, "tool_example.py")
        with open(tool_file_path, "w") as tool_file:
            tool_file.write("def tool_sample():\n    return 'Sample Tool'\n")
        tool_file_path2 = os.path.join(temp_dir, "tool_example2.py")
        with open(tool_file_path2, "w") as tool_file:
            tool_file.write("def tool_sample():\n    return 'Sample Tool2'\n")
        tools = ToolManager(temp_dir).load()
        assert "tool_sample" in tools
        assert hasattr(tools["tool_sample"], "__call__")
        assert tools["tool_sample"]() == "Sample Tool2"
