from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.calculator import calculate_generation_kwh

import pytest

def test_generation_normal_case():
    result=calculate_generation_kwh(system_kwp=5,solar_radiation=5.2,days_in_month=30,efficiency_factor=0.8051)
    assert result==pytest.approx(627.978,abs=0.01)

def test_generation_zero_solar_radiation():
    result=calculate_generation_kwh(system_kwp=5,solar_radiation=0,days_in_month=30,efficiency_factor=0.8051)
    assert result==0
    
def test_generation_invalid_solar_radiation():
    with pytest.raises(ValueError):
        calculate_generation_kwh(system_kwp=5,solar_radiation=-5.2,days_in_month=30,efficiency_factor=0.8051)
        
def test_generation_invalid_system_capacity():
    with pytest.raises(ValueError):
        calculate_generation_kwh(system_kwp=0,solar_radiation=5.2,days_in_month=30,efficiency_factor=0.8051)
        
def test_generation_invalid_efficiency_factor():
    with pytest.raises(ValueError):
        calculate_generation_kwh(system_kwp=5,solar_radiation=5.2,days_in_month=30,efficiency_factor=1.5)
        
