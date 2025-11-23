import sys
import pathlib
import tempfile
import os

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp_project"))

from mcp_project.utils import generic_utils as gu


def test_get_keys_simple():
    data = {"a": 1, "b": {"c": 2}, "d": [ {"e": 3}, {"f": 4} ]}
    keys = gu.get_keys(data)
    assert keys >= {"a", "b", "c", "d", "e", "f"}


def test_get_precise_time_returns_datetime():
    t = gu.get_precise_time()
    import datetime
    assert isinstance(t, datetime.datetime)
