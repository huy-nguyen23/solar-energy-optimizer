import streamlit as st
import pandas as pd
import time

from src import config
from src.visualization import (
    create_energy_distribution_pie_chart,
    create_monthly_generation_bar_chart,
    create_cumulative_cash_flow_line_chart
)
from src.api import fetch_nasa_solar_data, geocode_address
from src.processing import convert_power_data_to_monthly_dataframe
from src.calculator import (
    calculate_all_systems_advanced,
    build_generation_summary
)
from src.financial import (
    build_financial_input,
    compare_battery_options,
    recommend_best_option
)

def main():
    st.set_page_config(page_title="Solar Energy Optimizer", page_icon="☀️", layout="wide")
    
    st.title("☀️ Solar Energy Optimizer")
    st.markdown("""
    Welcome to the **Solar Energy Optimizer**! 
    Simply enter your address and electricity usage details below to discover the most cost-effective solar energy system for your home.*
    """)
    
    with st.expander("📖 How to use this app", expanded=False):
        st.markdown("""
        **Step 1:** Enter your full address so we can query precise solar radiation data from NASA for your location.\n
        **Step 2:** Provide your available roof area (in square meters) and your average monthly electricity bill (in VND).\n
        **Step 3 (Optional):** Open "Advanced Settings" if you want to tweak generation rules, self-consumption ratios, or NASA data years.\n
        **Step 4:** Click **Calculate Optimization** and wait for the physics and financial analysis.\n
        **Step 5:** Explore the results across 3 tabs:
        - 🏡 **Homeowner Overview:** Get a quick summary of the best system, investment costs, and ROI.
        - 💻 **Engineering Report:** Dive deep into monthly generation charts, cumulative cash flow, and comparison tables.
        - 🛠️ **Installer Guide:** View technical parameters like coordinates, optimal tilt angle, and facing direction for physical installation.
        """)
    with st.expander("💡 Learn about System Types (Grid-Tied vs Hybrid)", expanded=False):
        st.info("""
        **1. Grid-Tied System (No Battery):**
        - **How it works:** Operates only during the day. Solar energy is consumed directly by active appliances.
        - **Best for:** Households consuming most of their electricity during the day (running ACs, working from home).
        - **Pros:** Lower upfront cost, extremely fast payback period (typically 3 - 5 years).

        **2. Hybrid System (With Lithium Battery Storage):**
        - **How it works:** Excess solar energy generated during the day charges the battery. The stored energy is used at night.
        - **Best for:** Households empty during the day, where most electricity is consumed at night.
        - **Pros:** Maximizes night-time savings, provides backup power during grid outages. Slightly longer payback period (typically 5 - 7 years).
        """)

    # Form groups all inputs together for a better UX
    with st.form("input_form"):
        st.subheader("📍 Location Details")
        address = st.text_input("Your Address", value="Ben Van Don Ho Chi Minh city Viet Nam", 
                                help="Enter your full address to calculate precise solar radiation using NASA API.")
        
        st.subheader("⚙️ Primary Parameters")
        col1, col2 = st.columns(2)
        with col1:
            roof_area = st.number_input("Roof Area (m²)", value=60.0, step=5.0,
                                        help="Estimated available roof space. A minimum of 15m² is required for a basic 3 kWp system.")
        with col2:
            monthly_bill = st.number_input("Monthly Electricity Bill (VND)", min_value=100_000, max_value=50_000_000, value=2_400_000, step=100_000,
                                           help="Your average monthly electricity bill. We will estimate your consumption using the tiered pricing model.")
            
        with st.expander("🛠️ Advanced Settings (NASA API & Optimization Rules)"):
            c1, c2, c3 = st.columns(3)
            with c1:
                start_year = st.number_input("NASA Data Start Year", min_value=2015, max_value=2026, value=config.START_YEAR, step=1)
                end_year = st.number_input("NASA Data End Year", min_value=2015, max_value=2026, value=config.END_YEAR, step=1)
            with c2:
                min_gen_ratio = st.slider("Min Generation Ratio", min_value=0.1, max_value=1.5, value=config.MIN_GENERATION_RATIO, step=0.1,
                                          help="The minimum ratio of (Solar Generation / Household Consumption) to consider a system 'suitable'.")
                max_payback = st.slider("Max Payback Years", min_value=1, max_value=15, value=config.MAX_PAYBACK_YEARS, step=1,
                                        help="Maximum acceptable payback period (years) for the recommended system.")
            with c3:
                grid_tied_ratio = st.slider("Grid-tied Self-Consumption", min_value=0.1, max_value=1.0, value=config.GRID_TIED_SELF_CONSUMPTION_RATIO, step=0.05,
                                            help="Estimated percentage of solar energy consumed directly by the household for Grid-tied systems.")
                hybrid_ratio = st.slider("Hybrid Self-Consumption", min_value=0.1, max_value=1.0, value=config.HYBRID_SELF_CONSUMPTION_RATIO, step=0.05,
                                         help="Estimated percentage of solar energy consumed directly for Hybrid systems (with battery).")
                
        submitted = st.form_submit_button("🚀 Calculate Optimization", type="primary")
        
    if submitted:
        if not address.strip():
            st.error("❌ Please enter a valid address to proceed!")
            return
            
        if roof_area < 15.0:
            st.error("❌ Roof area is too small! You need at least 15 m² to install the smallest system (3 kWp).")
            return
            
        if roof_area > 60.0:
            st.error("❌ Roof area exceeds the maximum supported size (60 m²) for our largest 10 kWp system package.")
            return
            
        # Create placeholders for dynamic status updates
        status_text = st.empty()
        progress_bar = st.progress(0)
        

        status_text.info("🔍 Geocoding address into coordinates...")
        latitude, longitude = geocode_address(address)
        progress_bar.progress(20)
        
        status_text.info(f"🛰️ Fetching solar radiation data from NASA API for Lat: {latitude:.4f}, Lon: {longitude:.4f}...")
        
        # Filter system sizes based on roof area
        max_kwp = roof_area / 5
        valid_system_sizes = [s for s in config.SYSTEM_SIZES if s <= max_kwp]
        
        if not valid_system_sizes:
            st.toast("Roof area is small. Defaulting to 3kWp system.", icon="⚠️")
            valid_system_sizes = [3]
        # Step 1: Call NASA API
        nasa_data = fetch_nasa_solar_data(
            latitude=latitude, 
            longitude=longitude, 
            start_year=start_year, 
            end_year=end_year, 
            parameters=config.NASA_PARAMETERS
        )
        progress_bar.progress(50)
    
        status_text.info("⚡ Simulating solar generation and calculating financial metrics...")
        
        # Step 2: Process NASA data
        monthly_df = convert_power_data_to_monthly_dataframe(nasa_data, "Custom Location")
        
        # Step 3: Physics Calculation & Optimization
        generation_df = calculate_all_systems_advanced(
            monthly_df=monthly_df,
            system_sizes=valid_system_sizes
        )
        
        generation_summary_df = build_generation_summary(
            generation_df=generation_df,
            location_name="Custom Location"
        )
        
        # Override Self-Consumption ratios temporarily for this run
        import src.financial
        from src.financial import BatteryScenario
        
        src.financial.BATTERY_SCENARIOS = (
            BatteryScenario(
                option_name="grid_tied_no_battery",
                option_description="Grid-tied without battery storage",
                self_consumption_ratio=grid_tied_ratio,
                has_battery=False,
                cost_ranges=config.GRID_TIED_COST_RANGES,
            ),
            BatteryScenario(
                option_name="hybrid_with_battery",
                option_description="Hybrid with battery storage",
                self_consumption_ratio=hybrid_ratio,
                has_battery=True,
                cost_ranges=config.HYBRID_COST_RANGES,
            ),
        )
        
        # Step 4: Financial Logic Integration
        financial_input_df = build_financial_input(
            location_name="Custom Location",
            monthly_bill_vnd=monthly_bill,
            vat_rate=config.VAT_RATE,
            electricity_tiers=config.ELECTRICITY_TIERS
        )
        
        battery_option_df = compare_battery_options(
            summary_df=generation_summary_df,
            financial_df=financial_input_df,
            location_name="Custom Location"
        )
        
        recommended_df = recommend_best_option(
            option_df=battery_option_df,
            min_generation_ratio=min_gen_ratio,
            max_payback_years=max_payback
        )
        
        progress_bar.progress(100)
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
        st.success("✅ Analysis completed successfully!")

        # --- DISPLAY RESULTS IN 3 TABS ---
        st.header("📋 Comprehensive Analysis Report")
        tab_homeowner, tab_engineer, tab_installer = st.tabs([
            "🏡 1. Homeowner Overview", 
            "💻 2. Engineering & Financial Report", 
            "🛠️ 3. Installer Guide"
        ])
        
        recommended = recommended_df.iloc[0]
        
        # -------------------------------------------------------------
        # TAB 1: HOMEOWNER
        # -------------------------------------------------------------
        with tab_homeowner:
            st.subheader("Your Recommended Solar Setup")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Optimal System Size", f"{recommended['system_kwp']} kWp")
            m2.metric("Est. Investment Cost", f"{recommended['investment_cost']:,.0f} VND")
            m3.metric("Payback Period", f"{recommended['payback_years']:.1f} years")
            m4.metric("Annual Savings", f"{recommended['annual_saving']:,.0f} VND")
            
            st.info(f"**Recommendation Rationale:** {recommended['recommendation_reason']}\n\n**System Architecture:** {recommended['option_description']}")
            
            # Pie Chart: Energy Usage Breakdown
            st.markdown("### ⚡ Where Does Your Solar Energy Go?")
            fig_pie = create_energy_distribution_pie_chart(
                self_used_kwh=recommended['self_used_kwh'],
                unused_exported_kwh=recommended['unused_or_exported_kwh']
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # -------------------------------------------------------------
        # TAB 2: ENGINEER
        # -------------------------------------------------------------
        with tab_engineer:
            st.subheader("Data & Financial Analysis")
            
            # Monthly Generation Bar Chart using Plotly
            st.markdown("#### 📊 Monthly Generation Across System Sizes")
            st.write("Based on real NASA POWER climatic data and physics simulation.")
            fig_bar = create_monthly_generation_bar_chart(generation_df)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Cumulative Cash Flow Line Chart
            st.markdown("#### 📈 Cumulative Cash Flow & Break-even Analysis")
            st.write("Tracing the ROI over 15 years for the recommended system.")
            fig_line = create_cumulative_cash_flow_line_chart(
                investment_cost_vnd=recommended['investment_cost'],
                annual_saving_vnd=recommended['annual_saving']
            )
            st.plotly_chart(fig_line, use_container_width=True)
            
            # Detailed Options Table
            st.markdown("#### 📋 Comparison of All Evaluated Scenarios")
            
            # Make the table more user-friendly
            display_df = battery_option_df[[
                "system_kwp", "option_description", "investment_cost", 
                "monthly_avg_generation_kwh", "annual_saving", "payback_years"
            ]].copy()
            
            display_df.rename(columns={
                "system_kwp": "Size (kWp)",
                "option_description": "System Type",
                "investment_cost_vnd": "Investment (VND)",
                "monthly_generation_kwh": "Monthly Generation (kWh)",
                "annual_saving_vnd": "Annual Savings (VND)",
                "payback_years": "Payback (Years)"
            }, inplace=True)
            
            st.dataframe(display_df.style.format({
                "Investment (VND)": "{:,.0f}",
                "Monthly Generation (kWh)": "{:.1f}",
                "Annual Savings (VND)": "{:,.0f}",
                "Payback (Years)": "{:.1f}"
            }), use_container_width=True, hide_index=True)
            
        # -------------------------------------------------------------
        # TAB 3: INSTALLER
        # -------------------------------------------------------------
        with tab_installer:
            st.subheader("Construction & Installation Blueprint")
            st.write("Technical parameters required for physical installation of the system.")
            
            # Optimal tilt and facing
            optimal_tilt = round(abs(latitude))
            facing_dir = "South" if latitude > 0 else "North"
            
            ic1, ic2 = st.columns(2)
            with ic1:
                st.info(f"**📍 Target Coordinates:** \n\nLatitude: {latitude:.4f}, Longitude: {longitude:.4f}")
                st.info(f"**⚡ Target System Size:** \n\n{recommended['system_kwp']} kWp")
            with ic2:
                st.success(f"**🧭 Optimal Facing Direction:** \n\n{facing_dir}")
                st.success(f"**📐 Optimal Tilt Angle:** \n\n{optimal_tilt} degrees")
                
            st.markdown("""
            > **Note to Installers:**
            > This software is developed for simulation and analysis purposes only. The calculated values are estimates based on provided data and standard physical models.
            > Always perform an on-site assessment and consult with a qualified professional before physical construction.
            """)

if __name__ == "__main__":
    main()