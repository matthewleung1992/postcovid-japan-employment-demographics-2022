import pandas as pd

df = pd.read_csv('estat_employment_data.csv', skiprows=29, encoding='utf-8')

print(f"\nTotal rows: {len(df):,}")
print(f"Total columns: {len(df.columns)}")

# BREAKDOWN
# Get unique industry codes and names
industry_lookup = df[['cat05_code', 'Industry']].drop_duplicates().sort_values('cat05_code')
print(f"\nAll {len(industry_lookup)} industries found:\n")
print(industry_lookup.to_string(index=False)) #print cat05_code output

# Get employment by industry
# Filter to: Total sex, Total marital status, Total education, Total employment type, Total age
industry_totals = df[
    (df['Sex'] == 'Both sexes') &
    (df['Marital Status'] == 'Total') &
    (df['Education'] == 'Total') &
    (df['Status in Employment, Type of ...'] == 'Total') &
    (df['Age'] == 'Total')
][['Industry', 'value']].copy()

# Remove non-numeric values (like '-')
industry_totals['value'] = pd.to_numeric(industry_totals['value'], errors='coerce')
industry_totals = industry_totals.dropna()
industry_totals = industry_totals.sort_values('value', ascending=False)

print(industry_totals.to_string(index=False)) #print overview count table

print("AGE GROUP BREAKDOWN")

age_lookup = df[['cat06_code', 'Age']].drop_duplicates().sort_values('cat06_code')
print(f"\nAll {len(age_lookup)} age groups found:\n")
print(age_lookup.to_string(index=False)) #print count by age group

#other info
print("\nSex categories:")
print(df['Sex'].unique())

print("\nEmployment types:")
print(df['Status in Employment, Type of ...'].unique()[:10])  # First 10

print("\nEducation levels:")
print(df['Education'].unique()[:10])  # First 10

#check data quality
print(f"\nRows with valid numeric values: {df['value'].apply(lambda x: str(x).replace('.','').replace('-','').isdigit()).sum():,}") #real number value
print(f"Rows with '-' (suppressed data): {(df['value'] == '-').sum():,}") #partially hidden data
print(f"Rows with NaN: {df['value'].isna().sum():,}") #broken NaN
