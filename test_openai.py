"""
Simple test to check OpenAI client initialization
"""

from openai_client import OpenAIClient

# Test with your actual API key
OPENAI_API_KEY = "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"

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