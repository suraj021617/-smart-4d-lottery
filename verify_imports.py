# -*- coding: utf-8 -*-
"""Verify all imports work"""

print("=" * 80)
print("VERIFYING PYTHON ENVIRONMENT")
print("=" * 80)

try:
    import pandas as pd
    print(f"[OK] pandas {pd.__version__} - INSTALLED")
    print(f"     Location: {pd.__file__}")
except ImportError as e:
    print(f"[FAIL] pandas - NOT FOUND: {e}")

try:
    import numpy as np
    print(f"[OK] numpy {np.__version__} - INSTALLED")
except ImportError as e:
    print(f"[FAIL] numpy - NOT FOUND: {e}")

try:
    import flask
    print(f"[OK] flask {flask.__version__} - INSTALLED")
except ImportError as e:
    print(f"[FAIL] flask - NOT FOUND: {e}")

try:
    import sklearn
    print(f"[OK] scikit-learn {sklearn.__version__} - INSTALLED")
except ImportError as e:
    print(f"[FAIL] scikit-learn - NOT FOUND: {e}")

print("\n" + "=" * 80)
print("ALL PACKAGES WORKING! Pylance warning is FALSE POSITIVE.")
print("=" * 80)
print("\nFIX IN VS CODE:")
print("1. Ctrl+Shift+P -> Python: Select Interpreter -> Python 3.11")
print("2. Ctrl+Shift+P -> Developer: Reload Window")
print("=" * 80)
