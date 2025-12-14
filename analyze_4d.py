import pandas as pd
import re

# Read CSV
df = pd.read_csv('4d_results_history.csv', header=None)

# Extract winning numbers from prize column
def extract_numbers(text):
    if pd.isna(text):
        return []
    numbers = re.findall(r'\b\d{4}\b', str(text))
    return numbers[:3]  # First 3 prizes

# Get all winning numbers
all_numbers = []
for _, row in df.iterrows():
    numbers = extract_numbers(row[4])
    all_numbers.extend(numbers)

# Count frequency
from collections import Counter
freq = Counter(all_numbers)

print("Top 10 most frequent 4D numbers:")
for num, count in freq.most_common(10):
    print(f"{num}: {count} times")