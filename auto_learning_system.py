"""
🎯 AUTO LEARNING SYSTEM - Learns from actual results and improves predictions
This system:
1. Tracks which prediction methods work best
2. Learns from actual winning numbers
3. Updates predictions based on new CSV data
4. Shows accuracy for each button/method
"""

import pandas as pd
import json
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict

class AutoLearningSystem:
    def __init__(self):
        self.learning_file = "learning_data.json"
        self.tracking_file = "method_tracking.json"
        self.load_learning_data()
    
    def load_learning_data(self):
        """Load existing learning data"""
        if os.path.exists(self.learning_file):
            with open(self.learning_file, 'r') as f:
                self.learning_data = json.load(f)
        else:
            self.learning_data = {
                'method_accuracy': {},
                'number_patterns': {},
                'last_update': None,
                'total_predictions': 0,
                'total_hits': 0
            }
        
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, 'r') as f:
                self.tracking_data = json.load(f)
        else:
            self.tracking_data = {
                'advanced_predictor': {'predictions': 0, 'hits': 0, 'accuracy': 0},
                'smart_predictor': {'predictions': 0, 'hits': 0, 'accuracy': 0},
                'ml_predictor': {'predictions': 0, 'hits': 0, 'accuracy': 0},
                'pattern_predictor': {'predictions': 0, 'hits': 0, 'accuracy': 0},
                'ultimate_predictor': {'predictions': 0, 'hits': 0, 'accuracy': 0}
            }
    
    def save_learning_data(self):
        """Save learning data"""
        with open(self.learning_file, 'w') as f:
            json.dump(self.learning_data, f, indent=2)
        
        with open(self.tracking_file, 'w') as f:
            json.dump(self.tracking_data, f, indent=2)
    
    def check_predictions_against_results(self, csv_file='4d_results_history.csv'):
        """
        Check all predictions against actual results from CSV
        This is the MAIN function that learns from results
        """
        print("🔍 Checking predictions against actual results...")
        
        # Load CSV data
        df = pd.read_csv(csv_file)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.sort_values('date', ascending=False)
        
        # Load prediction tracking file
        pred_file = "prediction_tracking.csv"
        if not os.path.exists(pred_file):
            print("❌ No predictions to check yet")
            return
        
        pred_df = pd.read_csv(pred_file)
        pred_df['draw_date'] = pd.to_datetime(pred_df['draw_date'], errors='coerce')
        
        updated_count = 0
        
        # Check each pending prediction
        for idx, pred_row in pred_df[pred_df['hit_status'] == 'pending'].iterrows():
            draw_date = pred_row['draw_date'].date()
            provider = str(pred_row['provider']).strip().lower()
            
            # Find actual results for this date and provider
            actual = df[(df['date'].dt.date == draw_date)]
            if not actual.empty:
                actual_row = actual.iloc[0]
                
                # Extract actual winning numbers
                actual_1st = str(actual_row.get('1st', '')).strip()
                actual_2nd = str(actual_row.get('2nd', '')).strip()
                actual_3rd = str(actual_row.get('3rd', '')).strip()
                
                # Extract predicted numbers
                import re
                predicted_nums = re.findall(r'\d{4}', str(pred_row['predicted_numbers']))
                
                # Check for matches
                actual_nums = [actual_1st, actual_2nd, actual_3rd]
                hits = [p for p in predicted_nums if p in actual_nums]
                
                # Update prediction record
                pred_df.at[idx, 'actual_1st'] = actual_1st
                pred_df.at[idx, 'actual_2nd'] = actual_2nd
                pred_df.at[idx, 'actual_3rd'] = actual_3rd
                
                if hits:
                    pred_df.at[idx, 'hit_status'] = f'✅ HIT ({len(hits)} matches: {", ".join(hits)})'
                    pred_df.at[idx, 'accuracy_score'] = (len(hits) / len(predicted_nums)) * 100
                    
                    # Learn from this success
                    self.learn_from_hit(predicted_nums, hits, pred_row.get('predictor_methods', ''))
                else:
                    pred_df.at[idx, 'hit_status'] = '❌ MISS'
                    pred_df.at[idx, 'accuracy_score'] = 0
                
                updated_count += 1
        
        # Save updated predictions
        pred_df.to_csv(pred_file, index=False)
        print(f"✅ Updated {updated_count} predictions")
        
        # Update method tracking
        self.update_method_tracking(pred_df)
        self.save_learning_data()
        
        return updated_count
    
    def learn_from_hit(self, predicted_nums, hits, methods):
        """Learn from successful predictions"""
        for hit_num in hits:
            if hit_num not in self.learning_data['number_patterns']:
                self.learning_data['number_patterns'][hit_num] = {
                    'success_count': 0,
                    'methods_used': []
                }
            
            self.learning_data['number_patterns'][hit_num]['success_count'] += 1
            self.learning_data['number_patterns'][hit_num]['methods_used'].append(methods)
        
        self.learning_data['total_hits'] += len(hits)
        self.learning_data['total_predictions'] += len(predicted_nums)
        self.learning_data['last_update'] = datetime.now().isoformat()
    
    def update_method_tracking(self, pred_df):
        """Update accuracy tracking for each method"""
        completed = pred_df[pred_df['hit_status'] != 'pending']
        
        for method_name in self.tracking_data.keys():
            method_preds = completed[completed['predictor_methods'].str.contains(method_name, na=False, case=False)]
            
            if len(method_preds) > 0:
                hits = len(method_preds[method_preds['hit_status'].str.contains('HIT', na=False)])
                total = len(method_preds)
                accuracy = (hits / total) * 100 if total > 0 else 0
                
                self.tracking_data[method_name] = {
                    'predictions': total,
                    'hits': hits,
                    'accuracy': round(accuracy, 2)
                }
    
    def get_best_method(self):
        """Get the best performing prediction method"""
        best_method = None
        best_accuracy = 0
        
        for method, stats in self.tracking_data.items():
            if stats['predictions'] >= 5 and stats['accuracy'] > best_accuracy:
                best_accuracy = stats['accuracy']
                best_method = method
        
        return best_method, best_accuracy
    
    def get_learning_report(self):
        """Generate a learning report"""
        report = {
            'total_predictions': self.learning_data['total_predictions'],
            'total_hits': self.learning_data['total_hits'],
            'overall_accuracy': (self.learning_data['total_hits'] / self.learning_data['total_predictions'] * 100) if self.learning_data['total_predictions'] > 0 else 0,
            'last_update': self.learning_data['last_update'],
            'method_performance': self.tracking_data,
            'best_method': self.get_best_method()
        }
        return report
    
    def get_smart_predictions(self, df, top_n=5):
        """
        Generate SMART predictions based on learning data
        This uses what the system has learned to make better predictions
        """
        # Get numbers that have been successful before
        successful_patterns = self.learning_data.get('number_patterns', {})
        
        # Get recent numbers from CSV
        recent_nums = []
        for col in ['1st', '2nd', '3rd']:
            if col in df.columns:
                recent_nums.extend([str(n) for n in df[col].tail(100) if str(n).isdigit() and len(str(n)) == 4])
        
        # Score numbers based on:
        # 1. Recent frequency
        # 2. Past success rate
        # 3. Pattern learning
        
        number_scores = {}
        freq_counter = Counter(recent_nums)
        
        for num, freq in freq_counter.most_common(50):
            score = freq  # Base score from frequency
            
            # Boost score if this number was successful before
            if num in successful_patterns:
                success_boost = successful_patterns[num]['success_count'] * 10
                score += success_boost
            
            number_scores[num] = score
        
        # Sort by score and return top N
        sorted_nums = sorted(number_scores.items(), key=lambda x: x[1], reverse=True)
        
        predictions = []
        for num, score in sorted_nums[:top_n]:
            confidence = min(int((score / sorted_nums[0][1]) * 100), 99) if sorted_nums else 50
            reason = f"Learned pattern (success: {successful_patterns.get(num, {}).get('success_count', 0)})"
            predictions.append((num, confidence, reason))
        
        return predictions

def main():
    """Main function to run auto learning"""
    print("=" * 60)
    print("🤖 AUTO LEARNING SYSTEM - Starting...")
    print("=" * 60)
    
    learner = AutoLearningSystem()
    
    # Check predictions against results
    updated = learner.check_predictions_against_results()
    
    # Generate report
    report = learner.get_learning_report()
    
    print("\n📊 LEARNING REPORT:")
    print(f"Total Predictions: {report['total_predictions']}")
    print(f"Total Hits: {report['total_hits']}")
    print(f"Overall Accuracy: {report['overall_accuracy']:.2f}%")
    print(f"Last Update: {report['last_update']}")
    
    print("\n🎯 METHOD PERFORMANCE:")
    for method, stats in report['method_performance'].items():
        if stats['predictions'] > 0:
            print(f"  {method}: {stats['accuracy']:.2f}% ({stats['hits']}/{stats['predictions']})")
    
    best_method, best_accuracy = report['best_method']
    if best_method:
        print(f"\n🏆 BEST METHOD: {best_method} ({best_accuracy:.2f}%)")
    
    print("\n✅ Learning complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
