TRAVELER_MODEL = "gemini-2.5-flash"
VERIFIER_MODEL = "gemini-2.5-pro"
NOT_FOUND_ERROR_INSTRUCTION = "Try to answer without it. If you cant, ask the user to provide more information in his question."
ALLOWED_KINDS = {
    "restaurants", "cafes", "pubs", "bars", "malls",
    "natural", "beaches", "waterfalls", "nature_reserves", "volcanoes", "caves", "mountain_peaks",
    "museums", "art_galleries", "theatres_and_entertainments", "sculptures", "gardens_and_parks",
    "aquariums", "zoos", "castles", "historic_districts", "monuments", "archaeology", "pyramids",
    "battlefields", "churches", "mosques", "synagogues", "hindu_temples", "monasteries", "towers",
    "bridges", "lighthouses", "skyscrapers", "palaces", "amusement_parks", "water_parks", "cinemas",
    "nightclubs", "view_points", "sundials", "unclassified_objects"
}

PACKING_LIST_EXAMPLE = {
    "clothing": [
        "Mixed short and long-sleeved shirts",
        "Light jacket or sweater",
        "Jeans or trousers",
        "Comfortable walking shoes",
        "Small, foldable umbrella",
        "Sunglasses"
    ],
    "toiletries_personal": [
        "Sunscreen",
        "Lip balm",
        "Hand sanitizer"
    ],
    "essentials": [
        "Passport/Visa",
        "UK-compatible power adapter (Type G)",
        "Portable charger",
        "Local currency/credit cards"
    ]
}
