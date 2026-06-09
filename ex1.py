def coordinates(latitude,longitude):
    import requests
    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN",
        "community":  "RE",
        "latitude":   latitude,
        "longitude":  longitude,
        "start":      2010,
        "end":        2024,
        "format":     "JSON"
    }

    response = requests.get(url, params=params)
    data= response.json()
    monthly=data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    avg=sum(monthly.values())/len(monthly.values())
    print(f"Buc Xa TB: {avg:.2f} kWh/m^2/ngay")
coordinates(10.763445, 106.677559) # PTNK HighSchool
coordinates(10.767907, 106.703273) # My House
coordinates(40.712776, -74.005974) # New York