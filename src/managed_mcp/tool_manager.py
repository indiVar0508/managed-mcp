import ast
import os
import logging
from pathlib import Path

logging.basicConfig()
logger  = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def detect_tools(tool_dir: str) -> dict[str, list]:
    """
    Scans the specified directory recursively for Python files and detects functions
    whose names start with 'tool_'.
    Args:
        tool_dir (str): The path to the directory to scan for tool functions.
    Returns:
        list: A list of function names (str) that start with 'tool_' found in the Python files
              within the specified directory. Returns an empty list if the directory is invalid
              or no such functions are found.
    """

    tool_dir = Path(tool_dir)
    if not tool_dir.is_dir():
        logger.error(f"Invalid tool directory: {tool_dir}")
        return {}

    module_to_tool = {}
    for file_path in tool_dir.glob("**/*.py"):
        logger.debug(f"Processing file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # ref: https://stackoverflow.com/questions/64225210/python-ast-decide-whether-a-functiondef-is-inside-a-classdef-or-not
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        child.parent = node
            elif isinstance(node, ast.FunctionDef) and node.name.startswith("tool_"):
                if hasattr(node, "parent"):
                    # TODO: support class based methods
                    logger.warning(f"Skipping function '{node.name}' in class '{node.parent.name}'")
                    continue
                module = str(file_path).replace(str(tool_dir), "").replace(os.path.sep, ".").strip(".").removesuffix(".py")
                logger.info(f"Found function '{node.name}' in {module}")
                module_to_tool.setdefault(module, []).append(node.name)

    return module_to_tool
