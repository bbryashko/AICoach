"""
Strava OAuth Authentication Manager
Handles semi-automated OAuth flow, token management, and refresh
"""

import json
import os
import time
import webbrowser
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, Optional
import requests


class StravaAuthManager:
    """
    Manages Strava OAuth 2.0 authentication with semi-automated setup
    and automatic token refresh for multiple users.
    """
    
    def __init__(self, config):
        """
        Initialize with OAuth configuration from .env
        
        Args:
            config: Configuration object with OAuth credentials
        """
        self.client_id = config.STRAVA_CLIENT_ID
        self.client_secret = config.STRAVA_CLIENT_SECRET
        self.redirect_uri = config.STRAVA_REDIRECT_URI
        self.base_url = config.STRAVA_BASE_URL
        self.tokens_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'tokens')
        self.verify_ssl = config.VERIFY_SSL
        self.proxies = config.get_proxies()
        
        # Ensure tokens directory exists
        os.makedirs(self.tokens_dir, exist_ok=True)
    
    def get_valid_token(self, user_id: str) -> str:
        """
        Get a valid access token for the user, handling all OAuth complexity
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            str: Valid access token
        """
        print(f"🔐 Getting Strava authentication for user: {user_id}")
        
        # Check if we have stored tokens
        if self.has_valid_tokens(user_id):
            token_data = self.load_tokens(user_id)
            print("✅ Using existing valid token")
            return token_data['access_token']
        
        # Check if tokens exist but are expired - try refresh
        if self.has_tokens(user_id):
            print("🔄 Token expired, attempting refresh...")
            refreshed_token = self.refresh_tokens(user_id)
            if refreshed_token:
                print("✅ Token refreshed successfully")
                return refreshed_token
            else:
                print("❌ Token refresh failed, need new authorization")
        
        # First time setup or refresh failed - need new authorization
        print("🚀 Starting initial OAuth setup...")
        return self.initial_oauth_setup(user_id)
    
    def has_tokens(self, user_id: str) -> bool:
        """Check if user has any stored tokens"""
        token_file = self._get_token_file_path(user_id)
        return os.path.exists(token_file)
    
    def has_valid_tokens(self, user_id: str) -> bool:
        """Check if user has valid, non-expired tokens"""
        if not self.has_tokens(user_id):
            return False
        
        try:
            token_data = self.load_tokens(user_id)
            expires_at = token_data.get('expires_at', 0)
            # Consider token valid if it expires more than 5 minutes from now
            buffer_time = time.time() + 300  # 5 minutes buffer
            return expires_at > buffer_time
        except Exception:
            return False
    
    def load_tokens(self, user_id: str) -> Dict:
        """Load stored tokens for a user"""
        token_file = self._get_token_file_path(user_id)
        try:
            with open(token_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load tokens: {e}")
    
    def save_tokens(self, user_id: str, token_data: Dict) -> None:
        """Save tokens for a user"""
        token_file = self._get_token_file_path(user_id)
        try:
            # Add metadata
            token_data['user_id'] = user_id
            token_data['created_at'] = time.time()
            token_data['updated_at'] = time.time()
            
            with open(token_file, 'w') as f:
                json.dump(token_data, f, indent=2)
            print(f"💾 Tokens saved for user: {user_id}")
        except Exception as e:
            raise Exception(f"Failed to save tokens: {e}")
    
    def initial_oauth_setup(self, user_id: str) -> str:
        """
        Semi-automated initial OAuth setup
        Opens browser, user approves, copies code, we exchange for tokens
        """
        print(f"\\n🔐 First-time Strava setup for: {user_id}")
        print("=" * 60)
        
        # Build authorization URL
        auth_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'approval_prompt': 'auto',
            'scope': 'read,activity:read_all'
        }
        
        auth_url = f"https://www.strava.com/oauth/authorize?{urllib.parse.urlencode(auth_params)}"
        
        print("1. 🌐 Opening Strava authorization in your browser...")
        print(f"   URL: {auth_url}")
        
        try:
            webbrowser.open(auth_url)
            print("   ✅ Browser opened successfully")
        except Exception:
            print("   ⚠️  Could not open browser automatically")
            print(f"   Please manually open: {auth_url}")
        
        print("\\n2. 📋 After approving access, Strava will redirect to:")
        print(f"   {self.redirect_uri}?code=AUTHORIZATION_CODE&scope=...")
        print("\\n3. 📝 Copy the authorization code from the URL")
        
        # Get authorization code from user
        while True:
            try:
                code = input("\\n   Paste the authorization code here: ").strip()
                if code:
                    break
                print("   ❌ Please enter a valid code")
            except KeyboardInterrupt:
                print("\\n\\n❌ Setup cancelled by user")
                raise Exception("OAuth setup cancelled")
        
        print("\\n4. 🔄 Exchanging authorization code for tokens...")
        
        # Exchange code for tokens
        try:
            tokens = self.exchange_code_for_tokens(code)
            self.save_tokens(user_id, tokens)
            
            print("\\n✅ OAuth setup completed successfully!")
            print(f"   User: {user_id}")
            print(f"   Athlete ID: {tokens.get('athlete', {}).get('id', 'Unknown')}")
            print(f"   Token expires: {datetime.fromtimestamp(tokens['expires_at'])}")
            
            return tokens['access_token']
            
        except Exception as e:
            print(f"\\n❌ Failed to exchange code for tokens: {e}")
            raise
    
    def exchange_code_for_tokens(self, code: str) -> Dict:
        """Exchange authorization code for access and refresh tokens"""
        token_url = "https://www.strava.com/oauth/token"
        
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        
        try:
            response = requests.post(
                token_url,
                data=payload,
                verify=self.verify_ssl,
                proxies=self.proxies,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Token exchange failed: {e}")
    
    def refresh_tokens(self, user_id: str) -> Optional[str]:
        """
        Refresh expired tokens using refresh token
        
        Returns:
            str: New access token if successful, None if failed
        """
        try:
            current_tokens = self.load_tokens(user_id)
            refresh_token = current_tokens.get('refresh_token')
            
            if not refresh_token:
                print("❌ No refresh token available")
                return None
            
            token_url = "https://www.strava.com/oauth/token"
            payload = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token'
            }
            
            response = requests.post(
                token_url,
                data=payload,
                verify=self.verify_ssl,
                proxies=self.proxies,
                timeout=30
            )
            
            if response.status_code == 200:
                new_tokens = response.json()
                # Preserve user metadata
                new_tokens['user_id'] = user_id
                new_tokens['created_at'] = current_tokens.get('created_at', time.time())
                new_tokens['updated_at'] = time.time()
                
                self.save_tokens(user_id, new_tokens)
                print(f"🔄 Tokens refreshed for {user_id}")
                return new_tokens['access_token']
            else:
                print(f"❌ Token refresh failed: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Token refresh error: {e}")
            return None
    
    def revoke_tokens(self, user_id: str) -> bool:
        """
        Revoke and delete stored tokens for a user
        Useful for logout or switching accounts
        """
        try:
            if self.has_tokens(user_id):
                token_data = self.load_tokens(user_id)
                access_token = token_data.get('access_token')
                
                # Revoke token with Strava
                if access_token:
                    revoke_url = "https://www.strava.com/oauth/deauthorize"
                    headers = {"Authorization": f"Bearer {access_token}"}
                    
                    try:
                        response = requests.post(
                            revoke_url,
                            headers=headers,
                            verify=self.verify_ssl,
                            proxies=self.proxies,
                            timeout=30
                        )
                        if response.status_code == 200:
                            print(f"✅ Token revoked with Strava for {user_id}")
                        else:
                            print(f"⚠️  Token revocation failed: {response.status_code}")
                    except Exception as e:
                        print(f"⚠️  Token revocation error: {e}")
                
                # Delete local token file
                token_file = self._get_token_file_path(user_id)
                os.remove(token_file)
                print(f"🗑️  Local tokens deleted for {user_id}")
                return True
            else:
                print(f"ℹ️  No tokens found for {user_id}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to revoke tokens: {e}")
            return False
    
    def get_token_info(self, user_id: str) -> Optional[Dict]:
        """Get token information for debugging/status"""
        if not self.has_tokens(user_id):
            return None
        
        try:
            token_data = self.load_tokens(user_id)
            expires_at = token_data.get('expires_at', 0)
            athlete = token_data.get('athlete', {})
            
            return {
                'user_id': user_id,
                'athlete_id': athlete.get('id', 'Unknown'),
                'athlete_name': f"{athlete.get('firstname', '')} {athlete.get('lastname', '')}".strip(),
                'expires_at': datetime.fromtimestamp(expires_at) if expires_at else 'Unknown',
                'is_valid': self.has_valid_tokens(user_id),
                'scopes': token_data.get('scope', 'Unknown'),
                'created_at': datetime.fromtimestamp(token_data.get('created_at', 0)) if token_data.get('created_at') else 'Unknown'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def list_authenticated_users(self) -> list:
        """List all users with stored tokens"""
        users = []
        try:
            if os.path.exists(self.tokens_dir):
                for filename in os.listdir(self.tokens_dir):
                    if filename.endswith('_strava.json'):
                        user_id = filename[:-12]  # Remove '_strava.json'
                        token_info = self.get_token_info(user_id)
                        if token_info:
                            users.append(token_info)
        except Exception as e:
            print(f"Error listing users: {e}")
        
        return users
    
    def _get_token_file_path(self, user_id: str) -> str:
        """Get the file path for storing user tokens"""
        safe_user_id = "".join(c for c in user_id if c.isalnum() or c in ('_', '-', '.'))
        return os.path.join(self.tokens_dir, f"{safe_user_id}_strava.json")


# Utility functions for easy integration
def get_strava_token(config, user_id: str) -> str:
    """
    Convenience function to get a valid Strava token
    
    Args:
        config: Configuration object
        user_id: User identifier
        
    Returns:
        str: Valid access token
    """
    auth_manager = StravaAuthManager(config)
    return auth_manager.get_valid_token(user_id)


def setup_new_user(config, user_id: str) -> str:
    """
    Setup OAuth for a new user
    
    Args:
        config: Configuration object  
        user_id: User identifier
        
    Returns:
        str: Access token
    """
    auth_manager = StravaAuthManager(config)
    return auth_manager.initial_oauth_setup(user_id)


if __name__ == "__main__":
    # Test the auth manager
    print("Strava OAuth Manager Test")
    print("=" * 40)
    print("This module handles Strava OAuth authentication.")
    print("Import and use get_strava_token(config, user_id) in your application.")