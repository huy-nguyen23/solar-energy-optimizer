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
    """
    Estimate total loss factor using temperature and fixed system losses.

    cell_temperature = air_temperature + 25
    temperature_factor = 1 + temperature_coefficient * (cell_temperature - 25)

    The final loss_factor combines:
    - temperature loss
    - inverter loss
    - soiling loss
    - wiring loss
    - shading loss
    - availability loss
    """
    cell_temperature=air_temperature+25
        
    temperature_factor=1+temperature_coefficient*(cell_temperature-25)
        
    loss_factor=temperature_factor*shading_factor*wiring_factor*soiling_factor*inverter_factor*availability_factor
    
    return cell_temperature,temperature_factor,loss_factor

def calculate_generation_kwh(system_kwp,solar_radiation,days_in_month,efficiency_factor):
    """
    Calculate monthly solar generation in kWh.

    Formula:
    generation_kwh = system_kwp * solar_radiation * days_in_month * efficiency_factor
    
    Args:
        system_kwp (float): The capacity of the solar system in kWp.
        solar_radiation (float): Daily solar radiation (kWh/m²/day).
        days_in_month (int): Number of days in the month.
        efficiency_factor (float): The total loss factor or performance ratio.
        
    Returns:
        float: Total generation in kWh for the month.
    """
    return efficiency_factor*system_kwp*days_in_month*solar_radiation

def calculate_all_systems_advanced(monthly_df,system_sizes=SYSTEM_SIZES):
    """
    Calculate solar generation with temperature and equipment loss factors.
    
    Args:
        monthly_df (pd.DataFrame): A DataFrame containing monthly climatic input data 
            (must include 'air_temperature', 'solar_radiation', and 'days_in_month' columns).
        system_sizes (list, optional): A list of solar system capacities (in kWp) to simulate. 
            Defaults to the sizes defined in config.SYSTEM_SIZES.
            
    Returns:
        pd.DataFrame: A comprehensive DataFrame containing the simulated results for all 
            system sizes, including intermediate calculation values such as 'cell_temperature', 
            'temperature_factor', 'loss_factor', and the final 'generation_kwh'.
    """
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

def build_generation_summary(generation_df,location_name):
    """
    Calculate average monthly generation by solar system size.
    """
    summary_df = generation_df.groupby("system_kwp")["generation_kwh"].mean().reset_index()
    summary_df["generation_kwh"] = summary_df["generation_kwh"].round(2)

    summary_df=summary_df.rename(columns={"generation_kwh":"monthly_avg_generation_kwh"})

    summary_df["location_name"]=location_name
    
    summary_df = summary_df[["location_name","system_kwp","monthly_avg_generation_kwh"]]
    return summary_df
    
def compare_model_with_survey(generation_df,location_name,survey_ranges):
    """
    Compare model average generation with real-world survey ranges.
    """
    rows=[]

    for system_kwp,survey_range in survey_ranges.items():
        system_df=generation_df[generation_df["system_kwp"]==system_kwp]
        
        model_average=system_df["generation_kwh"].mean()
        
        survey_low=survey_range[0]
        survey_high=survey_range[1]
        
        if survey_low<=model_average<=survey_high:
            conclusion="Reasonable" 
        elif model_average<survey_low:
            conclusion="Lower Than Survey"
        else:
            conclusion="Higher Than Survey"    
            
        rows.append({
            "location_name":location_name,
            "system_kwp":system_kwp,
            "model_average_kwh_per_month":round(model_average,2),
            "survey_low_kwh_per_month":survey_low,
            "survey_high_kwh_per_month":survey_high,
            "conclusion":conclusion
        })

    comparison_df=pd.DataFrame(rows)
    return comparison_df