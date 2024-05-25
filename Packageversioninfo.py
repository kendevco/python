import requests

def get_latest_version(package_name):
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    data = response.json()
    return data["info"]["version"]

print(get_latest_version("whisper"))