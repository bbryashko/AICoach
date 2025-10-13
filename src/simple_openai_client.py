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
        
        # Build the messages array for context and tone
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an experienced running coach specializing in half-marathon preparation. "
                    "You create personalized, structured, and actionable training guidance. "
                    "Your tone is supportive, motivational, and data-driven. "
                    "You adapt the plan based on fatigue, terrain, and feedback."
                )
            },
            {"role": "user", "content": prompt}
        ]

        # Call your chat completion method with improved parameters
        return self._chat_completion(
            messages=messages,
            model=self.model,      # Explicitly pass the model from .env
            temperature=0.7,       # balance of structure and creativity
            max_tokens=2000        # ensures full plan fits comfortably
        )
    
   
    
   
    def _chat_completion(self, prompt: str = None, max_tokens: int = 1000, messages: list = None, model: str = None, temperature: float = None) -> str:
        """
        Internal method to make chat completion requests using direct HTTP.
        
        Args:
            prompt (str, optional): The prompt to send to OpenAI (for simple calls)
            max_tokens (int): Maximum tokens in response
            messages (list, optional): Messages array for advanced calls
            model (str, optional): Override the default model
            temperature (float, optional): Override the default temperature
            
        Returns:
            str: AI response
        """
        try:
            # Use provided model or fall back to instance model
            request_model = model if model else self.model
            # Use provided temperature or default
            request_temperature = temperature if temperature is not None else 0.7
            
            # Build messages array - either from provided messages or from prompt
            if messages:
                request_messages = messages
            elif prompt:
                request_messages = [
                    {"role": "system", "content": "You are an expert AI fitness coach and sports scientist."},
                    {"role": "user", "content": prompt}
                ]
            else:
                raise ValueError("Either 'prompt' or 'messages' must be provided")
            
            # Prepare the request payload
            payload = {
                "model": request_model,
                "messages": request_messages,
                "max_tokens": max_tokens,
                "temperature": request_temperature
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