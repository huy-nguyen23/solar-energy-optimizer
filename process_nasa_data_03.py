import json


with open("data/raw/nasa_solar_raw.json", "r", encoding="utf-8") as file:
    data = json.load(file)


monthly_data = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]

print("===== TÁCH YEAR VÀ MONTH_NUMBER TỪ KEY =====")

for key, value in monthly_data.items():

  
    year = int(key[:4])
    month_number = int(key[4:])
    month=f"{year}-{month_number:02d}"
 
    if month_number == 13:
        print(f"{key} -> bỏ qua vì đây là dữ liệu tổng hợp năm")
    else:
        print(
            f"{key} -> year = {year}, "
            f"month_number = {month_number}, "
            f"số bức xạ : {value:.2f} kWh/m²/ngày"
        )
        
rows={
        "month":month,
        "year":year,
        "month_number":month_number,
        "solar_radiation":value
    }
rows.append(rows)
df=pd.DataFrame(rows)
print("===== DATAFRAME =====")
    