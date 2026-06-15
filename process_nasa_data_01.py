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

def main():
    json_data = load_json_file("data/raw/nasa_solar_raw.json")
    
    print("===== KIỂU DỮ LIỆU CỦA DATA =====")
    print(type(json_data))

    print("\n===== CÁC KEY NGOÀI CÙNG =====")
    print(json_data.keys())
    
    monthly_data = get_monthly_solar_data(json_data)

    print("\n===== KIỂU DỮ LIỆU CỦA MONTHLY_DATA =====")
    print(type(monthly_data))

    print("\n===== DỮ LIỆU MONTHLY =====")
    print(monthly_data)

    print("\n===== SỐ THÁNG DỮ LIỆU =====")
    print(len(monthly_data))
    
if __name__ == '__main__':
    main()
