import pandas as pd

def read_file_csv(path):
    df = pd.read_csv(path)
    return df

def main():
    nasa_data = read_file_csv("data/processed/solar_monthly.csv")
    
    print("===== 5 DÒNG ĐẦU TIÊN =====")
    print(nasa_data.head())

    print("\n===== SỐ DÒNG DỮ LIỆU =====")
    print(len(nasa_data))

    print("\n===== DANH SÁCH CỘT =====")
    print(nasa_data.columns)
    
if __name__ == '__main__':
    main()