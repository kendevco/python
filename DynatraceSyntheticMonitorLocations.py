import requests
import json

API_URL_LOCATIONS = "https://zlx31990.live.dynatrace.com/api/v1/synthetic/locations"
API_KEY = "dt0c01.DF2ZFTMNGC4RLKAUBZPSBQCF.IG3WW2V7FQMLWFKYFX7CMC6EEHKFE6NVKUH5ZZ42MSAUMTIHYYIOAJBGXC77VBPA"

headers = {
    "Authorization": f"Api-Token {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.get(API_URL_LOCATIONS, headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)
    locations = data['locations']
    print("All Synthetic Monitor Locations:")
    for location in locations:
        print(f"ID: {location['entityId']}, Name: {location['name']}, Type: {location['type']}, Cloud: {location.get('cloudPlatform', 'N/A')}")
else:
    print("Error fetching locations:", response.text)