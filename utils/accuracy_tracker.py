"""Auto Prediction Accuracy Tracker - No Manual Input"""
import pandas as pd
from datetime import datetime, timedelta
import json
import os

class AccuracyTracker:
    def __init__(self, predictions_file='data/predictions_log.json'):
        self.predictions_file = predictions_file
        os.makedirs(os.path.dirname(predictions_file), exist_ok=True)
    
    def save_prediction(self, provider, draw_date, method, numbers, confidence):
        """Auto-save prediction"""
        pred = {
            'provider': provider,
            'draw_date': draw_date,
            'method': method,
            'numbers': numbers,
            'confidence': confidence,
            'predicted_at': datetime.now().isoformat(),
            'checked': False
        }
        
        preds = self._load_predictions()
        preds.append(pred)
        
        with open(self.predictions_file, 'w') as f:
            json.dump(preds, f, indent=2)
    
    def check_accuracy(self, df):
        """Auto-check predictions against actual results"""
        preds = self._load_predictions()
        unchecked = [p for p in preds if not p.get('checked')]
        
        for pred in unchecked:
            draw_date = pd.to_datetime(pred['draw_date']).date()
            provider = pred['provider']
            
            # Find actual result
            actual = df[(df['date_parsed'].dt.date == draw_date) & 
                       (df['provider_key'] == provider)]
            
            if not actual.empty:
                winning_nums = []
                for col in ['number_1st', 'number_2nd', 'number_3rd']:
                    num = str(actual.iloc[0][col])
                    if num.isdigit() and len(num) == 4:
                        winning_nums.append(num)
                
                # Check hits
                hits = [n for n in pred['numbers'] if n in winning_nums]
                pred['hits'] = hits
                pred['hit_count'] = len(hits)
                pred['winning_numbers'] = winning_nums
                pred['checked'] = True
        
        with open(self.predictions_file, 'w') as f:
            json.dump(preds, f, indent=2)
        
        return preds
    
    def get_accuracy_stats(self, method=None, provider=None):
        """Get accuracy statistics"""
        preds = self._load_predictions()
        checked = [p for p in preds if p.get('checked')]
        
        if method:
            checked = [p for p in checked if p['method'] == method]
        if provider:
            checked = [p for p in checked if p['provider'] == provider]
        
        if not checked:
            return {'total': 0, 'hits': 0, 'accuracy': 0}
        
        total_predictions = len(checked) * 5  # 5 numbers per prediction
        total_hits = sum(p.get('hit_count', 0) for p in checked)
        
        return {
            'total_predictions': len(checked),
            'total_numbers': total_predictions,
            'total_hits': total_hits,
            'accuracy': round(total_hits / total_predictions * 100, 2) if total_predictions > 0 else 0,
            'predictions': checked
        }
    
    def _load_predictions(self):
        if os.path.exists(self.predictions_file):
            with open(self.predictions_file, 'r') as f:
                return json.load(f)
        return []
