"""
Quick Route Verification Script
Tests if all main routes are defined in app.py
"""

from app import app

# List of all routes that should exist
required_routes = [
    '/',
    '/past-results',
    '/consensus-predictor',
    '/advanced-features',
    '/decision-helper',
    '/quick-pick',
    '/pattern-analyzer',
    '/statistics',
    '/frequency-analyzer',
    '/hot-cold',
    '/day-to-day-predictor',
    '/accuracy-dashboard',
    '/best-predictions',
    '/ultimate-predictor',
    '/smart-predictor',
    '/ml-predictor',
    '/learning-insights',
    '/empty-box-predictor',
    '/master-analyzer',
    '/advanced-analytics',
    '/prediction-history',
    '/lucky-generator',
]

print("=" * 60)
print("ROUTE VERIFICATION TEST")
print("=" * 60)

# Get all registered routes
registered_routes = []
for rule in app.url_map.iter_rules():
    if rule.endpoint != 'static':
        registered_routes.append(rule.rule)

# Check each required route
missing_routes = []
found_routes = []

for route in required_routes:
    if route in registered_routes:
        found_routes.append(route)
        print(f"[OK] {route}")
    else:
        missing_routes.append(route)
        print(f"[MISSING] {route}")

print("=" * 60)
print(f"SUMMARY:")
print(f"  Found: {len(found_routes)}/{len(required_routes)}")
print(f"  Missing: {len(missing_routes)}")
print("=" * 60)

if missing_routes:
    print("\nMISSING ROUTES:")
    for route in missing_routes:
        print(f"  - {route}")
    print("\nStatus: FAILED - Some routes are missing")
else:
    print("\nStatus: SUCCESS - All routes are registered!")

print("=" * 60)
