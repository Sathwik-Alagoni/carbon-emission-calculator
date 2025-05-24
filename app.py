# app.py
import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
from calculations import (
    calculate_home_energy_emissions,
    calculate_transport_emissions,
    calculate_diet_emissions,
    calculate_waste_emissions
)
from emission_factors import EMISSION_FACTORS_INDIA, STATE_GRID_EMISSIONS

st.set_page_config(page_title="Carbon Footprint", page_icon="🌱")
st.title("India Carbon Footprint Calculator")

with st.sidebar:
    household_members = st.number_input("Household members", min_value=1, value=1)

tab_home, tab_transport, tab_diet, tab_waste,tab_results = st.tabs(["🏡 Home", "🚗 Transport", "🥗 Diet & Waste","♻️ Waste", "📊 Results"])

# -- HOME TAB --
with tab_home:
    st.subheader("⚡ Energy Consumption")
    col1, col2 = st.columns(2)
    with col1:
        electricity_kwh = st.number_input("Monthly electricity (kWh)", min_value=0, max_value=2000, value=200)
        lpg_cylinders = st.number_input("LPG cylinders/month", min_value=0, max_value=10, value=1)
        solar_pct = st.slider("Solar generation (% of your electricity)", 0, 100, 0)
    with col2:
        state = st.selectbox("Your State", list(STATE_GRID_EMISSIONS.keys()))
        biomass_usage = st.selectbox("Biomass usage", ["Never", "Occasionally", "Daily"])
    home_emissions = calculate_home_energy_emissions(state, electricity_kwh, lpg_cylinders, biomass_usage, solar_pct)
    st.write(f"🏠 **Home Emissions:** {home_emissions:.1f} kg CO₂e/month (after {solar_pct}% solar offset)")



# -- TRANSPORT TAB --
with tab_transport:
    st.subheader("🚗 Transport")
    # Row 1: Vehicle selection and personal use
    col1, col2 = st.columns(2)
    with col1:
        vehicle_type = st.selectbox("Personal vehicle", [
            "No personal vehicle", "Petrol Car", "Diesel Car", "CNG Car", "EV Car",
            "Petrol Bike", "Diesel Bike", "EV Bike"
        ])
    with col2:
        km_personal_weekly = st.number_input("Km/week (personal)", 0, 2000, 0)
    # Row 2: Public transport
    col3, col4 = st.columns(2)
    with col3:
        bus_km_weekly = st.number_input("Bus km/week", 0, 2000, 0)
    with col4:
        train_km_weekly = st.number_input("Train/Metro km/week", 0, 2000, 0)
    # Row 3: Flights
    col5, col6 = st.columns(2)
    with col5:
        short_flights = st.number_input("Short flights/year", 0, 10, 0)
    with col6:
        long_flights = st.number_input("Long flights/year", 0, 10, 0)
    transport_emissions = calculate_transport_emissions(
        vehicle_type, km_personal_weekly, bus_km_weekly, train_km_weekly, short_flights, long_flights
    )
    st.write(f"🚗 **Transport Emissions:** {transport_emissions:.1f} kg CO₂e/month")

# -- DIET TAB --
with tab_diet:
    st.subheader("🥗 Diet Details")
    diet_options = ["Vegan", "Vegetarian", "Non-Vegetarian", "Heavy Meat Eater"]
    col1, col2 = st.columns(2)
    with col1:
        diet_type = st.selectbox("Diet type", diet_options)
    with col2:
        meals_per_day = st.number_input("Meals per day", 1, 6, 3)

    meat_freq_factor = 0
    if diet_type in ["Non-Vegetarian", "Heavy Meat Eater"]:
        meat_options = {
            "None": 0,
            "Occasional (1–2)": 0.5,
            "Frequent (3–5)": 1.0,
            "Very frequent (6–7)": 1.2
        }
        meat_freq = st.selectbox("Meat/fish meals per week", list(meat_options.keys()))
        meat_freq_factor = meat_options[meat_freq]

    col3, _ = st.columns(2)
    with col3:
        dairy_l_per_day = st.number_input("Dairy (liters/day)", 0.0, 5.0, 0.5, 0.1)

    organic_pct = st.slider("% organic/local sourcing", 0, 100, 20, 5)

    # Calculation
    total_co2e = calculate_diet_emissions(diet_type, meals_per_day, meat_freq_factor, dairy_l_per_day, organic_pct)
    st.write(f"🗓️ **Estimated Monthly Diet Footprint:** `{total_co2e:,.1f} kg CO₂e`")



with tab_waste:
    st.subheader("♻️ Waste Emissions")

    # Group input fields into collapsible sections to reduce scrolling
    with st.expander("🗑️ Waste Quantities", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            food_waste_kg    = st.number_input(
                "Food waste (kg/month)", 0.0, 50.0, 5.0, 0.5
            )
            paper_waste_kg   = st.number_input(
                "Paper waste (kg/month)", 0.0, 50.0, 5.0, 0.5
            )
        with col2:
            plastic_waste_kg = st.number_input(
                "Plastic waste (kg/month)", 0.0, 50.0, 5.0, 0.5
            )
            textile_waste_kg = st.number_input(
                "Textile waste (kg/month)", 0.0, 50.0, 5.0, 0.5
            )
        with col3:
            e_waste_kg       = st.number_input(
                "E-waste (kg/month)", 0.0, 10.0, 0.5, 0.1
            )

    with st.expander("⚙️ Disposal Options", expanded=False):
        pct_composted = st.slider(
            "Percent of food waste composted", 0, 100, 20, 5
        )
        pct_recycled  = st.slider(
            "Percent of plastic/paper/textile recycled", 0, 100, 30, 5
        )

    # Calculation & result
    total_waste_co2e = calculate_waste_emissions(
        food_waste_kg,
        plastic_waste_kg,
        paper_waste_kg,
        textile_waste_kg,
        e_waste_kg,
        pct_composted,
        pct_recycled
    )
    st.write(
        f"♻️ **Estimated Monthly Waste Footprint:** `{total_waste_co2e:,.1f} kg CO₂e`"
    )







with tab_results:
    st.subheader("📊 Total Footprint Summary & Recommendations")

    # Compact layout using expanders and columns
    with st.expander("📈 Your Footprint Breakdown", expanded=True):
        col1, col2 = st.columns([1, 1])
        # Left: metrics
        with col1:
            st.caption(f"🏠 Home: {home_emissions:,.1f} kg CO₂e")
            st.caption(f"🚗 Transport: {transport_emissions:,.1f} kg CO₂e")
            st.caption(f"🥗 Diet: {total_co2e:,.1f} kg CO₂e")
            st.caption(f"♻️ Waste: {total_waste_co2e:,.1f} kg CO₂e")
        # Right: pie chart
        with col2:
            categories = ["Home", "Transport", "Diet", "Waste"]
            user_vals = [home_emissions, transport_emissions, total_co2e, total_waste_co2e]
            fig1, ax1 = plt.subplots()
            ax1.pie(user_vals, labels=categories, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

    with st.expander("📊 Total vs National Average & Trees", expanded=False):
        # Prepare data
        national_averages = [750.0, 350.0, 800.0, 100.0]
        total_user = sum(user_vals)
        total_national = sum(national_averages)
        df_total = pd.DataFrame({"You": [total_user], "Indian Average": [total_national]}, index=["Annual Total (kg CO₂e)"])
        # Show bar chart and tree offset side by side
        col3, col4 = st.columns(2)
        with col3:
            st.bar_chart(df_total)
        with col4:
            # Trees needed
            trees_needed = (total_user) / 22
            st.metric(label="🌳 Trees Needed (annual)", value=f"{trees_needed:.0f}")
            st.caption("Assumes each tree absorbs ~22 kg CO₂/year.")

    with st.expander("📝 Personal Recommendations", expanded=False):
        national_averages_map = dict(zip(categories, national_averages))
        for cat, you in zip(categories, user_vals):
            avg = national_averages_map[cat]
            if you > avg:
                diff = you - avg
                st.markdown(f"**{cat}:** You're ~{diff:,.1f} kg CO₂e above average. Aim to cut 10–20%.")
            else:
                st.markdown(f"**{cat}:** Great! You're ~{avg - you:,.1f} kg CO₂e below average.")
        st.info(
            "💡 **Tip:** Carpool or public transit for transport; swap one meat meal/week; compost organic waste and recycle plastics."
        )
