# 🏗️ SYSTEM ARCHITECTURE

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE (Web)                        │
│  [Recent Stats] [Last 3Y] [Last 5Y] [ML] [AI] [Smart] [Full]  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK APP (app.py)                         │
│  • Route requests to appropriate predictors                     │
│  • Handle logging and evaluation                                │
│  • Serve API endpoints                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  PREDICTION RUNNER                              │
│  • Orchestrate all predictors                                   │
│  • Enforce anti-leakage rules                                   │
│  • Generate final consensus                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   ADVANCED   │    │      ML      │    │  AI PATTERN  │
│  PREDICTOR   │    │  PREDICTOR   │    │  PREDICTOR   │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌──────────────────┐
                    │    CONSENSUS     │
                    │  (Weighted Avg)  │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   TOP 5 OUTPUT   │
                    └──────────────────┘
```

---

## Data Flow

### 1. Prediction Flow (Before Result Known)

```
CSV File → History Loader → Cache → Active Data Filter
                                            │
                                            ▼
                              ┌─────────────────────────┐
                              │  Filter by Time Window  │
                              │  • Recent 100           │
                              │  • Recent 300           │
                              │  • Last 3 Years         │
                              │  • Last 5 Years ⭐      │
                              │  • Full History         │
                              └─────────────────────────┘
                                            │
                                            ▼
                              ┌─────────────────────────┐
                              │  Anti-Leakage Filter    │
                              │  date < target_date     │
                              └─────────────────────────┘
                                            │
                                            ▼
                              ┌─────────────────────────┐
                              │  Run Predictors         │
                              │  • Advanced Stats       │
                              │  • ML Features          │
                              │  • AI Patterns          │
                              └─────────────────────────┘
                                            │
                                            ▼
                              ┌─────────────────────────┐
                              │  Consensus Engine       │
                              │  • Load weights         │
                              │  • Merge predictions    │
                              │  • Remove duplicates    │
                              │  • Score & rank         │
                              └─────────────────────────┘
                                            │
                                            ▼
                              ┌─────────────────────────┐
                              │  Prediction Logger      │
                              │  Save to JSONL          │
                              └─────────────────────────┘
                                            │
                                            ▼
                              ┌─────────────────────────┐
                              │  Display Top 5          │
                              └─────────────────────────┘
```

### 2. Evaluation Flow (After Result Known)

```
User Input (Log ID + Actual Result)
                │
                ▼
┌───────────────────────────────┐
│  Load Prediction Log          │
│  (from JSONL)                 │
└───────────────────────────────┘
                │
                ▼
┌───────────────────────────────┐
│  Compare Each Predictor       │
│  • Check exact match          │
│  • Calculate position score   │
│  • Find best match            │
└───────────────────────────────┘
                │
                ▼
┌───────────────────────────────┐
│  Save Evaluation              │
│  (to evaluation_logs.jsonl)   │
└───────────────────────────────┘
                │
                ▼
┌───────────────────────────────┐
│  Auto-Tune System             │
│  • Calculate performance      │
│  • Update weights             │
│  • Save new weights           │
└───────────────────────────────┘
                │
                ▼
┌───────────────────────────────┐
│  Display Evaluation Report    │
└───────────────────────────────┘
```

---

## Module Responsibilities

### history_loader.py
- Load CSV with caching
- Normalize numbers to 4D
- Drop duplicates
- Detect file changes
- Provide anti-leakage filtering

### active_data_filter.py
- Filter by time windows
- Recent N draws
- Last N years
- Full history

### advanced_predictor.py
- Digit frequency analysis
- Hot/cold digits
- Pair/triple patterns
- Transition logic

### ml_predictor.py
- Positional features
- Sum distribution
- Odd/even patterns
- ML-based scoring

### ai_predictor.py
- Grid patterns
- Reverse patterns
- Sequential patterns
- Mirror patterns

### consensus.py
- Load adaptive weights
- Merge predictions
- Remove duplicates
- Weighted scoring
- Save weights

### prediction_logger.py
- Save predictions to JSONL
- Generate log IDs
- Load logs by ID/date
- Provide summary

### result_evaluator.py
- Compare predictions vs actual
- Calculate match scores
- Track exact hits
- Generate leaderboard
- Format reports

### weight_updater.py
- Calculate performance scores
- Update weights with learning rate
- Suggest best window
- Auto-tune system

### drift_analyzer.py
- Digit frequency drift
- Hot/cold changes
- Sum distribution drift
- Odd/even ratio drift
- Positional drift
- Pair frequency drift

### prediction_runner.py
- Orchestrate all predictors
- Enforce anti-leakage
- Route to specific predictors
- Format for display

---

## Anti-Leakage Design

### Critical Points

1. **Data Loading**
   ```python
   # ALWAYS filter by date
   past_data = df[df['date'] < target_date]
   ```

2. **Prediction Time**
   ```python
   # NEVER include target date
   get_data_until_date(df, target_date, exclude_target=True)
   ```

3. **Evaluation Time**
   ```python
   # ONLY after result is known
   evaluate_after_result(log_id, actual_result)
   ```

4. **Learning Time**
   ```python
   # ONLY after evaluation
   update_weights_after_result()
   ```

---

## Adaptive Learning Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                    LEARNING CYCLE                           │
└─────────────────────────────────────────────────────────────┘

1. PREDICT (Before Result)
   ↓
   • Use current weights
   • Generate predictions
   • Log everything
   
2. WAIT (Result Announced)
   ↓
   • No system changes
   • Predictions are frozen
   
3. EVALUATE (After Result)
   ↓
   • Compare predictions vs actual
   • Calculate scores
   • Track performance
   
4. LEARN (Auto-Tune)
   ↓
   • Update weights based on performance
   • Increase weight for good predictors
   • Decrease weight for poor predictors
   
5. REPEAT
   ↓
   • Next prediction uses new weights
   • System gets smarter over time
```

---

## Weight Update Formula

```python
# Performance score (0.0 to 1.0)
performance = (exact_hits * 100 + avg_match_score * 25) / max_score

# Target weight (0.5 to 1.5)
target_weight = 0.5 + performance * 1.0

# Smooth update (learning_rate = 0.1)
new_weight = old_weight * 0.9 + target_weight * 0.1

# Clamp to range (0.3 to 2.0)
new_weight = max(0.3, min(2.0, new_weight))
```

---

## Consensus Scoring

```python
# For each number predicted by multiple engines:

weighted_score = Σ(predictor_score * predictor_weight)

consensus_bonus = number_of_predictors * 10

final_score = weighted_score + consensus_bonus

# Sort by final_score, return Top 5
```

---

## Performance Optimization

### Caching Strategy
```
CSV File (19,000+ records)
    ↓
Load Once → Cache in Memory
    ↓
Check File Hash → Invalidate if Changed
    ↓
Reuse Cache → Fast Subsequent Loads
```

### Data Window Strategy
```
Full History (2015-2025)
    ↓
Filter to Last 5 Years (Default)
    ↓
Use for ML/AI Training
    ↓
Fast & Relevant
```

### UI Strategy
```
All Predictions Generated
    ↓
Show Only Top 5 on Main Screen
    ↓
Hide Engine Details (Expandable)
    ↓
Clean & Fast Display
```

---

## File Formats

### prediction_logs.jsonl
```json
{"log_id": "20250924_all", "target_date": "2025-09-24", "predictions": {...}}
{"log_id": "20250925_all", "target_date": "2025-09-25", "predictions": {...}}
```

### evaluation_logs.jsonl
```json
{"log_id": "20250924_all", "actual_result": "2999", "predictor_results": {...}}
{"log_id": "20250925_all", "actual_result": "1234", "predictor_results": {...}}
```

### model_weights.json
```json
{
  "recent_stats": 1.05,
  "last_3y": 0.95,
  "last_5y": 1.20,
  "ml": 1.10,
  "ai_pattern": 0.90,
  "full_history": 0.80
}
```

---

## API Architecture

```
GET  /                          → Serve HTML
POST /api/predict               → Run all predictors
POST /api/predict/<name>        → Run specific predictor
POST /api/evaluate              → Evaluate predictions
GET  /api/leaderboard           → Get performance stats
POST /api/drift                 → Analyze drift
GET  /api/weights               → Get current weights
POST /api/history_match         → Check history
GET  /api/stats                 → Get system stats
```

---

## Error Handling

### Insufficient Data
```python
if len(past_data) == 0:
    return fallback_predictions()
```

### Missing Log
```python
if not log_exists:
    return {'error': 'Log not found'}
```

### Invalid Date
```python
if target_date > today:
    # Allow future predictions
    # But use only past data
```

---

## Testing Strategy

1. **Unit Tests**: Test each predictor independently
2. **Integration Tests**: Test full prediction flow
3. **Anti-Leakage Tests**: Verify no future data used
4. **Performance Tests**: Measure speed with large datasets
5. **Evaluation Tests**: Verify scoring accuracy

---

## Scalability

### Current: Single Machine
- Handles 19,000+ records easily
- Fast with 5-year default window
- Suitable for personal use

### Future: Distributed
- Separate prediction workers
- Centralized evaluation service
- Shared weight storage
- API-based architecture

---

**🏗️ Clean, Modular, Production-Ready Architecture**
