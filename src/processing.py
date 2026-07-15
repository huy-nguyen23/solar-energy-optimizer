import pandas as pd
import calendar
from src.config import SOLAR_PARAMETER,TEMPERATURE_PARAMETER

def get_monthly_parameter_data(nasa_data,parameter):
    """
    Extract one monthly parameter dictionary from a NASA API response.

    Example parameters:
    - ALLSKY_SFC_SW_DWN: solar radiation
    - T2M: air temperature
    """
    monthly_data = nasa_data["properties"]["parameter"][parameter]
    return monthly_data


def parse_month_key(month_key):
    """
    Convert a NASA month key in YYYYMM format into year and month number. 
    Args: 
        month_key (str): A month key in YYYYMM format, such as "202401". 
    Returns: 
        tuple: A tuple containing the year and month number.
    """
    year_text = month_key[:4] 
    month_text = month_key[4:6]  
    year = int(year_text)  
    month_number = int(month_text)  
    return year, month_number

def convert_power_data_to_monthly_dataframe(nasa_data, location_name):
    """
    Convert NASA solar and temperature data into the monthly model input DataFrame.

    Args:
        nasa_data (dict): The full JSON response from the NASA API.
        location_name (str): The name of the location being analyzed.

    Returns:
        pd.DataFrame: A DataFrame containing monthly solar radiation, temperature, and days in month.
    """
    solar_data=get_monthly_parameter_data(nasa_data,SOLAR_PARAMETER)
    temperature_data=get_monthly_parameter_data(nasa_data,TEMPERATURE_PARAMETER)
    rows=[]

    for month_key, solar_radiation in solar_data.items(): 
        year, month_number=parse_month_key(month_key)
        
        if month_number==13:
            continue
        
        month=f"{year}-{month_number:02d}"
        days_in_month=calendar.monthrange(year,month_number)[1]
        air_temperature=temperature_data[month_key]
        
        row={
            'location_name':location_name,
            'month':month,
            'year':year,
            'month_number':month_number,
            'solar_radiation':solar_radiation,
            'air_temperature':air_temperature,
            'days_in_month':days_in_month
        }
        
        rows.append(row)

    df=pd.DataFrame(rows)
    return df


