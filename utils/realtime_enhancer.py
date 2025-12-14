"""
Real-time Data Enhancement for Better Predictions
"""
import requests
import pandas as pd
from datetime import datetime
import json

class RealtimeEnhancer:
    def __init__(self):
        self.external_data = {}
    
    def get_market_sentiment(self):
        """Get market sentiment data (mock implementation)"""
        # In real implementation, connect to financial APIs
        return {
            'sentiment_score': 0.65,  # 0-1 scale
            'volatility_index': 0.3,
            'trend_direction': 'bullish'
        }
    
    def get_weather_correlation(self):
        """Weather patterns can influence lottery behavior"""
        # Mock weather data - in real implementation use weather API
        return {
            'temperature': 28,
            'humidity': 65,
            'weather_type': 'sunny',
            'correlation_factor': 1.1
        }
    
    def get_social_trends(self):
        """Social media trends affecting number choices"""
        # Mock social data - in real implementation use social APIs
        trending_numbers = ['1234', '8888', '9999']
        return {
            'trending_numbers': trending_numbers,
            'social_influence_score': 0.4
        }
    
    def enhance_predictions(self, base_predictions):
        """Enhance predictions with real-time data"""
        enhanced = []
        
        market = self.get_market_sentiment()
        weather = self.get_weather_correlation()
        social = self.get_social_trends()
        
        for num, score, reason in base_predictions:
            enhanced_score = score
            enhancement_factors = []
            
            # Market sentiment boost
            if market['sentiment_score'] > 0.6:
                enhanced_score *= 1.1
                enhancement_factors.append("Market+")
            
            # Weather correlation
            enhanced_score *= weather['correlation_factor']
            enhancement_factors.append("Weather+")
            
            # Social trend boost
            if num in social['trending_numbers']:
                enhanced_score *= 1.15
                enhancement_factors.append("Social+")
            
            enhanced_reason = reason
            if enhancement_factors:
                enhanced_reason += f" ({'+'.join(enhancement_factors)})"
            
            enhanced.append((num, enhanced_score, enhanced_reason))
        
        return sorted(enhanced, key=lambda x: x[1], reverse=True)
    
    def get_global_lottery_patterns(self):
        """Analyze global lottery patterns for insights"""
        # Mock global data - in real implementation, aggregate from multiple sources
        return {
            'global_hot_digits': [1, 3, 7, 9],
            'global_cold_digits': [0, 2, 4],
            'international_trends': {
                'asia_pacific': ['ascending_sequences'],
                'europe': ['prime_numbers'],
                'americas': ['fibonacci_patterns']
            }
        }
    
    def calculate_prediction_confidence(self, predictions, historical_accuracy):
        """Calculate dynamic confidence based on multiple factors"""
        confidence_factors = {
            'historical_accuracy': historical_accuracy,
            'data_freshness': self.get_data_freshness_score(),
            'pattern_strength': self.calculate_pattern_strength(predictions),
            'market_stability': self.get_market_sentiment()['sentiment_score']
        }
        
        # Weighted confidence calculation
        weights = {
            'historical_accuracy': 0.4,
            'data_freshness': 0.2,
            'pattern_strength': 0.3,
            'market_stability': 0.1
        }
        
        confidence = sum(confidence_factors[factor] * weights[factor] 
                        for factor in confidence_factors)
        
        return min(confidence * 100, 95)  # Cap at 95%
    
    def get_data_freshness_score(self):
        """Calculate how fresh/recent the data is"""
        # Mock implementation - in real system, check last update time
        return 0.85  # 85% fresh
    
    def calculate_pattern_strength(self, predictions):
        """Calculate strength of detected patterns"""
        if not predictions:
            return 0.5
        
        # Analyze score distribution
        scores = [score for _, score, _ in predictions]
        if not scores:
            return 0.5
        
        # Higher variance in scores indicates stronger patterns
        variance = sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)
        strength = min(variance / 0.1, 1.0)  # Normalize to 0-1
        
        return strength