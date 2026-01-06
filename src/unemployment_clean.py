from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

unemp = pd.read_csv(
    RAW_DIR / "unemployment.csv",
    sep=",",
    encoding="utf-8"
)
print("UNEMPLOYMENT COLUMNS:")
print(unemp.columns)
print(unemp.head())

unemp = unemp[["day", "polska"]]

unemp.rename(columns={
    "day": "date",
    "polska": "unemployment_rate"
}, inplace=True)

unemp["unemployment_rate"] = unemp["unemployment_rate"].astype(float)
unemp["date"] = pd.to_datetime(unemp["date"])

unemp = unemp.sort_values("date")

PROCESSED_DIR.mkdir(exist_ok=True)
unemp.to_csv(PROCESSED_DIR / "unemployment_clean.csv", index=False)

print("Unemployment data processed successfully.")




