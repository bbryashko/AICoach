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
    

    def analyze_workout_with_feedback(self, workout_data, runner_feedback: str) -> str:
        """
        Analyze workout data with additional runner feedback and insights.
        
        Args:
            workout_data: Single workout (Dict) or multiple workouts (List[Dict]) from Strava API
            runner_feedback (str): Additional feedback/notes from the runner
            
        Returns:
            str: AI analysis incorporating runner feedback
        """
        # Handle both single activity and multiple activities
        if isinstance(workout_data, list):
            if not workout_data:
                return "❌ No workout data available for analysis."
            
            if runner_feedback.strip():
                prompt = f"""
        As an AI fitness coach, analyze these {len(workout_data)} recent workouts along with the runner's personal feedback:
        
        WORKOUT DATA:
        {json.dumps(workout_data, indent=2)}
        
        Runner's Feedback about recent training:
        "{runner_feedback}"
        
        Please provide a comprehensive analysis that incorporates both the objective data and the runner's subjective experience:
        1. Overall performance analysis across all activities (considering both data and feedback)
        2. How the runner's feelings align with the objective training patterns
        3. Training progression and consistency analysis
        4. Alignment of subjective experience with objective metrics
        5. Progress towards Dresden half marathon on October 26th
        6. Propose a detailed Training Plan for the next 2 weeks before the race
        
        Keep the response comprehensive, personal, and encouraging.
        """
            else:
                prompt = f"""
        As an AI fitness coach, analyze these {len(workout_data)} recent workouts and provide comprehensive insights:
        
        WORKOUT DATA:
        {json.dumps(workout_data, indent=2)}
        
        Please provide:
        1. Overall training pattern analysis across all activities
        2. Performance trends and progression
        3. Training balance (intensity, volume, recovery)
        4. Areas for improvement based on the pattern
        5. Specific recommendations for upcoming Dresden half marathon on October 26th
        6. Training plan adjustments based on recent performance
        
        Keep the response comprehensive but actionable.
        """
        else:
            # Single activity analysis (backward compatibility)
            if runner_feedback.strip():
                prompt = f"""
        As an AI fitness coach, analyze this workout data along with the runner's personal feedback:
        
        Workout Data:
        {json.dumps(workout_data, indent=2)}
        
        Runner's Feedback:
        "{runner_feedback}"
        
        Please provide a comprehensive analysis that incorporates both the objective data and the runner's subjective experience:
        1. Performance analysis (considering both data and feedback)
        2. How the runner's feelings align with the objective metrics
        3. Areas for improvement based on feedback alignment
        4. Progress towards Dresden half marathon on October 26th
        5. Propose a real Training Plan for the next 2 week before the race
        
        Keep the response personal, actionable, and encouraging.
        """
            else:
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
    
    def _chat_completion_with_messages(self, messages: list, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Chat completion specifically for chat sessions with custom message history.
        
        Args:
            messages (list): Array of message dictionaries with 'role' and 'content'
            max_tokens (int): Maximum tokens in response
            temperature (float): Response creativity (0.0 to 1.0)
            
        Returns:
            str: AI response
        """
        return self._chat_completion(
            messages=messages, 
            max_tokens=max_tokens, 
            temperature=temperature
        )


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