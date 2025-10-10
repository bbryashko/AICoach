import requests
import certifi
import json

proxies = {
    "http": "http://b2b-http.dhl.com:8080",
    "https": "http://b2b-http.dhl.com:8080",
}

token = "97dd1f5609836c695a40b6af01f4b75bc839196d"
url = "https://www.strava.com/api/v3/athlete/activities"


headers = {"Authorization": f"Bearer {token}"}
# response = requests.get(url, headers=headers, proxies=proxies, verify=False)  # ignore SSL for now

response = requests.get(url, headers=headers, verify=False)  # ignore SSL for now

print(response.status_code)
data = response.json()
#print(response.text[:500])  # first 500 chars
#print(response.json())

print(json.dumps(data, indent=4))
