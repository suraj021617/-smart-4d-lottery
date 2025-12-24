import pandas as pd
from collections import Counter, defaultdict
import re

df = pd.read_csv('4d_results_history.csv', on_bad_lines='skip')

# Extract 1st Prize numbers chronologically
first_prizes = []
for _, row in df.iterrows():
    prize_text = str(row['1st']) if '1st' in df.columns else ''
    match = re.search(r'(\d{4})', prize_text)
    if match:
        num = match.group(1)
        if len(num) == 4 and num.isdigit():
            first_prizes.append(num)

# Build transition matrix
transitions = defaultdict(list)
for i in range(len(first_prizes) - 1):
    today = first_prizes[i]
    tomorrow = first_prizes[i + 1]
    transitions[today].append(tomorrow)

# Get today's number (last in history)
today_num = first_prizes[-1]
print(f"Today's number: {today_num}")

# Get all numbers that followed today's number in history
if today_num in transitions:
    next_numbers = transitions[today_num]
    print(f"Numbers that followed {today_num}: {next_numbers}")
else:
    print(f"{today_num} not found in history, using frequency-based fallback")
    # Fallback: use most frequent numbers overall
    all_nums = first_prizes
    next_numbers = Counter(all_nums).most_common(23)
    next_numbers = [num for num, _ in next_numbers]

# Calculate confidence scores based on frequency
freq_counter = Counter(next_numbers)
total = len(next_numbers)

# Generate 23 predictions with confidence scores
predictions = []
for num, count in freq_counter.most_common(23):
    confidence = (count / total) * 10  # Scale to 10
    predictions.append((num, confidence))

# Fill to 23 if needed
if len(predictions) < 23:
    # Add more from overall frequency
    all_nums = first_prizes
    overall_freq = Counter(all_nums)
    existing = set([p[0] for p in predictions])
    for num, count in overall_freq.most_common(100):
        if num not in existing and len(predictions) < 23:
            confidence = (count / len(all_nums)) * 10
            predictions.append((num, confidence))
            existing.add(num)

# Display 23 predictions
print("\n23 Predictions for tomorrow:")
for i, (num, conf) in enumerate(predictions[:23], 1):
    print(f"{num} - {conf:.1f}")
print(f"Total: 23 predictions")
