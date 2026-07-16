from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.financial import estimate_kwh_from_tiered_bill
from src.config import ELECTRICITY_TIERS,VAT_RATE

test_cases=[
    {
        "name":"2 millions bill",
        "bill":2000000,
        "expected_min":624,
        "expected_max":625
    },
    {
        "name":"Zero bill",
        "bill":0,
        "expected_min":0,
        "expected_max":0
    }
]

for test_case in test_cases:
    total_kwh,_=estimate_kwh_from_tiered_bill(test_case["bill"],ELECTRICITY_TIERS,VAT_RATE)
    print("\nTest:", test_case["name"])
    print("Actual:", round(total_kwh, 2), "kWh")
    if test_case["expected_min"] <=total_kwh<=test_case["expected_max"]:
        print("Result: PASS")
    else:
        print("Result: FAIL")

print("\nTest: Negative bill")

try:
    total_kwh,_=estimate_kwh_from_tiered_bill(-363667,ELECTRICITY_TIERS,VAT_RATE)
    print("Result: FAIL")
except ValueError as e:
    print("Error:",e)  
    print("Result: PASS")
    
    
