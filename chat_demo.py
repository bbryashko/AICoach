#!/usr/bin/env python3
"""
AI Coach Chat Demo
Demonstrates the conversational interface for workout analysis
"""

import sys
import os
import argparse

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import get_config
from simple_openai_client import SimpleOpenAIClient
from strava_auth import get_strava_token
from chat_session import AICoachChatSession, ChatSessionManager
import requests
import json


def get_strava_activities(config, limit=None, user_id=None):
    """Get recent activities from Strava (reused from main.py)"""
    if limit is None:
        limit = config.MAX_ACTIVITIES
    
    if not user_id:
        print("❌ User ID required for Strava OAuth authentication")
        return []
    
    if not config.has_oauth_config():
        print("❌ Strava OAuth not configured")
        return []
    
    try:
        strava_token = get_strava_token(config, user_id)
        print(f"🔐 Using OAuth authentication for user: {user_id}")
    except Exception as e:
        print(f"❌ OAuth authentication failed: {e}")
        return []
    
    headers = {"Authorization": f"Bearer {strava_token}"}
    params = {"per_page": limit}
    proxies = config.get_proxies()
    
    try:
        response = requests.get(
            f"{config.STRAVA_BASE_URL}/athlete/activities",
            headers=headers, 
            params=params, 
            proxies=proxies,
            verify=config.VERIFY_SSL
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error fetching Strava data: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def interactive_chat_demo():
    """Demonstrate the interactive chat functionality"""
    parser = argparse.ArgumentParser(description="AI Coach Chat Demo")
    parser.add_argument('--user', type=str, required=True, help='User ID for OAuth authentication')
    parser.add_argument('--limit', type=int, default=5, help='Number of activities to fetch')
    parser.add_argument('--feedback', type=str, default="", help='Initial runner feedback')
    
    args = parser.parse_args()
    
    print("🤖 AI COACH - INTERACTIVE CHAT DEMO")
    print("=" * 50)
    
    # Load configuration
    config = get_config()
    
    # Validate configuration
    is_valid, missing_keys = config.validate_keys()
    if not is_valid:
        print(f"❌ Missing configuration: {', '.join(missing_keys)}")
        return
    
    print(f"📱 Fetching {args.limit} recent activities...")
    activities = get_strava_activities(config, args.limit, args.user)
    
    if not activities:
        print("❌ No activities found.")
        return
    
    print(f"✅ Found {len(activities)} activities:")
    for i, activity in enumerate(activities, 1):
        distance_km = activity.get('distance', 0) / 1000
        name = activity.get('name', 'Unnamed')
        activity_type = activity.get('type', 'Unknown')
        date = activity.get('start_date_local', '')[:10]
        print(f"   {i}. {name} ({activity_type}) - {distance_km:.1f}km on {date}")
    
    # Get initial feedback if not provided
    initial_feedback = args.feedback
    if not initial_feedback:
        print("\\n💬 Add initial runner feedback (optional, press Enter to skip):")
        print("Examples: 'Felt strong this week', 'Legs were tired', 'Ready for race'")
        try:
            initial_feedback = input("Your feedback: ").strip()
        except (EOFError, KeyboardInterrupt):
            initial_feedback = ""
    
    # Create AI client and chat session
    ai_client = SimpleOpenAIClient(
        config.OPENAI_API_KEY, 
        config.OPENAI_MODEL, 
        config.OPENAI_BASE_URL
    )
    
    print("\\n🚀 Starting interactive chat session...")
    print("💡 Type 'quit', 'exit', or 'q' to end the session")
    print("💡 Type 'stats' to see conversation statistics")
    print("=" * 50)
    
    # Create chat session
    chat_session = AICoachChatSession(ai_client, args.user, activities, initial_feedback)
    
    # Get initial analysis
    print("\\n🤖 AI Coach: Let me analyze your recent workouts...")
    initial_analysis = chat_session.start_analysis()
    print(f"\\n{initial_analysis}")
    
    # Interactive chat loop
    print("\\n" + "=" * 50)
    print("💬 Now you can ask follow-up questions!")
    
    while True:
        try:
            print("\\n" + "-" * 30)
            user_input = input("\\n🏃 Your question: ").strip()
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            elif user_input.lower() == 'stats':
                stats = chat_session.get_conversation_stats()
                print(f"\\n📊 Chat Statistics:")
                print(f"   • Total messages: {stats['total_messages']}")
                print(f"   • Your questions: {stats['user_messages']}")
                print(f"   • AI responses: {stats['assistant_messages']}")
                print(f"   • Estimated tokens: {stats['estimated_tokens']}")
                print(f"   • Session duration: {stats['session_duration_minutes']:.1f} minutes")
                continue
            elif not user_input:
                print("❓ Please ask a question or type 'quit' to exit.")
                continue
            
            # Get AI response
            print("\\n🤖 AI Coach:")
            response = chat_session.ask_question(user_input)
            print(f"{response}")
            
        except (EOFError, KeyboardInterrupt):
            print("\\n\\n👋 Chat session interrupted.")
            break
        except Exception as e:
            print(f"\\n❌ Error: {e}")
            continue
    
    # End session
    print("\\n" + "=" * 50)
    print("👋 Ending chat session...")
    
    # Show final statistics
    final_stats = chat_session.get_conversation_stats()
    print(f"\\n📊 Final Session Statistics:")
    print(f"   • Total conversation: {final_stats['total_messages']} messages")
    print(f"   • Your questions: {final_stats['user_messages']}")
    print(f"   • Duration: {final_stats['session_duration_minutes']:.1f} minutes")
    print(f"   • Estimated tokens used: {final_stats['estimated_tokens']}")
    
    print("\\n✅ Chat session completed!")
    print("💡 To start a new session: python chat_demo.py --user <user_id>")


if __name__ == "__main__":
    try:
        interactive_chat_demo()
    except KeyboardInterrupt:
        print("\\n\\n👋 Goodbye!")
    except Exception as e:
        print(f"\\n❌ Unexpected error: {e}")
        print("💡 Try running: python main.py --config-check")