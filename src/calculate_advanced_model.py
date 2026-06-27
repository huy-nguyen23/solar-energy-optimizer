import pandas as pd
import os

location_name="PTNK"

monthly_csv_path=f"data/processed/nasa_{location_name}_monthly.csv"
output_csv_path = f"data/processed/generation_{location_name}_all_systems_advanced.csv"

df=pd.read_csv(monthly_csv_path)

system_sizes=[3,5,6,10]

temperature_coefficient=-0.0035

inverter_factor = 0.976
soiling_factor = 0.95
wiring_factor = 0.98
shading_factor = 1.00
availability_factor = 0.99 

rows=[]

for i,row in df.iterrows():
    month=row['month']
    year=row['year']
    month_number=row['month_number']
    solar_radiation=row['solar_radiation']
    air_temperature=row['air_temperature']
    days_in_month=row["days_in_month"]
    
    cell_temperature=air_temperature+25
    
    temperature_factor=1+temperature_coefficient*(cell_temperature-25)
    
    loss_factor=temperature_factor*shading_factor*wiring_factor*soiling_factor*inverter_factor*availability_factor
    
    for system_kwp in system_sizes:
        generation_kwh=loss_factor*system_kwp*days_in_month*solar_radiation
        
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

print("===== ADVANCED GENERATION CALCULATION MODEL =====")
print(result_df)

summary_df = result_df.groupby("system_kwp")["generation_kwh"].mean().reset_index()
summary_df["generation_kwh"] = summary_df["generation_kwh"].round(2)

print("\n===== AVERAGE MONTHLY GENERATION =====")
print(summary_df)

os.makedirs("data/processed", exist_ok=True)

result_df.to_csv(output_csv_path,index=False)

print("\nFile saved at:")
print(output_csv_path)