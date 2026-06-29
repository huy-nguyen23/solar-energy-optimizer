import pandas as pd
import os

location_name="PTNK"

financial_input_path=f"data/processed/financial_input_{location_name}.csv"
generation_summmary_path=f"data/processed/generation_summary_{location_name}.csv"
output_csv_path=f"data/processed/self_used_energy_{location_name}.csv"

finanical_df=pd.read_csv(financial_input_path)
generation_df=pd.read_csv(generation_summmary_path)

self_consumption_ratio=0.6

monthly_consumption_kwh=finanical_df.loc[0,"monthly_consumption_kwh"]

rows=[]

for i,row in generation_df.iterrows():
    system_kwp=row["system_kwp"]
    monthly_avg_generation_kwh=row["monthly_avg_generation_kwh"]
    
    self_used_kwh=min(
        monthly_avg_generation_kwh*self_consumption_ratio,
        monthly_consumption_kwh
    )
    
    rows.append({
        "location_name":location_name,
        "system_kwp":system_kwp,
        "monthly_consumption_kwh":round(monthly_consumption_kwh,2),
        "monthly_avg_generation_kwh":round(monthly_avg_generation_kwh,2),
        "self_consumption_ratio":self_consumption_ratio,
        "self_used_kwh":round(self_used_kwh,2)  
    })

result_df=pd.DataFrame(rows)

print("===== SELF-CONSUMED SOLAR ENERGY =====")
print(result_df)

os.makedirs("data/processed", exist_ok=True)
result_df.to_csv(output_csv_path,index=False)

print("\nSaved file at:")
print(output_csv_path)
