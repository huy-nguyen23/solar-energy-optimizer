import requests
from src.config import (
    GEOCODING_USER_AGENT,
    GEOCODING_URL,
    NASA_COMMUNITY,
    NASA_FORMAT,
    NASA_API_URL
)

def geocode_address(address,user_agent=GEOCODING_USER_AGENT):
    """
    Convert an address into latitude and longitude using Nominatim OpenStreetMap API.
    
    Args:
        address (str): The physical address to geocode.
        user_agent (str): The user agent string for the API request.

    Returns:
        tuple: (latitude, longitude) as floats.
        
    Raises:
        RuntimeError: If the API request fails.
        ValueError: If no coordinates are found for the address.
    """
    geo_params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    
    geo_headers = {
        "User-Agent": user_agent
    }
    
    geo_response = requests.get(
        GEOCODING_URL, 
        params=geo_params,
        headers=geo_headers 
    )
    
    if geo_response.status_code != 200:
        raise RuntimeError(f"Failed to geocode address: {geo_response.text}")
    
    geo_data = geo_response.json()
    
    if not geo_data:
        raise ValueError(f"Coordinates not found for address: {address}")
    
    latitude=float(geo_data[0]['lat'])
    longitude=float(geo_data[0]['lon'])
    return latitude,longitude

def fetch_nasa_solar_data(latitude,longitude,start_year,end_year,parameters):
    """
    Fetch monthly NASA POWER data for one or more parameters.
    
    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        start_year (int): The starting year for historical data.
        end_year (int): The ending year for historical data.
        parameters (str): Comma-separated list of NASA parameters to fetch.

    Returns:
        dict: The raw JSON data returned from the NASA POWER API.
        
    Raises:
        RuntimeError: If the API request fails.
    """
    nasa_params = {
        "parameters": parameters,  
        "community": NASA_COMMUNITY,                  
        "latitude": latitude,                
        "longitude": longitude,             
        "start": start_year,                     
        "end": end_year,                        
        "format": NASA_FORMAT                    
    }
    
    nasa_response = requests.get(
        NASA_API_URL, 
        params=nasa_params,
    )

    if nasa_response.status_code != 200:
        raise RuntimeError(f"Failed to fetch data from NASA API: {nasa_response.text}")
    nasa_data = nasa_response.json()
    return nasa_data


    
