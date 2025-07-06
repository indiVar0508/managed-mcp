import re
import tempfile
from pathlib import Path
from managed_mcp.tool_manager import detect_tools

def test_detect_tools_valid_directory(tmp_path):
    # Create Python files with functions
    file1 = Path(tmp_path) / "file1.py"
    file1.write_text("def tool_example(): pass\ndef another_function(): pass \n\nclass ManagedTool:\n    def tool_method(self): pass")

    file2 = Path(tmp_path) / "file2.py"
    file2.write_text("def tool_another(): pass\n\ndef tool_another1(): pass\n\ndef _tool_another1(): pass")

    # Run the function
    result = detect_tools(tmp_path)
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

    # Run the function
    result = detect_tools(tmp_path)
    assert result == {}

def test_detect_tools_invalid_directory():
    # Run the function with an invalid directory
    result = detect_tools("non_existent_directory")
    assert result == {}
