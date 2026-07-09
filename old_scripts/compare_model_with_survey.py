import pandas as pd
import os

location_name="PTNK"

input_csv_path=f"data/processed/generation_{location_name}_all_systems_advanced.csv"
output_csv_path=f"data/processed/model_vs_survey_{location_name}.csv"

df=pd.read_csv(input_csv_path)

survey_ranges={
    3:(350,400),
    5:(600,650),
    6:(720,800),
    10:(1200,1300),
}

rows=[]

for system_kwp,survey_range in survey_ranges.items():
    system_df=df[df["system_kwp"]==system_kwp]
    
    model_average=system_df["generation_kwh"].mean()
    
    survey_low=survey_range[0]
    survey_high=survey_range[1]
    
    if survey_low<=model_average<=survey_high:
        conclusion="Reasonable" 
    elif model_average<survey_low:
        conclusion="Lower Than Survey"
    else:
        conclusion="Higher Than Survey"    
        
    rows.append({
        "location_name":location_name,
        "system_kwp":system_kwp,
        "model_average_kwh_per_month":round(model_average,2),
        "survey_low_kwh_per_month":survey_low,
        "survey_high_kwh_per_month":survey_high,
        "conclusion":conclusion
    })

comparison_df=pd.DataFrame(rows)

print("===== COMPARING NASA MODEL WITH SURVEY =====")
print(comparison_df)

os.makedirs("data/processed", exist_ok=True)

comparison_df.to_csv(output_csv_path,index=False)

print("\nFile saved at:")
print(output_csv_path)
    
    








