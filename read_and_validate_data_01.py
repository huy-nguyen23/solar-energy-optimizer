import pandas as pd

df = pd.read_csv("data/processed/solar_monthly.csv")

print("===== 5 DÒNG ĐẦU TIÊN =====")
print(df.head())

print("\n===== SỐ DÒNG DỮ LIỆU =====")
print(len(df))

print("\n===== DANH SÁCH CỘT =====")
print(df.columns)