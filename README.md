# Solar Energy Optimizer

## 1. Project Overview

Solar Energy Optimizer is an interactive web application built with Streamlit. It helps homeowners and businesses evaluate the feasibility, financial savings, and technical parameters of installing a solar energy system (both Grid-Tied and Hybrid options) based on their specific location, roof area, and electricity bills.


## 2. Main Features

- **Automated Geocoding:** Translates any text address into precise GPS coordinates.
- **NASA Data Integration:** Fetches location-specific solar radiation and temperature data.
- **Physics Simulation Engine:** Calculates solar generation by factoring in system size, temperature coefficients, shading, inverter efficiency, and real-world performance ratios (PR).
- **Financial Modeling:** Compares **Grid-Tied (No Battery)** and **Hybrid (With Battery)** scenarios based on upfront investment, monthly EVN tiered-pricing savings, and payback periods (ROI).
- **Interactive Dashboards (UI):** Uses Streamlit and Plotly to present Energy Usage Distribution (Pie chart), Monthly Generation (Bar chart), and Cumulative Cash Flow (Line chart).
- **Persona-Based Results:** Displays tailored insights for Homeowners (ROI), Engineers (Charts & Scenarios), and Installers (Tilt Angle & Direction).

## 3. Data Sources

The project integrates data from two primary external sources:
- **Climatic Data (NASA POWER API):** Provides historical solar radiation (`ALLSKY_SFC_SW_DWN`) and air temperature (`T2M`) data for the user's specific geographical coordinates.
- **Geocoding Data (Nominatim/OpenStreetMap API):** Converts the user's free-text address into exact latitude and longitude coordinates.


## 4. Project Structure

```text
solar-energy-optimizer/
│
├── .streamlit/               # Streamlit theme and configuration
├── tests/                    # Unit test suite (pytest)
├── src/
│   ├── __init__.py
│   ├── config.py             # Global constants, equipment costs, and physical factors
│   ├── api.py                # NASA API and Geocoding functions
│   ├── processing.py         # JSON to DataFrame transformations
│   ├── calculator.py         # Physics simulation for solar generation
│   ├── financial.py          # Payback, savings, and system recommendation logic
│   ├── visualization.py      # Plotly charting logic
│   └── utils.py              # Helper functions for file I/O
├── app.py                    # Main Streamlit web application (UI)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 5. Installation

First, ensure you have Python 3 installed. It is highly recommended to use a virtual environment:
```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment (Linux/macOS)
source .venv/bin/activate
# Or on Windows:
# venv\Scripts\activate

# Install the required dependencies
pip install -r requirements.txt
```

## 6. Usage Instructions

To start the application, run the Streamlit app from your terminal (make sure your virtual environment is activated):
```bash
streamlit run app.py
```
Once the app is running:
1. Open the local URL provided in your terminal (usually `http://localhost:8501`) in your web browser.
2. Enter your address in the `Location Details` section.
3. Input your available roof area and average monthly electricity bill.
4. (Optional) Adjust advanced settings like NASA year ranges and consumption ratios.
5. Click the **"Calculate Optimization"** button to execute the pipeline (Geocode -> NASA API -> Physics Calc -> Financial Calc).
6. Explore the generated results across the UI tabs.

## 7. Testing 

The project uses the `pytest` framework to ensure the accuracy of the mathematical formulas and gracefully handle edge cases (e.g., negative inputs, zero efficiency).
To run the full test suite, execute the following command in your activated virtual environment:
```bash
python3 -m pytest tests/
```
To see detailed output for each test case, use the verbose flag:
```bash
python3 -m pytest tests/ -v
```

## 8. Analysis Output
The program outputs a comprehensive analysis report divided into three actionable tabs:
1. **Homeowner Overview:** A recommendation of the optimal system size (in kWp), estimated investment cost, payback period, annual savings, and a visual pie chart of energy distribution.
2. **Engineering & Financial Report:** Detailed monthly generation bar charts, a 15-year cumulative cash flow line chart, and a comparison table of all evaluated system scenarios.
3. **Installer Guide:** The precise target coordinates, optimal facing direction (South/North based on hemisphere), and optimal tilt angle required for physical panel installation.

## 9. Project Limitations
- **Data Dependency:** The application relies entirely on the NASA POWER and Nominatim APIs, which can occasionally experience downtime or rate-limiting. 
- **Approximations in Financials:** The tiered electricity pricing calculations are based on standard current estimates and do not account for future utility price hikes, inflation, or lithium battery degradation over time.
- **Static Physical Constraints:** The simulation uses fixed average loss factors (for shading, soiling, wiring). Real-world localized issues (like a tall tree or neighboring building blocking the sun during peak hours) cannot be automatically detected by the address alone.
- **UI Race Condition:** Due to the nature of Streamlit forms, pressing "Enter" rapidly inside a number input field might submit the form before the new value is fully registered by the frontend. Using the dedicated "Calculate" button is always recommended.