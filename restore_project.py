import os
import shutil

# Create directories
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True) 
os.makedirs('utils', exist_ok=True)

print("Project structure created successfully!")
print("Now manually copy your backup files:")
print("1. Copy app_20251013011244.py as app.py")
print("2. Copy 4d_results_history_20251210205421.csv as 4d_results_history.csv") 
print("3. Copy all templates from .history/templates/")
print("4. Copy all utils from .history/utils/")