import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

from agent_analytical_runner import process_script_and_update_db
from clickhouse_tools import (
    get_budget_by_category,
    get_budget_by_scene,
    get_total_budget_summary,
    get_all_line_items,
    clear_budget_data,
)

st.set_page_config(
    page_title="Script-to-Budget Assistant", page_icon="🎬", layout="wide"
)

import streamlit as st

# Must be the very first Streamlit command
st.set_page_config(
    page_title="Script-to-Budget Assistant", page_icon="🎬", layout="wide"
)

# --- COMPLETE CLEAN APP CSS (Hides Fork, GitHub, Share, Star, and Streamlit Badge) ---
hide_app_elements = """
    <style>
    /* 1. Hide the top-right header elements (Fork, GitHub, Share, Star, Pencil) */
    [data-testid="stHeaderActionElements"],
    [data-testid="stHeader"] button,
    [data-testid="stHeader"] a,
    header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* 2. Hide the main menu (three dots) if you want a 100% clean app UI */
    #MainMenu {
        visibility: hidden !important;
        display: none !important;
    }

    /* 3. Hide the Streamlit footer and bottom floating badge (Crown / Host badge) */
    footer {
        visibility: hidden !important;
        display: none !important;
    }
    
    .viewerBadge_container__1QSob,
    [data-testid="stStatusWidget"],
    .styles_stateContainer__29P98,
    #data-testid="stDecoration" {
        display: none !important;
        visibility: hidden !important;
    }

    /* 4. Remove extra whitespace at the top of the main container */
    .main .block-container {
        padding-top: 1rem !important;
    }
    </style>
"""
st.markdown(hide_app_elements, unsafe_allow_html=True)
# Sidebar - Controls & Script Draft Input
with st.sidebar:
    st.title("🎬 Pipeline Controls")
    script_text = st.text_area(
        "Script Draft",
        height=300,
        placeholder="EXT. NEO-TOKYO STREETS - NIGHT (SCENE 101)\nHeavy synthetic rain ($10,000/hr effect)...",
    )
    process_btn = st.button(
        "🚀 Process Script", type="primary", use_container_width=True
    )

    st.divider()
    if st.button("Clear ClickHouse Data", use_container_width=True):
        clear_budget_data()
        st.toast("Data cleared from ClickHouse!")
        st.rerun()

# Execute Agent Pipeline
if process_btn:
    if script_text.strip():
        with st.spinner("Processing with Gemini and updating ClickHouse..."):
            res = process_script_and_update_db(script_text)
            st.success("Script parsed & line items stored successfully!")
            st.rerun()
    else:
        st.error("Please enter a script draft first.")

# Main Executive Dashboard
st.title("📊 Script-to-Budget Executive Dashboard")

summary = get_total_budget_summary()
col1, col2, col3 = st.columns(3)
col1.metric("Total Budget", f"${summary.get('total_cost', 0.0):,.2f}")
col2.metric("Departments / Scenes", f"{summary.get('total_scenes', 0)}")
col3.metric("Line Items", f"{summary.get('total_items', 0)}")

st.divider()

cat_data = get_budget_by_category()
scene_data = get_budget_by_scene()

if cat_data or scene_data:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Category Breakdown")
        if cat_data:
            df_cat = pd.DataFrame(cat_data)
            fig_pie = px.pie(
                df_cat,
                names="category",
                values="total_cost",
                hole=0.4,
                title="Spend by Category",
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No category data available.")

    with c2:
        st.subheader("Department / Scene Breakdown")
        if scene_data:
            df_scene = pd.DataFrame(scene_data)
            # Use 'department' column returned by clickhouse_tools
            x_col = (
                "department"
                if "department" in df_scene.columns
                else df_scene.columns[0]
            )
            fig_bar = px.bar(
                df_scene,
                x=x_col,
                y="total_cost",
                title="Spend by Department",
                color="total_cost",
                color_continuous_scale="Viridis",
                labels={x_col: "Department / Scene", "total_cost": "Cost ($)"},
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No department data available.")

st.divider()
st.subheader("📋 Itemized Line Items")

items = get_all_line_items()
if items:
    items_df = pd.DataFrame(items)
    # Format currency column for clean presentation
    if "cost" in items_df.columns:
        items_df["cost"] = items_df["cost"].apply(lambda x: f"${x:,.2f}")
    st.dataframe(items_df, use_container_width=True)
else:
    st.info("No line items stored yet. Process a script via the sidebar!")
