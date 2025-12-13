"""
🎯 ULTIMATE WHAT TO PLAY ENGINE
All advanced features integrated into one powerful system
"""
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import re
import json
import os

class UltimateWhatToPlay:
    def __init__(self, df):
        self.df = df
        self.all_numbers = self._extract_all_numbers()
        
    def _extract_all_numbers(self):
        numbers = []
        for col in ['1st_real', '2nd_real', '3rd_real']:
            if col in self.df.columns:
                numbers.extend([n for n in self.df[col].astype(str) if len(n) == 4 and n.isdigit()])
        return numbers
    
    def get_ultimate_recommendations(self, budget=100, provider='all', risk_level='medium'):
        """Main function that returns complete recommendations"""
        
        # 1. AI Risk Assessment
        risk_analysis = self._calculate_risk_assessment()
        
        # 2. Multi-Provider Strategy
        provider_strategy = self._analyze_provider_strategy(provider)
        
        # 3. Budget Optimizer
        budget_plan = self._optimize_budget(budget, risk_level)
        
        # 4. Timing Intelligence
        timing_intel = self._analyze_timing_patterns()
        
        # 5. Personal Lucky Algorithm
        personal_patterns = self._get_personal_patterns()
        
        # 6. Confidence Scoring System
        confidence_scores = self._calculate_confidence_scores()
        
        # 7. Advanced Pattern Recognition
        advanced_patterns = self._detect_advanced_patterns()
        
        # 8. Real-time Market Analysis
        market_analysis = self._analyze_market_conditions()
        
        # Combine all recommendations
        final_recommendations = self._synthesize_recommendations(
            risk_analysis, provider_strategy, budget_plan, timing_intel,
            personal_patterns, confidence_scores, advanced_patterns, market_analysis
        )
        
        return final_recommendations
    
    def _calculate_risk_assessment(self):
        """Calculate risk levels for each number"""
        freq_counter = Counter(self.all_numbers)
        total_numbers = len(self.all_numbers)
        
        risk_levels = {}
        for num, count in freq_counter.items():
            frequency_rate = count / total_numbers
            
            if frequency_rate > 0.02:  # Very frequent
                risk = 'Low'
                roi_estimate = 85
            elif frequency_rate > 0.01:  # Moderate
                risk = 'Medium'
                roi_estimate = 120
            else:  # Rare
                risk = 'High'
                roi_estimate = 200
                
            risk_levels[num] = {
                'risk': risk,
                'frequency_rate': round(frequency_rate * 100, 2),
                'roi_estimate': roi_estimate,
                'probability': round(frequency_rate * 100, 1)
            }
        
        return risk_levels
    
    def _analyze_provider_strategy(self, selected_provider):
        """Analyze which provider has better odds"""
        provider_analysis = {}
        providers = self.df['provider'].unique()
        
        for provider in providers:
            if not provider or str(provider).strip() == '':
                continue
                
            provider_df = self.df[self.df['provider'] == provider]
            provider_nums = []
            
            for col in ['1st_real', '2nd_real', '3rd_real']:
                provider_nums.extend([n for n in provider_df[col].astype(str) if len(n) == 4 and n.isdigit()])
            
            if provider_nums:
                freq = Counter(provider_nums)
                diversity = len(set(provider_nums)) / len(provider_nums)
                
                provider_analysis[provider] = {
                    'total_draws': len(provider_df),
                    'unique_numbers': len(set(provider_nums)),
                    'diversity_score': round(diversity, 3),
                    'top_numbers': freq.most_common(5),
                    'recommendation': 'High' if diversity > 0.8 else 'Medium' if diversity > 0.6 else 'Low'
                }
        
        return provider_analysis
    
    def _optimize_budget(self, budget, risk_level):
        """Calculate optimal number combinations within budget"""
        budget_plan = {
            'total_budget': budget,
            'risk_level': risk_level,
            'recommendations': []
        }
        
        # Budget allocation based on risk level
        if risk_level == 'conservative':
            allocation = {'low_risk': 0.7, 'medium_risk': 0.3, 'high_risk': 0.0}
        elif risk_level == 'aggressive':
            allocation = {'low_risk': 0.2, 'medium_risk': 0.3, 'high_risk': 0.5}
        else:  # medium
            allocation = {'low_risk': 0.4, 'medium_risk': 0.4, 'high_risk': 0.2}
        
        risk_analysis = self._calculate_risk_assessment()
        
        for risk_type, percentage in allocation.items():
            if percentage == 0:
                continue
                
            risk_budget = budget * percentage
            risk_map = {'low_risk': 'Low', 'medium_risk': 'Medium', 'high_risk': 'High'}
            target_risk = risk_map[risk_type]
            
            suitable_numbers = [num for num, data in risk_analysis.items() if data['risk'] == target_risk]
            
            if suitable_numbers:
                bet_per_number = min(10, risk_budget / min(5, len(suitable_numbers)))
                selected_numbers = suitable_numbers[:int(risk_budget / bet_per_number)]
                
                budget_plan['recommendations'].append({
                    'risk_category': target_risk,
                    'budget_allocated': risk_budget,
                    'numbers': selected_numbers[:5],
                    'bet_per_number': round(bet_per_number, 2),
                    'expected_roi': sum([risk_analysis[num]['roi_estimate'] for num in selected_numbers[:5]]) / len(selected_numbers[:5]) if selected_numbers else 0
                })
        
        return budget_plan
    
    def _analyze_timing_patterns(self):
        """Analyze best timing patterns"""
        timing_analysis = {
            'best_days': {},
            'seasonal_trends': {},
            'time_recommendations': []
        }
        
        if 'date_parsed' in self.df.columns:
            self.df['day_of_week'] = self.df['date_parsed'].dt.day_name()
            self.df['month'] = self.df['date_parsed'].dt.month
            
            # Day of week analysis
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                day_df = self.df[self.df['day_of_week'] == day]
                if not day_df.empty:
                    day_numbers = []
                    for col in ['1st_real', '2nd_real', '3rd_real']:
                        day_numbers.extend([n for n in day_df[col].astype(str) if len(n) == 4 and n.isdigit()])
                    
                    if day_numbers:
                        freq = Counter(day_numbers)
                        timing_analysis['best_days'][day] = {
                            'total_draws': len(day_df),
                            'hot_numbers': freq.most_common(3),
                            'diversity': len(set(day_numbers)) / len(day_numbers)
                        }
            
            # Seasonal trends
            for month in range(1, 13):
                month_df = self.df[self.df['month'] == month]
                if not month_df.empty:
                    month_numbers = []
                    for col in ['1st_real', '2nd_real', '3rd_real']:
                        month_numbers.extend([n for n in month_df[col].astype(str) if len(n) == 4 and n.isdigit()])
                    
                    if month_numbers:
                        freq = Counter(month_numbers)
                        timing_analysis['seasonal_trends'][month] = freq.most_common(2)
        
        # Generate recommendations
        if timing_analysis['best_days']:
            best_day = max(timing_analysis['best_days'].items(), key=lambda x: x[1]['diversity'])
            timing_analysis['time_recommendations'].append(f"Best day to play: {best_day[0]} (diversity: {best_day[1]['diversity']:.2f})")
        
        return timing_analysis
    
    def _get_personal_patterns(self):
        """Generate personal lucky patterns"""
        personal_patterns = {
            'birth_date_patterns': [],
            'lucky_digit_combinations': [],
            'personal_frequency_analysis': {}
        }
        
        # Analyze digit frequency for personal patterns
        all_digits = ''.join(self.all_numbers)
        digit_freq = Counter(all_digits)
        
        # Generate lucky combinations based on most frequent digits
        top_digits = [d for d, c in digit_freq.most_common(6)]
        
        if len(top_digits) >= 4:
            for i in range(3):
                combo = ''.join(top_digits[i:i+4] if len(top_digits[i:i+4]) == 4 else top_digits[:4])
                personal_patterns['lucky_digit_combinations'].append(combo)
        
        # Personal frequency analysis
        for digit in '0123456789':
            count = digit_freq.get(digit, 0)
            personal_patterns['personal_frequency_analysis'][digit] = {
                'count': count,
                'percentage': round((count / len(all_digits)) * 100, 1) if all_digits else 0,
                'luck_rating': 'High' if count > len(all_digits) * 0.12 else 'Medium' if count > len(all_digits) * 0.08 else 'Low'
            }
        
        return personal_patterns
    
    def _calculate_confidence_scores(self):
        """Calculate confidence scores for each number"""
        confidence_scores = {}
        freq_counter = Counter(self.all_numbers)
        
        # Recent trend analysis
        recent_numbers = self.all_numbers[-100:] if len(self.all_numbers) >= 100 else self.all_numbers
        recent_freq = Counter(recent_numbers)
        
        for num in set(self.all_numbers):
            historical_freq = freq_counter[num]
            recent_freq_count = recent_freq.get(num, 0)
            
            # Calculate confidence based on multiple factors
            historical_score = min(historical_freq * 2, 40)
            recent_trend_score = min(recent_freq_count * 5, 30)
            consistency_score = 20 if historical_freq > 0 and recent_freq_count > 0 else 10
            
            total_confidence = historical_score + recent_trend_score + consistency_score
            
            # Color coding
            if total_confidence >= 70:
                color = 'green'
                level = 'High'
            elif total_confidence >= 50:
                color = 'yellow'
                level = 'Medium'
            else:
                color = 'red'
                level = 'Low'
            
            confidence_scores[num] = {
                'confidence': min(total_confidence, 99),
                'level': level,
                'color': color,
                'reasoning': f"Historical: {historical_score}, Recent: {recent_trend_score}, Consistency: {consistency_score}"
            }
        
        return confidence_scores
    
    def _detect_advanced_patterns(self):
        """Detect advanced mathematical patterns"""
        patterns = {
            'fibonacci_numbers': [],
            'golden_ratio_patterns': [],
            'arithmetic_progressions': [],
            'zodiac_correlations': {}
        }
        
        # Fibonacci detection
        fib_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        for num in self.all_numbers:
            if any(str(fib) in num for fib in fib_sequence):
                patterns['fibonacci_numbers'].append(num)
        
        # Golden ratio patterns (1.618)
        for num in self.all_numbers:
            digits = [int(d) for d in num]
            for i in range(len(digits) - 1):
                if digits[i+1] != 0:
                    ratio = digits[i] / digits[i+1]
                    if abs(ratio - 1.618) < 0.3:
                        patterns['golden_ratio_patterns'].append(num)
        
        # Arithmetic progressions
        for num in self.all_numbers:
            digits = [int(d) for d in num]
            if len(digits) >= 3:
                for i in range(len(digits) - 2):
                    if digits[i+1] - digits[i] == digits[i+2] - digits[i+1]:
                        patterns['arithmetic_progressions'].append(num)
        
        # Zodiac correlations (simplified)
        zodiac_numbers = {
            'rat': [1, 13, 25, 37], 'ox': [2, 14, 26, 38], 'tiger': [3, 15, 27, 39],
            'rabbit': [4, 16, 28, 40], 'dragon': [5, 17, 29, 41], 'snake': [6, 18, 30, 42]
        }
        
        for animal, lucky_nums in zodiac_numbers.items():
            matching_numbers = []
            for num in self.all_numbers:
                if any(str(lucky).zfill(2) in num for lucky in lucky_nums):
                    matching_numbers.append(num)
            if matching_numbers:
                patterns['zodiac_correlations'][animal] = matching_numbers[:3]
        
        return patterns
    
    def _analyze_market_conditions(self):
        """Analyze current market conditions"""
        market_analysis = {
            'overdue_numbers': [],
            'hot_streaks': [],
            'gap_analysis': {},
            'momentum_indicators': {}
        }
        
        freq_counter = Counter(self.all_numbers)
        
        # Overdue analysis
        recent_50 = self.all_numbers[-50:] if len(self.all_numbers) >= 50 else self.all_numbers
        recent_freq = Counter(recent_50)
        
        for num in freq_counter:
            if freq_counter[num] >= 3 and recent_freq.get(num, 0) == 0:
                market_analysis['overdue_numbers'].append({
                    'number': num,
                    'historical_frequency': freq_counter[num],
                    'days_since_last': 'Unknown',
                    'overdue_score': freq_counter[num] * 2
                })
        
        # Hot streaks
        for num, count in recent_freq.most_common(10):
            if count >= 2:
                market_analysis['hot_streaks'].append({
                    'number': num,
                    'recent_appearances': count,
                    'momentum': 'Strong' if count >= 3 else 'Moderate'
                })
        
        # Gap analysis
        all_possible = [f"{i:04d}" for i in range(10000)]
        appeared_numbers = set(self.all_numbers)
        never_appeared = [num for num in all_possible if num not in appeared_numbers]
        
        market_analysis['gap_analysis'] = {
            'never_appeared_count': len(never_appeared),
            'sample_never_appeared': never_appeared[:10],
            'coverage_percentage': round((len(appeared_numbers) / 10000) * 100, 1)
        }
        
        return market_analysis
    
    def _synthesize_recommendations(self, risk_analysis, provider_strategy, budget_plan, 
                                  timing_intel, personal_patterns, confidence_scores, 
                                  advanced_patterns, market_analysis):
        """Combine all analyses into final recommendations"""
        
        # Get top recommendations from each system
        top_confidence = sorted(confidence_scores.items(), key=lambda x: x[1]['confidence'], reverse=True)[:5]
        top_overdue = sorted(market_analysis['overdue_numbers'], key=lambda x: x['overdue_score'], reverse=True)[:3]
        hot_streak_numbers = [item['number'] for item in market_analysis['hot_streaks'][:3]]
        
        final_recommendations = {
            'primary_picks': [],
            'backup_picks': [],
            'strategy_summary': {},
            'risk_breakdown': {},
            'timing_advice': {},
            'budget_allocation': budget_plan,
            'confidence_analysis': {},
            'market_insights': {},
            'advanced_insights': {}
        }
        
        # Primary picks (highest confidence + market conditions)
        primary_candidates = []
        
        # Add high confidence numbers
        for num, data in top_confidence:
            if data['confidence'] >= 60:
                primary_candidates.append({
                    'number': num,
                    'confidence': data['confidence'],
                    'source': 'High Confidence',
                    'risk': risk_analysis.get(num, {}).get('risk', 'Unknown'),
                    'reasoning': data['reasoning']
                })
        
        # Add overdue numbers with high potential
        for overdue in top_overdue:
            if overdue['overdue_score'] >= 6:
                primary_candidates.append({
                    'number': overdue['number'],
                    'confidence': min(overdue['overdue_score'] * 10, 85),
                    'source': 'Overdue Analysis',
                    'risk': 'High',
                    'reasoning': f"Overdue with {overdue['historical_frequency']} historical appearances"
                })
        
        # Add hot streak numbers
        for num in hot_streak_numbers:
            if num not in [p['number'] for p in primary_candidates]:
                primary_candidates.append({
                    'number': num,
                    'confidence': 70,
                    'source': 'Hot Streak',
                    'risk': 'Medium',
                    'reasoning': 'Currently in hot streak'
                })
        
        # Sort and select top 5 primary picks
        primary_candidates.sort(key=lambda x: x['confidence'], reverse=True)
        final_recommendations['primary_picks'] = primary_candidates[:5]
        
        # Backup picks
        backup_candidates = primary_candidates[5:10]
        final_recommendations['backup_picks'] = backup_candidates
        
        # Strategy summary
        final_recommendations['strategy_summary'] = {
            'recommended_approach': 'Balanced Risk',
            'primary_strategy': 'Confidence + Market Analysis',
            'risk_distribution': self._calculate_risk_distribution(primary_candidates[:5]),
            'expected_roi': sum([risk_analysis.get(p['number'], {}).get('roi_estimate', 100) for p in primary_candidates[:5]]) / 5
        }
        
        # Additional insights
        final_recommendations['timing_advice'] = timing_intel.get('time_recommendations', [])
        final_recommendations['market_insights'] = {
            'total_overdue': len(market_analysis['overdue_numbers']),
            'hot_streak_count': len(market_analysis['hot_streaks']),
            'market_coverage': market_analysis['gap_analysis']['coverage_percentage']
        }
        
        final_recommendations['advanced_insights'] = {
            'fibonacci_found': len(advanced_patterns['fibonacci_numbers']),
            'golden_ratio_patterns': len(advanced_patterns['golden_ratio_patterns']),
            'arithmetic_progressions': len(advanced_patterns['arithmetic_progressions'])
        }
        
        return final_recommendations
    
    def _calculate_risk_distribution(self, picks):
        """Calculate risk distribution of picks"""
        if not picks:
            return {'Low': 0, 'Medium': 0, 'High': 0}
        
        risk_count = {'Low': 0, 'Medium': 0, 'High': 0}
        for pick in picks:
            risk = pick.get('risk', 'Unknown')
            if risk in risk_count:
                risk_count[risk] += 1
        
        total = len(picks)
        return {risk: round((count/total)*100, 1) for risk, count in risk_count.items()}

def get_ultimate_what_to_play_recommendations(df, budget=100, provider='all', risk_level='medium'):
    """Main function to get ultimate recommendations"""
    engine = UltimateWhatToPlay(df)
    return engine.get_ultimate_recommendations(budget, provider, risk_level)