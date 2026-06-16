import pandas as pd
from src.config import PARAMETER

def get_monthly_solar_data(nasa_data):
    """
    Extract monthly solar radiation data from a NASA API response. 
    Args: 
        nasa_data (dict): The NASA API response as a Python dictionary. 
    Returns: 
        dict: Monthly solar radiation data with month keys in YYYYMM format.
    """
    monthly_data = nasa_data["properties"]["parameter"][PARAMETER]
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


def convert_monthly_data_to_dataframe(monthly_solar_data):
    """
    Convert monthly solar radiation data into a pandas DataFrame. 
    Args: 
        monthly_solar_data (dict): Monthly solar radiation data from NASA. 
    Returns: 
        pandas.DataFrame: A DataFrame with month, year, month_number, and solar_radiation columns.
    """
    rows = []
    for month_key, value in monthly_solar_data.items():
        year, month_number = parse_month_key(month_key)
        row = {
            "month": month_key,
            "year": year,
            "month_number": month_number,
            "solar_radiation": value
        }
        rows.append(row)
    solar_df = pd.DataFrame(rows)
    return solar_df