import html

# Read CSV
with open('4d_results_history.csv', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix HTML entities
fixed = html.unescape(content)

# Write back
with open('4d_results_history.csv', 'w', encoding='utf-8') as f:
    f.write(fixed)

print("✅ CSV fixed! HTML entities removed.")
