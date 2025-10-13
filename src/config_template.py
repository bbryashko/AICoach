# Configuration template for AI Coach
# Copy this file to config.py and add your actual API keys

class Config:
    """Configuration class for AI Coach application"""
    
    # Strava API Configuration
    STRAVA_TOKEN = "your-strava-access-token-here"
    STRAVA_BASE_URL = "https://www.strava.com/api/v3"
    
    # OpenAI API Configuration  
    OPENAI_API_KEY = "sk-your-openai-api-key-here"
    OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4" if you have access
    
    # Proxy settings (if needed for corporate networks)
    USE_PROXY = True  # Set to False if you don't need proxy
    PROXIES = {
        "http": "http://b2b-http.dhl.com:8080",
        "https": "http://b2b-http.dhl.com:8080",
    }
    
    # SSL Verification
    VERIFY_SSL = False  # Set to True in production
    
    # AI Coach Settings
    MAX_ACTIVITIES_TO_ANALYZE = 10
    DEFAULT_TRAINING_GOALS = "Improve overall fitness and performance"

# Example usage:
# from config import Config
# 
# # Initialize AI Coach with config
# coach = AICoach(Config.STRAVA_TOKEN, Config.OPENAI_API_KEY)
# 
# # Use proxy settings for Strava requests if needed
# if Config.USE_PROXY:
#     response = requests.get(url, headers=headers, 
#                           proxies=Config.PROXIES, 
#                           verify=Config.VERIFY_SSL)