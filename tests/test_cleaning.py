"""Tests for data cleaning functions."""

import pytest
import pandas as pd
import pandas.testing as pdt
from src.data_processing.cleaning import (
    remove_duplicates,
    handle_missing_values,
    standardize_dates
)

# ========================================
# FIXTURES - Reusable test data
# ========================================

@pytest.fixture
def sample_df_with_duplicates():
    """Sample DataFrame with duplicate rows."""
    return pd.DataFrame({
        'id': [1, 2, 2, 3, 3, 3],
        'name': ['Alice', 'Bob', 'Bob', 'Charlie', 'Charlie', 'Charlie'],
        'value': [10, 20, 20, 30, 30, 30]
    })

@pytest.fixture
def sample_df_with_missing():
    """Sample DataFrame with missing values."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', None, 'Charlie', 'David'],
        'value': [10, 20, None, 40]
    })

@pytest.fixture
def sample_df_with_dates():
    """Sample DataFrame with date strings."""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'date': ['2025-11-01', '01/11/2025', 'Nov 1, 2025']
    })


# ========================================
# TESTS FOR remove_duplicates()
# ========================================

def test_remove_duplicates_basic(sample_df_with_duplicates):
    """Basic duplicate removal test."""
    result = remove_duplicates(sample_df_with_duplicates, subset=['id'])
    expected = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'value': [10, 20, 30]
    })
    result = result.reset_index(drop=True)
    pdt.assert_frame_equal(result, expected)

def test_remove_duplicates_empty_df():
    """Removing duplicates from empty DataFrame returns empty DataFrame."""
    empty_df = pd.DataFrame({'id': [], 'name': []})
    result = remove_duplicates(empty_df)
    assert len(result) == 0
    pdt.assert_frame_equal(result, empty_df)


# ========================================
# TESTS FOR handle_missing_values()
# ========================================

def test_handle_missing_drop(sample_df_with_missing):
    """Test dropping rows with missing values."""
    result = handle_missing_values(sample_df_with_missing, strategy='drop')
    assert len(result) == 2
    assert result['name'].notna().all()
    assert result['value'].notna().all()

def test_handle_missing_fill(sample_df_with_missing):
    """Test filling missing values."""
    result = handle_missing_values(sample_df_with_missing, strategy='fill', fill_value=0)
    assert len(result) == 4
    # Check missing values filled
    assert result['name'].notna().all() or (result['name'] == 0).any()
    assert result['value'].notna().all()


# ========================================
# TESTS FOR standardize_dates()
# ========================================

def test_standardize_dates(sample_df_with_dates):
    """Test that standardize_dates can be called and preserves length."""
    result = standardize_dates(sample_df_with_dates, 'date')

    # Ensure the column exists and has same number of rows
    assert 'date' in result.columns
    assert len(result) == len(sample_df_with_dates)

    # Optionally check the first row parses correctly
    import pandas as pd
    first_date = pd.to_datetime(result['date'].iloc[0], errors='coerce')
    assert first_date == pd.Timestamp('2025-11-01')





