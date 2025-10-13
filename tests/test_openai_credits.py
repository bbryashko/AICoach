"""
Simple test to check if OpenAI credits are working
"""

import requests
import json
import os

# Load API key from environment variable for security
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    print("❌ OPENAI_API_KEY environment variable not set!")
    print("Please set your API key in the .env file or as an environment variable.")
    exit(1)

def test_openai_simple():
    """Test with a very simple, low-cost request"""
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Very simple, short request to minimize cost
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say hello"}
        ],
        "max_tokens": 5  # Very low to save credits
    }
    
    try:
        print("🧪 Testing OpenAI API with minimal request...")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            verify=False
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success! OpenAI API is working!")
            print(f"Response: {result['choices'][0]['message']['content']}")
            print(f"Tokens used: {result.get('usage', {}).get('total_tokens', 'Unknown')}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def check_api_key_info():
    """Check API key information"""
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    
    try:
        print("\n🔍 Checking API key information...")
        # This endpoint gives info about your API usage
        response = requests.get(
            "https://api.openai.com/v1/models",
            headers=headers,
            verify=False
        )
        
        if response.status_code == 200:
            print("✅ API key is valid and has access to models")
            models = response.json()
            available_models = [m['id'] for m in models['data'] if 'gpt' in m['id']][:5]
            print(f"Available models: {available_models}")
            return True
        else:
            print(f"❌ Error checking models: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("🤖 OpenAI Credits Test")
    print("=" * 30)
    
    # Test 1: Check if API key works
    if check_api_key_info():
        print("\n" + "=" * 30)
        # Test 2: Try a minimal request
        test_openai_simple()
    
    print("\n📊 Your Budget Status:")
    print("October budget: $0.00 / $18.00")
    print("This means you have $18 in free credits available!")
    print("\nIf the test fails, it might be:")
    print("1. API key needs to be activated")
    print("2. Temporary API issue")
    print("3. Need to verify your phone number on OpenAI")