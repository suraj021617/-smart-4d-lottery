# Provider Normalization Architecture - Production Design

## Problem Statement
SportsToto data not showing due to inconsistent provider names in CSV:
- "Sports Toto", "SPORTS-TOTO", "SportsToto", "toto", etc.
- Exact string matching causes silent failures
- No centralized provider management

## Solution Architecture

### 1. **Canonical Provider Registry** (Single Source of Truth)
```
utils/provider_registry.py - ALREADY CREATED ✅
```

**Key Features:**
- Canonical keys: `sportstoto`, `magnum`, `damacai`, etc.
- Alias mapping for all variations
- Display names for UI
- Metadata (colors, logos)

### 2. **Data Ingestion Layer** (Normalize at Entry)
```python
# In load_csv_data() function - LINE 57-110
df['provider'] = df['provider'].apply(ProviderRegistry.normalize)
```

**Benefits:**
- All data normalized ONCE at load time
- No repeated normalization overhead
- Consistent internal representation

### 3. **Business Logic Layer** (Always Use Canonical Keys)
```python
# All routes and functions use canonical keys
if provider != 'all':
    df = df[df['provider'] == 'sportstoto']  # Always lowercase canonical
```

### 4. **Presentation Layer** (Display Names for UI)
```python
# In templates
{{ ProviderRegistry.get_display_name(provider) }}  # Shows "Sports Toto"
```

## Implementation Steps

### Step 1: Update load_csv_data()
```python
from utils.provider_registry import ProviderRegistry

def load_csv_data():
    # ... existing code ...
    
    # REPLACE existing provider normalization with:
    df['provider'] = df['provider'].apply(ProviderRegistry.normalize)
    
    # Remove old hardcoded replace() calls
```

### Step 2: Update All Routes
```python
# BEFORE (Inconsistent)
provider = request.args.get('provider', 'all').lower().strip()

# AFTER (Consistent)
provider = ProviderRegistry.normalize(request.args.get('provider', 'all'))
```

### Step 3: Update Templates
```html
<!-- BEFORE -->
<option value="toto">SportsToto</option>

<!-- AFTER -->
{% for key in provider_keys %}
<option value="{{ key }}">{{ get_display_name(key) }}</option>
{% endfor %}
```

## Benefits

### 1. **Single Source of Truth**
- All provider logic in ONE place
- Easy to add new providers
- No scattered hardcoded values

### 2. **Prevents Future Bugs**
- New CSV variations automatically handled
- Centralized alias management
- Type-safe canonical keys

### 3. **Maintainability**
- Add provider: Update ONE file
- Change display name: Update ONE place
- No grep-and-replace needed

### 4. **Performance**
- Normalize ONCE at data load
- No repeated string operations
- Efficient lookups

## Testing Strategy

### Test Cases:
1. CSV with "Sports Toto" → normalizes to `sportstoto`
2. CSV with "SPORTS-TOTO" → normalizes to `sportstoto`
3. UI filter with `sportstoto` → matches all variations
4. Display shows "Sports Toto" (user-friendly)

## Migration Path

### Phase 1: Add Registry (DONE ✅)
- Created `utils/provider_registry.py`
- No breaking changes

### Phase 2: Update Data Layer
- Modify `load_csv_data()`
- Test with existing data

### Phase 3: Update Routes
- Replace hardcoded provider logic
- Use canonical keys everywhere

### Phase 4: Update Templates
- Use display names from registry
- Dynamic provider dropdowns

## Code Locations to Update

1. **app.py** (Line 57-110): `load_csv_data()` function
2. **app.py** (Multiple routes): Provider filtering logic
3. **templates/*.html**: Provider dropdowns and displays

## Example: Adding New Provider

```python
# ONLY update utils/provider_registry.py
'sabah88': {
    'display_name': 'Sabah 88',
    'aliases': ['sabah', 'sabah88', 'sabah 88', 'sabah-88'],
    'color': '#AA96DA',
    'logo': 'sabah.png'
}
```

That's it! No other files need changes.

## Rollback Plan

If issues occur:
1. Registry is additive (doesn't break existing code)
2. Can revert `load_csv_data()` changes
3. Old hardcoded logic still works as fallback

## Success Metrics

- ✅ SportsToto data appears in past results
- ✅ All provider variations work
- ✅ No duplicate provider entries
- ✅ Consistent filtering across all pages
- ✅ Easy to add new providers (< 5 minutes)

## Next Steps

1. Test current implementation
2. Update `load_csv_data()` to use registry
3. Gradually migrate routes
4. Update templates last (cosmetic)
