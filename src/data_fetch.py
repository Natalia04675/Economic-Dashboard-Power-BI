from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(exist_ok=True)

# ---- Load data ----
inflation = pd.read_csv(
    DATA_DIR / "inflation.csv",
    sep=";",
    encoding="cp1250"
)

# ---- Clean column names ----
inflation.columns = inflation.columns.str.strip()

# ---- Select & rename ----
inflation = inflation[["Rok", "Miesiąc", "Wartość"]]
inflation.rename(columns={
    "Rok": "year",
    "Miesiąc": "month",
    "Wartość": "inflation_cpi"
}, inplace=True)

# ---- Create date ----
inflation["date"] = pd.to_datetime(
    inflation["year"].astype(str) + "-" +
    inflation["month"].astype(str) + "-01"
)

inflation = inflation[["date", "inflation_cpi"]]
inflation.sort_values("date", inplace=True)

# ---- Save ----
inflation.to_csv(
    OUTPUT_DIR / "inflation_clean.csv",
    index=False
)

print("Inflation data processed successfully.")

import csv


wages = pd.read_csv(
    DATA_DIR / "wages.csv",
    sep=",",
    encoding="latin1",
    engine="python",
    skiprows=3
)


# ---- Clean wages columns ----
wages = wages.iloc[:, :3]
wages.columns = ["year", "month", "wage_avg"]

wages["year"] = wages["year"].ffill()

wages["wage_avg"] = (
    wages["wage_avg"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

wages["wage_avg"] = pd.to_numeric(
    wages["wage_avg"],
    errors="coerce"
)

wages = wages.dropna(subset=["wage_avg"])

wages["date"] = pd.to_datetime(
    wages["year"].astype(int).astype(str) + "-" +
    wages["month"].astype(int).astype(str) + "-01"
)

wages = wages[["date", "wage_avg"]]
wages.sort_values("date", inplace=True)

wages.to_csv(
    OUTPUT_DIR / "wages_clean.csv",
    index=False
)

print("Wages data processed successfully.")







