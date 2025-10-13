import requests
import certifi
import json
import os

# Load token and URL from environment variables for security
token = os.getenv('STRAVA_TOKEN', '774e677f73fa4b58e17bf195ae40f153cff55ccc')
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
