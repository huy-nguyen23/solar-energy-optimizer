from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.financial import calculate_payback_years

import pytest

def test_payback_normal_case():
    assert calculate_payback_years(annual_saving=13000000,investment_cost=65000000)==5

def test_payback_decimal_result():
    assert calculate_payback_years(annual_saving=14400000,investment_cost=65000000)==pytest.approx(4.5139,rel=1e-3)
    
def test_payback_zero_saving():
    assert calculate_payback_years(annual_saving=0,investment_cost=65000000)==None

def test_payback_negative_saving():
    assert calculate_payback_years(annual_saving=-1000000,investment_cost=65000000)==None

def test_payback_invalid_investment_cost():
    with pytest.raises(ValueError):
        calculate_payback_years(annual_saving=13000000,investment_cost=-65000000)
        
def test_payback_zero_investment_cost():
    with pytest.raises(ValueError):
        calculate_payback_years(annual_saving=13000000,investment_cost=0)