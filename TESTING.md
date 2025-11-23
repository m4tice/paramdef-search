# Running tests

This project uses `pytest` for unit tests. The repository contains a virtual environment at `.venv` — use it to run tests so results are reproducible.

PowerShell (recommended)

1. From the repository root (`D:/workspace/paramdef-search`) activate the venv:

```powershell
& D:/workspace/paramdef-search/.venv/Scripts/Activate.ps1
```

2. Install dependencies (only needed if you haven't already):

```powershell
D:/workspace/paramdef-search/.venv/Scripts/python.exe -m pip install -r D:/workspace/paramdef-search/requirements.txt
```

3. Run all tests (quiet):

```powershell
D:/workspace/paramdef-search/.venv/Scripts/python.exe -m pytest -q
```

4. Run a single test file:

```powershell
D:/workspace/paramdef-search/.venv/Scripts/python.exe -m pytest tests/test_generic_utils.py -q
```

Notes

- If you activated the venv in the current shell, you can run `pytest -q` directly.
- If tests raise import errors, ensure you're running from the repo root and that the `.venv` Python is used.
- To run tests with verbose output use `-vv` instead of `-q`.
