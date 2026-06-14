import os
import pandas as pd
import requests

try:
    # ===== 1. KIỂM TRA FILE CSV CÓ TỒN TẠI KHÔNG =====
    file_path = "data\processed\solar_monthly.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError("File CSV chưa tồn tại. Hãy chạy file process_nasa_data_03.py trước.")

    # ===== 2. ĐỌC FILE CSV =====
    df = pd.read_csv(file_path)

    print("===== 5 DÒNG ĐẦU TIÊN =====")
    print(df.head())

    print("\n===== SỐ DÒNG DỮ LIỆU =====")
    print(len(df))

    print("\n===== DANH SÁCH CỘT =====")
    print(df.columns)

    # ===== 3. KIỂM TRA LATITUDE VÀ LONGITUDE =====
    latitude = 10.8231
    longitude = 106.6297

    if latitude < -90 or latitude > 90:
        raise ValueError("Latitude không hợp lệ. Latitude phải nằm trong khoảng [-90, 90].")

    if longitude < -180 or longitude > 180:
        raise ValueError("Longitude không hợp lệ. Longitude phải nằm trong khoảng [-180, 180].")

    # ===== 4. GỌI NASA API =====
    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"

    params = {
        "parameters": "ALLSKY_SFC_SW_DWN",
        "community": "RE",
        "latitude": latitude,
        "longitude": longitude,
        "start": 2024,
        "end": 2024,
        "format": "JSON"
    }

    response = requests.get(url, params=params)

    # ===== 5. KIỂM TRA NASA API CÓ TRẢ VỀ THÀNH CÔNG KHÔNG =====
    if response.status_code != 200:
        raise Exception(f"Gọi NASA API thất bại. Status code: {response.status_code}")

    data = response.json()

    print("\n===== GỌI NASA API THÀNH CÔNG =====")
    print("Status code:", response.status_code)
    print("URL:", response.url)

except FileNotFoundError as error:
    print("LỖI FILE:")
    print(error)

except ValueError as error:
    print("LỖI DỮ LIỆU NHẬP:")
    print(error)

except requests.exceptions.RequestException as error:
    print("LỖI KẾT NỐI HOẶC REQUEST:")
    print(error)

except Exception as error:
    print("LỖI KHÁC:")
    print(error)