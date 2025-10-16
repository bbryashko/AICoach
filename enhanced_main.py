#!/usr/bin/env python3
"""
Enhanced AI Coach - Main Entry Point with Chat Support
Extends the original functionality with conversational interface
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
    """Get recent activities from Strava using OAuth"""
    if limit is None:
        limit = config.MAX_ACTIVITIES
    
    if not user_id:
        print("❌ User ID required for Strava OAuth authentication")
        print("💡 Use --user <user_id> parameter or setup new user with --oauth-setup <user_id>")
        return []
    
    if not config.has_oauth_config():
        print("❌ Strava OAuth not configured")
        print("💡 Please set STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET in .env")
        return []
    
    try:
        strava_token = get_strava_token(config, user_id)
        print(f"🔐 Using OAuth authentication for user: {user_id}")
    except Exception as e:
        print(f"❌ OAuth authentication failed: {e}")
        print(f"💡 Try setting up OAuth: python main.py --oauth-setup {user_id}")
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


def analyze_workout(config, activities, feedback=""):
    """Analyze workout with AI (legacy single-shot analysis)"""
    if not config.OPENAI_API_KEY:
        print("❌ OpenAI API key not configured. Please set OPENAI_API_KEY in .env file.")
        return "No AI analysis available."
    
    try:
        ai_client = SimpleOpenAIClient(
            config.OPENAI_API_KEY, 
            config.OPENAI_MODEL, 
            config.OPENAI_BASE_URL
        )
        
        # Analyze all activities with optional feedback
        return ai_client.analyze_workout_with_feedback(activities, feedback)
            
    except Exception as e:
        return f"❌ Error with AI analysis: {e}"


def interactive_chat_mode(config, activities, user_id, initial_feedback=""):
    """Start interactive chat mode"""
    ai_client = SimpleOpenAIClient(
        config.OPENAI_API_KEY, 
        config.OPENAI_MODEL, 
        config.OPENAI_BASE_URL
    )
    
    print("\n🚀 INTERACTIVE CHAT MODE")
    print("=" * 50)
    print("💡 Ask follow-up questions about your training")
    print("💡 Type 'quit', 'exit', or 'q' to end")
    print("💡 Type 'stats' for conversation statistics")
    
    # Create chat session
    chat_session = AICoachChatSession(ai_client, user_id, activities, initial_feedback)
    
    # Get initial analysis
    print("\n🤖 Starting comprehensive analysis...")
    initial_analysis = chat_session.start_analysis()
    print(f"\n{initial_analysis}")
    
    # Interactive loop
    while True:
        try:
            print("\n" + "-" * 30)
            question = input("\n🏃 Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
            elif question.lower() == 'stats':
                stats = chat_session.get_conversation_stats()
                print(f"\n📊 Statistics: {stats['total_messages']} messages, "
                      f"{stats['estimated_tokens']} tokens, "
                      f"{stats['session_duration_minutes']:.1f} min")
                continue
            elif not question:
                continue
            
            print("\n🤖 AI Coach:")
            response = chat_session.ask_question(question)
            print(response)
            
        except (EOFError, KeyboardInterrupt):
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Final stats
    final_stats = chat_session.get_conversation_stats()
    print(f"\n📊 Session completed: {final_stats['total_messages']} messages, "
          f"{final_stats['session_duration_minutes']:.1f} minutes")


def main():
    """Enhanced main application entry point"""
    parser = argparse.ArgumentParser(description="Enhanced AI Coach - Strava + OpenAI Integration with Chat")
    parser.add_argument('--config-check', action='store_true', help='Check configuration only')
    parser.add_argument('--feedback', type=str, help='Add runner feedback for analysis')
    parser.add_argument('--limit', type=int, default=None, help='Number of activities to fetch')
    parser.add_argument('--user', type=str, help='User ID for OAuth authentication (required)')
    parser.add_argument('--oauth-setup', type=str, help='Setup OAuth for new user')
    parser.add_argument('--list-users', action='store_true', help='List authenticated users')
    parser.add_argument('--chat', action='store_true', help='Start interactive chat mode after analysis')
    parser.add_argument('--chat-only', action='store_true', help='Start only in chat mode (no initial analysis)')
    
    args = parser.parse_args()
    
    print("🤖 ENHANCED AI COACH - Strava + OpenAI + Chat")
    print("=" * 60)
    
    # Load configuration
    config = get_config()
    config.print_status()
    
    if args.config_check:
        print("\\n✅ Configuration check complete!")
        return
    
    # Handle OAuth-specific commands (same as original)
    if args.list_users:
        from strava_auth import StravaAuthManager
        auth_manager = StravaAuthManager(config)
        users = auth_manager.list_authenticated_users()
        
        print("\\n👥 Authenticated Users:")
        print("=" * 40)
        if users:
            for user in users:
                status = "✅ Valid" if user.get('is_valid') else "❌ Expired"
                print(f"• {user.get('user_id', 'Unknown')} - {user.get('athlete_name', 'Unknown')} ({status})")
        else:
            print("No authenticated users found.")
            print("💡 Use --oauth-setup <user_id> to authenticate a new user")
        return
    
    if args.oauth_setup:
        from strava_auth import setup_new_user
        print(f"\\n🔐 Setting up OAuth for new user: {args.oauth_setup}")
        try:
            setup_new_user(config, args.oauth_setup)
            print(f"✅ OAuth setup completed for {args.oauth_setup}")
        except Exception as e:
            print(f"❌ OAuth setup failed: {e}")
        return
    
    # Validate configuration
    is_valid, missing_keys = config.validate_keys()
    if not is_valid:
        print(f"\\n❌ Missing configuration: {', '.join(missing_keys)}")
        print("\\n📋 Setup Instructions:")
        print("1. Copy .env.template to .env")
        print("2. Edit .env with your actual API keys")
        print("3. Run: python main.py --config-check")
        return
    
    # Require user_id for analysis
    if not args.user:
        print("\n❌ User ID is required for analysis")
        print("\n💡 Usage:")
        print("  • First time: python enhanced_main.py --oauth-setup <user_id>")
        print("  • Analysis:   python enhanced_main.py --user <user_id>")
        print("  • Chat mode:  python enhanced_main.py --user <user_id> --chat")
        print("  • Chat only:  python enhanced_main.py --user <user_id> --chat-only")
        return
    
    # Get activities limit
    if args.limit is None:
        if args.chat_only:
            args.limit = config.MAX_ACTIVITIES
        else:
            try:
                user_input = input(f"\n📱 How many recent activities to analyze? (default: {config.MAX_ACTIVITIES}): ").strip()
                args.limit = int(user_input) if user_input else config.MAX_ACTIVITIES
            except (ValueError, KeyboardInterrupt):
                args.limit = config.MAX_ACTIVITIES
    
    print(f"\n📱 Fetching your recent {args.limit} activities...")
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
    
    # Get feedback
    feedback = args.feedback or ""
    if not feedback and not args.chat_only:
        print("\n💬 Add runner feedback (optional, press Enter to skip):")
        print("Examples: 'Felt strong', 'Legs were tired', 'Ready for race'")
        try:
            feedback = input("Your feedback: ").strip()
        except (EOFError, KeyboardInterrupt):
            feedback = ""
    
    # Handle different modes
    if args.chat_only:
        # Go directly to chat mode
        interactive_chat_mode(config, activities, args.user, feedback)
    elif args.chat:
        # Do initial analysis then switch to chat
        print(f"\\n🧠 AI ANALYSIS OF ALL {len(activities)} ACTIVITIES")
        print("=" * 60)
        
        if feedback:
            print(f"📝 Including your feedback: \"{feedback}\"")
        
        analysis = analyze_workout(config, activities, feedback)
        print(f"\n{analysis}")
        
        print("\n" + "=" * 60)
        print("🔄 Switching to interactive chat mode...")
        interactive_chat_mode(config, activities, args.user, feedback)
    else:
        # Traditional single-shot analysis (original behavior)
        print(f"\n🧠 AI ANALYSIS OF ALL {len(activities)} ACTIVITIES")
        print("=" * 60)
        
        if feedback:
            print(f"📝 Including your feedback: \"{feedback}\"")
        
        analysis = analyze_workout(config, activities, feedback)
        print(f"\n{analysis}")
        
        print("\n💡 Tip: Add --chat flag for interactive follow-up questions!")
    
    print("\n🎯 Next Steps:")
    print("• Interactive chat: python enhanced_main.py --user <user_id> --chat")
    print("• Chat only mode: python enhanced_main.py --user <user_id> --chat-only")
    print("• Regular analysis: python enhanced_main.py --user <user_id>")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Try running: python enhanced_main.py --config-check")