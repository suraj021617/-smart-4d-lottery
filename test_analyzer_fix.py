"""
Test script to verify Pattern Analyzer buttons logic fix
"""

from utils.ai_predictor import predict_top_5
from utils.app_grid import generate_4x4_grid, generate_reverse_grid

# Test data
test_number = "1234"
test_draws = [{
    "number": test_number,
    "grid": generate_4x4_grid(test_number),
    "reverse_grid": generate_reverse_grid(test_number),
    "date": "2025-02-22"
}]

print("=" * 60)
print("🧪 TESTING PATTERN ANALYZER BUTTONS LOGIC")
print("=" * 60)

# Test Pattern Mode
print("\n1️⃣ Testing PATTERN Mode:")
print("-" * 60)
pattern_results = predict_top_5(test_draws, mode="pattern")
print(f"Mode: pattern")
print(f"Predictions: {pattern_results.get('combined', [])[:3]}")

# Test Frequency Mode
print("\n2️⃣ Testing FREQUENCY Mode:")
print("-" * 60)
freq_results = predict_top_5(test_draws, mode="history")
print(f"Mode: history (frequency)")
print(f"Predictions: {freq_results.get('combined', [])[:3]}")

# Test Combined Mode
print("\n3️⃣ Testing COMBINED Mode:")
print("-" * 60)
combined_results = predict_top_5(test_draws, mode="combined")
print(f"Mode: combined")
print(f"Predictions: {combined_results.get('combined', [])[:3]}")

# Verify they're different
print("\n" + "=" * 60)
print("✅ VERIFICATION:")
print("=" * 60)

pattern_nums = [p[0] for p in pattern_results.get('combined', [])[:3]]
freq_nums = [p[0] for p in freq_results.get('combined', [])[:3]]
combined_nums = [p[0] for p in combined_results.get('combined', [])[:3]]

if pattern_nums != freq_nums:
    print("✅ Pattern vs Frequency: DIFFERENT (GOOD!)")
else:
    print("❌ Pattern vs Frequency: SAME (BAD!)")

if pattern_nums != combined_nums:
    print("✅ Pattern vs Combined: DIFFERENT (GOOD!)")
else:
    print("⚠️ Pattern vs Combined: SAME (May be OK)")

if freq_nums != combined_nums:
    print("✅ Frequency vs Combined: DIFFERENT (GOOD!)")
else:
    print("⚠️ Frequency vs Combined: SAME (May be OK)")

print("\n" + "=" * 60)
print("🎯 TEST COMPLETE!")
print("=" * 60)
print("\nIf you see 'DIFFERENT' for Pattern vs Frequency, the fix is working!")
print("The predictions should change based on the selected mode.")
