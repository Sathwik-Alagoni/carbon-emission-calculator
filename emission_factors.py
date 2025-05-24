# emission_factors.py

EMISSION_FACTORS_INDIA = {
    "GRID": 0.82,
    "LPG": 2.983,
    "BIOMASS": 0.075,
    "PETROL_CAR": 0.192,
    "DIESEL_CAR": 0.171,
    "CNG": 0.135,
    "EV_CAR": 0.100,
    "PETROL_MOTORBIKE": 0.082,
    "DIESEL_MOTORBIKE": 0.080,
    "EV_MOTORBIKE": 0.050,
    "BUS": 0.089,
    "TRAIN": 0.041,
    "SHORT_FLIGHT": 300,
    "LONG_FLIGHT": 700,
    "Vegan": 1.2,
    "Vegetarian": 1.5,
    "Non-Vegetarian": 2.5,
    "Heavy Meat Eater": 3.0,

    "ORGANIC_DISCOUNT": 0.20,


        # Waste-related factors (kg CO₂e per kg of waste)
    "FOOD_WASTE": 2.0,
    "PLASTIC_WASTE": 6.0,
    "PAPER_WASTE": 1.5,
    "TEXTILE_WASTE": 3.0,
    "E_WASTE": 5.0,

    # Discounts / avoided emissions (fraction)
    # e.g. composting organic waste avoids methane
    "COMPOSTING_DISCOUNT": 0.7,    # 70% reduction if composted
    "RECYCLING_DISCOUNT": 0.5      # 50% reduction if recycled
}

STATE_GRID_EMISSIONS = {
    "Andhra Pradesh": 0.82,
    "Delhi": 0.90,
    "Karnataka": 0.65,
    "Maharashtra": 0.79,
    "Tamil Nadu": 0.63,
    "Telangana": 0.75,
    "Uttar Pradesh": 0.85,
    "Other": 0.82
}