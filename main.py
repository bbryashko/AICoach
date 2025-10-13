#!/usr/bin/env python3
"""
AI Coach - Main Entry Point
Run this script to start the AI Coach application
"""

import sys
import os
import argparse

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import get_config
from simple_openai_client import SimpleOpenAIClient
from strava_auth import get_strava_token
import requests
import json


def get_strava_activities(config, limit=None, user_id=None):
    """Get recent activities from Strava using OAuth or legacy token"""
    # Use config default if no limit specified
    if limit is None:
        limit = config.MAX_ACTIVITIES
    
    # Require OAuth authentication with user_id
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
    """Analyze workout with AI"""
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


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="AI Coach - Strava + OpenAI Integration")
    parser.add_argument('--config-check', action='store_true', help='Check configuration only')
    parser.add_argument('--feedback', type=str, help='Add runner feedback for analysis')
    parser.add_argument('--limit', type=int, default=None, help='Number of activities to fetch (default from MAX_ACTIVITIES in .env)')
    parser.add_argument('--user', type=str, help='User ID for OAuth authentication (required for analysis, e.g., boris_ryashko)')
    parser.add_argument('--oauth-setup', type=str, help='Setup OAuth for new user (provide user ID)')
    parser.add_argument('--list-users', action='store_true', help='List authenticated users')
    
    args = parser.parse_args()
    
    print("🤖 AI COACH - Strava + OpenAI Integration")
    print("=" * 60)
    
    # Load configuration
    config = get_config()
    config.print_status()
    
    if args.config_check:
        print("\n✅ Configuration check complete!")
        return
    
    # Handle OAuth-specific commands
    if args.list_users:
        from strava_auth import StravaAuthManager
        auth_manager = StravaAuthManager(config)
        users = auth_manager.list_authenticated_users()
        
        print("\n👥 Authenticated Users:")
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
        print(f"\n🔐 Setting up OAuth for new user: {args.oauth_setup}")
        try:
            setup_new_user(config, args.oauth_setup)
            print(f"✅ OAuth setup completed for {args.oauth_setup}")
        except Exception as e:
            print(f"❌ OAuth setup failed: {e}")
        return
    
    # Validate configuration
    is_valid, missing_keys = config.validate_keys()
    if not is_valid:
        print(f"\n❌ Missing configuration: {', '.join(missing_keys)}")
        print("\n📋 Setup Instructions:")
        print("1. Copy .env.template to .env")
        print("2. Edit .env with your actual API keys")
        print("3. Run: python main.py --config-check")
        return
    
    # Require user_id for analysis
    if not args.user:
        print("\n❌ User ID is required for analysis")
        print("\n💡 Usage:")
        print("  • First time: python main.py --oauth-setup <user_id>")
        print("  • Analysis:   python main.py --user <user_id>")
        print("  • List users: python main.py --list-users")
        return
    
    # Ask user for number of activities or use provided/default value
    if args.limit is None:
        try:
            user_input = input(f"\n📱 How many recent activities to analyze? (default: {config.MAX_ACTIVITIES}): ").strip()
            if user_input:
                args.limit = int(user_input)
            else:
                args.limit = config.MAX_ACTIVITIES
        except (ValueError, KeyboardInterrupt):
            print(f"\nUsing default: {config.MAX_ACTIVITIES} activities")
            args.limit = config.MAX_ACTIVITIES
    else:
        print(f"\n📱 Using specified limit: {args.limit} activities")
    
    # Get user ID for OAuth
    user_id = args.user
    if not user_id and config.has_oauth_config():
        # Ask for user ID if OAuth is configured but no user specified
        user_id = input("\n👤 Enter user ID for OAuth authentication (or press Enter for legacy token): ").strip()
        if not user_id:
            user_id = None
    
    print(f"\n📱 Fetching your recent {args.limit} activities...")
    activities = get_strava_activities(config, args.limit, user_id)
    
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
    
    print(f"\n🧠 AI ANALYSIS OF ALL {len(activities)} ACTIVITIES")
    print("=" * 60)
    
    # Get feedback if not provided via command line
    feedback = args.feedback or ""
    if not feedback:
        print("💬 Add runner feedback (optional, press Enter to skip):")
        print("Examples: 'Felt strong', 'Legs were tired', 'Could have gone faster'")
        try:
            feedback = input("Your feedback: ").strip()
        except (EOFError, KeyboardInterrupt):
            feedback = ""
            print("\nNo feedback provided.")
    
    # Analyze with AI
    print(f"\n🚀 AI Analysis:")
    if feedback:
        print(f"📝 Including your feedback: \"{feedback}\"")
    
    analysis = analyze_workout(config, activities, feedback)
    print(f"\n{analysis}")
    
    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Try running: python main.py --config-check")