import pandas as pd
import os

location_name="PTNK"

monthly_csv_path=f"data/processed/nasa_{location_name}_monthly.csv"
output_csv_path=f"data/processed/generation_{location_name}_5kwp_simple.csv"

df=pd.read_csv(monthly_csv_path)

system_kwp=5

pr=0.79

generation_kwh=pr*system_kwp*df["solar_radiation"]*df["days_in_month"]
generation_kwh=generation_kwh.round(2)

df["system_kwp"]=system_kwp
df["pr"]=pr
df["generation_kwh"]=generation_kwh

print("===== 5 KWP SYSTEM POWER GENERATION =====")
print(df[[
    "location_name",
    "month",
    "solar_radiation",
    "days_in_month",
    "system_kwp",
    "pr",
    "generation_kwh"
]])

average_generation=df["generation_kwh"].mean()

print("\nAverage monthly generation:")
print(round(average_generation, 2), "kWh/month")

os.makedirs("data/processed", exist_ok=True)

df.to_csv(output_csv_path,index=False)

print("\nFile saved at:")
print(output_csv_path)