import pandas as pd
import os 

location_name="PTNK"

output_csv_path=f"data/processed/financial_input_{location_name}.csv"

monthly_bill_vnd=2000000
vat_rate=0.08

electricity_tiers=[
    (50,1984),
    (50,2050),
    (100,2380),
    (100,2998),
    (100,3350),
    (None,3460)
]

def estimate_kwh_from_tiered_bill(total_bill_vnd,tiers,vat_rate):
    money_before_vat=total_bill_vnd/(1+vat_rate)
    
    total_kwh=0
    remaining_money=money_before_vat
    
    for tier_kwh,price_per_kwh in tiers:
        if tier_kwh==None:
            kwh_in_this_tier=remaining_money/price_per_kwh
            total_kwh+=kwh_in_this_tier
            break
        
        tier_cost=tier_kwh*price_per_kwh
        
        if remaining_money<tier_cost:
            kwh_in_this_tier=remaining_money/price_per_kwh
            total_kwh+=kwh_in_this_tier
            break
        
        else:
            remaining_money=remaining_money-tier_cost
            total_kwh+=tier_kwh
    return total_kwh,money_before_vat

monthly_consumption_kwh,money_before_vat=estimate_kwh_from_tiered_bill(
    monthly_bill_vnd,
    electricity_tiers,
    vat_rate
)

average_price_per_kwh_after_vat=monthly_bill_vnd/monthly_consumption_kwh

result=[{
    "location_name":location_name,
    "monthly_bill_vnd":monthly_bill_vnd,
    "vat_rate":vat_rate,
    "monthly_before_vat":round(money_before_vat),
    "monthly_consumption_kwh":round(monthly_consumption_kwh,2),
    "average_price_per_kwh_after_vat":round(average_price_per_kwh_after_vat,2)
}]

df=pd.DataFrame(result)

print("===== ESTIMATED ELECTRICITY CONSUMPTION BY TIERED PRICING =====")
print(df)

os.makedirs("data/processed", exist_ok=True)

df.to_csv(output_csv_path,index=False)

print("\nFile saved at:")
print(output_csv_path)