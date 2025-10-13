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
import requests
import json


def get_strava_activities(config, limit=None):
    """Get recent activities from Strava"""
    # Use config default if no limit specified
    if limit is None:
        limit = config.MAX_ACTIVITIES
        
    if not config.STRAVA_TOKEN:
        print("❌ Strava token not configured. Please set STRAVA_TOKEN in .env file.")
        return []
    
    headers = {"Authorization": f"Bearer {config.STRAVA_TOKEN}"}
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
        
        activity = activities[0] if activities else {}
        
        if feedback.strip():
            return ai_client.analyze_workout_with_feedback(activity, feedback)
        else:
            return ai_client.analyze_workout_data(activity)
            
    except Exception as e:
        return f"❌ Error with AI analysis: {e}"


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="AI Coach - Strava + OpenAI Integration")
    parser.add_argument('--config-check', action='store_true', help='Check configuration only')
    parser.add_argument('--feedback', type=str, help='Add runner feedback for analysis')
    parser.add_argument('--limit', type=int, default=None, help='Number of activities to fetch (default from MAX_ACTIVITIES in .env)')
    
    args = parser.parse_args()
    
    print("🤖 AI COACH - Strava + OpenAI Integration")
    print("=" * 60)
    
    # Load configuration
    config = get_config()
    config.print_status()
    
    if args.config_check:
        print("\n✅ Configuration check complete!")
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
    
    print(f"\n📱 Fetching your recent {args.limit} activities...")
    activities = get_strava_activities(config, args.limit)
    
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
    
    print(f"\n🧠 AI ANALYSIS OF LATEST ACTIVITY")
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
    
    print(f"\n🎯 Next Steps:")
    print("• Run with different feedback: python main.py --feedback 'your thoughts'")
    print("• Check more activities: python main.py --limit 5")
    print("• Try examples: python examples/secure_demo.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Try running: python main.py --config-check")