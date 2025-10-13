"""
Test the correct OpenAI API syntax
"""

try:
    from openai import OpenAI
    
    # Your API key
    OPENAI_API_KEY = "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"
    
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