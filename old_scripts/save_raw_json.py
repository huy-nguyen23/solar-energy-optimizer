import requests
import json
import os

# URL API NASA POWER lấy dữ liệu theo tháng tại một điểm
url = "https://power.larc.nasa.gov/api/temporal/monthly/point"

# Các tham số gửi lên NASA API
params = {
    "parameters": "ALLSKY_SFC_SW_DWN",  # Dữ liệu bức xạ mặt trời
    "community": "RE",                  # Nhóm Renewable Energy
    "latitude": 10.8231,                # Vĩ độ
    "longitude": 106.6297,              # Kinh độ
    "start": 2024,                      # Năm bắt đầu
    "end": 2024,                        # Năm kết thúc
    "format": "JSON"                    # Định dạng dữ liệu trả về
}

# Gọi API NASA
response = requests.get(url, params=params)

# In status code để biết gọi API thành công hay lỗi
print("Status code:", response.status_code)

# In URL thật đã gửi lên NASA
print("URL:", response.url)

# Nếu gọi API thất bại thì dừng chương trình
if response.status_code != 200:
    print("Gọi NASA API thất bại")
    print(response.text)
    exit()

# Chuyển dữ liệu JSON NASA trả về thành dict Python
data = response.json()

# Tạo thư mục data/raw nếu chưa có
os.makedirs("data/raw", exist_ok=True)

# Lưu dữ liệu gốc vào file JSON
with open("data/raw/nasa_solar_raw.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

# Thông báo lưu thành công
print("Đã lưu file: data/raw/nasa_solar_raw.json")