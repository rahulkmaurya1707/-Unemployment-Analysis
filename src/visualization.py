"""
Visualization Module for Unemployment Analysis in India.

This module provides functions to create professional, publication-quality
visualizations using Matplotlib and Seaborn, and save them as high-resolution
PNG files in the `visualizations/` folder.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set global aesthetic styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_palette('deep')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8


def set_custom_theme():
    """Apply unified aesthetic theme for all charts."""
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.titlesize': 16
    })


def generate_all_visualizations(df: pd.DataFrame, output_dir: str = 'visualizations') -> list:
    """
    Generate and save all 14 required visualizations for the project.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame.
        output_dir (str): Folder path to save PNG images.
        
    Returns:
        list: Paths of created visualization files.
    """
    os.makedirs(output_dir, exist_ok=True)
    created_files = []
    set_custom_theme()
    
    # 1. Unemployment Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Unemployment_Rate'], kde=True, color='#1f77b4', bins=30, edgecolor='black', alpha=0.7)
    plt.axvline(df['Unemployment_Rate'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: {df['Unemployment_Rate'].mean():.2f}%")
    plt.axvline(df['Unemployment_Rate'].median(), color='green', linestyle='-', linewidth=2, label=f"Median: {df['Unemployment_Rate'].median():.2f}%")
    plt.title('Distribution of Estimated Unemployment Rate (%) in India', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Unemployment Rate (%)', fontsize=12)
    plt.ylabel('Frequency (Observation Count)', fontsize=12)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    path1 = os.path.join(output_dir, '01_unemployment_distribution.png')
    plt.savefig(path1, dpi=300)
    plt.close()
    created_files.append(path1)

    # 2. Overall Unemployment Trend Over Time with MA
    monthly_avg = df.groupby('Date')['Unemployment_Rate'].mean().reset_index()
    monthly_avg['3M_MA'] = monthly_avg['Unemployment_Rate'].rolling(window=3, min_periods=1).mean()
    
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_avg['Date'], monthly_avg['Unemployment_Rate'], marker='o', linewidth=2.5, color='#d62728', label='Monthly Mean Unemployment Rate')
    plt.plot(monthly_avg['Date'], monthly_avg['3M_MA'], linestyle='--', linewidth=2, color='#1f77b4', label='3-Month Moving Average')
    plt.axvspan(pd.to_datetime('2020-03-01'), pd.to_datetime('2020-06-30'), color='#ffbbbb', alpha=0.4, label='COVID-19 Lockdown Period')
    plt.title('Overall Unemployment Rate Trend in India (May 2019 – June 2020)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Unemployment Rate (%)', fontsize=12)
    plt.legend(loc='upper left', frameon=True, facecolor='white')
    plt.tight_layout()
    path2 = os.path.join(output_dir, '02_overall_unemployment_trend.png')
    plt.savefig(path2, dpi=300)
    plt.close()
    created_files.append(path2)

    # 3. Monthly Average Unemployment Bar Chart
    monthly_avg['Month_Label'] = monthly_avg['Date'].dt.strftime('%b %Y')
    plt.figure(figsize=(12, 6))
    colors = ['#2ca02c' if d < pd.to_datetime('2020-03-01') else '#d62728' for d in monthly_avg['Date']]
    bars = plt.bar(monthly_avg['Month_Label'], monthly_avg['Unemployment_Rate'], color=colors, edgecolor='black', alpha=0.85)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{height:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    plt.title('Monthly Average Unemployment Rate in India (Pre-COVID vs COVID)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Average Unemployment Rate (%)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    path3 = os.path.join(output_dir, '03_monthly_unemployment_bar.png')
    plt.savefig(path3, dpi=300)
    plt.close()
    created_files.append(path3)

    # 4. Pre-COVID vs COVID-19 Period Comparison
    covid_df = df.groupby('COVID_Period')['Unemployment_Rate'].agg(['mean', 'median', 'std']).reset_index()
    plt.figure(figsize=(8, 6))
    bars = plt.bar(covid_df['COVID_Period'], covid_df['mean'], yerr=covid_df['std'], capsize=7, color=['#2ca02c', '#d62728'], edgecolor='black', alpha=0.85, width=0.5)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height / 2, f'{height:.2f}%', ha='center', va='center', color='white', fontsize=14, fontweight='bold')
    plt.title('Impact of COVID-19 on Mean Unemployment Rate in India', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Mean Unemployment Rate (%)', fontsize=12)
    plt.tight_layout()
    path4 = os.path.join(output_dir, '04_covid_period_comparison.png')
    plt.savefig(path4, dpi=300)
    plt.close()
    created_files.append(path4)

    # 5. COVID Impact by Area (Rural vs Urban)
    area_covid = df.groupby(['Area', 'COVID_Period'])['Unemployment_Rate'].mean().reset_index()
    plt.figure(figsize=(9, 6))
    sns.barplot(data=area_covid, x='Area', y='Unemployment_Rate', hue='COVID_Period', palette=['#2ca02c', '#d62728'], edgecolor='black')
    plt.title('COVID-19 Impact on Unemployment: Rural vs Urban', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Geographical Area', fontsize=12)
    plt.ylabel('Mean Unemployment Rate (%)', fontsize=12)
    plt.legend(title='Period', frameon=True)
    plt.tight_layout()
    path5 = os.path.join(output_dir, '05_area_covid_comparison.png')
    plt.savefig(path5, dpi=300)
    plt.close()
    created_files.append(path5)

    # 6. Regional Unemployment Comparison (All 28 States/UTs)
    regional_avg = df.groupby('Region')['Unemployment_Rate'].mean().sort_values(ascending=True).reset_index()
    plt.figure(figsize=(12, 10))
    bars = plt.barh(regional_avg['Region'], regional_avg['Unemployment_Rate'], color='#1f77b4', edgecolor='black', alpha=0.85)
    plt.axvline(df['Unemployment_Rate'].mean(), color='red', linestyle='--', label=f"National Mean ({df['Unemployment_Rate'].mean():.2f}%)")
    plt.title('State-wise Average Unemployment Rate in India (May 2019 – June 2020)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Mean Unemployment Rate (%)', fontsize=12)
    plt.ylabel('State / Region', fontsize=12)
    plt.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    path6 = os.path.join(output_dir, '06_regional_unemployment_all.png')
    plt.savefig(path6, dpi=300)
    plt.close()
    created_files.append(path6)

    # 7. Top 10 Highest Unemployment States
    top10 = regional_avg.tail(10).sort_values(by='Unemployment_Rate', ascending=False)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(top10['Region'], top10['Unemployment_Rate'], color='#d62728', edgecolor='black', alpha=0.85)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.3, f'{height:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    plt.title('Top 10 States with Highest Average Unemployment Rate', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('State / Region', fontsize=12)
    plt.ylabel('Average Unemployment Rate (%)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    path7 = os.path.join(output_dir, '07_top10_highest_unemployment_states.png')
    plt.savefig(path7, dpi=300)
    plt.close()
    created_files.append(path7)

    # 8. Top 10 Lowest Unemployment States
    bottom10 = regional_avg.head(10)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(bottom10['Region'], bottom10['Unemployment_Rate'], color='#2ca02c', edgecolor='black', alpha=0.85)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    plt.title('Top 10 States with Lowest Average Unemployment Rate', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('State / Region', fontsize=12)
    plt.ylabel('Average Unemployment Rate (%)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    path8 = os.path.join(output_dir, '08_top10_lowest_unemployment_states.png')
    plt.savefig(path8, dpi=300)
    plt.close()
    created_files.append(path8)

    # 9. Seasonal Heatmap (Region vs Month_Year)
    heatmap_data = df.pivot_table(index='Region', columns='Date', values='Unemployment_Rate', aggfunc='mean')
    heatmap_data.columns = [d.strftime('%b %y') for d in heatmap_data.columns]
    plt.figure(figsize=(14, 10))
    sns.heatmap(heatmap_data, cmap='YlOrRd', annot=False, cbar_kws={'label': 'Unemployment Rate (%)'}, linewidths=0.5)
    plt.title('State-wise Monthly Unemployment Rate Heatmap (May 2019 – June 2020)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('State / Region', fontsize=12)
    plt.tight_layout()
    path9 = os.path.join(output_dir, '09_seasonal_regional_heatmap.png')
    plt.savefig(path9, dpi=300)
    plt.close()
    created_files.append(path9)

    # 10. Correlation Heatmap
    plt.figure(figsize=(8, 6))
    corr = df[['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']].corr()
    corr.columns = ['Unemployment Rate', 'Employed', 'Labour Participation']
    corr.index = ['Unemployment Rate', 'Employed', 'Labour Participation']
    sns.heatmap(corr, annot=True, fmt='.3f', cmap='Blues', vmin=-1, vmax=1, square=True, linewidths=1)
    plt.title('Correlation Matrix of Economic Indicators', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    path10 = os.path.join(output_dir, '10_correlation_heatmap.png')
    plt.savefig(path10, dpi=300)
    plt.close()
    created_files.append(path10)

    # 11. Labour Participation Rate vs Unemployment Rate Scatter Plot
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='Labour_Participation_Rate', y='Unemployment_Rate', scatter_kws={'alpha':0.5, 'color':'#1f77b4'}, line_kws={'color':'#d62728', 'linewidth':2})
    plt.title('Scatter Plot: Labour Participation Rate vs Unemployment Rate', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Labour Participation Rate (%)', fontsize=12)
    plt.ylabel('Unemployment Rate (%)', fontsize=12)
    plt.tight_layout()
    path11 = os.path.join(output_dir, '11_labour_participation_vs_unemployment.png')
    plt.savefig(path11, dpi=300)
    plt.close()
    created_files.append(path11)

    # 12. Employment Trend Over Time
    employment_trend = df.groupby('Date')['Employed'].sum() / 1e6  # in Millions
    plt.figure(figsize=(12, 6))
    plt.plot(employment_trend.index, employment_trend.values, marker='s', linewidth=2.5, color='#2ca02c')
    plt.axvspan(pd.to_datetime('2020-03-01'), pd.to_datetime('2020-06-30'), color='#ffbbbb', alpha=0.4, label='COVID-19 Lockdown Impact')
    plt.title('Total Estimated Employed Population Trend in India (in Millions)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Total Employed Population (Millions)', fontsize=12)
    plt.legend(loc='lower left', frameon=True)
    plt.tight_layout()
    path12 = os.path.join(output_dir, '12_employment_trend_millions.png')
    plt.savefig(path12, dpi=300)
    plt.close()
    created_files.append(path12)

    # 13. Rolling Average & Volatility Chart
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_avg['Date'], monthly_avg['Unemployment_Rate'], label='Raw Monthly Mean', color='#7f7f7f', alpha=0.6, linewidth=1.5)
    plt.plot(monthly_avg['Date'], monthly_avg['3M_MA'], label='3-Month Moving Average', color='#1f77b4', linewidth=2.5)
    plt.title('Rolling 3-Month Moving Average of Unemployment Rate', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Unemployment Rate (%)', fontsize=12)
    plt.legend(frameon=True)
    plt.tight_layout()
    path13 = os.path.join(output_dir, '13_rolling_average_trend.png')
    plt.savefig(path13, dpi=300)
    plt.close()
    created_files.append(path13)

    # 14. Month-over-Month (MoM) Changes in Unemployment Rate
    mom_diff = monthly_avg.set_index('Date')['Unemployment_Rate'].diff().dropna()
    mom_labels = [d.strftime('%b %y') for d in mom_diff.index]
    plt.figure(figsize=(12, 6))
    colors = ['#d62728' if val > 0 else '#2ca02c' for val in mom_diff.values]
    bars = plt.bar(mom_labels, mom_diff.values, color=colors, edgecolor='black', alpha=0.85)
    for bar in bars:
        height = bar.get_height()
        va = 'bottom' if height > 0 else 'top'
        plt.text(bar.get_x() + bar.get_width()/2., height + (0.5 if height > 0 else -0.8), f'{height:+.1f}%', ha='center', va=va, fontsize=9, fontweight='bold')
    plt.axhline(0, color='black', linewidth=1)
    plt.title('Month-over-Month (MoM) Change in Mean Unemployment Rate (Percentage Points)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('MoM Change (% Points)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    path14 = os.path.join(output_dir, '14_mom_unemployment_change.png')
    plt.savefig(path14, dpi=300)
    plt.close()
    created_files.append(path14)

    return created_files


if __name__ == "__main__":
    from data_cleaning import load_dataset, clean_dataset
    path = r"c:\Users\mrmau\OneDrive\Desktop\Unemployment Analysis\data\unemployment_dataset.csv"
    df = clean_dataset(load_dataset(path))
    files = generate_all_visualizations(df)
    print(f"Generated {len(files)} visualization charts successfully.")
    for f in files:
        print(" Saved:", f)
