import requests
import os

# Load API key from environment variable for security
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("❌ OPENAI_API_KEY environment variable not set!")
    print("Please set your API key in the .env file or as an environment variable.")
    exit(1)

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Test 1: Check if we can access models
print("Testing API key access...")
try:
    response = requests.get("https://api.openai.com/v1/models", headers=headers, verify=False)
    print(f"Models endpoint status: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")

# Test 2: Minimal chat request
print("\nTesting minimal chat request...")
payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hi"}],
    "max_tokens": 1
}

try:
    response = requests.post("https://api.openai.com/v1/chat/completions", 
                           headers=headers, json=payload, verify=False)
    print(f"Chat endpoint status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Success! Credits are working")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")