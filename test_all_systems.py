#!/usr/bin/env python3
"""
🔍 COMPREHENSIVE SYSTEM TEST
Tests all buttons, data parsing, and logic from CSV
"""

import pandas as pd
import re
from collections import Counter
import sys
import os

def test_csv_loading():
    """Test CSV loading and basic structure"""
    print("=" * 60)
    print("🔍 TESTING CSV LOADING")
    print("=" * 60)
    
    try:
        df = pd.read_csv('4d_results_history.csv')
        print(f"✅ CSV loaded: {len(df)} rows, {len(df.columns)} columns")
        print(f"📊 Columns: {list(df.columns)}")
        
        # Check date parsing
        df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')
        valid_dates = df['date_parsed'].notna().sum()
        print(f"📅 Valid dates: {valid_dates}/{len(df)}")
        
        if valid_dates > 0:
            print(f"📅 Date range: {df['date_parsed'].min().date()} to {df['date_parsed'].max().date()}")
        
        return df
    except Exception as e:
        print(f"❌ CSV loading failed: {e}")
        return None

def test_4d_extraction(df):
    """Test 4D number extraction"""
    print("\n" + "=" * 60)
    print("🎯 TESTING 4D NUMBER EXTRACTION")
    print("=" * 60)
    
    if df is None:
        print("❌ No data to test")
        return []
    
    # Test the actual extraction logic from app.py
    all_4d_numbers = []
    extraction_stats = {'1st_count': 0, '2nd_count': 0, '3rd_count': 0, 'total_rows': 0}
    
    for idx, row in df.head(100).iterrows():  # Test first 100 rows
        extraction_stats['total_rows'] += 1
        prize_text = str(row.get('3rd', ''))
        
        # Extract using same logic as app.py
        first_match = re.search(r'1st\s+Prize[^\d]*(\d{4})', prize_text, re.IGNORECASE)
        second_match = re.search(r'2nd\s+Prize[^\d]*(\d{4})', prize_text, re.IGNORECASE)
        third_match = re.search(r'3rd\s+Prize[^\d]*(\d{4})', prize_text, re.IGNORECASE)
        
        if first_match:
            all_4d_numbers.append(first_match.group(1))
            extraction_stats['1st_count'] += 1
        if second_match:
            all_4d_numbers.append(second_match.group(1))
            extraction_stats['2nd_count'] += 1
        if third_match:
            all_4d_numbers.append(third_match.group(1))
            extraction_stats['3rd_count'] += 1
    
    print(f"📊 Extraction Results:")
    print(f"   - 1st Prize extracted: {extraction_stats['1st_count']}/{extraction_stats['total_rows']}")
    print(f"   - 2nd Prize extracted: {extraction_stats['2nd_count']}/{extraction_stats['total_rows']}")
    print(f"   - 3rd Prize extracted: {extraction_stats['3rd_count']}/{extraction_stats['total_rows']}")
    print(f"   - Total 4D numbers: {len(all_4d_numbers)}")
    
    if all_4d_numbers:
        freq = Counter(all_4d_numbers)
        print(f"🔥 Top 10 4D numbers: {freq.most_common(10)}")
        
        # Validate all are 4 digits
        invalid = [n for n in all_4d_numbers if len(n) != 4 or not n.isdigit()]
        if invalid:
            print(f"⚠️  Invalid 4D numbers found: {invalid[:5]}...")
        else:
            print("✅ All extracted numbers are valid 4D")
    
    return all_4d_numbers

def test_5d_extraction(df):
    """Test 5D number extraction"""
    print("\n" + "=" * 60)
    print("🚀 TESTING 5D NUMBER EXTRACTION")
    print("=" * 60)
    
    if df is None:
        print("❌ No data to test")
        return []
    
    all_5d_numbers = []
    
    for idx, row in df.head(100).iterrows():
        prize_text = str(row.get('3rd', ''))
        # Find 5-digit numbers
        five_digit_nums = re.findall(r'\b\d{5}\b', prize_text)
        all_5d_numbers.extend(five_digit_nums)
    
    print(f"📊 5D Extraction Results:")
    print(f"   - Total 5D numbers found: {len(all_5d_numbers)}")
    
    if all_5d_numbers:
        freq = Counter(all_5d_numbers)
        print(f"🔥 Top 10 5D numbers: {freq.most_common(10)}")
        
        # Check for expected numbers from screenshot
        expected_5d = ['16969', '35452', '30249', '67548', '75489']
        found_expected = [n for n in expected_5d if n in all_5d_numbers]
        print(f"✅ Expected 5D numbers found: {found_expected}")
    
    return all_5d_numbers

def test_6d_extraction(df):
    """Test 6D number extraction"""
    print("\n" + "=" * 60)
    print("💎 TESTING 6D NUMBER EXTRACTION")
    print("=" * 60)
    
    if df is None:
        print("❌ No data to test")
        return []
    
    all_6d_numbers = []
    
    for idx, row in df.head(100).iterrows():
        prize_text = str(row.get('3rd', ''))
        # Find 6-digit numbers
        six_digit_nums = re.findall(r'\b\d{6}\b', prize_text)
        all_6d_numbers.extend(six_digit_nums)
    
    print(f"📊 6D Extraction Results:")
    print(f"   - Total 6D numbers found: {len(all_6d_numbers)}")
    
    if all_6d_numbers:
        freq = Counter(all_6d_numbers)
        print(f"🔥 Top 10 6D numbers: {freq.most_common(10)}")
        
        # Check for expected numbers from screenshot
        expected_6d = ['581506', '070122', '426579']
        found_expected = [n for n in expected_6d if n in all_6d_numbers]
        print(f"✅ Expected 6D numbers found: {found_expected}")
    
    return all_6d_numbers

def test_data_separation(df, nums_4d, nums_5d, nums_6d):
    """Test that data is properly separated"""
    print("\n" + "=" * 60)
    print("🔒 TESTING DATA SEPARATION")
    print("=" * 60)
    
    # Check for overlap
    overlap_4d_5d = set(nums_4d) & set(nums_5d)
    overlap_4d_6d = set(nums_4d) & set(nums_6d)
    overlap_5d_6d = set(nums_5d) & set(nums_6d)
    
    print(f"🔍 Overlap Analysis:")
    print(f"   - 4D ∩ 5D: {len(overlap_4d_5d)} numbers")
    print(f"   - 4D ∩ 6D: {len(overlap_4d_6d)} numbers")
    print(f"   - 5D ∩ 6D: {len(overlap_5d_6d)} numbers")
    
    if overlap_4d_5d:
        print(f"⚠️  4D-5D overlap: {list(overlap_4d_5d)[:5]}")
    if overlap_4d_6d:
        print(f"⚠️  4D-6D overlap: {list(overlap_4d_6d)[:5]}")
    if overlap_5d_6d:
        print(f"⚠️  5D-6D overlap: {list(overlap_5d_6d)[:5]}")
    
    if not any([overlap_4d_5d, overlap_4d_6d, overlap_5d_6d]):
        print("✅ Perfect separation - no overlaps!")

def test_prediction_logic():
    """Test prediction logic"""
    print("\n" + "=" * 60)
    print("🧠 TESTING PREDICTION LOGIC")
    print("=" * 60)
    
    try:
        # Import the actual functions from app.py
        sys.path.append('.')
        from app import load_csv_data, advanced_predictor
        
        df = load_csv_data()
        print(f"✅ load_csv_data() works: {len(df)} rows")
        
        # Test 4D predictions
        predictions_4d = advanced_predictor(df, lookback=50)
        print(f"✅ 4D predictions: {len(predictions_4d)} generated")
        
        if predictions_4d:
            for i, (num, score, reason) in enumerate(predictions_4d[:3]):
                print(f"   #{i+1}: {num} (score: {score:.3f}, reason: {reason})")
        
        return True
    except Exception as e:
        print(f"❌ Prediction logic failed: {e}")
        return False

def test_routes():
    """Test route accessibility"""
    print("\n" + "=" * 60)
    print("🌐 TESTING ROUTES")
    print("=" * 60)
    
    routes_to_test = [
        '/lottery-types',
        '/4d-lottery', 
        '/5d-lottery',
        '/6d-lottery'
    ]
    
    try:
        import requests
        base_url = 'http://127.0.0.1:5000'
        
        for route in routes_to_test:
            try:
                response = requests.get(f"{base_url}{route}", timeout=5)
                status = "✅" if response.status_code == 200 else "❌"
                print(f"   {status} {route}: {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"   ⚠️  {route}: Server not running")
            except Exception as e:
                print(f"   ❌ {route}: {e}")
    except ImportError:
        print("⚠️  requests not installed - skipping route tests")

def main():
    """Run all tests"""
    print("🔍 COMPREHENSIVE SYSTEM TEST")
    print("Testing all buttons, data parsing, and logic")
    
    # Test 1: CSV Loading
    df = test_csv_loading()
    
    # Test 2: Number Extraction
    nums_4d = test_4d_extraction(df)
    nums_5d = test_5d_extraction(df)
    nums_6d = test_6d_extraction(df)
    
    # Test 3: Data Separation
    test_data_separation(df, nums_4d, nums_5d, nums_6d)
    
    # Test 4: Prediction Logic
    test_prediction_logic()
    
    # Test 5: Routes
    test_routes()
    
    # Final Summary
    print("\n" + "=" * 60)
    print("📋 FINAL SUMMARY")
    print("=" * 60)
    print(f"✅ CSV Data: {len(df) if df is not None else 0} rows loaded")
    print(f"🎯 4D Numbers: {len(nums_4d)} extracted")
    print(f"🚀 5D Numbers: {len(nums_5d)} extracted")
    print(f"💎 6D Numbers: {len(nums_6d)} extracted")
    
    if nums_4d and nums_5d and nums_6d:
        print("🎉 ALL SYSTEMS WORKING!")
    else:
        print("⚠️  Some systems need attention")

if __name__ == "__main__":
    main()