import requests

websites = [
    "www.AltonMemorialHospital.org",
    "www.BarnesCare.com",
    "www.BarnesJewish.org",
    "www.BarnesJewishWestCounty.org",
    "www.BJC.org",
    "www.BJCBehavioralHealth.org",
    "www.BJCEAP.com",
    "www.BJCHomeCare.org",
    "www.BJCHospice.org",
    "www.BJCMedicalGroup.org",
    "www.BJCSchoolOutreach.org",
    "www.BJCStCharlesCounty.org",
    "www.BJCTotalRewards.org",
    "www.BJSPH.org",
    "www.ChristianHospital.org",
    "www.Epic1.org",
    "www.FoundationBarnesJewish.org",
    "www.MissouriBaptist.org",
    "www.MissouriBaptistSullivan.org",
    "www.MOBapBaby.org",
    "www.MoveByBJC.org",
    "www.ParklandHealthCenter.org",
    "www.progresswest.org",
]

for site in websites:
    url = f"https://{site}/sitemaps"
    
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        continue

    if response.status_code != 200:
        print(f"Website '{site}' has a non-200 status code: {response.status_code}")