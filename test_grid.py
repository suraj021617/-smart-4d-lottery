#!/usr/bin/env python
# Quick test script for grid and pattern logic

from utils.app_grid import generate_4x4_grid, generate_reverse_grid
from utils.pattern_finder import find_all_4digit_patterns

# Test with a sample number
test_number = "1234"

print("=" * 60)
print(f"Testing with number: {test_number}")
print("=" * 60)

# Generate grids
main_grid = generate_4x4_grid(test_number)
reverse_grid = generate_reverse_grid(test_number)

print("\nMAIN GRID (Forward):")
for i, row in enumerate(main_grid, 1):
    print(f"Row {i}: {row}")

print("\nREVERSE GRID (Backward):")
for i, row in enumerate(reverse_grid, 1):
    print(f"Row {i}: {row}")

# Find patterns
print("\nPATTERNS IN MAIN GRID:")
main_patterns = find_all_4digit_patterns(main_grid)
print(f"Total patterns found: {len(main_patterns)}")
if main_patterns:
    for i, (kind, idx, pattern, coords) in enumerate(main_patterns[:10], 1):
        print(f"{i}. {pattern} ({kind}) at {coords}")
else:
    print("NO PATTERNS FOUND!")

print("\nPATTERNS IN REVERSE GRID:")
reverse_patterns = find_all_4digit_patterns(reverse_grid)
print(f"Total patterns found: {len(reverse_patterns)}")
if reverse_patterns:
    for i, (kind, idx, pattern, coords) in enumerate(reverse_patterns[:10], 1):
        print(f"{i}. {pattern} ({kind}) at {coords}")
else:
    print("NO PATTERNS FOUND!")

# Test with actual lottery number
test_number2 = "5678"
print("\n" + "=" * 60)
print(f"Testing with number: {test_number2}")
print("=" * 60)

main_grid2 = generate_4x4_grid(test_number2)
print("\nMAIN GRID:")
for i, row in enumerate(main_grid2, 1):
    print(f"Row {i}: {row}")

patterns2 = find_all_4digit_patterns(main_grid2)
print(f"\nFound {len(patterns2)} patterns")
if patterns2:
    # Show unique patterns only
    unique_patterns = list(set([p for _, _, p, _ in patterns2]))
    print(f"Unique 4D patterns: {unique_patterns[:20]}")
