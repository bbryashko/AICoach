"""
Secure AI Coach Demo - Uses environment variables for API keys
"""

import requests
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from simple_openai_client import SimpleOpenAIClient
from config import get_config

def get_strava_activities(limit=5):
    """
    Get recent activities from Strava using configuration
    """
    config = get_config()
    
    if not config.STRAVA_TOKEN:
        print("❌ Strava token not configured. Please set STRAVA_TOKEN environment variable.")
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
    Mock AI analysis when OpenAI is not available
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
    
    # Enhanced mock analysis based on the data
    analysis = f"""
🏃 ACTIVITY ANALYSIS: {name}
📊 Type: {activity_type}
📏 Distance: {distance_km:.2f} km
⏱️  Time: {time_min:.1f} minutes
🚀 Average Speed: {avg_speed_kmh:.2f} km/h

💡 ENHANCED MOCK AI INSIGHTS:
"""
    
    if activity_type == "Run":
        # Pace analysis
        pace_min_per_km = time_min / distance_km if distance_km > 0 else 0
        analysis += f"⏱️  Pace: {pace_min_per_km:.1f} min/km\n"
        
        if avg_speed_kmh > 14:
            analysis += "• Excellent speed! This is race pace territory.\n"
        elif avg_speed_kmh > 12:
            analysis += "• Fast pace! Great for tempo runs and fitness.\n"
        elif avg_speed_kmh > 10:
            analysis += "• Good moderate pace, excellent for base building.\n"
        elif avg_speed_kmh > 8:
            analysis += "• Steady pace, perfect for long runs and endurance.\n"
        else:
            analysis += "• Easy/recovery pace, ideal for active recovery.\n"
            
        # Distance analysis
        if distance_km > 15:
            analysis += "• Long run completed - excellent endurance training!\n"
        elif distance_km > 10:
            analysis += "• Medium-long run - great for building fitness.\n"
        elif distance_km > 5:
            analysis += "• Good medium distance for regular training.\n"
        else:
            analysis += "• Short run - perfect for recovery or speed work.\n"
            
        # Training recommendations
        analysis += "\n🎯 TRAINING RECOMMENDATIONS:\n"
        if pace_min_per_km < 4.5:
            analysis += "• Consider adding easy runs to balance intensity\n"
        elif pace_min_per_km > 6:
            analysis += "• Try incorporating some tempo runs for speed\n"
        
        if distance_km > 12:
            analysis += "• Follow with easy runs for recovery\n"
            analysis += "• Focus on hydration and nutrition post-run\n"
    
    elif activity_type == "Ride":
        if avg_speed_kmh > 25:
            analysis += "• Fast cycling pace - excellent intensity!\n"
        else:
            analysis += "• Steady cycling pace - good for aerobic fitness.\n"
    
    analysis += "• Consider adding heart rate data for better analysis.\n"
    analysis += "• Maintain consistent training for continued progress.\n"
    
    return analysis

def analyze_with_real_ai(activity_data):
    """
    Real AI analysis using OpenAI (when configured)
    """
    config = get_config()
    
    if not config.OPENAI_API_KEY:
        return "⚠️  OpenAI API key not configured. Set OPENAI_API_KEY environment variable for real AI analysis."
    
    try:
        ai_client = SimpleOpenAIClient(config.OPENAI_API_KEY, config.OPENAI_MODEL, config.OPENAI_BASE_URL)
        if isinstance(activity_data, list) and activity_data:
            return ai_client.analyze_workout_data(activity_data[0])
        else:
            return ai_client.analyze_workout_data(activity_data)
    except Exception as e:
        return f"Error with AI analysis: {e}"

def main():
    """
    Main function demonstrating the secure integration
    """
    print("🤖 AI COACH: Secure Strava + OpenAI Integration")
    print("=" * 50)
    
    # Load and validate configuration
    config = get_config()
    config.print_status()
    
    is_valid, missing_keys = config.validate_keys()
    if not is_valid:
        print(f"\n❌ Missing configuration: {', '.join(missing_keys)}")
        print("Please set up your environment variables and try again.")
        return
    
    print("\n" + "=" * 50)
    
    # Step 1: Get your Strava data
    print("📱 Fetching your recent Strava activities...")
    activities = get_strava_activities(limit=3)
    
    if not activities:
        print("❌ No activities found. Check your configuration.")
        return
    
    print(f"✅ Found {len(activities)} recent activities:")
    for i, activity in enumerate(activities, 1):
        distance_km = activity.get('distance', 0) / 1000
        name = activity.get('name', 'Unnamed')
        activity_type = activity.get('type', 'Unknown')
        print(f"   {i}. {name} ({activity_type}) - {distance_km:.1f}km")
    
    print("\n" + "=" * 50)
    print("🧠 AI ANALYSIS OF YOUR LATEST ACTIVITY")
    print("=" * 50)
    
    # Step 2: Enhanced mock analysis
    print("📊 Enhanced Mock AI Analysis:")
    mock_analysis = analyze_with_mock_ai(activities)
    print(mock_analysis)
    
    # Step 3: Real AI analysis (if configured)
    print("\n" + "-" * 50)
    print("🚀 Real AI Analysis:")
    real_analysis = analyze_with_real_ai(activities)
    print(real_analysis)
    
    print("\n" + "=" * 50)
    print("🎯 NEXT STEPS:")
    print("1. Your API keys are now secure and not in source code!")
    print("2. Modify .env file to update your keys")
    print("3. Use the AICoach class for more advanced features")
    print("4. Commit your code safely without exposing secrets")

if __name__ == "__main__":
    main()