import pandas as pd

from src.calculator import calculate_all_systems_advanced,build_generation_summary,compare_model_with_survey

from src.processing import convert_power_data_to_monthly_dataframe

from src import config

from src.financial import build_financial_input,build_self_used_energy,build_financial_summary,compare_battery_options,recommend_test_option

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
    
    # ========================================================
    # 5. Summarize average generation by system size
    # ========================================================
    print_section("5. Summarize average generation by system size")
    
    summary_df=build_generation_summary(generation_df,location_name)
    save_csv_file(summary_df,config.GENERATION_SUMMARY_CSV_PATH)
    
    print(summary_df)
    
    # ========================================================
    # 6. Compare the model with real-world survey data
    # ========================================================
    print_section("6. Compare the model with real-world survey data")
    
    comparison_df=compare_model_with_survey(generation_df,location_name,config.SURVEY_RANGES)
    save_csv_file(comparison_df,config.MODEL_VS_SURVEY_CSV_PATH)
    
    print(comparison_df)
    
    # ========================================================
    # 7. Estimate household electricity consumption
    # ========================================================
    print_section("7. Estimate household electricity consumption")
    
    financial_df=build_financial_input(location_name,config.MONTHLY_BILL_VND,config.VAT_RATE,config.ELECTRICITY_TIERS)
    save_csv_file(financial_df,config.FINANCIAL_INPUT_CSV_PATH)
    
    print(financial_df)
    
    # ========================================================
    # 8. Calculate self-used solar energy
    # ========================================================
    print_section("8. Calculate self-used solar energy")
    
    self_used_energy_df=build_self_used_energy(summary_df,financial_df,location_name,config.GRID_TIED_SELF_CONSUMPTION_RATIO)
    save_csv_file(self_used_energy_df,config.SELF_USED_ENERGY_PATH)
    
    print(self_used_energy_df)
    
    # ========================================================
    # 9. Calculate savings and payback period
    # ========================================================
    print_section("9. Calculate savings and payback period")
    
    financial_summary_df=build_financial_summary(self_used_energy_df,financial_df,location_name,config.GRID_TIED_COST_RANGES,config.ROOF_AREA_RANGES)
    save_csv_file(financial_summary_df,config.FINANCIAL_SUMMARY_PATH)
    
    print(financial_summary_df)
    
    # ========================================================
    # 10. Compare battery and no-battery options
    # ========================================================
    print_section("10. Compare battery and no-battery options")
    
    battery_option_df=compare_battery_options(summary_df,financial_df,location_name)
    save_csv_file(battery_option_df,config.BATTERY_OPTION_CSV_PATH)
    
    print(battery_option_df)
    
    # ========================================================
    # 11. Recommend the best solar option
    # ========================================================
    print_section("11. Recommend the best solar option")
    
    recommended_df=recommend_test_option(battery_option_df,config.MIN_GENERATION_RATIO,config.MAX_PAYBACK_YEARS)
    save_csv_file(recommended_df,config.RECOMMENDED_SYSTEM_CSV_PATH)
    
    print(recommended_df)
    
    # ========================================================
    # 12. Print final conclusion
    # ========================================================
    print_section("12. Final conclusion")
    
    recommended = recommended_df.iloc[0]
    
    print("Location:", recommended["location_name"])
    print("Recommended system:", recommended["system_kwp"], "kWp")
    print("Recommended option:", recommended["option_description"])
    print("Investment cost:", f"{recommended['investment_cost']:,.0f}", "VNĐ")
    print("Average generation/month:", recommended["monthly_avg_generation_kwh"], "kWh")
    print("Self-used electricity/month:", recommended["self_used_kwh"], "kWh")
    print("Savings/month:", f"{recommended['monthly_saving']:,.0f}", "VNĐ")
    print("Savings/year:", f"{recommended['annual_saving']:,.0f}", "VNĐ")
    print("Payback:", recommended["payback_years"], "years")
    print("Reason:",  recommended["recommendation_reason"])
    
if __name__=="__main__":
    main()

