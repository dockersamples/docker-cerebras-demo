from collections import defaultdict
import os
import socket
from typing import List, Sequence, Union
from urllib.parse import urlparse

from google.adk.tools.base_toolset import BaseToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp.client.stdio import StdioServerParameters


def _tcp_check(host: str, port: int) -> None:
    """Fail fast if the MCP gateway is unreachable."""
    try:
        with socket.create_connection((host, port), timeout=5):
            pass
    except OSError as e:
        raise RuntimeError(f"cannot reach {host}:{port}: {e}") from e


def create_mcp_toolsets() -> List[BaseToolset]:
    """Return MCPToolset objects - let ADK handle async initialization naturally."""

    endpoint = os.environ["MCPGATEWAY_ENDPOINT"]
    conn_params: Union[SseConnectionParams, StdioServerParameters]
    if endpoint.startswith(("http://", "https://")):
        parsed = urlparse(endpoint)
        if not parsed.hostname:
            raise ValueError("invalid MCP gateway URL")
        host, port = parsed.hostname, parsed.port or 80
        _tcp_check(host, port)
        conn_params = SseConnectionParams(url=endpoint)
    else:
        host, port_str = endpoint.split(":")
        _tcp_check(host, int(port_str))
        conn_params = StdioServerParameters(
            command="socat",
            args=["STDIO", f"TCP:{endpoint}"],
        )

    return [MCPToolset(connection_params=conn_params)]