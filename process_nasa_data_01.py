import json

with open("data/raw/nasa_solar_raw.json","r",encoding="utf-8") as file:
    data=json.load(file)
    
print("===== KIỂU DỮ LIỆU CỦA DATA =====")
print(type(data))

print("\n===== CÁC KEY NGOÀI CÙNG =====")
print(data.keys())

monthly_data=data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]

print("\n===== KIỂU DỮ LIỆU CỦA MONTHLY_DATA =====")
print(type(monthly_data))

print("\n===== DỮ LIỆU MONTHLY =====")
print(monthly_data)

print("\n===== SỐ THÁNG DỮ LIỆU =====")
print(len(monthly_data))
