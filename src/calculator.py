import pandas as pd
from src.config import (
    SYSTEM_SIZES,
    DEFAULT_PR,
    TEMPERATURE_COEFFICIENT,
    INVERTER_FACTOR,
    SOILING_FACTOR,
    WIRING_FACTOR,
    AVAILABILITY_FACTOR,
    SHADING_FACTOR
)

def calculate_temperature_loss_factor(
    air_temperature,
    temperature_coefficient=TEMPERATURE_COEFFICIENT,
    inverter_factor=INVERTER_FACTOR,
    soiling_factor=SOILING_FACTOR,
    wiring_factor=WIRING_FACTOR,
    shading_factor=SHADING_FACTOR,
    availability_factor=AVAILABILITY_FACTOR
):
    cell_temperature=air_temperature+25
        
    temperature_factor=1+temperature_coefficient*(cell_temperature-25)
        
    loss_factor=temperature_factor*shading_factor*wiring_factor*soiling_factor*inverter_factor*availability_factor
    
    return cell_temperature,temperature_factor,loss_factor

def calculate_generation_kwh(system_kwp,solar_radiation,days_in_month,efficiency_factor):
    return efficiency_factor*system_kwp*days_in_month*solar_radiation

def calculate_all_systems_advanced(monthly_df,system_sizes=SYSTEM_SIZES):
    rows=[]

    for i,row in monthly_df.iterrows():
        month=row['month']
        year=row['year']
        month_number=row['month_number']
        solar_radiation=row['solar_radiation']
        air_temperature=row['air_temperature']
        days_in_month=row["days_in_month"]
        location_name=row["location_name"]
       
        cell_temperature,temperature_factor,loss_factor=calculate_temperature_loss_factor(air_temperature)
        
        for system_kwp in system_sizes:
            generation_kwh=calculate_generation_kwh(system_kwp,solar_radiation,days_in_month,loss_factor)
            
            rows.append({
                "location_name":location_name,
                "month":month,
                "year":year,
                "month_number":month_number,
                "solar_radiation":solar_radiation,
                "air_temperature":air_temperature,
                "cell_temperature":round(cell_temperature,2),
                "days_in_month":days_in_month,
                "system_kwp":system_kwp,
                "temperature_factor":round(temperature_factor,4),
                "loss_factor":round(loss_factor,4),
                "generation_kwh":round(generation_kwh,2)
            })
            
    result_df=pd.DataFrame(rows)
    return result_df