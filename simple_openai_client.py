"""
Simple OpenAI client using direct HTTP requests to avoid library conflicts
"""

import requests
import json
from typing import Dict, Optional


class SimpleOpenAIClient:
    """
    A simple OpenAI client using direct HTTP requests instead of the openai library.
    This avoids package version conflicts.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", base_url: str = "https://api.openai.com/v1"):
        """
        Initialize the simple OpenAI client.
        
        Args:
            api_key (str): Your OpenAI API key
            model (str): The model to use (default: gpt-3.5-turbo)
            base_url (str): OpenAI API base URL (default: https://api.openai.com/v1)
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
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
        5. Am I on a right way for Dresden half on October 26th?

        
        Keep the response concise and actionable.
        """
        
        return self._chat_completion(prompt)
    
    def analyze_workout_with_feedback(self, workout_data: Dict, runner_feedback: str) -> str:
        """
        Analyze workout data with additional runner feedback and insights.
        
        Args:
            workout_data (Dict): Workout data from Strava API
            runner_feedback (str): Additional feedback/notes from the runner
            
        Returns:
            str: AI analysis incorporating runner feedback
        """
        prompt = f"""
        As an AI fitness coach, analyze this workout data along with the runner's personal feedback:
        
        Workout Data:
        {json.dumps(workout_data, indent=2)}
        
        Runner's Feedback:
        "{runner_feedback}"
        
        Please provide a comprehensive analysis that incorporates both the objective data and the runner's subjective experience:
        1. Performance analysis (considering both data and feedback)
        2. How the runner's feelings align with the objective metrics

        4. Progress towards Dresden half marathon on October 26th
        5. Propose a real Training Plan for the next 2 week before the race
        
        Keep the response personal, actionable, and encouraging.
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
    
    def _chat_completion(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Internal method to make chat completion requests using direct HTTP.
        
        Args:
            prompt (str): The prompt to send to OpenAI
            max_tokens (int): Maximum tokens in response
            
        Returns:
            str: AI response
        """
        try:
            # Prepare the request payload
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are an expert AI fitness coach and sports scientist."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            # Make the HTTP request to OpenAI API
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                verify=False  # Disable SSL verification for simplicity
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error communicating with OpenAI: {str(e)}"


# Example usage
if __name__ == "__main__":
    # Test the simple client
    print("Simple OpenAI Client Test")
    print("=" * 30)
    
    # This would work with a real API key
    # client = SimpleOpenAIClient("your-api-key-here")
    # result = client.custom_query("Hello, can you help me with fitness advice?")
    # print(result)
    
    print("Simple OpenAI client created successfully!")
    print("This version uses direct HTTP requests to avoid package conflicts.")