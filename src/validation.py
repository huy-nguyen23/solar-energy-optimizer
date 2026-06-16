def validate_coordinates(latitude,longitude):
    """ 
    Validate latitude and longitude values. 
    Args: 
        latitude (float): The latitude of the location. 
        longitude (float): The longitude of the location. 
    Raises: 
        ValueError: If latitude is not between -90 and 90, or longitude is not between -180 and 180. 
    """
    if latitude < -90 or latitude > 90:
        raise ValueError("Latitude must be between -90 and 90.")

    if longitude < -180 or longitude > 180:
        raise ValueError("Longitude must be between -180 and 180.")


def check_number_of_months(df,expected_months):
    """ 
    Check whether the DataFrame has the expected number of months. 
    Args: 
        df (pandas.DataFrame): The solar radiation DataFrame. 
        expected_months (int): The expected number of months. 
    Returns: 
        bool: True if the DataFrame has the expected number of rows, otherwise False. 
    """
    return len(df)==expected_months


def check_missing_solar_radiation(df):
    """ 
    Check whether the solar_radiation column has missing values. 
    Args: 
        df (pandas.DataFrame): The solar radiation DataFrame. 
    Returns: 
        bool: True if there are no missing values in the solar_radiation column, otherwise False. 
    """
    return df.solar_radiation.isnull().sum()==0


def calculate_average_solar_radiation(df):
    """ 
    Calculate the average solar radiation value. 
    Args: 
        df (pandas.DataFrame): The solar radiation DataFrame. 
    Returns: 
        float: The average value of the solar_radiation column. 
    """
    return df.solar_radiation.mean()