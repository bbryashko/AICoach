"""
Strava Token Helper
This script helps you get and test Strava API tokens properly.
"""

import requests
import json
from datetime import datetime

def test_token(token):
    """
    Test if a Strava token is valid
    """
    url = "https://www.strava.com/api/v3/athlete"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, verify=False)
        
        if response.status_code == 200:
            athlete_data = response.json()
            print("✅ Token is VALID!")
            print(f"   Athlete: {athlete_data.get('firstname', '')} {athlete_data.get('lastname', '')}")
            print(f"   ID: {athlete_data.get('id', 'N/A')}")
            print(f"   Location: {athlete_data.get('city', 'N/A')}, {athlete_data.get('country', 'N/A')}")
            return True
        else:
            print("❌ Token is INVALID!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False

def get_activities_with_token(token, limit=3):
    """
    Try to get activities with the token
    """
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"per_page": limit}
    
    try:
        response = requests.get(url, headers=headers, params=params, verify=False)
        
        if response.status_code == 200:
            activities = response.json()
            print(f"✅ Successfully fetched {len(activities)} activities!")
            
            for i, activity in enumerate(activities, 1):
                name = activity.get('name', 'Unnamed')
                activity_type = activity.get('type', 'Unknown')
                distance = activity.get('distance', 0) / 1000  # Convert to km
                date = activity.get('start_date_local', '')[:10]  # Just the date part
                
                print(f"   {i}. {name} ({activity_type}) - {distance:.1f}km on {date}")
            
            return activities
        else:
            print("❌ Failed to fetch activities!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching activities: {e}")
        return []

def show_token_guide():
    """
    Show instructions for getting a proper Strava token
    """
    print("🔑 HOW TO GET A PROPER STRAVA TOKEN")
    print("=" * 50)
    print()
    print("Method 1: Quick Access Token (Easy, but expires in 6 hours)")
    print("1. Go to https://www.strava.com/settings/api")
    print("2. Click 'Create & View Your Access Token'")
    print("3. Copy the 'Your Access Token' value")
    print("4. This token expires in 6 hours")
    print()
    print("Method 2: OAuth Application (Permanent)")
    print("1. Go to https://www.strava.com/settings/api")
    print("2. Create an application:")
    print("   - Application Name: 'My AI Coach'")
    print("   - Category: 'Training'")
    print("   - Website: http://localhost")
    print("   - Authorization Callback Domain: localhost")
    print("3. Note your Client ID and Client Secret")
    print("4. Use OAuth flow to get a long-term token")
    print()
    print("Method 3: Manual OAuth (Quick test)")
    print("Replace YOUR_CLIENT_ID with your actual Client ID:")
    print("https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=read,activity:read_all")
    print()
    print("Required Scopes for AI Coach:")
    print("- read: Basic profile info")
    print("- activity:read_all: Access to all activities")

def main():
    """
    Main token testing function
    """
    print("🤖 STRAVA TOKEN HELPER")
    print("=" * 30)
    
    # Test current token
    current_token = "0d1b3b9104bd60ff5fecdc520f662e011a71588b"
    print(f"🔍 Testing current token: {current_token[:10]}...")
    
    if test_token(current_token):
        print("\n📱 Fetching recent activities...")
        activities = get_activities_with_token(current_token)
        
        if activities:
            print("\n🎉 Your token is working perfectly!")
            print("You can now use the AI Coach features!")
        else:
            print("\n⚠️  Token works for profile but not activities.")
            print("You might need additional scopes.")
    else:
        print("\n💡 Your token needs to be refreshed or recreated.")
        show_token_guide()
    
    print("\n" + "=" * 50)
    print("💡 TIP: Strava tokens expire regularly.")
    print("If you get 401 errors, generate a new token.")

if __name__ == "__main__":
    main()