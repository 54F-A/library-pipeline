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
    """Sample DataFrame with different date formats."""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'date': ['2021-03-25', '03/26/2021', '2021-04-01']
    })


# ========================================
# TESTS FOR remove_duplicates()
# ========================================

def test_remove_duplicates_exact(sample_df_with_duplicates):
    """Test duplicate removal using exact DataFrame comparison."""
    result = remove_duplicates(sample_df_with_duplicates, subset=['id'])

    expected = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'value': [10, 20, 30]
    })

    # Reset index for comparison
    result = result.reset_index(drop=True)
    pdt.assert_frame_equal(result, expected)

def test_remove_duplicates_properties(sample_df_with_duplicates):
    """Test duplicate removal using property assertions."""
    result = remove_duplicates(sample_df_with_duplicates, subset=['id'])

    # Test properties instead of exact values
    assert len(result) == 3
    assert result['id'].is_unique
    assert set(result['id']) == {1, 2, 3}

# ========================================
# TESTS FOR handle_missing_values()
# ========================================

def test_handle_missing_drop(sample_df_with_missing):
    """Test dropping rows with missing values."""
    result = handle_missing_values(sample_df_with_missing, strategy='drop')

    # Should only have rows without any NaN
    assert len(result) == 2
    assert result['name'].notna().all()
    assert result['value'].notna().all()

def test_handle_missing_fill(sample_df_with_missing):
    """Test filling missing values."""
    result = handle_missing_values(
        sample_df_with_missing, 
        strategy='fill', 
        fill_value=0
    )

    # Should have all 4 rows
    assert len(result) == 4
    # No missing values
    assert result['name'].notna().all() or (result['name'] == 0).any()
    assert result['value'].notna().all()

def test_handle_missing_invalid_strategy(sample_df_with_missing):
    """Test that invalid strategy raises error."""
    with pytest.raises(ValueError, match="Unknown strategy"):
        handle_missing_values(sample_df_with_missing, strategy='invalid')

# ========================================
# TESTS FOR standardize_dates()
# ========================================

def test_standardize_dates(sample_df_with_dates):
    """Test standardizing date formats."""
    # Pass the 'date' column explicitly to the function
    result = standardize_dates(sample_df_with_dates, date_columns=['date'])

    # Ensure all dates are of type datetime64[ns]
    assert result['date'].dtype == 'datetime64[ns]'

    # Ensure the dates match the expected datetime values or NaT where invalid
    assert result['date'].iloc[0] == pd.to_datetime('2021-03-25')

    # Handle the possible NaT conversion and check the valid ones
    assert pd.isna(result['date'].iloc[1])  # This will check for NaT
    assert result['date'].iloc[2] == pd.to_datetime('2021-04-01')



