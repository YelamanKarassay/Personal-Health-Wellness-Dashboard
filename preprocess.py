import pandas as pd
from io import StringIO
import numpy as np

# Markdown data as a multi-line string
markdown_data = """

| Date           | Weather                    | Weight | Feeling Morning | Feeling Evening | Physical Activity | Slept Hours       | Meals                                               | Air     |
| -------------- | -------------------------- | ------ | --------------- | --------------- | ----------------- | ----------------- | --------------------------------------------------- | ------- |
| YYYY-MM-DD     | Sunny, Rainy, Cloudy, etc. | XX kg  | 1-10            | 1-10            | Name/Duration     | sleep/<br>dept    | Breakfast/<br>Lunch/<br>Dinner                      | AQI     |
| [[2025-01-08]] | Sunny                      | 82 kg  | 5               | 9               | None              | 7hr26m/<br>3.3hr  | Subway:Egg&Mayo/<br>Tamjai/<br>Snacks               | 101-150 |
| [[2025-01-09]] | Sunny                      | 82 kg  | 6               | 8               | None              | 7hr6m/<br>3.7hr   | Subway:Egg&Mayo/<br>Japanese Curry/<br>McDonald<br> | 50-150  |
| [[2025-01-10]] | Sunny                      | 82kg   | 7               | 3               | None              | 6hr19m/<br>4.9hr  | Subway:Egg&Mayo/<br>Baked Curry/Pasta<br>           | 51-100  |
| [[2025-01-11]] | Sunny                      | 82kg   | 8               | 9               | None              | 9hr12m/<br>3.1hr  | Skip/<br>KFC/<br>Indian food                        | 51-100  |
| [[2025-01-12]] | Sunny                      | 82kg   | 10              | 9               | None              | 7hr/<br>3.1hr     | Skip/<br>KFC/<br>Boiled Noodle                      | 51-100  |
| [[2025-01-13]] | Sunny                      | 82kg   | 6               | 7               | None              | 7hr/<br>3.1hr     | Skip/<br>Japanese Beef/<br>Subway:Roast Beef        | 51-150  |
| [[2025-01-14]] | Cloudy                     | 82kg   | 7               | 9               | None              | 8hr36m/<br>1.4hr  | Skip/<br>Udon/<br>Ramen                             | 51-100  |
| [[2025-01-15]] | Sunny Periods              | 82kg   | 9               | 9               | None              | 7hr34m/<br>1.6hr  | Skip/<br>Tamjai/<br>Snacks                          | 51-100  |
| [[2025-01-16]] | Sunny                      | 82kg   | 8               | 9               | None              | 8hr37m/<br>0.7hr  | Subway:Egg&Mayo/<br>Pizza/<br>Snacks                | 101-150 |
| [[2025-01-17]] | Sunny                      | 82kg   | 9               | 9               | None              | 7hr38m/<br>1hr    | Subway:Egg&Mayo/<br>Pasta/Pizza<br>                 | 51-100  |
| [[2025-01-18]] | Sunny                      | 81kg   | 7               | 8               | None              | 6hr20m/<br>2.6hr  | Skip/KFC/Pasta<br>                                  | 101-150 |
| [[2025-01-19]] | Sunny                      | 81kg   | 7               | 8               | None              | 7hr30m/<br>3.0hr  | Skip/Burger/McDonald                                | 101-150 |
| [[2025-01-20]] | Sunny                      | 81kg   | 6               | 6               | None              | 8hr21m/<br>1.8hr  | Skip/Tamjai/McDonald                                | 51-150  |
| [[2025-01-21]] | Cloudy                     | 81kg   | 6               | 6               | None              | 8hr33m/<br>1.1hr  | Skip/Baked Fish/Kebab                               | 51-100  |
| [[2025-01-22]] | Cloudy                     | 81kg   | 7               | 7               | None              | 6hr11m/<br>2.7hr  | Snacks/Baked Fish/KFC                               | 51-100  |
| [[2025-01-23]] | Cloudy                     | 81kg   | 7               | 7               | None              | 7hr7m/<br>3.1hr   | Subway:Egg&Mayo/<br>Japanese Beef/Snacks            | 51-100  |
| [[2025-01-24]] | Sunny Periods              | 81.5kg | 8               | 9               | None              | 6hr12m/<br>4.5hr  | Skip/<br>Backed Fish/<br>Kebab                      | 51-100  |
| [[2025-01-25]] | Sunny Periods              | 81kg   | 9               | 8               | None              | 7hr41m/<br>4.2hr  | Skip/Korean Beef/Pizza                              | 51-100  |
| [[2025-01-26]] | Cloudy                     | 81kg   | 7               | 6               | None              | 10hr54m/<br>0.8hr | Skip/Pasta/Skip                                     | 51-100  |

"""

# Use pandas.read_csv with StringIO to convert the Markdown table into a DataFrame
df = pd.read_csv(StringIO(markdown_data), sep='|', skipinitialspace=True, engine='python')

# Drop unnecessary columns (the first and last empty columns resulting from the table format)
df = df.drop(columns=['Unnamed: 0', 'Unnamed: 10'])
# Drop the first row which contains the header information
df = df.drop(index=[0, 1]).reset_index(drop=True)

# Strip whitespace from column headers and data
df.columns = df.columns.str.strip()
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# Clean up the Date column by removing [[ ]] and replace <br> with chosen separator
df['Date'] = df['Date'].str.replace(r'\[\[|\]\]', '', regex=True)
df = df.map(lambda x: x.replace('<br>', '') if isinstance(x, str) else x)

df['Date'] = pd.to_datetime(df['Date']).dt.date

df[['Breakfast', 'Lunch', 'Dinner']] = df['Meals'].str.split('/', n=2, expand=True)
df.drop(columns=['Meals'], inplace=True)

# Replace 'None' with NaN
df = df.replace('None', pd.NA)

def extract_average_air_value(air_value):
    if pd.isna(air_value):
        return air_value
    if '-' in air_value:
        low, high = map(float, air_value.split('-'))
        return (low + high) / 2
    return float(air_value)

df['Air'] = df['Air'].apply(extract_average_air_value)

df[['Sport Name', 'Sport Duration']] = df['Physical Activity'].apply(
    lambda x: pd.Series(x.split('/', 1)) if pd.notna(x) else pd.Series([pd.NA, pd.NA])
)
df.drop(columns='Physical Activity', inplace=True)

# Divide the 'Slept Hours' column into 'Sleep Duration' and 'Sleep Debt'
df[['Sleep Duration', 'Sleep Debt']] = df['Slept Hours'].apply(
    lambda x: pd.Series(x.split('/', 1)) if pd.notna(x) else pd.Series([pd.NA, pd.NA])
)
df.drop(columns='Slept Hours', inplace=True)

def convert_sleep_duration(duration):
    if pd.isna(duration):
        return duration
    parts = duration.split('hr')
    hours = int(parts[0])
    minutes = int(parts[1][:-1]) if len(parts) > 1 and parts[1] else 0
    return round(hours + minutes / 60, 1)

df['Sleep Duration'] = df['Sleep Duration'].apply(convert_sleep_duration)

def convert_sleep_debt(debt):
    if pd.isna(debt):
        return debt
    return float(debt.replace('hr', ''))

df['Sleep Debt'] = df['Sleep Debt'].apply(convert_sleep_debt)

df['Weight'] = df['Weight'].str.replace('kg', '').str.strip().astype(float)


df.to_csv('daily_data.csv', index=False)