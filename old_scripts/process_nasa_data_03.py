import json
import os
import pandas as pd

def load_json_file(path):
    # Đọc file JSON đã lưu từ bài trước
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def get_monthly_solar_data(data):
    # Lấy dữ liệu bức xạ mặt trời theo tháng
    monthly_data = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    return monthly_data

def save_csv(df):
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/solar_monthly.csv", index=False, encoding="utf-8")
    
def parse_month_key(month_key):
    year_text = month_key[:4] 
    month_text = month_key[4:6]  
    year = int(year_text)  
    month_number = int(month_text)  
    return year, month_number

def convert_monthly_data_to_dataframe(monthly_data):
    rows = []
    for month_key, value in monthly_data.items():
        year, month_number = parse_month_key(month_key)
        row = {
            "month": month_key,
            "year": year,
            "month_number": month_number,
            "solar_radiation": value
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    save_csv(df)

def main():
    json_data = load_json_file("data/raw/nasa_solar_raw.json")
    monthly_data = get_monthly_solar_data(json_data)
    convert_monthly_data_to_dataframe(monthly_data)
    print("Đã lưu file: data/processed/solar_monthly.csv")
    
if __name__ == '__main__':
    main()
    