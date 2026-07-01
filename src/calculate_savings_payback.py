import pandas as pd
import os

location_name='PTNK'

input_csv_path=f"data/processed/self_used_energy_{location_name}.csv"
financial_input_path=f"data/processed/financial_input_{location_name}.csv"
output_csv_path=f"data/processed/solar_financial_summary_{location_name}.csv"

self_used_df=pd.read_csv(input_csv_path)
financial_df=pd.read_csv(financial_input_path)

average_price_per_kwh=financial_df.loc[0,"average_price_per_kwh_after_vat"]
monthly_bill_vnd=financial_df.loc[0,"monthly_bill_vnd"]

cost_ranges={
    3:(40000000,48000000),
    5:(60000000,70000000),
    6:(72000000,85000000),
    10:(110000000,130000000)
}

roof_area_ranges={
    3:"15-18 meters square",
    5:"25-30 meters square",
    6:"30-36 meters square",
    10:"50-60 meters square"
}

rows=[]
for i,row in self_used_df.iterrows():
    system_kwp=row["system_kwp"]
    self_used_kwh=row["self_used_kwh"]
    
    monthly_saving_vnd=average_price_per_kwh*self_used_kwh
    annual_saving=monthly_saving_vnd*12
    
    cost_low,cost_high=cost_ranges[system_kwp]
    investment_cost=(cost_high+cost_low)/2
    
    if annual_saving>0:
        payback_years=investment_cost/annual_saving
    else:
        payback_years=None
        
    rows.append({
        "location_name":location_name,
        "system_kwp":system_kwp, 
        "roof_area_required":roof_area_ranges[system_kwp],
        "monthly_bill_vnd":round(monthly_bill_vnd),
        "monthly_consumption_kwh":row["monthly_consumption_kwh"],
        "monthly_avg_generation_kwh":row["monthly_avg_generation_kwh"],
        "self_consumption_ratio":row["self_consumption_ratio"],
        "self_used_kwh":self_used_kwh,
        "average_price_per_kwh":average_price_per_kwh,
        "investment_cost":round(investment_cost),
        "monthly_saving_vnd":round(monthly_saving_vnd),
        "annual_saving_vnd":round(annual_saving),
        "payback_years":round(payback_years,2)
    })

result_df=pd.DataFrame(rows)

print("===== SOLAR FINANCIAL TABLE =====")
print(result_df)

os.makedirs("data/processed", exist_ok=True)
result_df.to_csv(output_csv_path,index=False)

print("\nSaved file at:")
print(output_csv_path)