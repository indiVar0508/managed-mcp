import sys
from contextlib import contextmanager

@contextmanager
def path_in_context(path: str):
    """
    Context manager to temporarily add a path to sys.path.
    
    Args:
        path (str): The path to add to sys.path.
    
    Yields:
        None
    """
    # ref: https://stackoverflow.com/questions/17211078/how-to-temporarily-modify-sys-path-in-python
    original_sys_path = sys.path.copy()
    sys.path.append(path)
    try:
        yield
    finally:
        sys.path = original_sys_path