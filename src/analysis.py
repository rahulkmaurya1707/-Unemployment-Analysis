"""
Core Analysis Module for Unemployment Analysis in India.

This module provides data-driven statistical calculation functions to compute
overall statistics, COVID-19 period impact, time-series trends, regional rankings,
rural vs urban differences, seasonality patterns, correlation matrices, and IQR outliers.
"""

import pandas as pd
import numpy as np


def calculate_overall_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate comprehensive overall statistical metrics for unemployment variables.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame.
        
    Returns:
        dict: Dictionary containing summary statistics.
    """
    metrics = {}
    for col in ['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']:
        series = df[col]
        q25, q75 = series.quantile(0.25), series.quantile(0.75)
        metrics[col] = {
            'mean': float(series.mean()),
            'median': float(series.median()),
            'std': float(series.std()),
            'min': float(series.min()),
            'max': float(series.max()),
            'q25': float(q25),
            'q75': float(q75),
            'iqr': float(q75 - q25)
        }
    return metrics


def analyze_covid_impact(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare economic metrics between Pre-COVID (May 2019 - Feb 2020) and COVID-19 (Mar 2020 - Jun 2020) periods.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame.
        
    Returns:
        pd.DataFrame: Summary comparison table.
    """
    covid_comparison = df.groupby('COVID_Period')[['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']].agg(
        Mean_Unemployment=('Unemployment_Rate', 'mean'),
        Median_Unemployment=('Unemployment_Rate', 'median'),
        Max_Unemployment=('Unemployment_Rate', 'max'),
        Mean_Employed=('Employed', 'mean'),
        Mean_Labour_Participation=('Labour_Participation_Rate', 'mean')
    ).reindex(['Pre-COVID', 'COVID-19 Period'])
    
    # Calculate difference and percentage change
    pre_ur = covid_comparison.loc['Pre-COVID', 'Mean_Unemployment']
    cov_ur = covid_comparison.loc['COVID-19 Period', 'Mean_Unemployment']
    abs_change_ur = cov_ur - pre_ur
    pct_change_ur = (abs_change_ur / pre_ur) * 100
    
    pre_emp = covid_comparison.loc['Pre-COVID', 'Mean_Employed']
    cov_emp = covid_comparison.loc['COVID-19 Period', 'Mean_Employed']
    abs_change_emp = cov_emp - pre_emp
    pct_change_emp = (abs_change_emp / pre_emp) * 100
    
    pre_lpr = covid_comparison.loc['Pre-COVID', 'Mean_Labour_Participation']
    cov_lpr = covid_comparison.loc['COVID-19 Period', 'Mean_Labour_Participation']
    abs_change_lpr = cov_lpr - pre_lpr
    pct_change_lpr = (abs_change_lpr / pre_lpr) * 100
    
    impact_metrics = pd.DataFrame({
        'Metric': ['Mean Unemployment Rate (%)', 'Mean Employed Population', 'Mean Labour Participation Rate (%)'],
        'Pre-COVID Baseline': [pre_ur, pre_emp, pre_lpr],
        'COVID-19 Period': [cov_ur, cov_emp, cov_lpr],
        'Absolute Change': [abs_change_ur, abs_change_emp, abs_change_lpr],
        'Percentage Change (%)': [pct_change_ur, pct_change_emp, pct_change_lpr]
    })
    
    return impact_metrics


def analyze_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute monthly aggregated metrics, rolling statistics, and month-over-month (MoM) change.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame.
        
    Returns:
        pd.DataFrame: Monthly trend analysis table.
    """
    monthly = df.groupby('Date')[['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']].agg(
        Mean_Unemployment=('Unemployment_Rate', 'mean'),
        Median_Unemployment=('Unemployment_Rate', 'median'),
        Std_Unemployment=('Unemployment_Rate', 'std'),
        Total_Employed=('Employed', 'sum'),
        Mean_Employed=('Employed', 'mean'),
        Mean_Labour_Participation=('Labour_Participation_Rate', 'mean')
    ).sort_index()
    
    # Calculate Rolling 3-Month Moving Average
    monthly['Unemployment_3M_MA'] = monthly['Mean_Unemployment'].rolling(window=3, min_periods=1).mean()
    
    # Calculate Month-over-Month (MoM) absolute and percentage change
    monthly['MoM_Unemployment_Diff'] = monthly['Mean_Unemployment'].diff()
    monthly['MoM_Unemployment_PctChange'] = monthly['Mean_Unemployment'].pct_change() * 100
    
    return monthly


def analyze_regional_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze state-wise unemployment statistics, ranking regions by average unemployment rate.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame.
        
    Returns:
        pd.DataFrame: Regional statistics table sorted by mean unemployment rate descending.
    """
    regional = df.groupby('Region')[['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']].agg(
        Mean_Unemployment=('Unemployment_Rate', 'mean'),
        Median_Unemployment=('Unemployment_Rate', 'median'),
        Max_Unemployment=('Unemployment_Rate', 'max'),
        Min_Unemployment=('Unemployment_Rate', 'min'),
        Std_Unemployment=('Unemployment_Rate', 'std'),
        Mean_Employed=('Employed', 'mean'),
        Mean_Labour_Participation=('Labour_Participation_Rate', 'mean')
    ).sort_values(by='Mean_Unemployment', ascending=False)
    
    return regional


def analyze_area_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare Rural vs Urban unemployment metrics across periods.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame.
        
    Returns:
        pd.DataFrame: Area breakdown analysis table.
    """
    area_summary = df.groupby(['Area', 'COVID_Period'])[['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']].agg(
        Mean_Unemployment=('Unemployment_Rate', 'mean'),
        Median_Unemployment=('Unemployment_Rate', 'median'),
        Max_Unemployment=('Unemployment_Rate', 'max'),
        Mean_Employed=('Employed', 'mean'),
        Mean_Labour_Participation=('Labour_Participation_Rate', 'mean')
    ).reset_index()
    
    return area_summary


def compute_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Pearson correlation matrix among numerical economic variables.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame.
        
    Returns:
        pd.DataFrame: Correlation matrix.
    """
    cols = ['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']
    corr = df[cols].corr(method='pearson')
    return corr


def detect_outliers_iqr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify statistical outliers in Unemployment Rate using IQR (Interquartile Range).
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame.
        
    Returns:
        pd.DataFrame: DataFrame containing detected outlier rows.
    """
    q1 = df['Unemployment_Rate'].quantile(0.25)
    q3 = df['Unemployment_Rate'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outliers = df[(df['Unemployment_Rate'] < lower_bound) | (df['Unemployment_Rate'] > upper_bound)].copy()
    outliers['Outlier_Type'] = np.where(outliers['Unemployment_Rate'] > upper_bound, 'High Outlier', 'Low Outlier')
    return outliers.sort_values(by='Unemployment_Rate', ascending=False)


if __name__ == "__main__":
    from data_cleaning import load_dataset, clean_dataset
    path = r"c:\Users\mrmau\OneDrive\Desktop\Unemployment Analysis\data\unemployment_dataset.csv"
    df = clean_dataset(load_dataset(path))
    
    print("=== OVERALL METRICS ===")
    print(calculate_overall_statistics(df))
    
    print("\n=== COVID IMPACT METRICS ===")
    print(analyze_covid_impact(df))
    
    print("\n=== REGIONAL TOP 5 HIGHEST ===")
    print(analyze_regional_performance(df).head())
    
    print("\n=== CORRELATION MATRIX ===")
    print(compute_correlation_matrix(df))
    
    print("\n=== OUTLIERS COUNT ===")
    outliers = detect_outliers_iqr(df)
    print(f"Total Outliers Found: {len(outliers)}")
    print(outliers[['Region', 'Date', 'Unemployment_Rate', 'Area', 'COVID_Period']].head())
