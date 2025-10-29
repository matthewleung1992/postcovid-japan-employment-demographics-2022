import requests
import pandas as pd
from datetime import datetime
import time

APP_ID = ""  #REDACTED

STATS_DATA_ID = "0004008113"  # Population (Persons Engaged in Work) by Sex, Marital Status, Education, Status in Employment, Type of Employment, Whether Starting a Business for Oneself, Industry, Age - Japan

BASE_URL = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData"

# Fetch data

def fetch_estat_data(app_id, stats_data_id):
    params = {
        'appId': app_id,
        'lang': 'E',  # English labels
        'statsDataId': stats_data_id,
        'metaGetFlg': 'Y',
        'cntGetFlg': 'N',
        'explanationGetFlg': 'Y',
        'annotationGetFlg': 'Y',
        'sectionHeaderFlg': '1',
        'replaceSpChars': '0'
    }
    
    print(f"Dataset ID: {stats_data_id}")

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise error if 404
        
        print(f"  Success")
        print(f"  Response size: {len(response.content)} bytes")
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

#Save to folder - CSV
def save_data(response, filename='estat_employment_data.csv'):

    if response is None:
        print("No data")
        return False
    
    # Save the raw first
    with open(filename, 'wb') as f:
        f.write(response.content)
    
    # Also save text
    with open('estat_raw_response.txt', 'w', encoding='utf-8') as f:
        f.write(response.text[:5000])  # First 5000 chars
    
    print(f"Data saved to: {filename}")
    print(f"Raw response preview saved to: estat_raw_response.txt")
    return True

#try to inspect before analysis

def inspect_data(filename='estat_employment_data.csv'):
    print("LOAD csv")
  
    print("\n[Parsing e-Stat format: skipping metadata rows...]")    
    try:
        # Line 30 is the header, line 31+ is data
        df = pd.read_csv(filename, skiprows=29, encoding='utf-8', low_memory=False)
        print(f"Successfully parsed")
        
        print(f"\nDataset shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"\nColumn names:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        print(f"\nFirst 5 rows:")
        print(df.head(5).to_string())
        
        print(f"\nLast 5 rows:")
        print(df.tail(5).to_string())
        
        # Check unique values in key columns
        print("KEY COLUMN ANALYSIS")
        
        # Industry
        if 'cat05_code' in df.columns:
            print(f"\nIndustries found: {df['cat05_code'].nunique()} unique values")
            print("Sample industries:")
            print(df['cat05_code'].value_counts().head(10))
        
        # Time
        if 'time_code' in df.columns:
            print(f"\nTime periods found:")
            print(df['time_code'].unique())
        
        # Age
        if 'cat06_code' in df.columns:
            print(f"\nAge groups found: {df['cat06_code'].nunique()} unique values")
        
        return df
        
    except Exception as e:
        print(f"Error: {e}")
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [f.readline() for _ in range(35)]
        for i, line in enumerate(lines[25:35], 26):
            print(f"Line {i}: {line.strip()[:120]}") # check console for debug
        return None

# MAIN process

if __name__ == "__main__":
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check if API key is set
    if APP_ID == None:
        print("Need API key from estat website")
    else:
        response = fetch_estat_data(APP_ID, STATS_DATA_ID)
        
        # Save to file
        if save_data(response):
            # Inspect
            df = inspect_data()
            
            print("COMPLETE!")
    
    print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
