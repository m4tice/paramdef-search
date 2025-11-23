"""
@author: m4tice
"""

import pytest

from anyio import Path
from mcp_project.paramdef_handler.paramdef_utils import (
    get_all_paramdef_files,
    get_close_matches_rapidfuzz,
)

@pytest.mark.xfail(reason="Repository may not include ARXML files")
def test_get_all_paramdef_files():
    files = get_all_paramdef_files()
    assert isinstance(files, list)
    # assert all(isinstance(f, Path) for f in files)

    # Check for standard param definition files in the test workspace
    assert any("Com" in str(f) for f in files)
    assert any("PduR" in str(f) for f in files)
    assert any("CanIf" in str(f) for f in files)
