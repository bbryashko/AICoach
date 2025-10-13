"""
Simple test to check OpenAI client initialization
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from openai_client import OpenAIClient

# Load API key from environment variable for security
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    print("❌ OPENAI_API_KEY environment variable not set!")
    print("Please set your API key in the .env file or as an environment variable.")
    exit(1)

try:
    print("Testing OpenAI client initialization...")
    ai_client = OpenAIClient(OPENAI_API_KEY)
    print("✅ OpenAI client created successfully!")
    
    # Test with simple data
    test_data = {
        "name": "Test Run",
        "type": "Run",
        "distance": 5000,
        "moving_time": 1800
    }
    
    print("Testing workout analysis...")
    result = ai_client.analyze_workout_data(test_data)
    print(f"✅ Analysis result: {result[:100]}...")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()