def calculate_full_estimate(sqft, material, pitch, complexity, floors):

    base_rate = 200  # per sq ft base

    # -------------------
    # MATERIAL COST
    # -------------------
    material_multiplier = {
        "asphalt": 1.0,
        "metal": 1.3,
        "clay": 1.5,
        "flat": 1.1
    }.get(material.lower(), 1.0)

    # -------------------
    # PITCH COST
    # -------------------
    pitch_multiplier = {
        "low": 1.0,
        "medium": 1.2,
        "high": 1.4
    }.get(pitch.lower(), 1.0)

    # -------------------
    # COMPLEXITY COST
    # -------------------
    complexity_multiplier = {
        "simple": 1.0,
        "medium": 1.25,
        "complex": 1.5
    }.get(complexity.lower(), 1.0)

    # -------------------
    # FLOORS COST
    # -------------------
    floor_multiplier = 1 + (floors * 0.1)

    # FINAL CALCULATION
    cost = sqft * base_rate

    cost *= material_multiplier
    cost *= pitch_multiplier
    cost *= complexity_multiplier
    cost *= floor_multiplier

    return int(cost)
