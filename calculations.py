
# calculations.py
from emission_factors import EMISSION_FACTORS_INDIA, STATE_GRID_EMISSIONS

def calculate_home_energy_emissions(state, electricity_kwh, lpg_cylinders, biomass_usage, solar_pct):
    grid_factor = STATE_GRID_EMISSIONS.get(state, EMISSION_FACTORS_INDIA["GRID"])
    effective_kwh = electricity_kwh * (1 - solar_pct / 100)
    electricity_emissions = effective_kwh * grid_factor
    lpg_emissions = lpg_cylinders * EMISSION_FACTORS_INDIA["LPG"]
    biomass_map = {"Never": 0, "Occasionally": 15, "Daily": 30}
    biomass_days = biomass_map.get(biomass_usage, 0)
    biomass_emissions = biomass_days * EMISSION_FACTORS_INDIA["BIOMASS"]
    return electricity_emissions + lpg_emissions + biomass_emissions

def calculate_transport_emissions(vehicle_type, km_personal_weekly, bus_km_weekly, train_km_weekly, short_flights_per_year, long_flights_per_year):
    key_map = {
        "No personal vehicle": None,
        "Petrol Car": "PETROL_CAR",
        "Diesel Car": "DIESEL_CAR",
        "CNG Car": "CNG",
        "EV Car": "EV_CAR",
        "Petrol Bike": "PETROL_MOTORBIKE",
        "Diesel Bike": "DIESEL_MOTORBIKE",
        "EV Bike": "EV_MOTORBIKE"
    }
    factor_key = key_map.get(vehicle_type)
    veh_factor = EMISSION_FACTORS_INDIA.get(factor_key, 0) if factor_key else 0
    personal_emissions = km_personal_weekly * 4.345 * veh_factor
    bus_emissions = bus_km_weekly * 4.345 * EMISSION_FACTORS_INDIA["BUS"]
    train_emissions = train_km_weekly * 4.345 * EMISSION_FACTORS_INDIA["TRAIN"]
    flight_emissions = (short_flights_per_year * EMISSION_FACTORS_INDIA["SHORT_FLIGHT"] + long_flights_per_year * EMISSION_FACTORS_INDIA["LONG_FLIGHT"]) / 12
    return personal_emissions + bus_emissions + train_emissions + flight_emissions

def calculate_diet_emissions(diet_type, meals_per_day, meat_freq_factor, dairy_l_per_day, organic_pct):
    base = EMISSION_FACTORS_INDIA[diet_type]
    diet_em = base * meals_per_day * 30 * (meat_freq_factor if diet_type != "Vegan" else 1)
    dairy_em = dairy_l_per_day * EMISSION_FACTORS_INDIA["Vegan"] * 30
    discount = 1 - (organic_pct / 100) * EMISSION_FACTORS_INDIA["ORGANIC_DISCOUNT"]
    return (diet_em + dairy_em) * discount


def calculate_waste_emissions(
    food_waste_kg,
    plastic_waste_kg,
    paper_waste_kg,
    textile_waste_kg,
    e_waste_kg,
    pct_composted,
    pct_recycled
):
    """
    Returns total monthly waste emissions (kg CO2e) for each category,
    accounting for composting and recycling discounts.
    """
    # Raw emissions
    food_em   = food_waste_kg   * EMISSION_FACTORS_INDIA["FOOD_WASTE"]
    plastic_em = plastic_waste_kg * EMISSION_FACTORS_INDIA["PLASTIC_WASTE"]
    paper_em  = paper_waste_kg  * EMISSION_FACTORS_INDIA["PAPER_WASTE"]
    textile_em = textile_waste_kg * EMISSION_FACTORS_INDIA["TEXTILE_WASTE"]
    ewaste_em = e_waste_kg      * EMISSION_FACTORS_INDIA["E_WASTE"]

    # Apply composting discount to the compostable portion of food waste
    composted_em = (pct_composted / 100) * food_em * (1 - EMISSION_FACTORS_INDIA["COMPOSTING_DISCOUNT"])
    non_composted_em = ((100 - pct_composted) / 100) * food_em

    # Apply recycling discount to the recyclable portion of plastic/paper/textile
    recyc_factor = EMISSION_FACTORS_INDIA["RECYCLING_DISCOUNT"]
    rec_em = (pct_recycled / 100) * (plastic_em + paper_em + textile_em) * (1 - recyc_factor)
    non_rec_em = ((100 - pct_recycled) / 100) * (plastic_em + paper_em + textile_em)

    total = (
        composted_em + non_composted_em
        + rec_em + non_rec_em
        + ewaste_em
    )
    return total
