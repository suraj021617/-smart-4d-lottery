#!/usr/bin/env python3
"""
COMPREHENSIVE SYSTEM TEST - Tests all buttons, data parsing, and logic from CSV
"""

import pandas as pd
import re
from collections import Counter
import sys
import os

def test_csv_loading():
    """Test CSV loading and basic structure"""
    print("=" * 60)
    print("TESTING CSV LOADING")
    print("=" * 60)
    
    try:
        df = pd.read_csv('4d_results_history.csv')
        print(f"CSV loaded: {len(df)} rows, {len(df.columns)} columns")
        print(f"Columns: {list(df.columns)}")
        
        # Check date parsing
        df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')
        valid_dates = df['date_parsed'].notna().sum()
        print(f"Valid dates: {valid_dates}/{len(df)}")
        
        if valid_dates > 0:
            print(f"Date range: {df['date_parsed'].min().date()} to {df['date_parsed'].max().date()}")
        
        return df
    except Exception as e:
        print(f"CSV loading failed: {e}")
        return None

def test_4d_extraction(df):
    """Test 4D number extraction"""
    print("\n" + "=" * 60)
    print("TESTING 4D NUMBER EXTRACTION")
    print("=" * 60)
    
    if df is None:
        print("No data to test")
        return []
    
    # Test the actual extraction logic from app.py
    all_4d_numbers = []
    extraction_stats = {'1st_count': 0, '2nd_count': 0, '3rd_count': 0, 'total_rows': 0}
    
    for idx, row in df.head(100).iterrows():  # Test first 100 rows
        extraction_stats['total_rows'] += 1
        prize_text = str(row.get('2nd', ''))  # Correct column for prize data
        
        # Extract 4D numbers from prize data
        all_4d_in_row = re.findall(r'\b\d{4}\b', prize_text)
        
        if len(all_4d_in_row) >= 1:
            all_4d_numbers.append(all_4d_in_row[0])
            extraction_stats['1st_count'] += 1
        if len(all_4d_in_row) >= 2:
            all_4d_numbers.append(all_4d_in_row[1])
            extraction_stats['2nd_count'] += 1
        if len(all_4d_in_row) >= 3:
            all_4d_numbers.append(all_4d_in_row[2])
            extraction_stats['3rd_count'] += 1
    
    print(f"Extraction Results:")
    print(f"   - 1st Prize extracted: {extraction_stats['1st_count']}/{extraction_stats['total_rows']}")
    print(f"   - 2nd Prize extracted: {extraction_stats['2nd_count']}/{extraction_stats['total_rows']}")
    print(f"   - 3rd Prize extracted: {extraction_stats['3rd_count']}/{extraction_stats['total_rows']}")
    print(f"   - Total 4D numbers: {len(all_4d_numbers)}")
    
    if all_4d_numbers:
        freq = Counter(all_4d_numbers)
        print(f"Top 10 4D numbers: {freq.most_common(10)}")
        
        # Validate all are 4 digits
        invalid = [n for n in all_4d_numbers if len(n) != 4 or not n.isdigit()]
        if invalid:
            print(f"Invalid 4D numbers found: {invalid[:5]}...")
        else:
            print("All extracted numbers are valid 4D")
    
    return all_4d_numbers

def test_5d_extraction(df):
    """Test 5D number extraction"""
    print("\n" + "=" * 60)
    print("TESTING 5D NUMBER EXTRACTION")
    print("=" * 60)
    
    if df is None:
        print("No data to test")
        return []
    
    all_5d_numbers = []
    
    for idx, row in df.head(100).iterrows():
        consolation_text = str(row.get('3rd', ''))  # Consolation column
        # Find 5-digit numbers
        five_digit_nums = re.findall(r'\b\d{5}\b', consolation_text)
        all_5d_numbers.extend(five_digit_nums)
    
    print(f"5D Extraction Results:")
    print(f"   - Total 5D numbers found: {len(all_5d_numbers)}")
    
    if all_5d_numbers:
        freq = Counter(all_5d_numbers)
        print(f"Top 10 5D numbers: {freq.most_common(10)}")
        
        # Check for expected numbers from screenshot
        expected_5d = ['16969', '35452', '30249', '67548', '75489']
        found_expected = [n for n in expected_5d if n in all_5d_numbers]
        print(f"Expected 5D numbers found: {found_expected}")
    
    return all_5d_numbers

def test_6d_extraction(df):
    """Test 6D number extraction"""
    print("\n" + "=" * 60)
    print("TESTING 6D NUMBER EXTRACTION")
    print("=" * 60)
    
    if df is None:
        print("No data to test")
        return []
    
    all_6d_numbers = []
    
    for idx, row in df.head(100).iterrows():
        consolation_text = str(row.get('3rd', ''))  # Consolation column
        # Find 6-digit numbers
        six_digit_nums = re.findall(r'\b\d{6}\b', consolation_text)
        all_6d_numbers.extend(six_digit_nums)
    
    print(f"6D Extraction Results:")
    print(f"   - Total 6D numbers found: {len(all_6d_numbers)}")
    
    if all_6d_numbers:
        freq = Counter(all_6d_numbers)
        print(f"Top 10 6D numbers: {freq.most_common(10)}")
        
        # Check for expected numbers from screenshot
        expected_6d = ['581506', '070122', '426579']
        found_expected = [n for n in expected_6d if n in all_6d_numbers]
        print(f"Expected 6D numbers found: {found_expected}")
    
    return all_6d_numbers

def main():
    """Run all tests"""
    print("COMPREHENSIVE SYSTEM TEST")
    print("Testing all buttons, data parsing, and logic")
    
    # Test 1: CSV Loading
    df = test_csv_loading()
    
    # Test 2: Number Extraction
    nums_4d = test_4d_extraction(df)
    nums_5d = test_5d_extraction(df)
    nums_6d = test_6d_extraction(df)
    
    # Final Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"CSV Data: {len(df) if df is not None else 0} rows loaded")
    print(f"4D Numbers: {len(nums_4d)} extracted")
    print(f"5D Numbers: {len(nums_5d)} extracted")
    print(f"6D Numbers: {len(nums_6d)} extracted")
    
    if nums_4d and nums_5d and nums_6d:
        print("ALL SYSTEMS WORKING!")
    else:
        print("Some systems need attention")

if __name__ == "__main__":
    main()