from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.financial import estimate_kwh_from_tiered_bill
from src.config import ELECTRICITY_TIERS,VAT_RATE

import pytest

def test_estimate_kwh_from_2_millions_bill():
    total_kwh,_=estimate_kwh_from_tiered_bill(total_bill_vnd=2000000,tiers=ELECTRICITY_TIERS,vat_rate=VAT_RATE)
    assert 624<=total_kwh<=625
    
def test_estimate_kwh_from_zero_bill():
    total_kwh,_=estimate_kwh_from_tiered_bill(total_bill_vnd=0,tiers=ELECTRICITY_TIERS,vat_rate=VAT_RATE)
    assert total_kwh==0
    
def test_estimate_kwh_from_negative_bill():
    with pytest.raises(ValueError):
        estimate_kwh_from_tiered_bill(total_bill_vnd=-2000000,tiers=ELECTRICITY_TIERS,vat_rate=VAT_RATE)

