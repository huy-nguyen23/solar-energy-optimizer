import pandas as pd
import os

location_name="PTNK"

monthly_csv_path=f"data/processed/nasa_{location_name}_monthly.csv"
output_csv_path = f"data/processed/generation_{location_name}_all_systems_simple.csv"

df=pd.read_csv(monthly_csv_path)

system_sizes=[3,5,6,10]

pr=0.79

rows=[]

for i,row in df.iterrows():
    for system_kwp in system_sizes:
        generation_kwh=pr*system_kwp*row["days_in_month"]*row["solar_radiation"]
        
        rows.append({
            "location_name":location_name,
            "month":row["month"],
            "year":row["year"],
            "month_number":row["month_number"],
            "solar_radiation":row["solar_radiation"],
            "days_in_month":row["days_in_month"],
            "system_kwp":system_kwp,
            "pr":pr,
            "generation_kwh":round(generation_kwh,2)
        })
        
result_df=pd.DataFrame(rows)

print("===== POWER GENERATION OF SOLAR SYSTEMS =====")
print(result_df)

summary_df = result_df.groupby("system_kwp")["generation_kwh"].mean().reset_index()
summary_df["generation_kwh"] = summary_df["generation_kwh"].round(2)

print("\n===== AVERAGE MONTHLY GENERATION =====")
print(summary_df)

os.makedirs("data/processed", exist_ok=True)

result_df.to_csv(output_csv_path,index=False)

print("\nFile saved at:")
print(output_csv_path)