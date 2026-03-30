# Remove broken venv
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

# Create new venv
python -m venv .venv

# Install packages
.\.venv\Scripts\pip.exe install flask pandas numpy scikit-learn

Write-Host ""
Write-Host "✅ FIXED! Now run: .\.venv\Scripts\python.exe app.py" -ForegroundColor Green
