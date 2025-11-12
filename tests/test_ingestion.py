import pytest
import pandas as pd
import json
from pathlib import Path
from src.data_processing.ingestion import load_csv, load_json, load_excel

# ========================================
# TESTS FOR load_csv
# ========================================

def test_load_csv_success(tmp_path):
    """Test that a valid CSV file is loaded correctly."""
    data = "id,name,value\n1,Alice,10\n2,Bob,20"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(data)

    df = load_csv(csv_file)
    expected = pd.DataFrame({
        'id': [1, 2],
        'name': ['Alice', 'Bob'],
        'value': [10, 20]
    })
    pd.testing.assert_frame_equal(df, expected)

def test_load_csv_file_not_found(tmp_path):
    """Test that FileNotFoundError is raised for missing CSV."""
    missing_file = tmp_path / "missing.csv"
    with pytest.raises(FileNotFoundError):
        load_csv(missing_file)

def test_load_csv_empty_file(tmp_path):
    """Test that empty CSV raises pd.errors.EmptyDataError."""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")
    with pytest.raises(pd.errors.EmptyDataError):
        load_csv(empty_file)


# ========================================
# TESTS FOR load_json
# ========================================

def test_load_json_success(tmp_path):
    """Test loading a valid JSON file."""
    data = {
        "events": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
    }
    json_file = tmp_path / "test.json"
    json_file.write_text(json.dumps(data))

    df = load_json(json_file)
    expected = pd.DataFrame([
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ])
    pd.testing.assert_frame_equal(df, expected)

def test_load_json_file_not_found(tmp_path):
    """Test that FileNotFoundError is raised for missing JSON."""
    missing_file = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        load_json(missing_file)

def test_load_json_invalid_json(tmp_path):
    """Test that invalid JSON raises JSONDecodeError."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid: json}")
    with pytest.raises(json.JSONDecodeError):
        load_json(bad_file)


# ========================================
# PLACEHOLDER TEST FOR load_excel
# ========================================

def test_load_excel_placeholder(tmp_path):
    """Placeholder test for load_excel (not yet implemented)."""
    excel_file = tmp_path / "test.xlsx"
    # Just check that calling it raises NotImplementedError or returns None
    result = load_excel(excel_file)
    assert result is None
