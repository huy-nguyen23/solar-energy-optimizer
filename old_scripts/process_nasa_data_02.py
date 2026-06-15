import json  

def load_json_file(path):
    # Đọc file JSON đã lưu từ bài trước
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def get_monthly_solar_data(data):
    # Lấy dữ liệu bức xạ mặt trời theo tháng
    monthly_data = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    return monthly_data

def parse_month_key(month_key):
    year_text = month_key[:4] 
    month_text = month_key[4:6]  
    year = int(year_text)  
    month_number = int(month_text)  
    return year, month_number

def main():
    json_data = load_json_file("data/raw/nasa_solar_raw.json")
    
    monthly_data = get_monthly_solar_data(json_data)
    
    print("===== TÁCH YEAR VÀ MONTH_NUMBER =====")  

    for month_key, value in monthly_data.items(): 
        year,month_number = parse_month_key(month_key)
        print(month_key, "-> year =", year, ", month_number =", month_number, ", value =", value)  
    
if __name__ == '__main__':
    main()