import pandas as pd

from src import config
from dataclasses import dataclass

@dataclass(frozen=True)
class BatteryScenario:
    option_name: str
    option_description: str
    self_consumption_ratio: float
    has_battery: bool
    cost_ranges: dict

BATTERY_SCENARIOS=(
    BatteryScenario(
        option_name="grid_tied_no_battery",
        option_description="Grid-tied without battery storage",
        self_consumption_ratio=config.GRID_TIED_SELF_CONSUMPTION_RATIO,
        has_battery=False,
        cost_ranges= config.GRID_TIED_COST_RANGES
    ),
    BatteryScenario(
        option_name="hybrid_with_battery",
        option_description="Hybrid with battery storage",
        self_consumption_ratio=config.HYBRID_SELF_CONSUMPTION_RATIO,
        has_battery=True,
        cost_ranges= config.HYBRID_COST_RANGES
    )
)

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

def build_financial_input(location_name,monthly_bill_vnd,vat_rate,electricity_tiers):
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
    return df

def build_self_used_energy(generation_summary_df,financial_df,location_name,self_consumption_ratio):
    monthly_consumption_kwh=financial_df.loc[0,"monthly_consumption_kwh"]

    rows=[]

    for i,row in generation_summary_df.iterrows():
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
    return result_df

def build_financial_summary(self_used_df,financial_df,location_name,cost_ranges,roof_area_ranges):
    average_price_per_kwh=financial_df.loc[0,"average_price_per_kwh_after_vat"]
    monthly_bill_vnd=financial_df.loc[0,"monthly_bill_vnd"]
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
    return result_df

def compare_battery_options(summary_df,financial_df,location_name):
    rows=[]
    for i,row in summary_df.iterrows():
        system_kwp=row["system_kwp"]
        monthly_avg_generation_kwh=row["monthly_avg_generation_kwh"]
        
        for scenario in BATTERY_SCENARIOS:
            option_name=scenario.option_name
            option_description=scenario.option_description
            self_consumption_ratio=scenario.self_consumption_ratio
            has_battery=scenario.has_battery
            cost_ranges=scenario.cost_ranges
            
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