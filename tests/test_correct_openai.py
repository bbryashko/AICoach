"""
Test the correct OpenAI API syntax
"""

try:
    from openai import OpenAI
    import os
    
    # Load API key from environment variable for security
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Please set your API key in the .env file or as an environment variable.")
        exit(1)
    
    print("Testing correct OpenAI API syntax...")
    
    # Correct syntax for OpenAI v1.x
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # The correct method is chat.completions.create (not responses.create)
    # Also, gpt-5 doesn't exist yet - use gpt-3.5-turbo or gpt-4
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
        ],
        max_tokens=100
    )
    
    # The response structure is different
    print("✅ Success!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()