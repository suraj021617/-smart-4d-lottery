# Column Name Mapping Reference

## Canonical Column Names (from data_normalizer.py)
These are the ACTUAL column names created by the data normalizer:
- `number_1st` - 1st Prize number
- `number_2nd` - 2nd Prize number
- `number_3rd` - 3rd Prize number
- `provider_key` - Provider identifier
- `date_parsed` - Parsed date
- `special` - Special prize numbers
- `consolation` - Consolation prize numbers

## Backward Compatibility Aliases (added in load_csv_data)
These aliases are created for backward compatibility:
- `1st_real` → `number_1st`
- `2nd_real` → `number_2nd`
- `3rd_real` → `number_3rd`
- `provider` → `provider_key`

## How to Check for Similar Issues

### Pattern 1: Direct DataFrame Column Access
```python
# ❌ WRONG - Will fail if column doesn't exist
df['1st_real']
df['2nd_real']
df['3rd_real']

# ✅ CORRECT - Use canonical names or aliases
df['number_1st']  # or df['1st_real'] (alias)
df['number_2nd']  # or df['2nd_real'] (alias)
df['number_3rd']  # or df['3rd_real'] (alias)
```

### Pattern 2: Iterating Over Columns
```python
# ❌ WRONG - Column names don't exist
for col in ['1st_real', '2nd_real', '3rd_real']:
    df[col]

# ✅ CORRECT - Check if column exists first
for col in ['number_1st', 'number_2nd', 'number_3rd']:
    if col in df.columns:
        df[col]
```

### Pattern 3: Using .get() on DataFrame Rows
```python
# ❌ WRONG - May return None if column doesn't exist
row.get('1st_real')

# ✅ CORRECT - Use canonical names
row.get('number_1st')
```

## Quick Fix Checklist

When you encounter a `KeyError` for a column:

1. **Identify the column name** that's causing the error
2. **Check if it's an alias** (1st_real, 2nd_real, 3rd_real, provider)
3. **Verify the canonical name** from data_normalizer.py
4. **Update the code** to use the correct column name
5. **Add validation** with `if col in df.columns:` before accessing

## Common Issues and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `KeyError: '1st_real'` | Column doesn't exist | Use `number_1st` or ensure aliases are created |
| `KeyError: 'provider'` | Column doesn't exist | Use `provider_key` or ensure aliases are created |
| `AttributeError: 'NoneType'` | Column value is None | Add null checks before processing |
| `ValueError: invalid literal` | Invalid data format | Validate data before type conversion |

## Testing Your Fix

After making changes:

```bash
# 1. Check syntax
python -m py_compile app.py

# 2. Test the specific route
# Navigate to the route in browser and check for errors

# 3. Check logs for warnings
# Look for any KeyError or AttributeError messages
```

## Prevention Tips

1. **Always use canonical column names** from data_normalizer.py
2. **Add column existence checks** before accessing
3. **Use .get() method** for safer dictionary/row access
4. **Test with actual data** to catch column name issues early
5. **Document column names** in function docstrings
