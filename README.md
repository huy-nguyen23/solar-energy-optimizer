# Solar Energy Optimizer
## 1. Project Overview
This project uses NASA POWER API data to analyze solar radiation in a particular location.

In details, this project collects data on NASA website, saves raw data as JSON format, processes it into a clean CSV file, and validates data before using it for web application development.

## 2. Project Structure
```text
solar-energy-optimizer/
│
├── data/
│   ├── raw/
│   │   └── nasa_solar_raw.json
│   └── processed/
│       └── solar_monthly.csv
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── nasa_api.py
│   ├── data_io.py
│   ├── processing.py
│   └── validation.py
├── main.py
├── requirements.txt
└── README.md
```


## 3. Data Source
The data is collected from the NASA POWER API.

API endpoint:

```text
https://power.larc.nasa.gov/api/temporal/monthly/point
```

The main parameter used in this project is:

```text
ALLSKY_SFC_SW_DWN
```

This parameter represents solar radiation received at the Earth's surface.

## 4. How To Run The Project
First, create a virtual environment, then install the required libraries using `requirements.txt`:

```bash
# Create and activate virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Then, run the project from the root folder:

```bash
python main.py
```
## 5. What I Learned
Through this project, I learned how to:
* Use `requests.get()` to call an API.
* Read JSON data returned from an API.
* Save raw JSON data into a file.
* Convert JSON data into a pandas DataFrame.
* Save processed data as a CSV file.
* Validate data before using it in an application.
* Refactor Python code into functions and modules.
* Write Python docstrings.
