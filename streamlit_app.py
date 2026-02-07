import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# Set page configuration for a premium DARK THEME production experience
st.set_page_config(
    page_title="Supplier Recommandation Analytics",
    page_icon="⚖️",
    layout="wide"
)

# --- PREMIUM DARK THEME CSS ---
# This ensures 100% white text on black/dark backgrounds for all components
# AND strictly styles the dropdowns for production-grade visual excellence.
st.markdown("""
<style>
    /* Global Background: Deep Black/Navy (Reverted to Premium Look) */
    .stApp { 
        background-color: #0f172a !important; 
        color: #ffffff !important; 
    }
    
    /* Target the Header at the top to match the theme */
    header[data-testid="stHeader"] {
        background-color: #0f172a !important;
    }
    header[data-testid="stHeader"] * {
        color: #ffffff !important;
        fill: #ffffff !important;
    }
    
    /* Force specific toolbar icons */
    [data-testid="stHeader"] button {
        color: #ffffff !important;
    }

    /* Target the Main Menu Popover (Top Right) & ALL other popovers */
    div[data-testid="stPopupMenu"], 
    div[data-baseweb="popover"], 
    div[data-baseweb="menu"], 
    ul[role="listbox"], 
    div[role="dialog"] {
        background-color: #0f172a !important; /* Matches main app background */
        border: 1px solid #334155 !important;
        color: #ffffff !important;
    }
    
    /* Force text and icons inside these containers to be white */
    div[data-baseweb="popover"] *, 
    div[data-baseweb="menu"] *, 
    ul[role="listbox"] *, 
    div[role="dialog"] * {
        color: #ffffff !important;
        fill: #ffffff !important;
    }
    
    /* Ensure list items (menu options) have the right background */
    li[role="option"], li {
        background-color: transparent !important;
    }
    
    /* Style menu items on hover */
    li[role="option"]:hover, li:hover {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
    }
    
    /* Sidebar: Professional Slate */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    
    /* Force ALL headers to Pure White */
    h1, h2, h3, h4, h5, h6 { 
        color: #ffffff !important; 
        font-weight: 800 !important;
    }

    /* Recommendation Card: Dark mode with subtle border */
    .recommendation-card {
        background-color: #1e293b;
        border: 2px solid #334155;
        padding: 40px;
        border-radius: 12px;
        margin-bottom: 30px;
        color: #ffffff !important;
    }
    
    /* Dropdown/Selectbox styling: High Contrast on Navy */
    div[data-baseweb="select"], div[data-baseweb="select"] > div {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] div {
        background-color: transparent !important; /* Fix for white background showing through */
        color: #ffffff !important;
    }
    ul[data-testid="stSelectboxVirtualList"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
    }
    li[role="option"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    li[role="option"]:hover {
        background-color: #334155 !important;
    }

    /* Force ALL standard text/lists to White */
    .stMarkdown, p, span, li, div {
        color: #ffffff !important;
    }
    
    /* Metric Styling: Radiant colors */
    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important; /* Sky Blue */
        font-weight: 900 !important;
        font-size: 2.5rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 700 !important;
    }

    /* Highlight classes for dark mode */
    .highlight-green { color: #4ade80 !important; font-weight: 800; }
    .highlight-blue { color: #38bdf8 !important; font-weight: 800; }
    
    /* Tables/Dataframes: Clear visibility */
    .stDataFrame, div[data-testid="stTable"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    
    /* Tabs: Navy styling */
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom-color: #38bdf8 !important;
    }

    /* Force all text in sidebar to white */
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
DATA_PATH = 'supplier_history_v2.csv'

def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"DEPLOYMENT ERROR: File '{DATA_PATH}' not found in the application root.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(DATA_PATH)
        df['PO_Created_Date'] = pd.to_datetime(df['PO_Created_Date'], errors='coerce')
        if 'Year' not in df.columns:
            df['Year'] = df['PO_Created_Date'].dt.year
        return df.dropna(subset=['Supplier_Name', 'Part_Number'])
    except Exception as e:
        st.error(f"CORRUPT DATA ERROR: Could not read CSV. Details: {e}")
        return pd.DataFrame()

df_history = load_data()

# --- Analysis Logic ---
def get_supplier_performance(part_id, year):
    if df_history.empty: return None
    try:
        filtered_df = df_history[df_history['Part_Number'] == part_id]
        if year != "All Years":
            filtered_df = filtered_df[filtered_df['Year'] == int(year)]
        if filtered_df.empty: return None
        
        perf = filtered_df.groupby('Supplier_Name').agg({
            'Price_USD': 'mean',
            'Delivery_Speed_Days': 'mean',
            'On_Time_Delivery': 'mean'
        }).reset_index()
        
        perf = perf.rename(columns={
            'Supplier_Name': 'Supplier Name',
            'Price_USD': 'Unit Price ($)',
            'Delivery_Speed_Days': 'Lead Time (Days)',
            'On_Time_Delivery': 'OTD %'
        })
        perf['OTD %'] = perf['OTD %'] * 100
        
        min_p = perf['Unit Price ($)'].min() if perf['Unit Price ($)'].min() > 0 else 1
        min_l = perf['Lead Time (Days)'].min() if perf['Lead Time (Days)'].min() > 0 else 1
        
        perf['Score'] = (
            (min_p / perf['Unit Price ($)'].replace(0, 1) * 0.4) + 
            (min_l / perf['Lead Time (Days)'].replace(0, 1) * 0.3) + 
            (perf['OTD %'] / 100 * 0.3)
        )
        return perf.sort_values(by='Score', ascending=False)
    except Exception:
        return None

# --- SIDEBAR ---
st.sidebar.markdown("# ⚙️ CRITERIA")
if not df_history.empty:
    part_list = sorted(df_history['Part_Number'].unique().tolist())
    selected_part = st.sidebar.selectbox("Part Number", part_list)
    available_years = ["All Years"] + sorted([str(int(y)) for y in df_history['Year'].dropna().unique()], reverse=True)
    selected_year = st.sidebar.selectbox("Analysis Year", available_years)
else:
    selected_part = None
    selected_year = "All Years"

# --- MAIN CONTENT ---
st.title("Supplier Recommandation Analytics Dashboard")

if df_history.empty:
    st.error("Data source missing.")
elif selected_part:
    performance_table = get_supplier_performance(selected_part, selected_year)
    
    if performance_table is not None:
        best = performance_table.iloc[0]
        
        # --- CONCLUSION CARD ---
        st.markdown(f"""
        <div class="recommendation-card">
            <span style="color: #94a3b8; font-weight: 800; font-size: 14px; text-transform: uppercase;">Decision Conclusion</span>
            <h1 style="margin-top: 5px; font-size: 4rem; color: #ffffff !important;">{best['Supplier Name']}</h1>
            <div style="margin-top: 20px; font-size: 1.25rem; font-weight: 400;">
                Recommended for <span style="font-weight: 800; color: #38bdf8;">{selected_part}</span> based on <b>{selected_year}</b> performance data.
                <ul style="margin-top: 15px;">
                    <li><b>Unit Price:</b> Average of <span class="highlight-green">${best['Unit Price ($)']:.2f}</span></li>
                    <li><b>Lead Time:</b> Delivered in <span class="highlight-blue">{best['Lead Time (Days)']:.1f} Days</span></li>
                    <li><b>Reliability:</b> <span class="highlight-green">{best['OTD %']:.1f}%</span> On-Time Delivery</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- KPI ROW ---
        k1, k2, k3 = st.columns(3)
        k1.metric("Avg Unit Price", f"${best['Unit Price ($)']:.2f}")
        k2.metric("Avg Lead Time", f"{best['Lead Time (Days)']:.1f} Days")
        k3.metric("OTD Reliability", f"{best['OTD %']:.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- COMPARATIVE PERFORMANCE MATRIX ---
        st.subheader("📊 Comparative Performance Matrix")
        display_df = performance_table[['Supplier Name', 'Unit Price ($)', 'Lead Time (Days)', 'OTD %']]
        st.dataframe(
            display_df.style.format({
                'Unit Price ($)': '${:,.2f}',
                'Lead Time (Days)': '{:.1f}',
                'OTD %': '{:.1f}%'
            }),
            use_container_width=True
        )

        # --- VISUALS ---
        st.divider()
        tab1, tab2 = st.tabs(["📉 Comparative Analysis Year", "📋 Transaction Logs"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.write("#### Total Price per Supplier ($)")
                st.bar_chart(display_df.set_index('Supplier Name')['Unit Price ($)'], color="#38bdf8")
            with col2:
                st.write("#### OTD % Reliability per Supplier")
                st.bar_chart(display_df.set_index('Supplier Name')['OTD %'], color="#4ade80")
        
        with tab2:
            st.write(f"Raw PO Data: {selected_part}")
            raw_view = df_history[df_history['Part_Number'] == selected_part]
            if selected_year != "All Years":
                raw_view = raw_view[raw_view['Year'] == int(selected_year)]
            st.dataframe(raw_view.drop(columns=['Year']), use_container_width=True)

else:
    st.info("Select criteria to begin analysis.")

st.markdown("<div style='text-align: center; color: #475569; padding: 60px;'>PRODUCTION READY | ENTERPRISE PROCUREMENT INTEL v7.0</div>", unsafe_allow_html=True)
