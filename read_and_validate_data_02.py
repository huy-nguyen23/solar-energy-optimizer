import pandas as pd

def read_file_csv(path):
    df = pd.read_csv(path)
    return df

def get_monthly_data(df):
    monthly_df = df[(df["month_number"] >= 1) & (df["month_number"] <= 12)]
    return monthly_df

def check_full_month(monthly_df):
    if len(monthly_df) == 12:
        return True
    else:
        return False

def get_missing_count(monthly_df):
    missing_count = monthly_df["solar_radiation"].isna().sum()
    return missing_count
        
def check_missing_values(missing_count):  
    if missing_count == 0:
        return False
    else: 
        return True
        
def get_avg_solar_radiation(monthly_df):
    avg = monthly_df["solar_radiation"].mean()
    return avg
    
def main():
    nasa_data = read_file_csv("data/processed/solar_monthly.csv")
    
    print("===== CSV DATA =====")
    print(nasa_data)
    
    
    monthly_df = get_monthly_data(nasa_data)
    print("\n===== 1. CHECK IF THE DATA HAS 12 MONTHS =====")
    if check_full_month(monthly_df):
        print("The data has all 12 monthly records.")
    else:
        print("The data does not have exactly 12 monthly records.")
        print("Number of monthly records found:", len(monthly_df))
    

    missing_count = get_missing_count(monthly_df)
    print("\n===== 2. CHECK MISSING VALUES IN SOLAR_RADIATION =====")
    if check_missing_values(missing_count):
        print("Missing values found in the solar_radiation column.")
        print("Number of missing values:", missing_count)
    else:
        print("No missing values found in the solar_radiation column.")
        
    
    print("\n===== 3. CALCULATE AVERAGE SOLAR_RADIATION =====")
    avg = get_avg_solar_radiation(monthly_df)
    print(f"Average solar radiation from 12 months: {avg:.2f} kWh/m²/day")


    print("\n===== 4. FINAL VALIDATION RESULT =====")
    if len(monthly_df) == 12 and missing_count == 0:
        print("The 12-month data is valid. It can be used for the web application.")
    else:
        print("The 12-month data is not valid. Please check the data before using it.")
    
if __name__ == '__main__':
    main()