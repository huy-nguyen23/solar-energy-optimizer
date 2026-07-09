import pandas as pd 
import os

location_name="PTNK"

input_csv_path=f"data/processed/solar_financial_summary_{location_name}.csv"
output_csv_path=f"data/processed/recommended_system_{location_name}.csv"

df=pd.read_csv(input_csv_path)

suitable_df=df[
    (df["monthly_avg_generation_kwh"]>=df["monthly_consumption_kwh"]*0.6) &
    (df["payback_years"]<=6)  
]
 
if len(suitable_df)>0:
    recommended=suitable_df.sort_values("payback_years").iloc[0]
    reason="This system meets at least 60% of electricity demand and payback is no more than 6 years."
else:
    recommended=df.sort_values("payback_years").iloc[0]
    reason="No system meets all conditions, so choosing the one with the lowest payback period."
    
recommended_df=pd.DataFrame([recommended])
recommended_df["recommendation_reason"]=reason

print("===== RECOMMENDED SOLAR SYSTEM =====")
print("Location:", recommended["location_name"])
print("Recommended system:", recommended["system_kwp"], "kWp")
print("Required roof area:", recommended["roof_area_required"])
print("Investment cost:", f"{recommended['investment_cost']:,.0f}", "VNĐ")
print("Average generation/month:", recommended["monthly_avg_generation_kwh"], "kWh")
print("Self-used electricity/month:", recommended["self_used_kwh"], "kWh")
print("Savings/month:", f"{recommended['monthly_saving_vnd']:,.0f}", "VNĐ")
print("Savings/year:", f"{recommended['annual_saving_vnd']:,.0f}", "VNĐ")
print("Payback:", recommended["payback_years"], "years")
print("Reason:", reason)

os.makedirs("data/processed", exist_ok=True)
recommended_df.to_csv(output_csv_path,index=False)

print("\nSaved file at:")
print(output_csv_path)