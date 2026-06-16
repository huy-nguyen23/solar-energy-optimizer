from src.nasa_api import fetch_nasa_solar_data
from src.config import LATITUDE,LONGITUDE,START_YEAR,END_YEAR,RAW_JSON_PATH,PROCESSED_CSV_PATH
from src.data_io import save_json_file,load_json_file,save_csv_file,load_csv_file
from src.processing import get_monthly_solar_data,convert_monthly_data_to_dataframe
from src.validation import check_number_of_months,check_missing_solar_radiation,calculate_average_solar_radiation,validate_coordinates

def main():
    """ 
    Run the full solar energy data processing pipeline. 
   
    This function validates the coordinates, fetches NASA solar radiation data, 
    saves the raw JSON file, processes the monthly solar data, saves the 
    processed CSV file, and prints basic validation results. 
    """
    validate_coordinates(LATITUDE,LONGITUDE)
    nasa_data=fetch_nasa_solar_data(LATITUDE,LONGITUDE,START_YEAR,END_YEAR)
    save_json_file(nasa_data,RAW_JSON_PATH)
    
    loaded_nasa_data=load_json_file(RAW_JSON_PATH)
    monthly_data=get_monthly_solar_data(loaded_nasa_data)
    solar_df=convert_monthly_data_to_dataframe(monthly_data)
    save_csv_file(solar_df,PROCESSED_CSV_PATH)
   
    loaded_solar_df=load_csv_file(PROCESSED_CSV_PATH)
    
    if check_number_of_months(loaded_solar_df, 12):
        print("The data has enough 12 monthly records.")
    else:
        print("The data does not have enough 12 monthly records.")
        
    if check_missing_solar_radiation(loaded_solar_df):
        print("No missing values found in the solar_radiation column.")
    else:
        print("Missing values found in the solar_radiation column.")
        
    print(f"Average solar radiation: {calculate_average_solar_radiation(loaded_solar_df):.2f}")

if __name__ == "__main__": 
    main()