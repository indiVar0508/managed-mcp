# Managed-MCP 

Managed MCP provides a standardized approach for building and deploying MCP servers. It enables users to focus on their tools rather than the MCP itself, supporting a "bring your own tool" philosophy.

## Tool Detector
Tool detector module scans a directory for python script and checks for method prefixed "tool_*", to be exposed as MCP tools.

#### TODO

    - Class based tool methods
    - async methods

## ManagedMCP
ManagedMCP is extension of FastMCP, with ability to scan tools directory and load them as tools automatically.

##### TODO
    - support resources
    - support prompts
    - Support directory wise server creation instead of one bloated server creation