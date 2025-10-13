"""
AI Coach Integration Example
Combines Strava API data with OpenAI analysis for intelligent coaching insights.
"""

import requests
import json
from .openai_client import OpenAIClient

class AICoach:
    """
    Main AI Coach class that integrates Strava data with OpenAI analysis.
    """
    
    def __init__(self, strava_token: str, openai_api_key: str):
        """
        Initialize the AI Coach with API credentials.
        
        Args:
            strava_token (str): Strava API access token
            openai_api_key (str): OpenAI API key
        """
        self.strava_token = strava_token
        self.strava_headers = {"Authorization": f"Bearer {strava_token}"}
        self.openai_client = OpenAIClient(openai_api_key)
        self.base_url = "https://www.strava.com/api/v3"
    
    def get_recent_activities(self, limit: int = 10) -> list:
        """
        Fetch recent activities from Strava.
        
        Args:
            limit (int): Number of activities to fetch
            
        Returns:
            list: List of recent activities
        """
        url = f"{self.base_url}/athlete/activities"
        params = {"per_page": limit}
        
        try:
            response = requests.get(
                url, 
                headers=self.strava_headers, 
                params=params,
                verify=False  # Note: Consider using proper SSL verification in production
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching Strava activities: {e}")
            return []
    
    def get_athlete_profile(self) -> dict:
        """
        Get athlete profile from Strava.
        
        Returns:
            dict: Athlete profile data
        """
        url = f"{self.base_url}/athlete"
        
        try:
            response = requests.get(
                url, 
                headers=self.strava_headers,
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching athlete profile: {e}")
            return {}
    
    def analyze_latest_workout(self) -> str:
        """
        Get the latest workout and provide AI analysis.
        
        Returns:
            str: AI analysis of the latest workout
        """
        activities = self.get_recent_activities(limit=1)
        if not activities:
            return "No recent activities found."
        
        latest_activity = activities[0]
        return self.openai_client.analyze_workout_data(latest_activity)
    
    def generate_weekly_insights(self) -> str:
        """
        Analyze the past week's activities and generate insights.
        
        Returns:
            str: Weekly training insights
        """
        activities = self.get_recent_activities(limit=7)
        if not activities:
            return "No recent activities found for weekly analysis."
        
        # Prepare summary data
        weekly_summary = {
            "total_activities": len(activities),
            "activities": activities,
            "total_distance": sum(act.get('distance', 0) for act in activities),
            "total_time": sum(act.get('moving_time', 0) for act in activities),
            "activity_types": list(set(act.get('type', 'Unknown') for act in activities))
        }
        
        prompt = f"""
        Analyze this week's training data and provide comprehensive insights:
        
        Weekly Summary:
        {json.dumps(weekly_summary, indent=2)}
        
        Please provide:
        1. Training volume analysis
        2. Recovery assessment
        3. Performance trends
        4. Recommendations for next week
        5. Areas of concern (if any)
        """
        
        return self.openai_client._chat_completion(prompt)
    
    def get_personalized_training_plan(self, goals: str) -> str:
        """
        Generate a personalized training plan based on athlete data and goals.
        
        Args:
            goals (str): Training goals
            
        Returns:
            str: Personalized training plan
        """
        profile = self.get_athlete_profile()
        recent_activities = self.get_recent_activities(limit=14)  # Last 2 weeks
        
        athlete_data = {
            "profile": profile,
            "recent_training": recent_activities
        }
        
        return self.openai_client.generate_training_plan(athlete_data, goals)
    
    def get_recovery_recommendations(self) -> str:
        """
        Get AI-powered recovery recommendations based on recent training.
        
        Returns:
            str: Recovery recommendations
        """
        activities = self.get_recent_activities(limit=7)
        profile = self.get_athlete_profile()
        
        if not activities:
            return "No recent activities found for recovery analysis."
        
        # Calculate training load metrics
        total_time = sum(act.get('moving_time', 0) for act in activities)
        total_distance = sum(act.get('distance', 0) for act in activities)
        avg_heart_rate = sum(act.get('average_heartrate', 0) for act in activities if act.get('average_heartrate')) / len([act for act in activities if act.get('average_heartrate')]) if activities else 0
        
        recovery_data = {
            "weekly_training_time": total_time,
            "weekly_distance": total_distance,
            "average_heart_rate": avg_heart_rate,
            "activity_count": len(activities),
            "athlete_profile": profile
        }
        
        prompt = f"""
        Based on this training data, provide recovery recommendations:
        
        Training Load Data:
        {json.dumps(recovery_data, indent=2)}
        
        Please provide:
        1. Recovery status assessment
        2. Sleep recommendations
        3. Nutrition for recovery
        4. Active recovery suggestions
        5. Warning signs to watch for
        """
        
        return self.openai_client._chat_completion(prompt)
    
    def ask_coach(self, question: str) -> str:
        """
        Ask the AI coach a specific question with context from your Strava data.
        
        Args:
            question (str): Your question for the coach
            
        Returns:
            str: AI coach response
        """
        # Get context data
        recent_activities = self.get_recent_activities(limit=5)
        profile = self.get_athlete_profile()
        
        context = {
            "recent_activities": recent_activities,
            "athlete_profile": profile
        }
        
        context_str = f"Athlete's recent training data: {json.dumps(context, indent=2)}"
        
        return self.openai_client.custom_query(question, context_str)


# Example usage
if __name__ == "__main__":
    # Configuration (replace with your actual tokens)
    STRAVA_TOKEN = "your-strava-token-here"
    OPENAI_API_KEY = "your-openai-api-key-here"
    
    # Initialize AI Coach
    # coach = AICoach(STRAVA_TOKEN, OPENAI_API_KEY)
    
    print("AI Coach Integration created successfully!")
    print("\nAvailable features:")
    print("1. analyze_latest_workout() - AI analysis of your most recent workout")
    print("2. generate_weekly_insights() - Weekly training analysis and recommendations")
    print("3. get_personalized_training_plan(goals) - Custom training plan based on your data")
    print("4. get_recovery_recommendations() - AI-powered recovery advice")
    print("5. ask_coach(question) - Ask specific questions to your AI coach")
    
    print("\nTo use this integration:")
    print("1. pip install openai")
    print("2. Set your Strava token and OpenAI API key")
    print("3. Initialize AICoach class with your credentials")