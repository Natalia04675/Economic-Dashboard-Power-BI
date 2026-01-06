from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# ---- Load cleaned data ----
inflation = pd.read_csv(PROCESSED_DIR / "inflation_clean.csv", parse_dates=["date"])
wages = pd.read_csv(PROCESSED_DIR / "wages_clean.csv", parse_dates=["date"])


df = pd.merge(
    wages,
    inflation,
    on="date",
    how="inner"
)

df.rename(columns={"wage_avg": "avg_wage"}, inplace=True)

# ---- Convert to numeric ----
df["avg_wage"] = (
    df["avg_wage"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .astype(float)
)

df["inflation_cpi"] = (
    df["inflation_cpi"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .astype(float)
)

# ---- Real wage ----
df["real_wage"] = df["avg_wage"] / (df["inflation_cpi"] / 100)



# ---- Save final dataset ----
df.to_csv(PROCESSED_DIR / "dashboard_data.csv", index=False)

print("Dashboard dataset created successfully.")
print(df.head())

unemp = pd.read_csv(
    PROCESSED_DIR / "unemployment_clean.csv",
    parse_dates=["date"]
)

df = pd.merge(
    df,
    unemp,
    on="date",
    how="left"
)

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# ---- Load datasets ----
inflation = pd.read_csv(PROCESSED_DIR / "inflation_clean.csv", parse_dates=["date"])
wages = pd.read_csv(PROCESSED_DIR / "wages_clean.csv", parse_dates=["date"])
unemp = pd.read_csv(PROCESSED_DIR / "unemployment_clean.csv", parse_dates=["date"])

# ---- Merge wages + inflation ----
df = pd.merge(
    wages,
    inflation,
    on="date",
    how="inner"
)

df.rename(columns={"wage_avg": "avg_wage"}, inplace=True)

# ---- Convert to numeric ----
df["avg_wage"] = (
    df["avg_wage"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .astype(float)
)

df["inflation_cpi"] = (
    df["inflation_cpi"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .astype(float)
)

# ---- Real wage ----
df["real_wage"] = df["avg_wage"] / (df["inflation_cpi"] / 100)

# ---- Merge unemployment ----
df = pd.merge(
    df,
    unemp,
    on="date",
    how="left"
)

# ---- Save final dataset ----
df = df.sort_values("date")
df.to_csv(PROCESSED_DIR / "dashboard_data.csv", index=False)

print("Final dashboard dataset created successfully.")
print(df.head())
