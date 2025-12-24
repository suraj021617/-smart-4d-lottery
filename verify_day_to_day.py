import pandas as pd
from collections import Counter
import re

df = pd.read_csv('4d_results_history.csv', on_bad_lines='skip')

first_prizes = []
for _, row in df.iterrows():
    prize_text = str(row['1st']) if '1st' in df.columns else ''
    match = re.search(r'(\d{4})', prize_text)
    if match:
        num = match.group(1)
        if len(num) == 4 and num.isdigit():
            first_prizes.append(num)

print(f"Total 1st Prize numbers extracted: {len(first_prizes)}")
print(f"First 15: {first_prizes[:15]}")

transitions = {}
for i in range(len(first_prizes) - 1):
    today = first_prizes[i]
    tomorrow = first_prizes[i + 1]
    if today not in transitions:
        transitions[today] = []
    transitions[today].append(tomorrow)

print(f"\nTransition matrix built: {len(transitions)} unique numbers")

test_num = '0832'
if test_num in transitions:
    print(f"\nNumbers that followed {test_num}:")
    counter = Counter(transitions[test_num])
    for num, count in counter.most_common():
        print(f"  -> {num} ({count}x)")
else:
    print(f"\n{test_num} not found in history")

print("\nSample transitions (first 5):")
for i, (num, nexts) in enumerate(list(transitions.items())[:5]):
    counter = Counter(nexts)
    print(f"{num} -> {dict(counter.most_common(3))}")

print(f"\nStatus: WORKING - Transition matrix has {len(transitions)} unique numbers")
