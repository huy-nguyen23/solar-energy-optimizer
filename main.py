import pandas as pd

from src.calculator import calculate_all_systems_advanced

from src.processing import convert_power_data_to_monthly_dataframe

from src import config

from src.api import(
    geocode_address,
    fetch_nasa_solar_data
)

from src.utils import(
    ensure_directories,
    print_section,
    save_csv_file,
    save_json_file,
    load_json_file
)

def main():
    ensure_directories(config.INPUT_DIR,config.RAW_DIR,config.PROCESSED_DIR)
    
    location_name=config.LOCATION_NAME
    start_year=config.START_YEAR
    end_year=config.END_YEAR
    refresh_nasa_data = getattr(config, "REFRESH_NASA_DATA", False)
    
    print_section("SOLAR-ENERGY OPTIMIZER")

    print("Location name:", location_name)
    print("Start year:", start_year)
    print("End year:", end_year)
    
    # ========================================================
    # 1. Prepare location information
    # ========================================================
    print_section("1. Prepare location information")
    
    address=config.ADDRESS
    
    latitude,longitude=geocode_address(address)
    
    location_df=pd.DataFrame([
        {
            "location_name":location_name,
            "address":address,
            "latitude":latitude,
            "longitude":longitude,
            "start_year":start_year,
            "end_year":end_year
        }
    ])
    
    save_csv_file(location_df,config.LOCATION_WITH_COORDINATES_CSV_PATH)
    
    print(location_df)
    
    # ========================================================
    # 2. Fetch NASA POWER data
    # ========================================================
    print_section("2. Fetch NASA POWER data")
    
    if refresh_nasa_data or not config.NASA_RAW_JSON_PATH.exists():
        print("Calling NASA POWER API...")
       
        nasa_data=fetch_nasa_solar_data(latitude,longitude,start_year,end_year,config.NASA_PARAMETERS)
        save_json_file(nasa_data,config.NASA_RAW_JSON_PATH)
        
        print("New NASA data has been downloaded.")
    else:
        print("NASA data already exists in data/raw.")
        print("Using file:", config.NASA_RAW_JSON_PATH)
        
        nasa_data=load_json_file(config.NASA_RAW_JSON_PATH)
        
    # ========================================================
    # 3. Convert NASA data into monthly weather table
    # ========================================================
    print_section("3. Convert NASA data into monthly weather table")
    
    monthly_df=convert_power_data_to_monthly_dataframe(nasa_data, location_name)
    save_csv_file(monthly_df,config.NASA_MONTHLY_CSV_PATH)
    
    print(monthly_df)
    
    # ========================================================
    # 4. Simulate solar power generation
    # ========================================================
    print_section("4. Simulate solar power generation")
    
    generation_df=calculate_all_systems_advanced(monthly_df,system_sizes=config.SYSTEM_SIZES)
    save_csv_file(generation_df,config.GENERATION_ADVANCED_CSV_PATH)
    
    print(generation_df)
    
if __name__=="__main__":
    main()

