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
    """
    Estimate monthly electricity consumption in kWh from a tiered electricity bill.
    """
    if total_bill_vnd<0:
        raise ValueError("Electricity bill must be non-negative.")
    
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
    """
    Build the financial input table.

    Output:
    - monthly bill
    - estimated monthly kWh consumption
    - average electricity price after VAT
    """    
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

def calculate_self_used_kwh(monthly_generation_kwh,self_consumption_ratio,monthly_consumption_kwh):
    """
    Calculate how much solar energy can be used by the household.

    Formula:
    self_used_kwh = min(
        monthly_generation_kwh * self_consumption_ratio,
        monthly_consumption_kwh
    )
    """
    self_used_kwh=min(monthly_generation_kwh*self_consumption_ratio,monthly_consumption_kwh)
    return  self_used_kwh

def build_self_used_energy(generation_summary_df,financial_df,location_name,self_consumption_ratio):
    """
    Build the self-used solar energy table for grid-tied systems.

    This is mainly used for the no-battery financial summary.
    """
    monthly_consumption_kwh=financial_df.loc[0,"monthly_consumption_kwh"]

    rows=[]

    for i,row in generation_summary_df.iterrows():
        system_kwp=row["system_kwp"]
        monthly_avg_generation_kwh=row["monthly_avg_generation_kwh"]
        
        self_used_kwh=calculate_self_used_kwh(monthly_avg_generation_kwh,self_consumption_ratio,monthly_consumption_kwh)
        
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

def get_investment_cost(cost_ranges,system_kwp):
    """
    Get the average investment cost for a solar system size.
    """
    cost_low,cost_high=cost_ranges[system_kwp]
    investment_cost=(cost_high+cost_low)/2
    return investment_cost

def calculate_payback_years(annual_saving,investment_cost):
    """
    Calculate payback years.

    If annual saving is 0 or negative, return None.
    """
    if investment_cost<=0:
        raise ValueError("Investment cost must be greater than 0")
    
    if annual_saving>0:
        payback_years=investment_cost/annual_saving
    else:
        payback_years=None
    return payback_years
        
def build_financial_summary(self_used_df,financial_df,location_name,cost_ranges,roof_area_ranges):
    """
    Build financial summary for grid-tied systems without battery storage.
    """
    average_price_per_kwh=financial_df.loc[0,"average_price_per_kwh_after_vat"]
    monthly_bill_vnd=financial_df.loc[0,"monthly_bill_vnd"]
    rows=[]
    for i,row in self_used_df.iterrows():
        system_kwp=row["system_kwp"]
        self_used_kwh=row["self_used_kwh"]
        
        monthly_saving_vnd=average_price_per_kwh*self_used_kwh
        annual_saving=monthly_saving_vnd*12
        
        investment_cost=get_investment_cost(cost_ranges,system_kwp)
        
        payback_years=calculate_payback_years(annual_saving,investment_cost)
            
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
    """
    Compare grid-tied systems and hybrid systems with battery storage.
    """   
    monthly_consumption_kwh=financial_df.loc[0,"monthly_consumption_kwh"]
    average_price_per_kwh_after_vat=financial_df.loc[0,"average_price_per_kwh_after_vat"]
    
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
            
            self_used_kwh=calculate_self_used_kwh(monthly_avg_generation_kwh,self_consumption_ratio,monthly_consumption_kwh)
            
            unused_or_exported_kwh=max(0,monthly_avg_generation_kwh-self_used_kwh)
            
            monthly_saving=self_used_kwh*average_price_per_kwh_after_vat
            annual_saving=monthly_saving*12
            
            investment_cost=get_investment_cost(cost_ranges,system_kwp)
            
            payback_years=calculate_payback_years(annual_saving,investment_cost)
            
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
                "annual_saving":round(annual_saving),
                "monthly_saving":round(monthly_saving),
                "payback_years":round(payback_years,2)
            })
            
    result_df=pd.DataFrame(rows)
    
    return result_df

def recommend_best_option(option_df,min_generation_ratio,max_payback_years):
    """
    Recommend the best option from both:
    - grid-tied without battery
    - hybrid with battery storage

    Rule:
    - monthly generation >= 60% of monthly consumption
    - payback years <= 6

    If no option satisfies the rule, choose the option with the lowest payback.
    """
    suitable_df=option_df[
        (option_df["monthly_avg_generation_kwh"]>=option_df["monthly_consumption_kwh"]*min_generation_ratio) &
        (option_df["payback_years"]<=max_payback_years)  
    ]
    
    if len(suitable_df)>0:
        recommended=suitable_df.sort_values("payback_years").iloc[0]
        reason="This system meets at least 60% of electricity demand and payback is no more than 6 years."
    else:
        recommended=option_df.sort_values("payback_years").iloc[0]
        reason="No system meets all conditions, so choosing the one with the lowest payback period."
        
    recommended_df=pd.DataFrame([recommended.to_dict()])
    recommended_df["recommendation_reason"]=reason
    return recommended_df