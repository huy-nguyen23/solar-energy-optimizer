import pandas as pd

# Read CSV file
df = pd.read_csv("data/processed/solar_monthly.csv")

print("===== CSV DATA =====")
print(df)

# Separate real monthly data: month 1 to month 12
monthly_df = df[(df["month_number"] >= 1) & (df["month_number"] <= 12)]

# Separate NASA annual average row: month_number = 13
annual_df = df[df["month_number"] == 13]

print("\n===== 1. CHECK IF THE FILE HAS 12 MONTHS =====")

if len(monthly_df) == 12:
    print("The data has all 12 monthly records.")
else:
    print("The data does not have exactly 12 monthly records.")
    print("Number of monthly records found:", len(monthly_df))

print("\n===== CHECK NASA ANNUAL AVERAGE ROW =====")

if len(annual_df) > 0:
    print("NASA also provides an annual average row:")
    print(annual_df)
else:
    print("No annual average row found.")

print("\n===== 2. CHECK MISSING VALUES IN SOLAR_RADIATION =====")

missing_count = monthly_df["solar_radiation"].isna().sum()

if missing_count == 0:
    print("No missing values found in the solar_radiation column.")
else:
    print("Missing values found in the solar_radiation column.")
    print("Number of missing values:", missing_count)

print("\n===== 3. CALCULATE AVERAGE SOLAR_RADIATION =====")

avg = monthly_df["solar_radiation"].mean()

print(f"Average solar radiation from 12 months: {avg:.2f} kWh/m²/day")

print("\n===== 4. FINAL VALIDATION RESULT =====")

if len(monthly_df) == 12 and missing_count == 0:
    print("The 12-month data is valid. It can be used for the web application.")
else:
    print("The 12-month data is not valid. Please check the data before using it.")