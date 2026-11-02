"""Fixed literals for db/seed.sql. No random, no now()."""
from __future__ import annotations

# Week of Monday 2026-11-02 (UTC dates and timestamps).

MENU_ITEMS: list[dict] = [
    # coffee
    {
        "id": "mi_americano",
        "name": "Americano",
        "category": "coffee",
        "price_cents": 350,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_cappuccino",
        "name": "Cappuccino",
        "category": "coffee",
        "price_cents": 420,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_espresso",
        "name": "Espresso",
        "category": "coffee",
        "price_cents": 300,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_flat_white",
        "name": "Flat white",
        "category": "coffee",
        "price_cents": 420,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_latte",
        "name": "Latte",
        "category": "coffee",
        "price_cents": 450,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_mocha",
        "name": "Mocha",
        "category": "coffee",
        "price_cents": 490,
        "vegan": False,
        "gluten_free": False,
    },
    # tea
    {
        "id": "mi_chai",
        "name": "Chai",
        "category": "tea",
        "price_cents": 440,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_earl_grey",
        "name": "Earl grey tea",
        "category": "tea",
        "price_cents": 320,
        "vegan": True,
        "gluten_free": False,
    },
    {
        "id": "mi_english_breakfast",
        "name": "English breakfast tea",
        "category": "tea",
        "price_cents": 320,
        "vegan": True,
        "gluten_free": False,
    },
    {
        "id": "mi_hot_chocolate",
        "name": "Hot chocolate",
        "category": "tea",
        "price_cents": 420,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_matcha",
        "name": "Matcha",
        "category": "tea",
        "price_cents": 480,
        "vegan": True,
        "gluten_free": False,
    },
    # breakfast
    {
        "id": "mi_avocado_toast",
        "name": "Avocado toast",
        "category": "breakfast",
        "price_cents": 1100,
        "vegan": True,
        "gluten_free": False,
    },
    {
        "id": "mi_bacon_egg_roll",
        "name": "Bacon and egg roll",
        "category": "breakfast",
        "price_cents": 950,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_granola_bowl",
        "name": "Granola bowl",
        "category": "breakfast",
        "price_cents": 850,
        "vegan": True,
        "gluten_free": True,
    },
    {
        "id": "mi_sourdough_toast",
        "name": "Sourdough toast with butter",
        "category": "breakfast",
        "price_cents": 550,
        "vegan": False,
        "gluten_free": False,
    },
    # lunch
    {
        "id": "mi_chicken_pesto_toastie",
        "name": "Chicken and pesto toastie",
        "category": "lunch",
        "price_cents": 1250,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_roast_pumpkin_salad",
        "name": "Roast pumpkin salad",
        "category": "lunch",
        "price_cents": 1300,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_soup_of_day",
        "name": "Soup of the day with bread",
        "category": "lunch",
        "price_cents": 1050,
        "vegan": False,
        "gluten_free": False,
    },
    # bakery
    {
        "id": "mi_almond_croissant",
        "name": "Almond croissant",
        "category": "bakery",
        "price_cents": 460,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_banana_bread",
        "name": "Banana bread",
        "category": "bakery",
        "price_cents": 400,
        "vegan": False,
        "gluten_free": True,
    },
    {
        "id": "mi_butter_croissant",
        "name": "Butter croissant",
        "category": "bakery",
        "price_cents": 380,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_cinnamon_bun",
        "name": "Cinnamon bun",
        "category": "bakery",
        "price_cents": 420,
        "vegan": False,
        "gluten_free": False,
    },
    {
        "id": "mi_orange_polenta_cake",
        "name": "Orange polenta cake",
        "category": "bakery",
        "price_cents": 520,
        "vegan": False,
        "gluten_free": True,
    },
]

STOCK_DAY = "2026-11-02"

STOCK: list[dict] = [
    {"item_id": "mi_butter_croissant", "day": STOCK_DAY, "left_count": 6},
    {"item_id": "mi_almond_croissant", "day": STOCK_DAY, "left_count": 2},
    {"item_id": "mi_cinnamon_bun", "day": STOCK_DAY, "left_count": 0},
    {"item_id": "mi_banana_bread", "day": STOCK_DAY, "left_count": 9},
    {"item_id": "mi_sourdough_toast", "day": STOCK_DAY, "left_count": 14},
    {"item_id": "mi_avocado_toast", "day": STOCK_DAY, "left_count": 5},
    {"item_id": "mi_bacon_egg_roll", "day": STOCK_DAY, "left_count": 3},
    {"item_id": "mi_granola_bowl", "day": STOCK_DAY, "left_count": 8},
    {"item_id": "mi_chicken_pesto_toastie", "day": STOCK_DAY, "left_count": 7},
    {"item_id": "mi_roast_pumpkin_salad", "day": STOCK_DAY, "left_count": 4},
    {"item_id": "mi_soup_of_day", "day": STOCK_DAY, "left_count": 10},
]

LOYALTY_CARDS: list[dict] = [
    {"member_id": "M-1182", "stamps": 7},
]

ORDERS: list[dict] = [
    {
        "id": "K-2041",
        "member_id": "M-1182",
        "status": "ready",
        "placed_at": "2026-11-02 08:12:00+00",
        "total_cents": 940,
    },
    {
        "id": "K-2042",
        "member_id": "M-1182",
        "status": "being_made",
        "placed_at": "2026-11-02 08:19:00+00",
        "total_cents": 1480,
    },
    {
        "id": "K-2043",
        "member_id": "M-3301",
        "status": "received",
        "placed_at": "2026-11-02 08:21:00+00",
        "total_cents": 840,
    },
]

ORDER_ITEMS: list[dict] = [
    {
        "order_id": "K-2041",
        "line": 1,
        "item_id": "mi_flat_white",
        "milk": "oat",
        "size": "regular",
        "qty": 1,
        "price_cents": 480,
    },
    {
        "order_id": "K-2041",
        "line": 2,
        "item_id": "mi_almond_croissant",
        "milk": None,
        "size": "regular",
        "qty": 1,
        "price_cents": 460,
    },
    {
        "order_id": "K-2042",
        "line": 1,
        "item_id": "mi_latte",
        "milk": "whole",
        "size": "large",
        "qty": 1,
        "price_cents": 530,
    },
    {
        "order_id": "K-2042",
        "line": 2,
        "item_id": "mi_bacon_egg_roll",
        "milk": None,
        "size": "regular",
        "qty": 1,
        "price_cents": 950,
    },
    {
        "order_id": "K-2043",
        "line": 1,
        "item_id": "mi_chai",
        "milk": None,
        "size": "regular",
        "qty": 1,
        "price_cents": 440,
    },
    {
        "order_id": "K-2043",
        "line": 2,
        "item_id": "mi_banana_bread",
        "milk": None,
        "size": "regular",
        "qty": 1,
        "price_cents": 400,
    },
]

DENTISTS: list[dict] = [
    {"id": "d_jordan_wells", "name": "Jordan Wells", "role": "dentist"},
    {"id": "d_morgan_chen", "name": "Morgan Chen", "role": "dentist"},
    {"id": "d_priya_nair", "name": "Priya Nair", "role": "dentist"},
    {"id": "h_ella_barton", "name": "Ella Barton", "role": "hygienist"},
    {"id": "h_sam_ortiz", "name": "Sam Ortiz", "role": "hygienist"},
]

TREATMENTS: list[dict] = [
    {
        "id": "tr_checkup_clean",
        "name": "Checkup and clean",
        "price_cents": 14500,
        "from_price": False,
        "minutes": 45,
    },
    {
        "id": "tr_child_checkup",
        "name": "Child checkup",
        "price_cents": 7500,
        "from_price": False,
        "minutes": 30,
    },
    {
        "id": "tr_crown",
        "name": "Crown",
        "price_cents": 145000,
        "from_price": True,
        "minutes": 60,
    },
    {
        "id": "tr_filling",
        "name": "Tooth coloured filling",
        "price_cents": 18000,
        "from_price": True,
        "minutes": 45,
    },
    {
        "id": "tr_new_patient_exam",
        "name": "New patient exam",
        "price_cents": 22000,
        "from_price": False,
        "minutes": 60,
    },
    {
        "id": "tr_root_canal",
        "name": "Root canal",
        "price_cents": 95000,
        "from_price": True,
        "minutes": 90,
    },
    {
        "id": "tr_whitening",
        "name": "Teeth whitening",
        "price_cents": 49000,
        "from_price": False,
        "minutes": 90,
    },
]

PATIENTS: list[dict] = [
    {"id": "P-1012", "name": "J. Park", "phone": "555 0103"},
    {"id": "P-1044", "name": "A. Ruiz", "phone": "555 0118"},
    {"id": "P-1066", "name": "L. Ruiz", "phone": "555 0124"},
    {"id": "P-1077", "name": "M. Cole", "phone": "555 0131"},
    {"id": "P-1088", "name": "T. Nguyen", "phone": "555 0146"},
    {"id": "P-1099", "name": "S. Ahmed", "phone": "555 0152"},
]

# starts_at UTC; free set in build from appointments
SLOTS: list[dict] = [
    {
        "id": "sl_20261102_0830_c2",
        "starts_at": "2026-11-02 08:30:00+00",
        "minutes": 60,
        "chair": "2",
        "dentist_id": "d_morgan_chen",
    },
    {
        "id": "sl_20261102_1300_c1",
        "starts_at": "2026-11-02 13:00:00+00",
        "minutes": 30,
        "chair": "1",
        "dentist_id": "h_ella_barton",
    },
    {
        "id": "sl_20261102_1630_c3",
        "starts_at": "2026-11-02 16:30:00+00",
        "minutes": 60,
        "chair": "3",
        "dentist_id": "d_priya_nair",
    },
    {
        "id": "sl_20261103_1000_c1",
        "starts_at": "2026-11-03 10:00:00+00",
        "minutes": 30,
        "chair": "1",
        "dentist_id": "h_ella_barton",
    },
    {
        "id": "sl_20261103_1515_c2",
        "starts_at": "2026-11-03 15:15:00+00",
        "minutes": 60,
        "chair": "2",
        "dentist_id": "d_jordan_wells",
    },
    {
        "id": "sl_20261104_0900_c3",
        "starts_at": "2026-11-04 09:00:00+00",
        "minutes": 60,
        "chair": "3",
        "dentist_id": "d_priya_nair",
    },
    {
        "id": "sl_20261104_1130_c1",
        "starts_at": "2026-11-04 11:30:00+00",
        "minutes": 30,
        "chair": "1",
        "dentist_id": "h_sam_ortiz",
    },
    {
        "id": "sl_20261104_1400_c2",
        "starts_at": "2026-11-04 14:00:00+00",
        "minutes": 30,
        "chair": "2",
        "dentist_id": "d_morgan_chen",
    },
    {
        "id": "sl_20261104_1700_c1",
        "starts_at": "2026-11-04 17:00:00+00",
        "minutes": 60,
        "chair": "1",
        "dentist_id": "d_jordan_wells",
    },
    {
        "id": "sl_20261105_0830_c1",
        "starts_at": "2026-11-05 08:30:00+00",
        "minutes": 30,
        "chair": "1",
        "dentist_id": "h_ella_barton",
    },
    {
        "id": "sl_20261105_1100_c2",
        "starts_at": "2026-11-05 11:00:00+00",
        "minutes": 60,
        "chair": "2",
        "dentist_id": "d_morgan_chen",
    },
    {
        "id": "sl_20261105_1415_c3",
        "starts_at": "2026-11-05 14:15:00+00",
        "minutes": 30,
        "chair": "3",
        "dentist_id": "d_priya_nair",
    },
    {
        "id": "sl_20261105_1645_c1",
        "starts_at": "2026-11-05 16:45:00+00",
        "minutes": 60,
        "chair": "1",
        "dentist_id": "d_jordan_wells",
    },
    {
        "id": "sl_20261106_0930_c2",
        "starts_at": "2026-11-06 09:30:00+00",
        "minutes": 60,
        "chair": "2",
        "dentist_id": "d_morgan_chen",
    },
    {
        "id": "sl_20261106_1345_c1",
        "starts_at": "2026-11-06 13:45:00+00",
        "minutes": 30,
        "chair": "1",
        "dentist_id": "h_sam_ortiz",
    },
    {
        "id": "sl_20261107_0915_c1",
        "starts_at": "2026-11-07 09:15:00+00",
        "minutes": 30,
        "chair": "1",
        "dentist_id": "h_ella_barton",
    },
    {
        "id": "sl_20261107_1100_c2",
        "starts_at": "2026-11-07 11:00:00+00",
        "minutes": 60,
        "chair": "2",
        "dentist_id": "d_jordan_wells",
    },
]

APPOINTMENTS: list[dict] = [
    {
        "id": "B-3107",
        "slot_id": "sl_20261105_1100_c2",
        "patient_id": "P-1044",
        "treatment_id": "tr_checkup_clean",
        "state": "booked",
    },
    {
        "id": "B-3108",
        "slot_id": "sl_20261106_0930_c2",
        "patient_id": "P-1077",
        "treatment_id": "tr_whitening",
        "state": "booked",
    },
]

BOOKED_SLOT_IDS = {a["slot_id"] for a in APPOINTMENTS}
