import requests
from requests.structures import CaseInsensitiveDict

url = "https://api.geoapify.com/v1/geocode/autocomplete?text=71 ST. NICHOLAS DRIVE&apiKey=42af86479ba04af69c0f993b9568f130"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

resp = requests.get(url, headers=headers)

print(resp.content)


