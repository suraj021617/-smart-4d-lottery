# 🎯 Smart 4D Lottery Prediction System - REFACTORED

## 🚀 Complete Modular Architecture with Adaptive Auto-Learning

### ✨ Key Features

- **Clean Modular Design**: Separate modules for each component
- **Anti-Data-Leakage**: Strict rules to prevent future data from leaking into predictions
- **Adaptive Auto-Learning**: System learns and improves after each evaluation
- **Top 5 Predictions**: Clean UI showing only top 5 consensus predictions
- **Separate Button Logic**: Each predictor has its own button and logic
- **Prediction Logging**: All predictions saved before results are known
- **Result Evaluation**: Compare predictions against actual results
- **Performance Leaderboard**: Track which predictors perform best
- **Drift Analysis**: Detect recent pattern changes in data
- **Optimized Loading**: Fast loading with intelligent caching

---

## 📁 Project Structure

```
smartsuraj/
├── app.py                          # Main Flask application
├── 4d_results_history.csv          # Historical lottery data (2015-2025)
├── model_weights.json              # Adaptive predictor weights (auto-generated)
├── prediction_logs.jsonl           # Prediction logs (auto-generated)
├── evaluation_logs.jsonl           # Evaluation logs (auto-generated)
├── utils/
│   ├── __init__.py
│   ├── history_loader.py           # Load and cache historical data
│   ├── active_data_filter.py       # Filter data by time windows
│   ├── advanced_predictor.py       # Statistical predictor
│   ├── ml_predictor.py             # Machine learning predictor
│   ├── ai_predictor.py             # AI pattern predictor
│   ├── consensus.py                # Merge predictions with weights
│   ├── prediction_logger.py        # Log predictions before results
│   ├── result_evaluator.py         # Evaluate after results known
│   ├── weight_updater.py           # Update weights (auto-learning)
│   ├── drift_analyzer.py           # Analyze pattern drift
│   └── prediction_runner.py        # Orchestrate all predictors
└── templates/
    └── index.html                  # Clean UI with separate buttons
```

---

## 🔧 Installation

### Prerequisites
- Python 3.8+
- pip

### Install Dependencies

```bash
pip install flask pandas numpy scikit-learn
```

---

## 🚀 Quick Start

### 1. Run the Application

```bash
python app.py
```

### 2. Open Browser

Navigate to: `http://127.0.0.1:5000`

---

## 📊 System Architecture

### Phase 1: History Loading
- Load full CSV (2015-2025)
- Normalize to 4-digit format
- Drop duplicates
- Cache with file change detection

### Phase 2: Active Data Filtering
- Recent 100 draws
- Recent 300 draws
- Last 3 years
- **Last 5 years (DEFAULT ACTIVE DATASET)**
- Full history (reference only)

### Phase 3: Separate Prediction Engines

#### 1. Recent Stats Predictor
- Uses recent 100-300 draws
- Hot digits, pairs, triples
- Transition logic

#### 2. Last 3 Years Predictor
- Uses 3-year window
- Statistical analysis

#### 3. Last 5 Years Predictor (DEFAULT)
- Uses 5-year window
- Main active learning dataset
- Best balance of speed and relevance

#### 4. ML Predictor
- Machine learning features
- Positional analysis
- Sum distribution
- Odd/even patterns

#### 5. AI Pattern Predictor
- 4x4 grid patterns
- Reverse patterns
- Sequential patterns
- Mirror patterns

#### 6. Smart Auto-Learn Predictor
- Combines all predictors
- Uses adaptive weights
- Updates after evaluations

#### 7. Full History Predictor
- Uses all historical data
- For reference/analysis only

### Phase 4: Final Consensus
- Merge all predictions
- Remove duplicates
- Weighted scoring
- Return Top 5

### Phase 5: Prediction Logging
Before result is known, save:
- Target date
- All predictor outputs
- Weights used
- Data used until date
- Timestamp

### Phase 6: Result Evaluation
After result is known:
- Compare actual vs predicted
- Calculate match scores (0-4)
- Track exact hits
- Track positional matches

### Phase 7: Auto-Learning
After evaluation:
- Update predictor weights
- Increase weight for better performers
- Decrease weight for poor performers
- Smooth updates with learning rate

### Phase 8: Drift Analysis
Detect changes in:
- Digit frequency
- Hot/cold digits
- Sum distribution
- Odd/even ratio
- Positional patterns
- Pair frequencies

---

## 🎮 Usage Guide

### Making Predictions

#### Option 1: Single Predictor
1. Select target date
2. Click any predictor button (e.g., "Last 5 Years")
3. View Top 5 predictions

#### Option 2: All Predictors (Consensus)
1. Select target date
2. Click "ALL (Consensus)" button
3. View Top 5 consensus predictions
4. Expand "Engine Details" to see individual predictor outputs

### Evaluating Predictions

1. After actual result is announced:
2. Enter the Log ID (auto-filled if you just ran predictions)
3. Enter the actual 4-digit result
4. Click "Evaluate"
5. System will:
   - Compare predictions vs actual
   - Calculate match scores
   - Update predictor weights automatically
   - Show evaluation report

### Viewing Leaderboard

1. Click "Load Leaderboard"
2. See which predictors perform best
3. View exact hits and average scores

### Checking History

1. Enter any 4-digit number
2. Click "Check History"
3. See if/when that number appeared before
4. **Note**: This is separate from predictions

---

## 🔒 Anti-Data-Leakage Rules

### CRITICAL RULES

1. **Never use target date data for prediction**
   - Only use data where `date < target_date`
   - Strict filtering in `get_data_until_date()`

2. **Learn only after evaluation**
   - Predictions logged BEFORE result known
   - Weights updated AFTER result known
   - No future information leakage

3. **Separate history matching from prediction**
   - History check is informational only
   - Does not influence predictions

4. **Cache invalidation**
   - Cache cleared when CSV changes
   - Ensures fresh data always used

---

## 📈 Performance Optimization

### Speed Improvements

1. **Default to 5-year dataset**
   - Fast loading
   - Relevant patterns
   - Good balance

2. **Intelligent caching**
   - Cache full history
   - Invalidate on file change
   - Reuse filtered datasets

3. **Top 5 only**
   - Minimal UI rendering
   - Fast display
   - Clean interface

4. **Lazy evaluation**
   - Only run requested predictors
   - Don't compute all unless needed

---

## 🎯 API Endpoints

### POST /api/predict
Run all predictors and return consensus

**Request:**
```json
{
  "target_date": "2025-09-25",
  "provider": "All"
}
```

**Response:**
```json
{
  "success": true,
  "final_predictions": [...],
  "log_id": "20250925_all",
  "data_used_until": "2025-09-24"
}
```

### POST /api/predict/<predictor_name>
Run specific predictor

**Predictor names:**
- `recent_stats`
- `last_3y`
- `last_5y`
- `ml`
- `ai_pattern`
- `smart_auto_learn`
- `full_history`

### POST /api/evaluate
Evaluate predictions after result known

**Request:**
```json
{
  "log_id": "20250925_all",
  "actual_result": "1234"
}
```

### GET /api/leaderboard
Get predictor performance leaderboard

### POST /api/drift
Analyze recent drift

### GET /api/weights
Get current predictor weights

### POST /api/history_match
Check if number exists in history

---

## 🧪 Testing Workflow

### 1. Make Prediction
```bash
# Select tomorrow's date
# Click "ALL (Consensus)"
# Note the Log ID
```

### 2. Wait for Actual Result
```bash
# After lottery draw happens
# Get actual winning number
```

### 3. Evaluate
```bash
# Enter Log ID
# Enter actual result
# Click "Evaluate"
# System auto-learns and updates weights
```

### 4. Check Leaderboard
```bash
# Click "Load Leaderboard"
# See which predictors performed best
```

### 5. Repeat
```bash
# System gets smarter with each evaluation
# Weights adapt to recent performance
```

---

## 📊 Data Format

### CSV Format
```csv
date,provider,number,draw_no
2025-09-24,Magnum,2999,262/25
2025-09-24,Magnum,7993,262/25
```

### Prediction Log Format (JSONL)
```json
{
  "log_id": "20250924_all",
  "target_date": "2025-09-24",
  "predictions": {
    "recent_stats": [...],
    "ml": [...],
    ...
  },
  "weights_used": {...}
}
```

### Evaluation Log Format (JSONL)
```json
{
  "log_id": "20250924_all",
  "actual_result": "2999",
  "predictor_results": {
    "recent_stats": {
      "exact_hit": true,
      "best_match_score": 4
    }
  }
}
```

---

## 🔧 Configuration

### Adjust Learning Rate
In `utils/weight_updater.py`:
```python
update_weights_after_result(recent_n=20, learning_rate=0.1)
```

### Change Default Window
In `utils/prediction_runner.py`:
```python
# Change from 5 years to 3 years
ml_data = get_last_3y_data(df, target_date)
```

### Adjust Top N
```python
predictions = predict_ml_mode(df, top_n=10)  # Change from 5 to 10
```

---

## 🐛 Troubleshooting

### Issue: Cache not updating
**Solution:** Delete cache manually or restart app

### Issue: No predictions generated
**Solution:** Check if sufficient historical data exists before target date

### Issue: Evaluation fails
**Solution:** Ensure Log ID exists in `prediction_logs.jsonl`

### Issue: Slow loading
**Solution:** Reduce window size or use recent data only

---

## 📝 Future Enhancements

- [ ] Provider-specific predictions
- [ ] Backtesting mode with walk-forward validation
- [ ] Recent number exclusion filter
- [ ] Confidence intervals
- [ ] Model version tracking
- [ ] Web dashboard for analytics
- [ ] Real-time result fetching
- [ ] Multi-provider consensus

---

## 🎓 Key Concepts

### Anti-Leakage
Never use future data for past predictions. Always filter by date.

### Adaptive Learning
System improves over time by tracking performance and adjusting weights.

### Consensus
Multiple predictors vote, weighted by recent performance.

### Drift Detection
Identify when patterns change, adapt accordingly.

---

## 📄 License

MIT License - Feel free to use and modify

---

## 🙏 Credits

Built with Flask, pandas, numpy, scikit-learn, and Tailwind CSS

---

## 📞 Support

For issues or questions, check the code comments or modify as needed.

---

**🎯 Remember: This is a prediction system for entertainment. Past performance does not guarantee future results. Gamble responsibly.**
