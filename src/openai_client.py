import openai
import json
import os
from typing import List, Dict, Optional

class OpenAIClient:
    """
    A client class for interacting with the OpenAI API.
    Useful for AI coaching features like workout analysis, recommendations, etc.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize the OpenAI client.
        
        Args:
            api_key (str): Your OpenAI API key
            model (str): The model to use (default: gpt-3.5-turbo)
        """
        # Clear any proxy environment variables that might interfere
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
        for var in proxy_vars:
            if var in os.environ:
                del os.environ[var]
        
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def analyze_workout_data(self, workout_data: Dict) -> str:
        """
        Analyze workout data from Strava and provide AI-powered insights.
        
        Args:
            workout_data (Dict): Workout data from Strava API
            
        Returns:
            str: AI analysis and recommendations
        """
        prompt = f"""
        As an AI fitness coach, analyze this workout data and provide insights:
        
        Workout Data:
        {json.dumps(workout_data, indent=2)}
        
        Please provide:
        1. Performance analysis
        2. Areas for improvement
        3. Training recommendations
        4. Recovery suggestions
        
        Keep the response concise and actionable.
        """
        
        return self._chat_completion(prompt)
    
    def generate_training_plan(self, athlete_profile: Dict, goals: str) -> str:
        """
        Generate a personalized training plan based on athlete profile and goals.
        
        Args:
            athlete_profile (Dict): Athlete's profile data
            goals (str): Training goals
            
        Returns:
            str: Personalized training plan
        """
        prompt = f"""
        Create a personalized training plan for this athlete:
        
        Athlete Profile:
        {json.dumps(athlete_profile, indent=2)}
        
        Goals: {goals}
        
        Please provide:
        1. Weekly training structure
        2. Specific workout types
        3. Progressive overload strategy
        4. Recovery recommendations
        5. Key metrics to track
        """
        
        return self._chat_completion(prompt)
    
    def nutrition_recommendations(self, workout_data: Dict, athlete_profile: Dict) -> str:
        """
        Get nutrition recommendations based on workout intensity and athlete profile.
        
        Args:
            workout_data (Dict): Recent workout data
            athlete_profile (Dict): Athlete's profile
            
        Returns:
            str: Nutrition recommendations
        """
        prompt = f"""
        As a sports nutritionist, provide nutrition recommendations:
        
        Recent Workout:
        {json.dumps(workout_data, indent=2)}
        
        Athlete Profile:
        {json.dumps(athlete_profile, indent=2)}
        
        Please provide:
        1. Pre-workout nutrition
        2. During workout fueling (if applicable)
        3. Post-workout recovery nutrition
        4. General daily nutrition guidelines
        """
        
        return self._chat_completion(prompt)
    
    def injury_prevention_advice(self, workout_history: List[Dict]) -> str:
        """
        Analyze workout patterns for injury prevention advice.
        
        Args:
            workout_history (List[Dict]): List of recent workouts
            
        Returns:
            str: Injury prevention recommendations
        """
        prompt = f"""
        Analyze this workout history for injury prevention:
        
        Workout History:
        {json.dumps(workout_history, indent=2)}
        
        Please identify:
        1. Potential overuse patterns
        2. Training load concerns
        3. Recovery gaps
        4. Specific injury prevention exercises
        5. Recommended modifications
        """
        
        return self._chat_completion(prompt)
    
    def motivational_message(self, recent_performance: Dict, goals: str) -> str:
        """
        Generate a motivational message based on recent performance.
        
        Args:
            recent_performance (Dict): Recent workout performance
            goals (str): Athlete's goals
            
        Returns:
            str: Motivational message
        """
        prompt = f"""
        Create a motivational message for this athlete:
        
        Recent Performance:
        {json.dumps(recent_performance, indent=2)}
        
        Goals: {goals}
        
        Provide an encouraging, personalized message that:
        1. Acknowledges their effort
        2. Highlights progress
        3. Motivates towards their goals
        4. Includes actionable next steps
        """
        
        return self._chat_completion(prompt)
    
    def _chat_completion(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Internal method to make chat completion requests.
        
        Args:
            prompt (str): The prompt to send to OpenAI
            max_tokens (int): Maximum tokens in response
            
        Returns:
            str: AI response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert AI fitness coach and sports scientist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error communicating with OpenAI: {str(e)}"
    
    def custom_query(self, query: str, context: Optional[str] = None) -> str:
        """
        Make a custom query to OpenAI with optional context.
        
        Args:
            query (str): The question or request
            context (str, optional): Additional context for the query
            
        Returns:
            str: AI response
        """
        prompt = query
        if context:
            prompt = f"Context: {context}\n\nQuery: {query}"
        
        return self._chat_completion(prompt)


# Example usage
if __name__ == "__main__":
    # Example of how to use the OpenAI client
    # Note: You'll need to set your actual OpenAI API key
    
    # Initialize client (replace with your actual API key)
    # openai_client = OpenAIClient("your-openai-api-key-here")
    
    # Example workout data structure
    sample_workout = {
        "name": "Morning Run",
        "type": "Run",
        "distance": 5000,  # meters
        "moving_time": 1800,  # seconds (30 minutes)
        "average_speed": 2.78,  # m/s
        "max_speed": 4.2,
        "average_heartrate": 145,
        "max_heartrate": 165,
        "total_elevation_gain": 50
    }
    
    # Example athlete profile
    sample_profile = {
        "age": 30,
        "weight": 70,  # kg
        "height": 175,  # cm
        "fitness_level": "intermediate",
        "primary_sport": "running"
    }
    
    print("OpenAI Client for AI Coach created successfully!")
    print("To use this class, you'll need to:")
    print("1. Install openai package: pip install openai")
    print("2. Get an OpenAI API key from https://platform.openai.com/")
    print("3. Initialize the client with your API key")