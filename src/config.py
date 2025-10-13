"""
Configuration manager for AI Coach
Handles API keys and settings securely using environment variables
"""

import os
from typing import Optional

class Config:
    """Configuration class that loads settings from environment variables"""
    
    def __init__(self):
        """Initialize configuration from environment variables"""
        self.load_from_env()
    
    def load_from_env(self):
        """Load configuration from environment variables"""
        
        # Strava Configuration
        self.STRAVA_BASE_URL = os.getenv('STRAVA_BASE_URL', 'https://www.strava.com/api/v3')
        
        # Strava OAuth Configuration
        self.STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
        self.STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
        self.STRAVA_REDIRECT_URI = os.getenv('STRAVA_REDIRECT_URI', 'http://localhost:8080/callback')
        
        # OpenAI Configuration
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        self.OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        
        # Proxy Configuration
        self.USE_PROXY = os.getenv('USE_PROXY', 'false').lower() == 'true'
        self.HTTP_PROXY = os.getenv('HTTP_PROXY')
        self.HTTPS_PROXY = os.getenv('HTTPS_PROXY')
        
        # SSL Configuration
        self.VERIFY_SSL = os.getenv('VERIFY_SSL', 'false').lower() == 'true'
        
        # Application Settings
        self.MAX_ACTIVITIES = int(os.getenv('MAX_ACTIVITIES', '10'))
        self.DEFAULT_GOALS = os.getenv('DEFAULT_GOALS', 'Improve overall fitness')
    
    def get_proxies(self) -> Optional[dict]:
        """Get proxy configuration if enabled"""
        if self.USE_PROXY and self.HTTP_PROXY:
            return {
                "http": self.HTTP_PROXY,
                "https": self.HTTPS_PROXY or self.HTTP_PROXY
            }
        return None
    
    def validate_keys(self) -> tuple[bool, list[str]]:
        """Validate that required API keys are present"""
        missing_keys = []
        
        # Require OAuth credentials (no more legacy token support)
        if not (self.STRAVA_CLIENT_ID and self.STRAVA_CLIENT_SECRET):
            missing_keys.append("STRAVA_CLIENT_ID + STRAVA_CLIENT_SECRET")
        
        if not self.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        
        is_valid = len(missing_keys) == 0
        return is_valid, missing_keys
    
    def has_oauth_config(self) -> bool:
        """Check if OAuth configuration is available"""
        return bool(self.STRAVA_CLIENT_ID and self.STRAVA_CLIENT_SECRET)
    
    def print_status(self):
        """Print configuration status (without exposing keys)"""
        print("🔧 AI Coach Configuration Status")
        print("=" * 40)
        
        # Check Strava OAuth configuration
        if self.has_oauth_config():
            print(f"✅ Strava OAuth: Client ID {self.STRAVA_CLIENT_ID}")
            print("✅ Strava OAuth: Client Secret configured")
        else:
            print("❌ Strava OAuth: Not configured")
            print("💡 Please set STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET in .env")
        
        # Check OpenAI
        if self.OPENAI_API_KEY:
            key_preview = f"{self.OPENAI_API_KEY[:8]}...{self.OPENAI_API_KEY[-4:]}"
            print(f"✅ OpenAI Key: {key_preview}")
            print(f"📊 OpenAI Model: {self.OPENAI_MODEL}")
        else:
            print("❌ OpenAI Key: Not set")
        
        # Other settings
        print(f"🌐 Use Proxy: {self.USE_PROXY}")
        print(f"🔒 Verify SSL: {self.VERIFY_SSL}")
        print(f"📈 Max Activities: {self.MAX_ACTIVITIES}")
        
        # Validation
        is_valid, missing = self.validate_keys()
        if is_valid:
            print("\n✅ All required keys are configured!")
        else:
            print(f"\n❌ Missing keys: {', '.join(missing)}")
            print("Please set these environment variables.")


def load_env_file(file_path: str = ".env"):
    """
    Load environment variables from a .env file
    This is a simple implementation - for production, use python-dotenv
    """
    # Look for .env file in project root (parent directory of src)
    project_root = os.path.dirname(os.path.dirname(__file__))
    env_path = os.path.join(project_root, file_path)
    
    if not os.path.exists(env_path):
        return False
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        return True
    except Exception as e:
        print(f"Error loading .env file: {e}")
        return False


# Global config instance
config = None

def get_config() -> Config:
    """Get the global configuration instance"""
    global config
    if config is None:
        # Try to load .env file first
        load_env_file()
        config = Config()
    return config


if __name__ == "__main__":
    # Test configuration
    print("Testing configuration...")
    config = get_config()
    config.print_status()
    
    print("\n" + "=" * 40)
    print("How to set up your environment variables:")
    print("1. Copy .env.template to .env")
    print("2. Edit .env with your actual API keys")
    print("3. Or set system environment variables")
    print("4. Run this script again to verify")