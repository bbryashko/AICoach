"""
Quick Start Example: Using Your Existing Strava Data with AI Coach
This example shows how to integrate your current Strava API test with OpenAI analysis.
Now uses secure configuration from environment variables.
"""

import requests
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from simple_openai_client import SimpleOpenAIClient
from config import get_config

# Load configuration from environment variables
config = get_config()
STRAVA_TOKEN = config.STRAVA_TOKEN
STRAVA_URL = f"{config.STRAVA_BASE_URL}/athlete/activities"
OPENAI_API_KEY = config.OPENAI_API_KEY

def get_strava_activities(limit=5):
    """
    Get recent activities from Strava using your existing token
    """
    headers = {"Authorization": f"Bearer {STRAVA_TOKEN}"}
    params = {"per_page": limit}
    
    try:
        # Exact same approach as strava_api_test.py
        response = requests.get(STRAVA_URL, headers=headers, params=params, verify=False)  # ignore SSL for now
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error response: {response.text}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching Strava data: {e}")
        return []

def analyze_with_mock_ai(activity_data):
    """
    Mock AI analysis when you don't have OpenAI API key yet
    """
    if not activity_data:
        return "No activity data to analyze"
    
    activity = activity_data[0] if isinstance(activity_data, list) else activity_data
    
    # Extract key metrics
    distance_km = activity.get('distance', 0) / 1000
    time_min = activity.get('moving_time', 0) / 60
    avg_speed_kmh = (activity.get('average_speed', 0) * 3.6) if activity.get('average_speed') else 0
    activity_type = activity.get('type', 'Unknown')
    name = activity.get('name', 'Unnamed Activity')
    
    # Mock analysis based on the data
    analysis = f"""
🏃 ACTIVITY ANALYSIS: {name}
📊 Type: {activity_type}
📏 Distance: {distance_km:.2f} km
⏱️  Time: {time_min:.1f} minutes
🚀 Average Speed: {avg_speed_kmh:.2f} km/h

💡 MOCK AI INSIGHTS:
"""
    
    if activity_type == "Run":
        if avg_speed_kmh > 12:
            analysis += "• Fast pace! Great speed work.\n"
        elif avg_speed_kmh > 10:
            analysis += "• Good moderate pace, excellent for base building.\n"
        else:
            analysis += "• Easy/recovery pace, perfect for aerobic development.\n"
            
        if distance_km > 10:
            analysis += "• Long run completed - great endurance work!\n"
        elif distance_km > 5:
            analysis += "• Medium distance run - good for fitness maintenance.\n"
        else:
            analysis += "• Short run - good for recovery or speed work.\n"
    
    elif activity_type == "Ride":
        if avg_speed_kmh > 25:
            analysis += "• Fast cycling pace - excellent intensity!\n"
        else:
            analysis += "• Steady cycling pace - good for aerobic fitness.\n"
    
    analysis += "• Consider adding heart rate data for better analysis.\n"
    analysis += "• Maintain consistent training for best results.\n"
    
    return analysis

def analyze_with_real_ai(activity_data, api_key, runner_feedback=""):
    """
    Real AI analysis using OpenAI (when you have API key)
    
    Args:
        activity_data: Workout data from Strava
        api_key: OpenAI API key
        runner_feedback: Additional feedback/notes from the runner
    """
    if api_key == "sk-your-openai-api-key-here":
        return "Please add your real OpenAI API key to use real AI analysis."
    
    try:
        ai_client = SimpleOpenAIClient(api_key, config.OPENAI_MODEL, config.OPENAI_BASE_URL)
        activity = activity_data[0] if isinstance(activity_data, list) and activity_data else activity_data
        
        # If runner feedback is provided, use custom analysis
        if runner_feedback.strip():
            return ai_client.analyze_workout_with_feedback(activity, runner_feedback)
        else:
            return ai_client.analyze_workout_data(activity)
            
    except Exception as e:
        return f"Error with AI analysis: {e}"

def main():
    """
    Main function demonstrating the integration
    """
    print("🤖 AI COACH: Strava + OpenAI Integration Demo (Secure Version)")
    print("=" * 60)
    
    # Check configuration first
    print("🔧 Checking configuration...")
    config.print_status()
    
    is_valid, missing_keys = config.validate_keys()
    if not is_valid:
        print(f"\n❌ Missing configuration: {', '.join(missing_keys)}")
        print("Please set up your environment variables:")
        print("1. Copy .env.template to .env")
        print("2. Edit .env with your actual API keys")
        print("3. Or set system environment variables")
        return
    
    print("\n" + "=" * 60)
    
    # Step 1: Get your Strava data
    print("📱 Fetching your recent Strava activities...")
    activities = get_strava_activities(limit=3)
    
    if not activities:
        print("❌ No activities found. Check your Strava token.")
        return
    
    print(f"✅ Found {len(activities)} recent activities:")
    for i, activity in enumerate(activities, 1):
        distance_km = activity.get('distance', 0) / 1000
        name = activity.get('name', 'Unnamed')
        activity_type = activity.get('type', 'Unknown')
        print(f"   {i}. {name} ({activity_type}) - {distance_km:.1f}km")
    
    print("\n" + "=" * 60)
    print("🧠 AI ANALYSIS OF YOUR LATEST ACTIVITY")
    print("=" * 60)
    
    # Step 2: Analyze with mock AI (works without OpenAI key)
    print("📊 Mock AI Analysis (no API key needed):")
    mock_analysis = analyze_with_mock_ai(activities)
    print(mock_analysis)
    
    # Step 3: Get runner feedback for AI analysis
    print("\n" + "-" * 50)
    print("💬 RUNNER FEEDBACK:")
    print("Share how you felt during/after this workout (optional):")
    print("Examples: 'Felt strong', 'Legs were tired', 'Great pace', 'Need more recovery'")
    
    try:
        runner_feedback = input("Your feedback: ").strip()
    except (EOFError, KeyboardInterrupt):
        runner_feedback = ""
        print("\nNo feedback provided.")
    
    # Step 4: Real AI analysis with feedback
    print("\n" + "-" * 60)
    print("🚀 Real AI Analysis (with your feedback):")
    real_analysis = analyze_with_real_ai(activities, OPENAI_API_KEY, runner_feedback)
    print(real_analysis)
    


    


if __name__ == "__main__":
    main()