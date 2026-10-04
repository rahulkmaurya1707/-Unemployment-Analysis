"""
Data Cleaning and Preprocessing Module for Unemployment Analysis.

This module provides functions to load, clean, and preprocess the unemployment dataset,
ensuring consistent column names, proper datatypes, date feature extraction, and missing
value handling.
"""

import pandas as pd
import numpy as np


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load raw unemployment dataset from CSV file.
    
    Parameters:
        file_path (str): Path to the CSV dataset.
        
    Returns:
        pd.DataFrame: Loaded raw DataFrame.
    """
    df = pd.read_csv(file_path)
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw DataFrame: handle whitespace, missing values, duplicates, and column mapping.
    
    Parameters:
        df (pd.DataFrame): Raw DataFrame.
        
    Returns:
        pd.DataFrame: Preprocessed and cleaned DataFrame.
    """
    # Create copy
    df_clean = df.copy()
    
    # 1. Clean Column Names (strip leading/trailing whitespace)
    df_clean.columns = df_clean.columns.str.strip()
    
    # 2. Standardize column names dictionary mapping if needed
    rename_dict = {
        'Region': 'Region',
        'Date': 'Date',
        'Frequency': 'Frequency',
        'Estimated Unemployment Rate (%)': 'Unemployment_Rate',
        'Estimated Employed': 'Employed',
        'Estimated Labour Participation Rate (%)': 'Labour_Participation_Rate',
        'Area': 'Area'
    }
    df_clean = df_clean.rename(columns=rename_dict)
    
    # 3. Drop completely empty rows
    df_clean = df_clean.dropna(how='all')
    
    # 4. Drop rows where key columns (Region, Date) are missing
    df_clean = df_clean.dropna(subset=['Region', 'Date'])
    
    # 5. Clean string columns (strip whitespace)
    string_cols = ['Region', 'Frequency', 'Area']
    for col in string_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            
    # 6. Convert Date column to datetime format (DD-MM-YYYY)
    df_clean['Date'] = df_clean['Date'].astype(str).str.strip()
    df_clean['Date'] = pd.to_datetime(df_clean['Date'], format='%d-%m-%Y', errors='coerce')
    
    # Drop any rows where Date conversion failed
    df_clean = df_clean.dropna(subset=['Date'])
    
    # 7. Convert numerical columns to float64
    num_cols = ['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']
    for col in num_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            
    # Drop any remaining rows with missing numerical values
    df_clean = df_clean.dropna(subset=num_cols)
    
    # 8. Sort chronologically by Date and Region
    df_clean = df_clean.sort_values(by=['Date', 'Region', 'Area']).reset_index(drop=True)
    
    # 9. Extract temporal features
    df_clean['Year'] = df_clean['Date'].dt.year
    df_clean['Month'] = df_clean['Date'].dt.month
    df_clean['Month_Name'] = df_clean['Date'].dt.strftime('%b')
    df_clean['Year_Month'] = df_clean['Date'].dt.to_period('M')
    df_clean['Quarter'] = df_clean['Date'].dt.to_period('Q')
    
    # 10. COVID-19 Period Flagging
    # Pre-COVID: Before March 2020 (May 2019 - Feb 2020)
    # COVID Lockdown / Disruption: March 2020 - June 2020
    df_clean['COVID_Period'] = np.where(df_clean['Date'] < '2020-03-01', 'Pre-COVID', 'COVID-19 Period')
    
    return df_clean


if __name__ == "__main__":
    path = r"c:\Users\mrmau\OneDrive\Desktop\Unemployment Analysis\data\unemployment_dataset.csv"
    raw = load_dataset(path)
    clean = clean_dataset(raw)
    print("Raw Shape:", raw.shape)
    print("Cleaned Shape:", clean.shape)
    print(clean.head())
