"""
Configure MCP transport protocol
This script updates the mcp.json file based on the protocol setting in mcp_settings.py
@author: GUU8HC
"""

import os
import json
import platform
from mcp_settings import SETTINGS, PROTOCOL, STDIO, SSE, PORT


def configure_mcp():
    """
    Configure the MCP transport protocol in mcp.json
    """
    
    mcp_json_path = ".vscode/mcp.json"
    
    # Create .vscode folder if it doesn't exist
    os.makedirs(os.path.dirname(mcp_json_path), exist_ok=True)
    
    # Create configuration based on protocol
    if SETTINGS[PROTOCOL] == SSE:
        config = {
            "servers": {
                "sie-sse-mcp-server": {
                    "type": "sse",
                    "url": f"http://127.0.0.1:{SETTINGS[PORT]}/sse"
                }
            }
        }
        print(f"Configured MCP for SSE transport on port {PORT}")
    else:
        # SETTINGS[PROTOCOL] == STDIO
        python_parent_dir = "Scripts" if platform.system() == "Windows" else "bin"
        config = {
            "servers": {
                "sie-mcp-server": {
                    "command": f"${{workspaceFolder}}/.venv/{python_parent_dir}/python",
                    "args": ["mcp_project/mcp_server.py"],
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}"
                    }
                }
            }
        }
        print(f"Configured MCP for STDIO transport")
    
    # Write to file with nice formatting
    with open(mcp_json_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"Updated {mcp_json_path} for {SETTINGS[PROTOCOL]} transport protocol")

if __name__ == "__main__":
    configure_mcp()
