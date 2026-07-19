from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.calculator import classify_model_result
from src.config import SURVEY_RANGES
import pytest

def test_classify_model_result_reasonable():
    assert classify_model_result(survey_ranges=SURVEY_RANGES,system_kwp=3,model_average=350)=="Reasonable"
    assert classify_model_result(survey_ranges=SURVEY_RANGES,system_kwp=3,model_average=375)=="Reasonable"
    assert classify_model_result(survey_ranges=SURVEY_RANGES,system_kwp=3,model_average=400)=="Reasonable"
    assert classify_model_result(survey_ranges=SURVEY_RANGES,system_kwp=10,model_average=1250)=="Reasonable"
          
def test_classify_model_result_lower_than_survey():
    assert classify_model_result(survey_ranges=SURVEY_RANGES,system_kwp=5,model_average=599.5)=="Lower Than Survey"
    assert classify_model_result(survey_ranges=SURVEY_RANGES,system_kwp=6,model_average=0)=="Lower Than Survey"

def test_classify_model_result_higher_than_survey():
    assert classify_model_result(survey_ranges=SURVEY_RANGES,system_kwp=5,model_average=651)=="Higher Than Survey"
    assert classify_model_result(survey_ranges=SURVEY_RANGES,system_kwp=10,model_average=1500)=="Higher Than Survey"
    
def test_classify_model_result_invalid_capacity():
    with pytest.raises(ValueError):
        classify_model_result(survey_ranges=SURVEY_RANGES,system_kwp=7,model_average=350)