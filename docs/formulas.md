# Generation and Financial Formulas

This document explains the core physical and financial formulas applied in the source code (`src/calculator.py` and `src/financial.py`).

## 1. Loss Factor Calculation
To simulate realistic scenarios, the software does not use a fixed PR (Performance Ratio) but calculates it dynamically based on ambient temperature and equipment losses.

- **Cell Temperature:**
  `T_cell = T_air + 25` (Assumes the solar panel is always 25°C hotter than ambient temperature).
- **Temperature Factor:**
  `f_temp = 1 + (T_cell - 25) * (-0.0035)` (Temperature coefficient is -0.35%/°C).
- **Total Loss Factor:**
  `loss_factor = f_temp * f_inverter * f_soiling * f_wiring * f_shading * f_availability`
  The equipment factors and realistic shading losses are derived from the provider survey.

## 2. Energy Generation Calculation
Based on solar radiation data retrieved from the NASA API:

`generation_kwh = system_kwp * solar_radiation * days_in_month * loss_factor`

## 3. Self-consumed Energy
A household cannot consume 100% of the generated electricity simultaneously.
- **Self-consumption ratio:** 60% for Grid-tied systems, 90% for Hybrid systems.
- **Actual Self-Consumed Electricity:**
  `self_used_kwh = MIN(monthly_generation_kwh * self_consumption_ratio, monthly_consumption_kwh)`

## 4. Financial Savings
Self-consumed electricity directly reduces the electricity bill based on the average price.
- **Average Price:** Calculated based on the EVN tiered pricing model from (Total Electricity Bill / Estimated Consumption).
- **Monthly Savings:**
  `monthly_saving_vnd = self_used_kwh * average_price`
- **Annual Savings:**
  `annual_saving_vnd = monthly_saving_vnd * 12`

## 5. Payback Period
Calculated as the ratio between the initial investment cost and the annual financial savings.
`payback_years = investment_cost_vnd / annual_saving_vnd`