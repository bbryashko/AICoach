#!/usr/bin/env python3
"""
Test Chat Session Functionality
Simple test to verify the chat classes work correctly
"""

import sys
import os
import json

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Mock classes for testing without real API calls
class MockOpenAIClient:
    """Mock OpenAI client for testing"""
    
    def __init__(self, api_key, model, base_url):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.call_count = 0
    
    def _chat_completion_with_messages(self, messages, max_tokens=1000, temperature=0.7):
        """Mock chat completion"""
        self.call_count += 1
        
        # Simulate different responses based on content
        last_message = messages[-1]['content'].lower()
        
        if 'analysis' in last_message or 'comprehensive' in last_message:
            return f"""**Mock Analysis #{self.call_count}**

Based on your workout data, here's my analysis:

1. **Performance**: Your recent activities show good consistency
2. **Training Balance**: Mix of easy runs and harder sessions
3. **Recommendations**: 
   - Continue current training pattern
   - Focus on recovery between hard sessions
   - Prepare for Dresden half marathon

This is a mock response for testing purposes."""
        
        elif 'nutrition' in last_message:
            return f"**Mock Nutrition Advice #{self.call_count}**: Focus on carb loading 3 days before the race, stay hydrated, and avoid trying new foods on race day."
        
        elif 'pace' in last_message:
            return f"**Mock Pace Advice #{self.call_count}**: Based on your recent runs, aim for a conservative start and negative split strategy."
        
        else:
            return f"**Mock Response #{self.call_count}**: That's a great question! Here's my advice based on your training data... (This is a mock response for testing)"


def test_chat_session():
    """Test the chat session functionality"""
    print("🧪 Testing AI Coach Chat Session")
    print("=" * 40)
    
    # Mock workout data
    mock_activities = [
        {
            "name": "Long Run",
            "type": "Run",
            "distance": 22100,  # 22.1km in meters
            "moving_time": 7200,  # 2 hours
            "start_date_local": "2024-10-12T08:00:00Z"
        },
        {
            "name": "Easy Recovery",
            "type": "Run", 
            "distance": 10000,  # 10km
            "moving_time": 3600,  # 1 hour
            "start_date_local": "2024-10-11T18:00:00Z"
        }
    ]
    
    # Create mock AI client
    mock_ai_client = MockOpenAIClient("test-key", "test-model", "test-url")
    
    # Import chat session after setting up mocks
    from chat_session import AICoachChatSession
    
    print("✅ Creating chat session...")
    chat_session = AICoachChatSession(
        ai_client=mock_ai_client,
        user_id="test_user",
        activities=mock_activities,
        initial_feedback="Feeling good this week"
    )
    
    print("✅ Starting initial analysis...")
    initial_response = chat_session.start_analysis()
    print(f"📝 Initial Analysis:\n{initial_response}\n")
    
    print("✅ Testing follow-up questions...")
    
    # Test follow-up questions
    questions = [
        "What should I focus on for nutrition before the race?",
        "What pace should I target for the half marathon?",
        "How many days should I rest before race day?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"❓ Question {i}: {question}")
        response = chat_session.ask_question(question)
        print(f"🤖 Response {i}: {response}\n")
    
    print("✅ Testing conversation statistics...")
    stats = chat_session.get_conversation_stats()
    print(f"📊 Conversation Stats:")
    for key, value in stats.items():
        print(f"   • {key}: {value}")
    
    print("\n✅ Testing conversation export...")
    export_data = chat_session.export_conversation()
    print(f"📦 Export keys: {list(export_data.keys())}")
    
    print("\n🎉 All tests completed successfully!")
    print(f"   • API calls made: {mock_ai_client.call_count}")
    print(f"   • Messages in conversation: {len(chat_session.messages)}")
    print(f"   • Estimated tokens: {stats['estimated_tokens']}")


def test_session_manager():
    """Test the session manager"""
    print("\n🧪 Testing Chat Session Manager")
    print("=" * 40)
    
    from chat_session import ChatSessionManager
    
    manager = ChatSessionManager()
    mock_ai_client = MockOpenAIClient("test-key", "test-model", "test-url")
    
    mock_activities = [{"name": "Test Run", "distance": 5000}]
    
    print("✅ Creating multiple sessions...")
    session1 = manager.create_session(mock_ai_client, "user1", mock_activities, "Feeling strong")
    session2 = manager.create_session(mock_ai_client, "user2", mock_activities, "Feeling tired")
    
    print(f"✅ Active sessions: {manager.list_active_sessions()}")
    
    # Test session retrieval
    retrieved = manager.get_session("user1")
    print(f"✅ Retrieved session for user1: {retrieved is not None}")
    
    # Test session stats
    stats = manager.get_session_stats("user1")
    print(f"✅ Session stats for user1: {stats is not None}")
    
    # Test ending session
    export = manager.end_session("user1")
    print(f"✅ Ended session for user1, got export: {export is not None}")
    print(f"✅ Remaining sessions: {manager.list_active_sessions()}")
    
    print("\n🎉 Session manager tests completed!")


if __name__ == "__main__":
    try:
        test_chat_session()
        test_session_manager()
        print("\n✅ ALL TESTS PASSED! 🎉")
        print("\nThe chat functionality is ready to use!")
        print("Try: python enhanced_main.py --user <user_id> --chat")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()