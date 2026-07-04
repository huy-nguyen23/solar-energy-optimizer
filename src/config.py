from pathlib import Path

# ============================================================
# 1. PROJECT INFORMATION
# ============================================================
LOCATION_NAME="home"
ADDRESS="Ben Van Don Ho Chi Minh city Viet Nam"
START_YEAR=2024
END_YEAR=2024

MONTHLY_BILL_VND=2000000

REFRESH_NASA_DATA=False

# ============================================================
# 2. FOLDER PATHS
# ============================================================
DATA_DIR=Path("data")
INPUT_DIR=DATA_DIR / "input"
RAW_DIR=DATA_DIR / "raw"
PROCESSED_DIR=DATA_DIR / "processed"

# ============================================================
# 3. INPUT / OUTPUT FILE PATHS
# ============================================================
ADDRESSES_CSV_PATH=INPUT_DIR / "addresses.csv"

NASA_RAW_JSON_PATH=RAW_DIR / f'nasa_{LOCATION_NAME}_{START_YEAR}_{END_YEAR}.json'

LOCATION_WITH_COORDINATES_CSV_PATH=PROCESSED_DIR / "locations_with_coordinates.csv"

NASA_MONTHLY_CSV_PATH=PROCESSED_DIR / f"nasa_{LOCATION_NAME}_monthly.csv"

GENERATION_ADVANCED_CSV_PATH=PROCESSED_DIR / f"generation_{LOCATION_NAME}_advanced.csv"

GENERATION_SUMMARY_CSV_PATH=PROCESSED_DIR / f"generation_summary_{LOCATION_NAME}.csv"

MODEL_VS_SURVEY_CSV_PATH=PROCESSED_DIR / f"model_vs_survey_{LOCATION_NAME}.csv"

FINANCIAL_INPUT_CSV_PATH=PROCESSED_DIR / f"financial_input_{LOCATION_NAME}.csv"

BATTERY_OPTION_CSV_PATH=PROCESSED_DIR / f"battery_option_comparison_{LOCATION_NAME}.csv"

RECOMMENDED_SYSTEM_CSV_PATH=PROCESSED_DIR / f"recommended_system_{LOCATION_NAME}.csv"

# ============================================================
# 4. NASA API CONFIG
# ============================================================
GEOCODING_URL = "https://nominatim.openstreetmap.org/search"

NASA_API_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"

NASA_PARAMETERS= "ALLSKY_SFC_SW_DWN,T2M"

NASA_COMMUNITY= "RE"

NASA_FORMAT="JSON"   

GEOCODING_USER_AGENT = "solar-project-student"

# ============================================================
# 5. SOLAR SYSTEM CONFIG
# ============================================================
SYSTEM_SIZES=[3,5,6,10]

DEFAULT_PR=0.75
TEMPERATURE_COEFFICIENT=-0.0035

INVERTER_FACTOR = 0.976
SOILING_FACTOR= 0.95
WIRING_FACTOR = 0.98
SHADING_FACTOR= 1.00
AVAILABILITY_FACTOR = 0.99 
