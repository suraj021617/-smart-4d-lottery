# 🔧 Quick Fix Reference - Decision Helper

## Problem
Backup numbers not changing when provider changes in Decision Helper

## Root Cause
1. Simple vote counting instead of weighted scoring
2. No cache clearing between requests
3. Provider filtering issues

## Solution Applied

### File: `app.py` (Line ~4800)

**Key Changes:**
```python
# 1. Clear caches
_smart_model_cache.clear()
_ml_model_cache.clear()

# 2. Filter by provider with fallback
if provider != 'all':
    df_filtered = df_filtered[df_filtered['provider_key'] == provider]
    if df_filtered.empty:
        df_filtered = df[df['provider_key'].str.lower() == provider.lower()]

# 3. Weighted scoring (not simple counting)
weighted_votes[num] = score * 1.2  # Advanced
weighted_votes[num] = score * 1.0  # Smart
weighted_votes[num] = score * 0.8  # ML

# 4. Sort by weighted score
sorted_votes = sorted(weighted_votes.items(), key=lambda x: x[1], reverse=True)

# 5. Extract top 5 + backup 10
final_picks = sorted_votes[:5]
backup_numbers = sorted_votes[5:15]
```

## Test
1. Go to `/decision-helper`
2. Change provider dropdown
3. Backup numbers should change

## Status
✅ FIXED AND WORKING

## Date
2026-01-24
