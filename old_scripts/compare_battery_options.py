import pandas as pd
import os 

location_name="PTNK"
financial_path=f"data/processed/financial_input_{location_name}.csv"
generation_summary_path=f"data/processed/generation_summary_{location_name}.csv"
output_csv_path = f"data/processed/battery_option_comparison_{location_name}.csv"

financial_df=pd.read_csv(financial_path)
generation_df=pd.read_csv(generation_summary_path)

monthly_consumption_kwh=financial_df.loc[0,"monthly_consumption_kwh"]
average_price_per_kwh_after_vat=financial_df.loc[0,"average_price_per_kwh_after_vat"]

grid_tied_cost_ranges={
    3:(40000000,48000000),
    5:(60000000,70000000),
    6:(72000000,85000000),
    10:(110000000,130000000)
}

hybrid_cost_ranges={
    3:(75000000,90000000),
    5:(110000000,130000000),
    6:(130000000,150000000),
    10:(200000000,230000000)
}

scenarios=[
    {
        "option_name":"grid_tied_no_battery",
        "option_description":"Grid-tied without battery storage",
        "self_consumption_ratio":0.6,
        "has_battery":False,
        "cost_ranges":grid_tied_cost_ranges
    },
    {
        "option_name":"hybrid_with_battery",
        "option_description":"hybrid with battery storage",
        "self_consumption_ratio":0.9,
        "has_battery":True,
        "cost_ranges":hybrid_cost_ranges  
    }
]

rows=[]
for i,row in generation_df.iterrows():
    system_kwp=row["system_kwp"]
    monthly_avg_generation_kwh=row["monthly_avg_generation_kwh"]
    for scenario in scenarios:
        option_name=scenario["option_name"]
        option_description=scenario["option_description"]
        self_consumption_ratio=scenario["self_consumption_ratio"]
        has_battery=scenario["has_battery"]
        cost_ranges=scenario["cost_ranges"]
        
        self_used_kwh=min(monthly_avg_generation_kwh*self_consumption_ratio,monthly_consumption_kwh)
        unused_or_exported_kwh=max(0,monthly_avg_generation_kwh-self_used_kwh)
        monthly_saving=self_used_kwh*average_price_per_kwh_after_vat
        anual_saving=monthly_saving*12
        
        cost_low,cost_high=cost_ranges[system_kwp]
        investment_cost=(cost_high+cost_low)/2
        if anual_saving>0:
            payback_years=investment_cost/anual_saving
        else:
            payback_years=None
        rows.append({
            "location_name":location_name,
            "system_kwp":system_kwp,
            "option_name":option_name,
            "option_description":option_description,
            "has_battery":has_battery,
            "monthly_consumption_kwh":round(monthly_consumption_kwh,2),
            "monthly_avg_generation_kwh":round(monthly_avg_generation_kwh,2),
            "self_consumption_ratio":self_consumption_ratio,
            "self_used_kwh":round(self_used_kwh,2),
            "unused_or_exported_kwh":round(unused_or_exported_kwh,2),
            "average_price_per_kwh_after_vat":round(average_price_per_kwh_after_vat,2),
            "investment_cost":round(investment_cost),
            "anual_saving":round(anual_saving),
            "monthly_saving":round(monthly_saving),
            "payback_years":round(payback_years,2)
        })
result_df=pd.DataFrame(rows)

print("===== COMPARISON OF OPTIONS WITH AND WITHOUT BATTERY STORAGE =====")
print(result_df)

print("\n===== COMPARISON BY CAPACITY =====")

for system_kwp in sorted(result_df["system_kwp"].unique()):
    system_df = result_df[result_df["system_kwp"] == system_kwp]
    no_battery = system_df[system_df["option_name"] == "grid_tied_no_battery"].iloc[0]
    with_battery = system_df[system_df["option_name"] == "hybrid_with_battery"].iloc[0]
    extra_cost = with_battery["investment_cost"] - no_battery["investment_cost"]
    extra_monthly_saving = with_battery["monthly_saving"] - no_battery["monthly_saving"]
    extra_annual_saving = extra_monthly_saving * 12
    
    if extra_annual_saving > 0:
        extra_payback_years = extra_cost / extra_annual_saving
    else:
        extra_payback_years = None
        
    print("\n------------------------------")
    print("Solar power system:", system_kwp, "kWp")
    print("Without battery storage:")
    print("- Cost:", f"{no_battery['investment_cost']:,.0f}", "VNĐ")
    print("- Savings/month:", f"{no_battery['monthly_saving']:,.0f}", "VNĐ")
    print("- Payback:", no_battery["payback_years"], "years")
    print("With battery storage:")
    print("- Cost:", f"{with_battery['investment_cost_vnd']:,.0f}", "VNĐ")
    print("- Savings/month:", f"{with_battery['monthly_saving']:,.0f}", "VNĐ")
    print("- Payback:", with_battery["payback_years"], "years")
    print("Additional part when installing battery:")
    print("- Additional cost:", f"{extra_cost:,.0f}", "VNĐ")
    print("- Additional savings/month:", f"{extra_monthly_saving:,.0f}", "VNĐ")
   
    if extra_payback_years is not None:
        print("- Years to payback battery portion specifically:", round(extra_payback_years, 2), "years")
    else:
        print("- Cannot calculate payback for battery portion specifically")
        
    if with_battery["payback_years"] <= no_battery["payback_years"]:
        conclusion = "With battery storage is better for payback."
    else:
        conclusion = "Without battery storage pays back faster; battery is mainly beneficial for backup and nighttime electricity use."
    
    print("Conclusion:", conclusion)

os.makedirs("data/processed", exist_ok=True)
result_df.to_csv(output_csv_path,index=False)

print("\nSaved file at:")
print(output_csv_path)
