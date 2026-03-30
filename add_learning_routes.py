"""
Add these routes to your app.py to enable the learning system
"""

ROUTES_TO_ADD = '''

# ============================================================
# 🤖 AUTO LEARNING SYSTEM ROUTES
# ============================================================

from auto_learning_system import AutoLearningSystem

@app.route('/method-performance')
def method_performance():
    """Show which prediction methods are working best"""
    return render_template('method_performance.html')

@app.route('/api/learning-report')
def api_learning_report():
    """API endpoint for learning report"""
    learner = AutoLearningSystem()
    report = learner.get_learning_report()
    return jsonify(report)

@app.route('/run-learning')
def run_learning():
    """Manually trigger learning from CSV data"""
    learner = AutoLearningSystem()
    updated = learner.check_predictions_against_results()
    report = learner.get_learning_report()
    
    return jsonify({
        'status': 'success',
        'updated_predictions': updated,
        'total_predictions': report['total_predictions'],
        'total_hits': report['total_hits'],
        'overall_accuracy': report['overall_accuracy'],
        'best_method': report['best_method']
    })

@app.route('/smart-predictions')
def smart_predictions_route():
    """Get predictions based on learning data"""
    df = load_csv_data()
    learner = AutoLearningSystem()
    
    provider = request.args.get('provider', 'all')
    if provider != 'all':
        df = df[df['provider_key'] == provider]
    
    # Get smart predictions based on learning
    predictions = learner.get_smart_predictions(df, top_n=10)
    
    # Get learning report
    report = learner.get_learning_report()
    best_method, best_accuracy = report['best_method']
    
    return render_template('smart_predictions.html',
                         predictions=predictions,
                         best_method=best_method,
                         best_accuracy=best_accuracy,
                         learning_report=report,
                         last_updated=time.strftime('%Y-%m-%d %H:%M:%S'))
'''

print("=" * 70)
print("📝 INSTRUCTIONS TO ADD LEARNING SYSTEM TO YOUR APP")
print("=" * 70)
print("\n1. Open app.py in your editor")
print("\n2. Add this import at the top (around line 20):")
print("   from auto_learning_system import AutoLearningSystem")
print("\n3. Copy the routes from 'learning_routes.txt' and paste at the end of app.py")
print("   (before the 'if __name__ == \"__main__\"' line)")
print("\n4. Save the file")
print("\n5. Restart your Flask app")
print("\n" + "=" * 70)

# Save routes to a file for easy copying
with open('learning_routes.txt', 'w') as f:
    f.write(ROUTES_TO_ADD)

print("\n✅ Routes saved to 'learning_routes.txt'")
print("\nOr I can add them automatically for you!")
