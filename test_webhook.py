import requests
import json

# Test data that simulates a Supabase webhook payload
test_data = {
    "record": {
        "id": "test-user-123",
        "name": "John Doe",
        "phone": "+1234567890",
        "email": "john.doe@example.com",
        "membership_anniversary": "2024-01-15",
        "rollover_date": "2024-12-31",
        "membership_type": "Premium"
    }
}

# Test locally (if running locally)
local_url = "http://localhost:5000/api/supabase-user-update"

# Test on Render (replace with your actual Render URL)
render_url = "https://your-app-name.onrender.com/api/supabase-user-update"

def test_webhook(url, data):
    try:
        response = requests.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Testing webhook locally...")
    test_webhook(local_url, test_data)
    
    print("\n" + "="*50 + "\n")
    
    print("Testing webhook on Render...")
    print("(Make sure to update the render_url variable with your actual URL)")
    # Uncomment the line below and update the URL to test on Render
    # test_webhook(render_url, test_data)
