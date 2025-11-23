"""
Sandbox
"""

from mcp_project.utils.generic_utils import info, debug, error
from mcp_project.paramdef_handler.paramdef_utils import get_definition_path_rapidfuzz

def main():
    keyword= "ComIpduDirection"
    result = get_definition_path_rapidfuzz(keyword)
    info(f"Results for keyword '{keyword}': {result[0]['file'].split('\\')[-1]}")

if __name__ == "__main__":
    main()
