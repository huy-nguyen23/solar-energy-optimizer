import requests
from src.config import NASA_API_URL,COMMUNITY,PARAMETER,FORMAT

def fetch_nasa_solar_data(latitude,longitude,start_year,end_year):
    '''
    Fetch monthly solar radiation data from the NASA POWER API.
    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        start_year (int): The first year of the data range.
        end_year (int): The last year of the data range.
    Returns:
        dict: The NASA API response converted from JSON into a Python dictionary.
    Raises:
        Exception: If the API request is not successful.
    '''
    params = {
        "parameters": PARAMETER,  
        "community": COMMUNITY,                  
        "latitude": latitude,               
        "longitude": longitude,              
        "start": start_year,                      
        "end": end_year,                        
        "format": FORMAT                  
    }
    response = requests.get(NASA_API_URL, params=params)
    if response.status_code!=200:
        raise Exception('Failed to fetch data from NASA API.')
    return response.json()
    
