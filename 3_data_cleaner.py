import pandas as pd
import numpy as np

# Load
df = pd.read_csv('estat_employment_data.csv', skiprows=29, encoding='utf-8')
print(f"\nLoaded {len(df):,} rows")


print("\n[Step 1: Filtering to key dimensions...]") #change below for different angles

filtered_df = df[
    (df['Marital Status'] == 'Total') &
    (df['Education'] == 'Total') &
    (df['Status in Employment, Type of ...'] == 'Total')
].copy()

print(f"Filtered to {len(filtered_df):,} rows (from {len(df):,})")

print("\nSelecting columns")

# Keep only below
tableau_df = filtered_df[[
    'Sex',
    'Industry', 
    'Age',
    'Area classification',
    'Time',
    'value'
]].copy()

# Rename
tableau_df.columns = ['Gender', 'Industry', 'Age_Group', 'Region', 'Year', 'Employment_Count']

print(f"Selected columns: {list(tableau_df.columns)}")

# Clean the data
print("\nCleaning data...")

tableau_df['Industry'] = tableau_df['Industry'].str.replace('Of which ', '', regex=False) # Remove "Of which" from label names
tableau_df['Employment_Count'] = pd.to_numeric(tableau_df['Employment_Count'], errors='coerce') # Remove hyphens
before_clean = len(tableau_df)
tableau_df = tableau_df.dropna(subset=['Employment_Count']) # remove NaN counts
print(f"Removed {before_clean - len(tableau_df):,} rows with missing data") # check how many rows excluded

print("\nCreating industry categories...")

# Simplify long industry names
industry_mapping = {
    'D_CONSTRUCTION': 'Construction',
    'E_MANUFACTURING': 'Manufacturing',
    'F_ELECTRICITY, GAS, HEAT SUPPLY AND WATER': 'Utilities',
    'G_INFORMATION AND COMMUNICATIONS': 'IT & Communications',
    'H_TRANSPORT AND POSTAL SERVICES': 'Transport & Postal',
    'I_WHOLESALE AND RETAIL TRADE': 'Wholesale & Retail',
    'J_FINANCE AND INSURANCE': 'Finance & Insurance',
    'K_REAL ESTATE AND GOODS RENTAL AND LEASING': 'Real Estate',
    'L_SCIENTIFIC RESEARCH, PROFESSIONAL AND TECHNICAL SERVICES': 'Research & Professional',
    'M_ACCOMMODATIONS, EATING AND DRINKING SERVICES': 'Hospitality',
    'N_LIVING-RELATED AND PERSONAL SERVICES AND AMUSEMENT SERVICES': 'Personal Services',
    'O_EDUCATION, LEARNING SUPPORT': 'Education',
    'P_MEDICAL, HEALTH CARE AND WELFARE': 'Healthcare & Welfare',
    'Q_COMPOUND SERVICES': 'Compound Services',
    'R_SERVICES, N.E.C.': 'Other Services',
    'S_GOVERNMENT, EXCEPT ELSEWHERE CLASSIFIED': 'Government',
    'Total': 'Total (All Industries)'
}

tableau_df['Industry_Short'] = tableau_df['Industry'].map(industry_mapping)

#Final summary

print(f"\nFinal rows: {len(tableau_df):,}")
print(f"Columns: {len(tableau_df.columns)}")

print("\nBreakdown:") #preview print to console
print(f"  - Industries: {tableau_df['Industry_Short'].nunique()}")
print(f"  - Age Groups: {tableau_df['Age_Group'].nunique()}")
print(f"  - Genders: {tableau_df['Gender'].nunique()}")

print("\nSample data:")
print(tableau_df.head(10).to_string(index=False))

#Save
print("\nSaving to CSV")

output_file = 'japan_employment_2022_tableau.csv'
tableau_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Saved to: {output_file}")

# Also a cleaned version without Total
tableau_df_no_totals = tableau_df[
    (tableau_df['Industry_Short'] != 'Total (All Industries)') &
    (tableau_df['Age_Group'] != 'Total')
].copy()

output_file_clean = 'japan_employment_2022_tableau_clean.csv'
tableau_df_no_totals.to_csv(output_file_clean, index=False, encoding='utf-8-sig')

print(f"Saved clean version (no totals) to: {output_file_clean}")

# Check possible areas to visualise
# Top industries by employment
print("\nTop 5 Industries by Employment:")
top_industries = tableau_df[
    (tableau_df['Gender'] == 'Both sexes') &
    (tableau_df['Age_Group'] == 'Total') &
    (tableau_df['Industry_Short'] != 'Total (All Industries)')
].nlargest(5, 'Employment_Count')[['Industry_Short', 'Employment_Count']]

for idx, row in top_industries.iterrows():
    millions = row['Employment_Count'] / 1_000_000
    print(f"  {row['Industry_Short']}: {millions:.1f}M workers")

# Gender distribution in top industry
print("\nGender Split in Manufacturing:")
mfg_gender = tableau_df[
    (tableau_df['Industry_Short'] == 'Manufacturing') &
    (tableau_df['Age_Group'] == 'Total') &
    (tableau_df['Gender'] != 'Both sexes')
][['Gender', 'Employment_Count']]

for idx, row in mfg_gender.iterrows():
    millions = row['Employment_Count'] / 1_000_000
    pct = (row['Employment_Count'] / 10477400) * 100  # Total manufacturing
    print(f"  {row['Gender']}: {millions:.1f}M ({pct:.1f}%)")
