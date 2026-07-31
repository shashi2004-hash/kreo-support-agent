eval_set = [
    # --- Returns & Refunds ---
    {"question": "What is your return policy?", "expected_keywords": ["7 days", "no signs of usage", "original box"]},
    {"question": "Do you offer reverse pickup for returns?", "expected_keywords": ["reverse pickup", "yes"]},
    {"question": "How long does a refund take after return?", "expected_keywords": ["2 to 3 days", "2-3 days"]},
    {"question": "I was charged twice, how do I get a refund?", "expected_keywords": ["refund", "few days"]},
    {"question": "Can I return a used product?", "expected_keywords": ["no", "not accept", "used", "unused"]},

    # --- Shipping ---
    {"question": "How long does delivery take?", "expected_keywords": ["3-5 business days"]},
    {"question": "Do you charge for shipping?", "expected_keywords": ["no", "not charge", "no shipping charges", "free"]},
    {"question": "Can I change my delivery address after ordering?", "expected_keywords": ["yes"]},
    {"question": "Do you offer same-day delivery?", "expected_keywords": ["not same day", "express"]},
    {"question": "How do I track my order?", "expected_keywords": ["tracking link", "email", "whatsapp"]},

    # --- Warranty ---
    {"question": "When does my product warranty start?", "expected_keywords": ["date of delivery", "invoice"]},
    {"question": "Is physical damage covered under warranty?", "expected_keywords": ["not", "physical damage"]},
    {"question": "What if I lost my invoice, can I still claim warranty?", "expected_keywords": ["order", "manufacturing date"]},
    {"question": "Do you have offline service centers?", "expected_keywords": ["no", "whatsapp"]},
    {"question": "Is warranty valid if I bought from a third-party seller?", "expected_keywords": ["official", "not eligible"]},

    # --- Payments ---
    {"question": "What payment methods do you accept?", "expected_keywords": ["credit", "debit", "upi", "net banking"]},
    {"question": "Are there hidden charges?", "expected_keywords": ["no hidden charges", "inclusive"]},
    {"question": "My payment was deducted but I got no order confirmation, what now?", "expected_keywords": ["refunded", "7 business days"]},

    # --- Product: Mirage controller ---
    {"question": "How do I activate Turbo Mode on the Mirage?", "expected_keywords": ["hold", "turbo", "button"]},
    {"question": "How do I reset the Mirage controller?", "expected_keywords": ["l3", "r3", "home", "reset"]},
    {"question": "Can I assign multiple buttons to Turbo Mode?", "expected_keywords": ["yes", "multiple"]},

    # --- Product: Chimera mouse ---
    {"question": "What is the battery life of the Chimera mouse?", "expected_keywords": ["24", "30", "hours", "hrs"]},
    {"question": "Why does the lighting turn off when I move the mouse?", "expected_keywords": ["battery life", "feature"]},
    {"question": "How do I pair the Chimera in Bluetooth mode?", "expected_keywords": ["left click", "scroll", "right click"]},

    # --- Product: Hive keyboard ---
    {"question": "What switches are compatible with the Hive keyboard?", "expected_keywords": ["outemu", "hot-swappable"]},
    {"question": "How do I fix swapped Alt and Windows keys?", "expected_keywords": ["fn", "s", "a"]},

    # --- Contact / General ---
    {"question": "How do I contact Kreo support?", "expected_keywords": ["whatsapp", "9611507877", "help@kreo-tech.com"]},
    {"question": "Do you sell offline?", "expected_keywords": ["online only", "no"]},
    {"question": "Do you offer bulk or corporate orders?", "expected_keywords": ["yes", "bulk"]},

    # --- Should REFUSE / out of scope (tests hallucination) ---
    {"question": "What is the weather today?", "expected_keywords": ["don't have", "contact"]},
    {"question": "Can you recommend a good laptop brand?", "expected_keywords": ["don't have", "contact"]},
    {"question": "What is Kreo's revenue?", "expected_keywords": ["don't have", "contact"]},
]