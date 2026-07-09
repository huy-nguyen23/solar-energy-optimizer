import json 
import calendar
import pandas as pd
import os

location_name='PTNK'
start_year=2024
end_year=2024

raw_json_path=f"data/raw/nasa_{location_name}_{start_year}_{end_year}.json"
monthly_csv_path=f"data/processed/nasa_{location_name}_monthly.csv"

with open(raw_json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

solar_data=data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
temperature_data=data["properties"]["parameter"]["T2M"]

rows=[]

for month_key, solar_radiation in solar_data.items(): 
    year = int(month_key[:4])  
    month_number = int(month_key[4:6])  
    
    if month_number==13:
        continue
    
    month=f"{year}-{month_number:02d}"
    days_in_month=calendar.monthrange(year,month_number)[1]
    air_temperature=temperature_data[month_key]
    
    row={
        'location_name':location_name,
        'month':month,
        'year':year,
        'month_number':month_number,
        'solar_radiation':solar_radiation,
        'air_temperature':air_temperature,
        'days_in_month':days_in_month
    }
    
    rows.append(row)
    
df=pd.DataFrame(rows)

print("===== PROCESSED NASA DATA TABLE =====")
print(df)

os.makedirs("data/processed", exist_ok=True)
df.to_csv(monthly_csv_path,index=False)

print("\nCSV file saved at:")
print(monthly_csv_path)