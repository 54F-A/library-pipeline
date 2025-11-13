"""
Library Data Pipeline - Orchestration Script
============================================

This script orchestrates the complete data pipeline:
1. Load raw data from bronze layer
2. Clean and validate the data
3. Save cleaned data to silver layer
4. Print summary statistics

Author: [Your Name]
Date: [Today's Date]
Module: DE5 Module 5 - Product Development
"""

import re
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# Ensure stdout is UTF-8 encoded
sys.stdout.reconfigure(encoding='utf-8')

# Import our custom functions
from src.data_processing.ingestion import load_csv, load_json, load_excel
from src.data_processing.cleaning import (
    remove_duplicates,
    handle_missing_values,
    standardize_dates
)
from src.data_processing.validation import validate_isbn

# ============================================
# CONFIGURATION
# ============================================

BRONZE_DIR = Path('data')
SILVER_DIR = Path('data/silver')
SILVER_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# HELPER FUNCTIONS
# ============================================

def print_section_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_dataframe_info(df, name):
    print(f"\n{name}:")
    print(f"  - Rows: {len(df):,}")
    print(f"  - Columns: {len(df.columns)}")
    print(f"  - Missing values: {df.isnull().sum().sum():,}")
    print(f"  - Duplicates: {df.duplicated().sum():,}")


def save_to_silver(df, filename):
    filepath = SILVER_DIR / filename
    df.to_csv(filepath, index=False)
    return filepath

# ============================================
# PIPELINE STAGES
# ============================================

def process_circulation_data():
    print_section_header("Processing Circulation Data")

    df = load_csv('data/circulation_data.csv')
    print_dataframe_info(df, "Raw data")

    df_clean = remove_duplicates(df, subset=['transaction_id'])
    print(f"  [OK] Removed {len(df) - len(df_clean)} duplicate rows")

    df_clean = handle_missing_values(df_clean, strategy='drop')
    print("  [OK] Dropped rows with missing values")

    filepath = save_to_silver(df_clean, 'circulation_clean.csv')
    print(f"  [OK] Saved to: {filepath}")
    print_dataframe_info(df_clean, "Cleaned data")

    return df_clean


def process_events_data():
    print_section_header("Processing Events Data")

    df = load_json('data/events_data.json')
    print_dataframe_info(df, "Raw data")

    df_clean = handle_missing_values(df, strategy='drop')

    filepath = save_to_silver(df_clean, 'events_clean.csv')
    print(f"  [OK] Saved to: {filepath}")
    print_dataframe_info(df_clean, "Cleaned data")

    return df_clean


def process_catalogue_data():
    print_section_header("Processing Catalogue Data")

    df = load_excel('data/catalogue.xlsx')
    print_dataframe_info(df, "Raw data")

    df_clean = remove_duplicates(df, subset=['ISBN'])
    print(f"  [OK] Removed {len(df) - len(df_clean)} duplicate rows")

    if 'ISBN' in df_clean.columns:
        df_clean['ISBN_valid'] = df_clean['ISBN'].apply(validate_isbn)
        invalid_count = (~df_clean['ISBN_valid']).sum()
        print(f"  [OK] Found {invalid_count} invalid ISBNs")

    filepath = save_to_silver(df_clean, 'catalogue_clean.csv')
    print(f"  [OK] Saved to: {filepath}")
    print_dataframe_info(df_clean, "Cleaned data")

    return df_clean


def process_feedback_data():
    print_section_header("Processing Feedback Data")

    with open('data/feedback.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    feedback_count = content.count('Feedback #')
    print(f"  [OK] Found {feedback_count} feedback entries")

    pattern = r"- ([A-Za-z\s]+ Branch) ~ (\d)⭐"
    matches = re.findall(pattern, content)

    df = pd.DataFrame(matches, columns=["branch", "rating"])
    df["rating"] = df["rating"].astype(int)

    df_summary = (
        df.groupby(["branch", "rating"], as_index=False).size().rename(columns={"size": "count"})
    )

    filepath = save_to_silver(df_summary, "feedback_summary.csv")
    print(f"  [OK] Saved to: {filepath}")
    print(f"  [OK] Processed {feedback_count} feedback entries")

    return df


# ============================================
# MAIN PIPELINE
# ============================================

def run_pipeline():
    print("\n" + "=" * 60)
    print("  LIBRARY DATA PIPELINE")
    print("  Starting pipeline execution...")
    print("  Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)

    start_time = datetime.now()
    results = {}

    try:
        results['circulation'] = process_circulation_data()
        # results['events'] = process_events_data()
        # results['catalogue'] = process_catalogue_data()
        # results['feedback'] = process_feedback_data()

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print_section_header("PIPELINE SUMMARY")
        print("\nPipeline completed successfully!")
        print(f"  - Duration: {duration:.2f} seconds")
        print(f"  - Files processed: {len(results)}")
        print(f"  - Output directory: {SILVER_DIR}")

        print("\nCleaned files created:")
        for file in SILVER_DIR.glob("*.csv"):
            print(f"  - {file.name}")

        print("\nNext steps:")
        print("  1. Review the cleaned data in data/silver/")
        print("  2. Run your data quality analysis")
        print("  3. Deploy to Microsoft Fabric\n")

        return results

    except Exception as e:
        print(f"\n[ERROR] Pipeline failed with error: {str(e)}")
        print("  - Check your data files exist")
        print("  - Check your functions are working")
        raise


# ============================================
# SCRIPT ENTRY POINT
# ============================================

if __name__ == "__main__":
    results = run_pipeline()
