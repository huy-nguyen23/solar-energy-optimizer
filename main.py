import requests
url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
params = {
    "parameters": "ALLSKY_SFC_SW_DWN",
    "community":  "RE",
    "latitude":   40.7128,
    "longitude":  -74.0060,
    "start":      2010,
    "end":        2024,
    "format":     "JSON"
}

response = requests.get(url, params=params)
data= response.json()
monthly=data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
avg=sum(monthly.values())/len(monthly.values())
print(f"Buc Xa TB: {avg:.2f} kWh/m^2/ngay")