import ast
import os
import importlib
import logging
from pathlib import Path
from .util import path_in_context


logging.basicConfig()
logger  = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ToolManager:
    """
    ToolManager is responsible for detecting and loading tool functions from a specified directory.
    Tool functions are identified by their names starting with 'tool_'.
    It scans Python files in the directory and its subdirectories, collects tool functions,
    and provides a way to load them dynamically.
    """

    def __init__(self, tool_dir: str):
        self.tool_dir = Path(tool_dir)
        if not self.tool_dir.is_dir():
            logger.error(f"Invalid tool directory: {self.tool_dir}")
            raise ValueError(f"Invalid tool directory: {self.tool_dir}")
        logger.info(f"ToolManager initialized with tool directory: {self.tool_dir}")
        self.live_tools = {}

    @classmethod
    def detect_tools(cls, tool_dir: str) -> dict[str, list[str]]:
        """
        Scans the specified directory recursively for Python files and detects functions
        whose names start with 'tool_'.
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

    def load_tools(self):
        """
        Loads tool functions from the specified directory.
        Only functions whose names start with 'tool_' are loaded.
        The functions are stored in a dictionary where the keys are the function names
        and the values are lists of function objects.
        If a function is defined in multiple modules, all instances are stored in the list.
        """
        logger.info(f"Loading tools from directory: {self.tool_dir}")
        tools = self.detect_tools(self.tool_dir)
        self.live_tools = {}
        with path_in_context(str(self.tool_dir)):
            for module, tool_list in tools.items():
                logger.info(f"Module: {module}, Tools: {', '.join(tool_list)}")
                for tool in tool_list:
                    logger.debug(f"Tool function detected: {tool} in module {module}")
                    function = getattr(importlib.import_module(module), tool)
                    if tool in self.live_tools:
                        # TODO: make behaviour configurable
                        logger.warning(f"Tool function '{tool}' already exists, overwriting.")
                    else:
                        logger.info(f"Loading tool function '{tool}' from module {module}")
                    self.live_tools[tool] = function
                    logger.info(f"Tool function '{tool}' loaded successfully.")

    def load(self) -> dict[str, callable]:
        """
        Loads the tools and returns a dictionary of tool function names to their callable objects.
        This method is a convenience method that calls `load_tools` and returns the loaded tools.
        """
        # TODO: support hooks
        self.load_tools()
        return self.live_tools