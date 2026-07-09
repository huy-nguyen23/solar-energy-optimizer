import pandas as pd 
import os

location_name="PTNK"

input_csv_file=f"data/processed/generation_{location_name}_all_systems_advanced.csv"
output_csv_path=f"data/processed/generation_summary_{location_name}.csv"

df=pd.read_csv(input_csv_file)

summary_df = df.groupby("system_kwp")["generation_kwh"].mean().reset_index()
summary_df["generation_kwh"] = summary_df["generation_kwh"].round(2)

summary_df=summary_df.rename(columns={
    "generation_kwh":"monthly_avg_generation_kwh"
})

summary_df["location_name"]=location_name

summary_df=summary_df[[
    "location_name",
    "system_kwp",
    "monthly_avg_generation_kwh"
]]

print("===== AVERAGE MONTHLY GENERATION =====")
print(summary_df)

os.makedirs("data/processed", exist_ok=True)
summary_df.to_csv(output_csv_path,index=False)

print("\nSaved file at:")
print(output_csv_path)