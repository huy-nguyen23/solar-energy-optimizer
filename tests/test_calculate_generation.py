from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.calculator import calculate_generation_kwh

actual=calculate_generation_kwh(system_kwp=5,solar_radiation=5.2,days_in_month=30,efficiency_factor=0.79)
expected=616.2

print("Expected:",expected)

print("Actual:",actual)

if abs(actual-expected)<0.01:
    print("Result: PASS")
else:
    print("Result: FAIL")

invalid_test_cases=[
    {
        "name":"System capacity is zero",
        "system_kwp":0,
        "solar_radiation":5.2,
        "days_in_month":30,
        "efficiency_factor":0.79
    },
    {
        "name":"Negative solar radiation",
        "system_kwp":5,
        "solar_radiation":-6736,
        "days_in_month":30,
        "efficiency_factor":0.79
    },
    {
        "name":"PR greater than 1",
        "system_kwp":5,
        "solar_radiation":5.2,
        "days_in_month":30,
        "efficiency_factor":3.6
    }
]

for test_case in invalid_test_cases:
    print("\nTest:", test_case["name"])
    
    try:
        calculate_generation_kwh(test_case["system_kwp"],test_case["solar_radiation"],test_case["days_in_month"],test_case["efficiency_factor"])
        print("Result: FAIL")
    except ValueError as e:
        print("Error:",e)
        print("Result: PASS")