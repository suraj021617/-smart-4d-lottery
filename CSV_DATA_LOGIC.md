# 📊 CSV Data Structure & Logic Guide

## Current CSV Format (4d_results_history.csv)

### Raw Columns (Before Normalization)
```
Col 0: date (YYYY-MM-DD)
Col 1: provider_url (https://www.live4d2u.net/images/gdlotto)
Col 2: provider_name (Grand Dragon 4D)
Col 3: draw_number (optional)
Col 4: draw_date_text (08-10-2025 (Wed))
Col 5: prize_text (1st Prize 0097 | 2nd Prize 8212 | 3rd Prize 7198)
Col 6: special (1194 2418 5298 ---- 0916 8723 7423 6269 8665 ---- 1285 ---- 3454)
Col 7: consolation (0113 0551 8063 2229 3182 2046 4171 8297 4776 7432)
```

### Normalized Columns (After data_normalizer.py)
```
date_parsed          → Parsed datetime
provider_key         → Normalized provider name (e.g., "GD Lotto")
number_1st           → 1st prize 4D number (e.g., "0097")
number_2nd           → 2nd prize 4D number (e.g., "8212")
number_3rd           → 3rd prize 4D number (e.g., "7198")
special              → Space-separated 4D numbers (e.g., "1194 2418 5298 0916...")
consolation          → Space-separated 4D numbers (e.g., "0113 0551 8063 2229...")
total_4d_found       → Count of all 4D numbers in row
is_valid             → Boolean (has date + provider + at least one 4D number)
```

## Data Extraction Logic

### 1. Main Prizes (1st, 2nd, 3rd)
```python
# Extract from prize_text column (Col 5)
# Pattern: "1st Prize XXXX | 2nd Prize XXXX | 3rd Prize XXXX"

first_match = re.search(r'1st[^0-9]*(\\d{4})', prize_text, re.IGNORECASE)
second_match = re.search(r'2nd[^0-9]*(\\d{4})', prize_text, re.IGNORECASE)
third_match = re.search(r'3rd[^0-9]*(\\d{4})', prize_text, re.IGNORECASE)

# Result: "0097", "8212", "7198"
```

### 2. Special Prizes
```python
# Extract from special column (Col 6)
# Format: "1194 2418 5298 ---- 0916 8723 7423 6269 8665 ---- 1285 ---- 3454"
# Note: "----" and "****" are placeholders for empty positions

special_4d = re.findall(r'\\b\\d{4}\\b', special_text)
special_nums = [n for n in special_4d if n != '----' and n != '****']

# Result: ["1194", "2418", "5298", "0916", "8723", "7423", "6269", "8665", "1285", "3454"]
# Stored as: "1194 2418 5298 0916 8723 7423 6269 8665 1285 3454"
```

### 3. Consolation Prizes
```python
# Extract from consolation column (Col 7)
# Format: "0113 0551 8063 2229 3182 2046 4171 8297 4776 7432"

consolation_4d = re.findall(r'\\b\\d{4}\\b', consolation_text)
consolation_nums = [n for n in consolation_4d if n != '----' and n != '****']

# Result: ["0113", "0551", "8063", "2229", "3182", "2046", "4171", "8297", "4776", "7432"]
# Stored as: "0113 0551 8063 2229 3182 2046 4171 8297 4776 7432"
```

## Day-to-Day Predictor Logic

### Step 1: Get Latest Date's Numbers
```python
latest_date = filtered_df['date_parsed'].max()  # e.g., 2025-10-12
today_data = filtered_df[filtered_df['date_parsed'] == latest_date]

# Extract all numbers from that date
today_numbers = []

# Add 1st, 2nd, 3rd prizes
for col in ['number_1st', 'number_2nd', 'number_3rd']:
    num = str(row.get(col, '')).strip()
    if num and len(num) == 4 and num.isdigit():
        today_numbers.append(num)

# Add special prizes (split by space)
special_str = str(row.get('special', '')).strip()
special_nums = special_str.split()  # ["1194", "2418", "5298", ...]
today_numbers.extend(special_nums)

# Add consolation prizes (split by space)
consolation_str = str(row.get('consolation', '')).strip()
consolation_nums = consolation_str.split()  # ["0113", "0551", "8063", ...]
today_numbers.extend(consolation_nums)

# Result: ["0097", "8212", "7198", "1194", "2418", "5298", ..., "0113", "0551", "8063", ...]
```

### Step 2: Build Markov Chain from History
```python
# Get all historical 1st prizes (excluding today)
historical_draws = []
for _, row in filtered_df[filtered_df['date_parsed'] < latest_date].iterrows():
    num = str(row.get('number_1st', '')).strip()
    if num and len(num) == 4 and num.isdigit():
        historical_draws.append(num)

# Build transitions: which numbers follow which
transitions = {}
for i in range(len(historical_draws) - 1):
    current = historical_draws[i]
    next_num = historical_draws[i + 1]
    
    if current not in transitions:
        transitions[current] = {}
    transitions[current][next_num] = transitions[current].get(next_num, 0) + 1

# Result: {"0097": {"8212": 2, "7198": 1}, "8212": {"7198": 3}, ...}
```

### Step 3: Generate Predictions
```python
# For each number in today_numbers, find what followed it historically
predictions = []

for today_num in today_numbers:
    if today_num in transitions:
        next_candidates = transitions[today_num]
        total = sum(next_candidates.values())
        
        for next_num, count in sorted(next_candidates.items(), key=lambda x: x[1], reverse=True):
            confidence = (count / total) * 100
            predictions.append((next_num, confidence, f"Followed {today_num} {count}x"))

# Result: [("8212", 66.7, "Followed 0097 2x"), ("7198", 33.3, "Followed 0097 1x"), ...]
```

## Past Results Display Logic

### Extract & Display
```python
for idx, row in filtered.iterrows():
    # Get date
    date_str = row['date_parsed'].strftime('%d-%m-%Y')  # "08-10-2025"
    
    # Get provider
    provider = str(row.get('provider_key', 'UNKNOWN')).upper()  # "GD LOTTO"
    
    # Get main prizes (with fallback to '-')
    first = str(row.get('number_1st', '')).strip() or '-'  # "0097"
    second = str(row.get('number_2nd', '')).strip() or '-'  # "8212"
    third = str(row.get('number_3rd', '')).strip() or '-'  # "7198"
    
    # Get special prizes (split by space)
    special_str = str(row.get('special', '')).strip()
    special_list = [n for n in special_str.split() if n and len(n) == 4 and n.isdigit()]
    # Result: ["1194", "2418", "5298", "0916", "8723", "7423", "6269", "8665", "1285", "3454"]
    
    # Get consolation prizes (split by space)
    consolation_str = str(row.get('consolation', '')).strip()
    consolation_list = [n for n in consolation_str.split() if n and len(n) == 4 and n.isdigit()]
    # Result: ["0113", "0551", "8063", "2229", "3182", "2046", "4171", "8297", "4776", "7432"]
    
    results.append({
        'date': '08-10-2025',
        'provider': 'GD LOTTO',
        'first': '0097',
        'second': '8212',
        'third': '7198',
        'special': ["1194", "2418", "5298", "0916", "8723", "7423", "6269", "8665", "1285", "3454"],
        'consolation': ["0113", "0551", "8063", "2229", "3182", "2046", "4171", "8297", "4776", "7432"]
    })
```

## Key Points

✅ **Special & Consolation are space-separated strings**
- Store: `"1194 2418 5298 0916 8723 7423 6269 8665 1285 3454"`
- Extract: `special_str.split()` → `["1194", "2418", "5298", ...]`

✅ **Empty positions marked with "----" or "****"**
- Filter them out: `if n != '----' and n != '****'`

✅ **Always validate 4D numbers**
- Check: `len(n) == 4 and n.isdigit()`

✅ **Handle null/empty values gracefully**
- Use: `str(row.get(col, '')).strip()`
- Check: `if value and value not in ['nan', '', 'None']`

✅ **Date filtering order matters**
- Filter by provider FIRST
- Get latest date SECOND
- Extract data THIRD

## Example CSV Row

```
2025-10-08 | https://www.live4d2u.net/images/gdlotto | Grand Dragon 4D | | 08-10-2025 (Wed) | 1st Prize 0097 | 2nd Prize 8212 | 3rd Prize 7198 | 1194 2418 5298 ---- 0916 8723 7423 6269 8665 ---- 1285 ---- 3454 | 0113 0551 8063 2229 3182 2046 4171 8297 4776 7432
```

After normalization:
```
date_parsed: 2025-10-08
provider_key: GD Lotto
number_1st: 0097
number_2nd: 8212
number_3rd: 7198
special: 1194 2418 5298 0916 8723 7423 6269 8665 1285 3454
consolation: 0113 0551 8063 2229 3182 2046 4171 8297 4776 7432
total_4d_found: 23
is_valid: True
```

This is now properly extracted and displayed! ✅
