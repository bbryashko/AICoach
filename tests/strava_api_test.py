import requests
import certifi
import json
import os

# Load .env file from parent directory
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load environment variables from .env file
load_env()

# Load token and URL from environment variables for security
token = os.getenv('STRAVA_TOKEN')
if not token:
    print("❌ STRAVA_TOKEN environment variable not set!")
    print("Please set your token in the .env file or as an environment variable.")
    exit(1)
base_url = os.getenv('STRAVA_BASE_URL', 'https://www.strava.com/api/v3')

proxies = {
    "http": "http://b2b-http.dhl.com:8080",
    "https": "http://b2b-http.dhl.com:8080",
}

url = f"{base_url}/athlete/activities"


headers = {"Authorization": f"Bearer {token}"}
# response = requests.get(url, headers=headers, proxies=proxies, verify=False)  # ignore SSL for now

response = requests.get(url, headers=headers, verify=False)  # ignore SSL for now

print(response.status_code)
data = response.json()
#print(response.text[:500])  # first 500 chars
#print(response.json())

print(json.dumps(data, indent=4))
