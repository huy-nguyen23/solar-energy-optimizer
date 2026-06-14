import json
import os
import pandas as pd

with open("data/raw/nasa_solar_raw.json", "r", encoding="utf-8") as file:
    data = json.load(file)

monthly_data = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]

rows = []

for month_key, value in monthly_data.items():
    year = int(month_key[:4])
    month_number = int(month_key[4:6])

    row = {
        "month": month_key,
        "year": year,
        "month_number": month_number,
        "solar_radiation": value
    }

    rows.append(row)
    
df = pd.DataFrame(rows)

os.makedirs("data/processed", exist_ok=True)

df.to_csv("data/processed/solar_monthly.csv", index=False, encoding="utf-8")

print("Đã lưu file: data/processed/solar_monthly.csv")
print(df)
    