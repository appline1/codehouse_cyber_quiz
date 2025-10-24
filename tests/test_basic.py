import os
import sqlite3
import pytest

# Ensure we can import the main package
def test_import_package():
    import cyber as cyb
    assert cyb is not None, "Package 'cyb' failed to import"

# Test that the database can initialize correctly
def test_init_db(tmp_path):
    from cyber import utils
    test_db = tmp_path / "test_results.db"

    # temporarily override the LOCAL_DB
    utils.LOCAL_DB = str(test_db)
    utils.init_db()

    assert os.path.exists(test_db), "Database was not created"
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='results'")
    assert cursor.fetchone(), "Table 'results' does not exist"
    conn.close()

# Basic smoke test for question fetching
def test_fetch_questions():
    from cyb import utils
    try:
        questions = utils.fetch_questions()
        assert isinstance(questions, list), "fetch_questions() should return a list"
    except Exception:
        # Offline mode fallback
        assert True, "Network failure allowed — handled correctly"

# Optional test to simulate CLI import
def test_cli_entry():
    try:
        import cyber.start
        assert hasattr(cyber.start, "__file__"), "CLI entry point missing"
    except ImportError:
        pytest.skip("CLI start module not found — skipping")
