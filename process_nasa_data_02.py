import json # Import thư viện json để đọc file JSON

with open("data/raw/nasa_solar_raw.json", "r", encoding="utf-8") as file: # Mở file JSON đã lưu
    data = json.load(file) # Đọc nội dung file JSON thành dictionary Python

monthly_data = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"] # Lấy phần dữ liệu bức xạ theo tháng

print("===== TÁCH YEAR VÀ MONTH_NUMBER =====") # In tiêu đề chương trình

for month_key, value in monthly_data.items(): # Duyệt từng cặp key-value trong monthly_data
    year_text = month_key[:4] # Lấy 4 ký tự đầu của key, ví dụ "202401" -> "2024"
    month_text = month_key[4:6] # Lấy 2 ký tự tiếp theo, ví dụ "202401" -> "01"
    
    year = int(year_text) # Chuyển year từ chuỗi sang số nguyên
    month_number = int(month_text) # Chuyển month từ chuỗi sang số nguyên
   
    print(month_key, "-> year =", year, ", month_number =", month_number, ", value =", value) # In kết quả tách được