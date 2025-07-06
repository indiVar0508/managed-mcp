import sys

from managed_mcp.util import path_in_context


def test_path_in_context():
    original_sys_path = sys.path.copy()
    test_path = "/test/path"

    # Ensure the path is not in sys.path initially
    assert test_path not in sys.path

    # Use the context manager
    with path_in_context(test_path):
        # Check if the path is added
        assert test_path in sys.path

    # Check if the path is removed after the context
    assert test_path not in sys.path

    # Ensure sys.path is restored to its original state
    assert original_sys_path == sys.path