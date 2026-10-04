"""
Executive Streamlit Dashboard: Unemployment Analysis & COVID-19 Economic Shock in India

Run locally via:
    streamlit run app/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add parent directory to path to import src modules if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_cleaning import load_dataset, clean_dataset
from src.analysis import (
    calculate_overall_statistics,
    analyze_covid_impact,
    analyze_monthly_trends,
    analyze_regional_performance,
    analyze_area_breakdown,
    compute_correlation_matrix,
    detect_outliers_iqr
)

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="India Unemployment & Economic Shock Intelligence Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling (CSS Injection)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }

    /* Main Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #1E3A8A 50%, #0F172A 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2.2rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        position: relative;
        overflow: hidden;
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #93C5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        font-weight: 500;
        max-width: 900px;
        line-height: 1.5;
    }

    .badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        border-radius: 9999px;
        background: rgba(59, 130, 246, 0.2);
        color: #60A5FA;
        border: 1px solid rgba(96, 165, 250, 0.3);
        margin-bottom: 0.8rem;
    }

    /* Metric Cards */
    .metric-container {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.25rem 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-container:hover {
        transform: translateY(-2px);
        border-color: #3B82F6;
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 0.25rem;
    }
    .metric-sub {
        font-size: 0.78rem;
        font-weight: 600;
    }
    .sub-green { color: #34D399; }
    .sub-red { color: #F87171; }
    .sub-amber { color: #FBBF24; }
    .sub-blue { color: #60A5FA; }

    /* Custom Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1E293B;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        padding: 0px 20px;
        background-color: transparent;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 600;
        font-size: 0.92rem;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }

    /* DataFrame Styling */
    [data-testid="stDataFrame"] {
        border: 1px solid #334155;
        border-radius: 10px;
        background-color: #1E293B;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }
    
    /* Section Headers */
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .info-box {
        background: rgba(30, 41, 59, 0.7);
        border-left: 4px solid #3B82F6;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        color: #CBD5E1;
        font-size: 0.93rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_data():
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'unemployment_dataset.csv')
    raw_df = load_dataset(dataset_path)
    clean_df = clean_dataset(raw_df)
    return clean_df

df = get_data()

# Dark Theme Plotly Template Settings
PLOTLY_LAYOUT_DEFAULTS = dict(
    paper_bgcolor='rgba(15, 23, 42, 0)',
    plot_bgcolor='rgba(30, 41, 59, 0.4)',
    font=dict(family='Plus Jakarta Sans', color='#94A3B8'),
    title_font=dict(size=16, color='#F8FAFC', family='Plus Jakarta Sans'),
    xaxis=dict(gridcolor='#334155', zerolinecolor='#334155', showgrid=True),
    yaxis=dict(gridcolor='#334155', zerolinecolor='#334155', showgrid=True),
    legend=dict(bgcolor='rgba(30, 41, 59, 0.8)', bordercolor='#334155', borderwidth=1, font=dict(color='#E2E8F0')),
    margin=dict(l=40, r=40, t=50, b=40)
)

# Header Hero Section
st.markdown("""
<div class="hero-banner">
    <div class="badge">National Economic Intelligence Platform</div>
    <div class="hero-title">Unemployment & COVID-19 Impact Analysis in India</div>
    <div class="hero-subtitle">
        Empirical macroeconomic analysis of monthly labor force indicators, employment contraction, regional state leaderboards, and urban-rural market disparities (May 2019 – June 2020).
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Filter Controls
st.sidebar.markdown("### 🎛️ Control Panel")
st.sidebar.markdown("---")

# Area Type Selection
area_filter = st.sidebar.radio(
    "📍 Geographical Area", 
    ["All Areas", "Rural", "Urban"], 
    index=0,
    help="Filter data between Rural agricultural markets and Urban industrial/service sectors."
)

# Region Multiselect
all_regions = sorted(df['Region'].unique().tolist())
select_all = st.sidebar.checkbox("Select All 28 States/UTs", value=True)

if select_all:
    selected_regions = st.sidebar.multiselect("🏛️ Filter States / UTs:", options=all_regions, default=all_regions)
else:
    selected_regions = st.sidebar.multiselect("🏛️ Filter States / UTs:", options=all_regions, default=['Maharashtra', 'Delhi', 'Tamil Nadu', 'Uttar Pradesh', 'Bihar'])

# Quick Date Preset Buttons
st.sidebar.markdown("📅 **Timeline Presets**")
preset = st.sidebar.radio("Select Analysis Period:", ["Entire Timeline (May 19 - Jun 20)", "Pre-COVID Baseline (May 19 - Feb 20)", "COVID-19 Lockdown Peak (Mar 20 - Jun 20)"])

if preset == "Pre-COVID Baseline (May 19 - Feb 20)":
    min_sel, max_sel = pd.to_datetime('2019-05-31'), pd.to_datetime('2020-02-29')
elif preset == "COVID-19 Lockdown Peak (Mar 20 - Jun 20)":
    min_sel, max_sel = pd.to_datetime('2020-03-31'), pd.to_datetime('2020-06-30')
else:
    min_sel, max_sel = df['Date'].min().to_pydatetime(), df['Date'].max().to_pydatetime()

# Date Range Picker
selected_date_range = st.sidebar.date_input(
    "Custom Date Range:", 
    value=(min_sel, max_sel), 
    min_value=df['Date'].min().to_pydatetime(), 
    max_value=df['Date'].max().to_pydatetime()
)

# Apply Filters
filtered_df = df.copy()

if area_filter != "All Areas":
    filtered_df = filtered_df[filtered_df['Area'] == area_filter]

if selected_regions:
    filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]

if len(selected_date_range) == 2:
    start_d, end_d = pd.to_datetime(selected_date_range[0]), pd.to_datetime(selected_date_range[1])
    filtered_df = filtered_df[(filtered_df['Date'] >= start_d) & (filtered_df['Date'] <= end_d)]

if filtered_df.empty:
    st.error("⚠️ No observations match your filter parameters. Please widen your date or state selection.")
    st.stop()

# Key Performance Indicators (KPI Cards)
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

mean_ur = filtered_df['Unemployment_Rate'].mean()
max_ur = filtered_df['Unemployment_Rate'].max()
min_ur = filtered_df['Unemployment_Rate'].min()
mean_emp = filtered_df['Employed'].mean() / 1e6
mean_lpr = filtered_df['Labour_Participation_Rate'].mean()

# Calculate baseline COVID deltas for comparison tag
pre_ur_base = df[df['COVID_Period']=='Pre-COVID']['Unemployment_Rate'].mean()
cov_ur_base = df[df['COVID_Period']=='COVID-19 Period']['Unemployment_Rate'].mean()
ur_pct_diff = ((cov_ur_base - pre_ur_base) / pre_ur_base) * 100

with kpi1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Avg Unemployment</div>
        <div class="metric-val">{mean_ur:.2f}%</div>
        <div class="metric-sub sub-red">+{ur_pct_diff:.1f}% COVID Surge</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Peak Unemployment</div>
        <div class="metric-val">{max_ur:.2f}%</div>
        <div class="metric-sub sub-red">Puducherry (Apr '20)</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Min Unemployment</div>
        <div class="metric-val">{min_ur:.2f}%</div>
        <div class="metric-sub sub-green">Full Employment Level</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Avg Employed</div>
        <div class="metric-val">{mean_emp:.2f} M</div>
        <div class="metric-sub sub-amber">-12.7% Job Loss</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Labour Participation</div>
        <div class="metric-val">{mean_lpr:.2f}%</div>
        <div class="metric-sub sub-blue">Active Labor Force</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Macro Trends",
    "🦠 COVID-19 Shock",
    "🗺️ State Leaderboard",
    "🏘️ Sectoral Disparity",
    "🔗 Econometrics",
    "🚨 Volatility & Outliers",
    "📋 Executive Report"
])

# TAB 1: MACRO TRENDS
with tab1:
    st.markdown('<div class="section-title">📈 Monthly Macroeconomic Unemployment & Moving Averages</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">This chart evaluates the temporal trajectory of national monthly mean unemployment rates alongside rolling 3-month moving averages. The shaded red region marks the peak COVID-19 lockdown shock (March–June 2020).</div>', unsafe_allow_html=True)
    
    monthly_trend = filtered_df.groupby('Date')[['Unemployment_Rate', 'Employed']].mean().reset_index()
    monthly_trend['3M_MA'] = monthly_trend['Unemployment_Rate'].rolling(window=3, min_periods=1).mean()
    monthly_trend['Employed_M'] = monthly_trend['Employed'] / 1e6
    monthly_trend['MoM_Diff'] = monthly_trend['Unemployment_Rate'].diff()

    fig_macro = go.Figure()
    fig_macro.add_trace(go.Scatter(
        x=monthly_trend['Date'], y=monthly_trend['Unemployment_Rate'],
        mode='lines+markers', name='Monthly Mean Unemployment Rate',
        line=dict(color='#EF4444', width=3),
        marker=dict(size=8, color='#EF4444')
    ))
    fig_macro.add_trace(go.Scatter(
        x=monthly_trend['Date'], y=monthly_trend['3M_MA'],
        mode='lines', name='3-Month Moving Average (MA)',
        line=dict(color='#3B82F6', width=2.5, dash='dash')
    ))
    fig_macro.add_vrect(
        x0="2020-03-01", x1="2020-06-30",
        fillcolor="#EF4444", opacity=0.15, line_width=0,
        annotation_text="COVID-19 Lockdown Peak", annotation_position="top left",
        annotation_font=dict(color="#F87171", size=12, family="Plus Jakarta Sans")
    )
    fig_macro.update_layout(**PLOTLY_LAYOUT_DEFAULTS, title='National Unemployment Rate (%) with 3-Month Moving Average')
    st.plotly_chart(fig_macro, use_container_width=True)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        fig_emp_line = px.line(
            monthly_trend, x='Date', y='Employed_M',
            title='Total Estimated Employed Population (Millions)',
            markers=True, color_discrete_sequence=['#10B981']
        )
        fig_emp_line.add_vrect(x0="2020-03-01", x1="2020-06-30", fillcolor="#EF4444", opacity=0.15, line_width=0)
        fig_emp_line.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
        st.plotly_chart(fig_emp_line, use_container_width=True)

    with col_t2:
        monthly_trend['MoM_Color'] = np.where(monthly_trend['MoM_Diff'] > 0, '#EF4444', '#10B981')
        fig_mom = px.bar(
            monthly_trend.dropna(subset=['MoM_Diff']),
            x='Date', y='MoM_Diff',
            title='Month-over-Month (MoM) Unemployment Rate Shift (% Points)',
            color='MoM_Color',
            color_discrete_map={'#EF4444': '#EF4444', '#10B981': '#10B981'}
        )
        fig_mom.update_layout(**PLOTLY_LAYOUT_DEFAULTS, showlegend=False)
        st.plotly_chart(fig_mom, use_container_width=True)

# TAB 2: COVID-19 SHOCK ANALYSIS
with tab2:
    st.markdown('<div class="section-title">🦠 COVID-19 Pandemic Disruption & Job Losses</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Comparing labor market baseline performance (May 2019 – Feb 2020) against the severe economic shock experienced during the COVID-19 national lockdown window (March 2020 – June 2020).</div>', unsafe_allow_html=True)

    cov_stats = analyze_covid_impact(filtered_df)
    
    col_c1, col_c2 = st.columns([1, 1.2])
    with col_c1:
        st.markdown("#### 📊 Quantitative Impact Matrix")
        st.dataframe(
            cov_stats.style.format({
                'Pre-COVID Baseline': '{:,.2f}',
                'COVID-19 Period': '{:,.2f}',
                'Absolute Change': '{:,.2f}',
                'Percentage Change (%)': '{:+.2f}%'
            }),
            use_container_width=True
        )

    with col_c2:
        covid_group = filtered_df.groupby('COVID_Period')[['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']].mean().reset_index()
        fig_cov_comp = px.bar(
            covid_group, x='COVID_Period', y='Unemployment_Rate',
            color='COVID_Period',
            color_discrete_map={'Pre-COVID': '#10B981', 'COVID-19 Period': '#EF4444'},
            text_auto='.2f',
            title='Pre-COVID vs. COVID-19 Period Mean Unemployment Rate (%)'
        )
        fig_cov_comp.update_layout(**PLOTLY_LAYOUT_DEFAULTS, showlegend=False)
        st.plotly_chart(fig_cov_comp, use_container_width=True)

    # State Shock Severity Chart
    st.markdown("#### 🚨 State-wise Absolute Unemployment Surge During COVID-19")
    state_cov_pivot = filtered_df.groupby(['Region', 'COVID_Period'])['Unemployment_Rate'].mean().unstack().reset_index()
    
    if 'Pre-COVID' in state_cov_pivot.columns and 'COVID-19 Period' in state_cov_pivot.columns:
        state_cov_pivot['Absolute Surge (% Points)'] = state_cov_pivot['COVID-19 Period'] - state_cov_pivot['Pre-COVID']
        state_cov_pivot = state_cov_pivot.sort_values(by='Absolute Surge (% Points)', ascending=False)
        
        fig_state_shock = px.bar(
            state_cov_pivot, x='Region', y='Absolute Surge (% Points)',
            color='Absolute Surge (% Points)',
            color_continuous_scale='Reds',
            title='State-wise Increase in Unemployment Rate (% Points) During Lockdown'
        )
        fig_state_shock.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
        st.plotly_chart(fig_state_shock, use_container_width=True)

# TAB 3: STATE LEADERBOARD
with tab3:
    st.markdown('<div class="section-title">🗺️ State & Union Territory Leaderboard</div>', unsafe_allow_html=True)
    
    metric_choice = st.selectbox(
        "Rank States By:",
        options=['Mean_Unemployment', 'Max_Unemployment', 'Mean_Employed', 'Mean_Labour_Participation'],
        format_func=lambda x: x.replace('_', ' ')
    )
    
    reg_perf = analyze_regional_performance(filtered_df).reset_index()
    reg_perf = reg_perf.sort_values(by=metric_choice, ascending=(metric_choice == 'Mean_Employed'))
    
    col_l1, col_l2 = st.columns([1, 1.5])
    with col_l1:
        st.markdown("#### 🏆 Top Rankings Table")
        st.dataframe(
            reg_perf[['Region', metric_choice]].head(12).style.format({metric_choice: '{:,.2f}'}),
            use_container_width=True
        )
        
    with col_l2:
        fig_reg_bar = px.bar(
            reg_perf, x=metric_choice, y='Region',
            orientation='h',
            color=metric_choice,
            color_continuous_scale='Blues' if metric_choice == 'Mean_Employed' else 'Reds',
            title=f'State Rankings by {metric_choice.replace("_", " ")}'
        )
        fig_reg_bar.update_layout(**PLOTLY_LAYOUT_DEFAULTS, height=650)
        st.plotly_chart(fig_reg_bar, use_container_width=True)

    # Specific State Deep-Dive Card
    st.markdown("---")
    st.markdown("#### 🔎 State Deep-Dive Analysis")
    selected_single_state = st.selectbox("Select a State for Detail Inspection:", all_regions, index=all_regions.index('Maharashtra') if 'Maharashtra' in all_regions else 0)
    
    state_df = df[df['Region'] == selected_single_state]
    col_sd1, col_sd2 = st.columns(2)
    
    with col_sd1:
        fig_sd_line = px.line(
            state_df, x='Date', y='Unemployment_Rate', color='Area',
            markers=True, title=f'{selected_single_state}: Unemployment Rate Over Time by Area',
            color_discrete_map={'Rural': '#3B82F6', 'Urban': '#F59E0B'}
        )
        fig_sd_line.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
        st.plotly_chart(fig_sd_line, use_container_width=True)
        
    with col_sd2:
        fig_sd_emp = px.bar(
            state_df, x='Date', y='Employed', color='Area',
            barmode='group', title=f'{selected_single_state}: Employed Population Trend',
            color_discrete_map={'Rural': '#3B82F6', 'Urban': '#F59E0B'}
        )
        fig_sd_emp.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
        st.plotly_chart(fig_sd_emp, use_container_width=True)

# TAB 4: SECTORAL DISPARITY
with tab4:
    st.markdown('<div class="section-title">🏘️ Rural vs Urban Sectoral Market Disparity</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Evaluating structural market disparities between Rural agrarian regions and Urban industrial/service hubs during economic disruptions.</div>', unsafe_allow_html=True)
    
    area_trend = filtered_df.groupby(['Area', 'Date'])['Unemployment_Rate'].mean().reset_index()
    
    fig_area_trend = px.line(
        area_trend, x='Date', y='Unemployment_Rate', color='Area',
        markers=True, color_discrete_map={'Rural': '#3B82F6', 'Urban': '#F59E0B'},
        title='Rural vs Urban Mean Unemployment Rate Trajectory (%)'
    )
    fig_area_trend.add_vrect(x0="2020-03-01", x1="2020-06-30", fillcolor="#EF4444", opacity=0.15, line_width=0)
    fig_area_trend.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
    st.plotly_chart(fig_area_trend, use_container_width=True)
    
    col_sec1, col_sec2 = st.columns(2)
    with col_sec1:
        fig_box = px.box(
            filtered_df, x='Area', y='Unemployment_Rate', color='COVID_Period',
            title='Unemployment Rate Distribution: Rural vs Urban',
            color_discrete_map={'Pre-COVID': '#10B981', 'COVID-19 Period': '#EF4444'}
        )
        fig_box.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_sec2:
        area_summary = analyze_area_breakdown(filtered_df)
        st.markdown("#### 📊 Sectoral Metric Summary Table")
        st.dataframe(
            area_summary.style.format({
                'Mean_Unemployment': '{:.2f}%',
                'Median_Unemployment': '{:.2f}%',
                'Max_Unemployment': '{:.2f}%',
                'Mean_Employed': '{:,.0f}',
                'Mean_Labour_Participation': '{:.2f}%'
            }),
            use_container_width=True
        )

# TAB 5: ECONOMETRICS & CORRELATION
with tab5:
    st.markdown('<div class="section-title">🔗 Econometric Correlations & Feature Interactions</div>', unsafe_allow_html=True)
    
    col_ec1, col_ec2 = st.columns(2)
    with col_ec1:
        corr_df = compute_correlation_matrix(filtered_df)
        fig_corr = px.imshow(
            corr_df, text_auto='.3f',
            color_continuous_scale='Blues',
            title='Pearson Correlation Matrix of Macro Variables'
        )
        fig_corr.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
        st.plotly_chart(fig_corr, use_container_width=True)
        
    with col_ec2:
        fig_scatter = px.scatter(
            filtered_df, x='Labour_Participation_Rate', y='Unemployment_Rate',
            color='Area', hover_data=['Region', 'Date'],
            trendline='ols', title='Scatter Plot: Labour Participation vs Unemployment Rate',
            color_discrete_map={'Rural': '#3B82F6', 'Urban': '#F59E0B'}
        )
        fig_scatter.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
        st.plotly_chart(fig_scatter, use_container_width=True)

# TAB 6: VOLATILITY & OUTLIERS
with tab6:
    st.markdown('<div class="section-title">🚨 Shock Volatility & Statistical Outlier Index</div>', unsafe_allow_html=True)
    
    outliers_df = detect_outliers_iqr(filtered_df)
    st.markdown(f"Detected **{len(outliers_df)}** statistical outlier observations exceeding the 1.5×IQR threshold (`Unemployment Rate > 32.73%`).")
    
    st.dataframe(
        outliers_df[['Region', 'Date', 'Unemployment_Rate', 'Area', 'COVID_Period', 'Outlier_Type']]
        .head(20)
        .style.format({'Unemployment_Rate': '{:.2f}%'}),
        use_container_width=True
    )
    
    fig_out_scatter = px.strip(
        filtered_df, x='COVID_Period', y='Unemployment_Rate', color='Area',
        hover_data=['Region', 'Date'], title='Jitter Plot of Extreme Lockdown Spikes'
    )
    fig_out_scatter.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
    st.plotly_chart(fig_out_scatter, use_container_width=True)

# TAB 7: EXECUTIVE REPORT & DATA CENTER
with tab7:
    st.markdown('<div class="section-title">📋 Executive Findings & Data Export Center</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 💡 Key Empirical Findings
    1. **COVID-19 Economic Disruption**: National average unemployment rose from **9.51%** pre-COVID to **17.77%** during COVID lockdown months (**+86.91%** increase), peaking at **24.88%** in May 2020.
    2. **Employment Contraction**: Total employed population dropped by **12.71%**, representing an average loss of ~950,000 workers per state observation.
    3. **Urban Vulnerability**: Urban regions suffered significantly higher average unemployment (**13.17%**) than Rural regions (**10.32%**) due to industrial and service sector shutdowns.
    4. **Peak State Spikes**: Urban Puducherry recorded a peak unemployment rate of **76.74%** in April 2020, followed by Urban Jharkhand (**70.17%**) and Urban Bihar (**58.77%**).
    
    ---
    ### 🛡️ Data-Informed Policy Recommendations
    - **Urban Employment Safety Net**: Establish formal urban employment guarantee programs modeled after rural MGNREGA.
    - **Targeted State Interventions**: Focus emergency relief on high-volatility states such as Tripura, Haryana, Jharkhand, and Bihar.
    - **Portable Social Security**: Implement portable health and food security benefits for informal migrant workers.
    """)
    
    st.markdown("### 📥 Download Cleaned Dataset")
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_bytes,
        file_name="cleaned_unemployment_india.csv",
        mime="text/csv"
    )

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem;">
    <strong>India Unemployment & Economic Shock Intelligence Dashboard</strong> | Built with Python 3, Pandas, Plotly Express & Streamlit<br>
    Designed by Data Science & Analytics Team | Antigravity AI Project Architecture
</div>
""", unsafe_allow_html=True)
