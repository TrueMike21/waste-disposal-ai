# Maps model output classes → disposal guidance
# Extend this dict as you add more classes

DISPOSAL_RULES = {
    "cardboard": {
        "category": "Recycling ♻️",
        "bin_color": "Blue",
        "instructions": [
            "Flatten all boxes before placing in the recycling bin.",
            "Remove any tape, staples, or plastic liners.",
            "Keep dry — wet cardboard is not recyclable.",
        ],
        "warning": None,
    },
    "glass": {
        "category": "Recycling ♻️",
        "bin_color": "Green / Clear",
        "instructions": [
            "Rinse the container to remove food residue.",
            "Remove lids (recycle metal lids separately).",
            "Do NOT recycle broken glass in curbside bins — wrap in newspaper and place in landfill bag.",
        ],
        "warning": "Broken glass is a safety hazard. Handle with care.",
    },
    "metal": {
        "category": "Recycling ♻️",
        "bin_color": "Blue",
        "instructions": [
            "Rinse cans clean.",
            "Crush cans to save space if your municipality allows it.",
            "Scrap metal and appliances go to a metal recycling depot.",
        ],
        "warning": None,
    },
    "paper": {
        "category": "Recycling ♻️",
        "bin_color": "Blue",
        "instructions": [
            "Shredded paper should be bagged separately (check local rules).",
            "Greasy paper (e.g., pizza boxes) goes in compost or landfill.",
            "Newspapers, magazines, and office paper are fine as-is.",
        ],
        "warning": None,
    },
    "plastic": {
        "category": "Recycling ♻️",
        "bin_color": "Blue",
        "instructions": [
            "Check the recycling number (1–7) on the bottom.",
            "Types 1 (PET) and 2 (HDPE) are widely accepted.",
            "Rinse containers before recycling.",
            "Plastic bags must be returned to store drop-off points — NOT curbside bins.",
        ],
        "warning": "Not all plastics are accepted curbside. Check your local guidelines.",
    },
    "trash": {
        "category": "Landfill 🗑️",
        "bin_color": "Black / Grey",
        "instructions": [
            "Place in your general waste (landfill) bin.",
            "Consider whether any components can be separated for recycling.",
        ],
        "warning": "If item contains batteries or electronics, use e-waste disposal instead.",
    },
    # Extendable categories
    "organic": {
        "category": "Compost 🌱",
        "bin_color": "Green",
        "instructions": [
            "Place in compost bin or green organics cart.",
            "Includes food scraps, coffee grounds, and yard waste.",
            "No meat or dairy in home composters.",
        ],
        "warning": None,
    },
    "battery": {
        "category": "Hazardous Waste ⚠️",
        "bin_color": "N/A — Special Collection",
        "instructions": [
            "Never place in regular bins — fire hazard.",
            "Drop off at a designated battery collection point (hardware stores, councils).",
        ],
        "warning": "Batteries can cause fires in recycling machinery. Dispose responsibly.",
    },
    "e-waste": {
        "category": "E-Waste ⚡",
        "bin_color": "N/A — Special Collection",
        "instructions": [
            "Take to an e-waste depot or retailer take-back program.",
            "Includes phones, computers, TVs, and small appliances.",
        ],
        "warning": "Contains toxic materials. Never landfill electronics.",
    },
}

CONFIDENCE_THRESHOLD = 0.55  # Below this → show low-confidence warning

def get_disposal_guidance(predicted_class: str, confidence: float) -> dict:
    rule = DISPOSAL_RULES.get(predicted_class, None)

    if rule is None:
        return {
            "category": "Unknown",
            "bin_color": "Unknown",
            "instructions": ["We couldn't identify this item. Please check your local council's waste guide."],
            "warning": "Classification failed. Do not guess — incorrect disposal causes contamination.",
            "low_confidence": True,
        }

    result = dict(rule)
    result["predicted_class"] = predicted_class
    result["confidence"] = round(confidence * 100, 1)
    result["low_confidence"] = confidence < CONFIDENCE_THRESHOLD

    if result["low_confidence"]:
        result["warning"] = (
            f"⚠️ Low confidence ({result['confidence']}%). "
            "This prediction may be incorrect. Please verify before disposing."
        )

    return result