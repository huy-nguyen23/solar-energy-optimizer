import requests
url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
params = {
    "parameters": "ALLSKY_SFC_SW_DWN",
    "community":  "RE",
    "latitude":   10.763836,
    "longitude":  -106.666068,
    "start":      2010,
    "end":        2010,
    "format":     "JSON"
}

response = requests.get(url, params=params)
data= response.json()
monthly=data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
