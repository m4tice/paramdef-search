"""
@author: m4tice
"""

import pytest
import pathlib
import logging

# Resolve parent directory and look for any '*ParamDef*.arxml' files
PARENT = pathlib.Path(__file__).resolve().parents[1]
found_paramdef_files = list(PARENT.glob('**/*[Pp]aram[Dd]ef*.arxml')) if PARENT.exists() else []

# Set up logging
log = logging.getLogger(__name__)


# CONDITIONAL TESTS
@pytest.mark.skipif(not found_paramdef_files,
                    reason=f"No '*ParamDef*.arxml' files found in {PARENT} directory")
def test_get_all_paramdef_files():
    # log.info(f"Search for ParamDef files in: {PARENT}")
    from mcp_project.paramdef_handler.paramdef_utils import get_all_paramdef_files
    files = get_all_paramdef_files()
    assert isinstance(files, list)
    # assert all(isinstance(f, Path) for f in files)

    # Check for standard param definition files in the test workspace
    assert any("Com" in str(f) for f in files)
    assert any("PduR" in str(f) for f in files)
    assert any("CanIf" in str(f) for f in files)

# CONDITIONAL TESTS
@pytest.mark.skipif(not found_paramdef_files,
                    reason=f"No '*ParamDef*.arxml' files found in {PARENT} directory")
def test_get_definition_path_rapidfuzz():
    from mcp_project.paramdef_handler.paramdef_utils import get_definition_path_rapidfuzz

    keyword_1 = "comipdudirection"
    keyword_2 = "pdurgeneral"
    keywrod_3 = "nonexistentkeyword"

    def strip_result(keyword):
        result = get_definition_path_rapidfuzz(keyword)
        return result[0]['file'].split('\\')[-1].lower() if result else None

    assert strip_result(keyword_1) == "com_ecucparamdef.arxml"
    assert strip_result(keyword_2) == "pdur_ecucparamdef.arxml"
    assert strip_result(keywrod_3) is None

# TESTS
def test_get_close_matches_rapidfuzz():
    """
    @author: m4tice
    """
    from mcp_project.paramdef_handler.paramdef_utils import get_close_matches_rapidfuzz


    def test_get_close_matches_rapidfuzz_exact_match_and_types():
        keys = ["Alpha", "Beta", "Gamma"]
        matches = get_close_matches_rapidfuzz("Alpha", keys, n=3, cutoff=0.0)
        assert isinstance(matches, list)
        assert len(matches) >= 1
        first = matches[0]
        # Each entry should be a tuple (match, score)
        assert isinstance(first, tuple)
        assert first[0] == "Alpha"
        assert isinstance(first[1], float)
        # Exact match should give the maximum score (100.0)
        assert first[1] == 100.0


    def test_get_close_matches_rapidfuzz_case_insensitive_and_limit():
        keys = ["Alpha", "alpha", "ALPHA", "Beta"]
        matches = get_close_matches_rapidfuzz("alpha", keys, n=2, cutoff=0.0)
        # Should return at most n results
        assert len(matches) <= 2
        # Scores should be floats and high for exact-case variants
        assert all(isinstance(score, float) for _, score in matches)
        # Ensure at least one of the case variants is present
        matched_keys = {m for m, _ in matches}
        assert matched_keys & {"Alpha", "alpha", "ALPHA"}


    def test_get_close_matches_rapidfuzz_respects_cutoff():
        keys = ["Alpha", "Beta"]
        # Use an extremely high cutoff so no matches are returned
        matches = get_close_matches_rapidfuzz("Zeta", keys, n=5, cutoff=0.99)
        assert matches == []


    def test_get_close_matches_rapidfuzz_limits_number_of_results():
        keys = ["A", "B", "C", "D", "E"]
        matches = get_close_matches_rapidfuzz("A", keys, n=2, cutoff=0.0)
        # Ensure we don't return more than n results
        assert len(matches) <= 2