import pandas as pd
import requests
import json
import time
import os

os.makedirs("data/input", exist_ok=True)
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

input_file="data/input/addresses.csv"
addresses_df=pd.read_csv(input_file)

geocoding_url = "https://nominatim.openstreetmap.org/search"

nasa_url = "https://power.larc.nasa.gov/api/temporal/monthly/point"

location_rows=[]

for i,row in addresses_df.iterrows():
    location_name=row['location_name']
    address=row['address']
    start_year=int(row['start_year'])
    end_year=int(row['end_year'])
    
    print("\n========================================")
    print("Location:", location_name)
    print("Address:", address)
    
    geo_params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    
    geo_headers = {
        "User-Agent": "solar-project-student"
    }
    
    geo_response = requests.get(
        geocoding_url, 
        params=geo_params,
        headers=geo_headers 
    )
    
    if geo_response.status_code != 200:
        print("Error calling geocoding API")
        print(geo_response.text)
        continue
    
    geo_data = geo_response.json()
    
    latitude=float(geo_data[0]['lat'])
    longitude=float(geo_data[0]['lon'])
    
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    
    location_rows.append({
       'location_name':location_name,
       'address':address,
       'latitude':latitude,
       'longitude':longitude,
       'start_year':start_year,
       'end_year':end_year
    })
    
    nasa_params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M",  
        "community": "RE",                  
        "latitude": latitude,                
        "longitude": longitude,             
        "start": start_year,                     
        "end": end_year,                        
        "format": "JSON"                    
    }
    
    nasa_response = requests.get(
        nasa_url, 
        params=nasa_params,
    )
    
    print("NASA status code:", nasa_response.status_code)
    print("NASA URL:", nasa_response.url)

    if nasa_response.status_code != 200:
        print("Failed to call NASA API")
        print(nasa_response.text)
        continue
    
    nasa_data = nasa_response.json()
    
    raw_json_path = f"data/raw/nasa_{location_name}_{start_year}_{end_year}.json"
    
    with open(raw_json_path, "w", encoding="utf-8") as file:
        json.dump(nasa_data, file, indent=4, ensure_ascii=False)
        
    print("Raw NASA JSON saved at:", raw_json_path)
    
    time.sleep(1)
locations_df = pd.DataFrame(location_rows)

locations_df.to_csv(
    "data/processed/locations_with_coordinates.csv",
    index=False
)
print("\n===== COMPLETED =====")
print("Coordinates file saved at:")
print("data/processed/locations_with_coordinates.csv")