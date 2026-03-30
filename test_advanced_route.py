from app import app

with app.test_client() as client:
    response = client.get('/advanced-features')
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data[:200]}")
