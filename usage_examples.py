"""
Complete Example: How to Use the AI Coach Classes
This script demonstrates practical usage of the OpenAI and AICoach integration classes.
"""

import json
from openai_client import OpenAIClient
from ai_coach_integration import AICoach

def demo_openai_client():
    """
    Demo 1: Using OpenAIClient class standalone
    """
    print("=" * 50)
    print("DEMO 1: OpenAI Client Usage")
    print("=" * 50)
    
    # Step 1: Initialize the OpenAI client
    # Replace with your actual OpenAI API key
    openai_api_key = "sk-your-openai-api-key-here"
    ai_client = OpenAIClient(openai_api_key)
    
    # Sample workout data (like what you'd get from Strava)
    workout_data = {
        "name": "Morning Run",
        "type": "Run", 
        "distance": 8000,  # 8km
        "moving_time": 2400,  # 40 minutes
        "average_speed": 3.33,  # m/s
        "average_heartrate": 155,
        "max_heartrate": 178,
        "total_elevation_gain": 120,
        "suffer_score": 65
    }
    
    # Sample athlete profile
    athlete_profile = {
        "age": 32,
        "weight": 75,
        "height": 180,
        "fitness_level": "intermediate",
        "primary_sport": "running",
        "weekly_training_hours": 6
    }
    
    print("🏃 Analyzing workout data...")
    try:
        # Analyze the workout
        analysis = ai_client.analyze_workout_data(workout_data)
        print(f"AI Analysis:\n{analysis}\n")
        
        # Get nutrition recommendations
        print("🥗 Getting nutrition recommendations...")
        nutrition = ai_client.nutrition_recommendations(workout_data, athlete_profile)
        print(f"Nutrition Advice:\n{nutrition}\n")
        
        # Generate training plan
        print("📋 Generating training plan...")
        goals = "Improve 10K time to under 45 minutes"
        training_plan = ai_client.generate_training_plan(athlete_profile, goals)
        print(f"Training Plan:\n{training_plan}\n")
        
        # Get motivational message
        print("💪 Getting motivational message...")
        motivation = ai_client.motivational_message(workout_data, goals)
        print(f"Motivation:\n{motivation}\n")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: You need a valid OpenAI API key to run this demo")

def demo_ai_coach_integration():
    """
    Demo 2: Using the full AICoach integration (Strava + OpenAI)
    """
    print("=" * 50)
    print("DEMO 2: AI Coach Integration Usage")
    print("=" * 50)
    
    # Your API credentials
    strava_token = "your-strava-token-here"
    openai_api_key = "sk-your-openai-api-key-here"
    
    # Initialize the AI Coach
    coach = AICoach(strava_token, openai_api_key)
    
    print("🤖 AI Coach initialized!")
    print("\nAvailable features:")
    print("1. analyze_latest_workout() - AI analysis of your most recent workout")
    print("2. generate_weekly_insights() - Analysis of your past week's training")
    print("3. get_personalized_training_plan(goals) - Custom training plan")
    print("4. get_recovery_recommendations() - Recovery advice based on training load")
    print("5. ask_coach(question) - Ask specific questions to your AI coach")
    
    # Example usage (commented out since we need real API keys)
    """
    try:
        # Analyze latest workout
        latest_analysis = coach.analyze_latest_workout()
        print(f"Latest Workout Analysis:\n{latest_analysis}\n")
        
        # Get weekly insights
        weekly_insights = coach.generate_weekly_insights()
        print(f"Weekly Insights:\n{weekly_insights}\n")
        
        # Get training plan
        goals = "Train for a half marathon in 3 months"
        training_plan = coach.get_personalized_training_plan(goals)
        print(f"Training Plan:\n{training_plan}\n")
        
        # Get recovery recommendations
        recovery = coach.get_recovery_recommendations()
        print(f"Recovery Recommendations:\n{recovery}\n")
        
        # Ask a specific question
        question = "Should I run today or take a rest day?"
        answer = coach.ask_coach(question)
        print(f"Coach Answer:\n{answer}\n")
        
    except Exception as e:
        print(f"Error: {e}")
    """

def demo_with_sample_data():
    """
    Demo 3: Working with sample data (no API keys needed)
    """
    print("=" * 50)
    print("DEMO 3: Sample Data Demo (No API Keys Required)")
    print("=" * 50)
    
    # Sample Strava activities data
    sample_activities = [
        {
            "name": "Morning Run",
            "type": "Run",
            "distance": 5000,
            "moving_time": 1800,
            "average_speed": 2.78,
            "average_heartrate": 145,
            "total_elevation_gain": 50
        },
        {
            "name": "Easy Bike Ride", 
            "type": "Ride",
            "distance": 15000,
            "moving_time": 2400,
            "average_speed": 6.25,
            "average_heartrate": 135,
            "total_elevation_gain": 200
        },
        {
            "name": "Track Intervals",
            "type": "Run", 
            "distance": 8000,
            "moving_time": 2100,
            "average_speed": 3.81,
            "average_heartrate": 165,
            "total_elevation_gain": 10
        }
    ]
    
    print("📊 Sample training data:")
    for i, activity in enumerate(sample_activities, 1):
        print(f"{i}. {activity['name']} - {activity['distance']/1000:.1f}km in {activity['moving_time']//60}min")
    
    # Calculate some basic metrics
    total_distance = sum(act['distance'] for act in sample_activities) / 1000
    total_time = sum(act['moving_time'] for act in sample_activities) / 3600
    avg_hr = sum(act['average_heartrate'] for act in sample_activities) / len(sample_activities)
    
    print(f"\n📈 Weekly Summary:")
    print(f"Total Distance: {total_distance:.1f} km")
    print(f"Total Time: {total_time:.1f} hours")
    print(f"Average Heart Rate: {avg_hr:.0f} bpm")
    print(f"Activities: {len(sample_activities)}")
    
    # Show what prompts would be sent to AI
    print(f"\n🤖 Sample AI Prompt for Analysis:")
    prompt_example = f"""
    As an AI fitness coach, analyze this training data:
    
    Weekly Activities: {json.dumps(sample_activities, indent=2)}
    
    Please provide:
    1. Training load assessment
    2. Recovery recommendations  
    3. Performance insights
    4. Next week's training suggestions
    """
    
    print(prompt_example[:500] + "..." if len(prompt_example) > 500 else prompt_example)

def setup_instructions():
    """
    Show setup instructions
    """
    print("=" * 50)
    print("SETUP INSTRUCTIONS")
    print("=" * 50)
    
    print("🔧 To use these classes, follow these steps:")
    print()
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Get OpenAI API Key:")
    print("   - Go to https://platform.openai.com/")
    print("   - Create an account and get an API key")
    print("   - Replace 'sk-your-openai-api-key-here' with your actual key")
    print()
    print("3. Get Strava API Token:")
    print("   - Go to https://www.strava.com/settings/api")
    print("   - Create an application")
    print("   - Get your access token")
    print("   - Replace 'your-strava-token-here' with your actual token")
    print()
    print("4. Basic Usage Examples:")
    print()
    print("   # OpenAI Client only")
    print("   from openai_client import OpenAIClient")
    print("   client = OpenAIClient('your-api-key')")
    print("   analysis = client.analyze_workout_data(workout_data)")
    print()
    print("   # Full AI Coach (Strava + OpenAI)")
    print("   from ai_coach_integration import AICoach") 
    print("   coach = AICoach('strava-token', 'openai-key')")
    print("   insights = coach.analyze_latest_workout()")
    print()
    print("5. Environment Variables (Recommended):")
    print("   Create a .env file with:")
    print("   STRAVA_TOKEN=your_token_here")
    print("   OPENAI_API_KEY=your_key_here")

def main():
    """
    Main demo function
    """
    print("🤖 AI COACH CLASSES USAGE GUIDE")
    print("This demo shows you how to use the created classes")
    print()
    
    # Show setup instructions first
    setup_instructions()
    
    # Demo with sample data (works without API keys)
    demo_with_sample_data()
    
    # Demo OpenAI client (needs API key)
    print("\n" + "="*50)
    print("NOTE: The following demos require valid API keys")
    print("="*50)
    
    # Uncomment these if you have API keys
    # demo_openai_client()
    # demo_ai_coach_integration()
    
    print("\n🎉 Demo complete!")
    print("Modify this script with your API keys to see the AI features in action!")

if __name__ == "__main__":
    main()