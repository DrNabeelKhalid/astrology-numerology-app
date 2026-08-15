"""
Numerology Calculation Engine
Supports Pythagorean (1-9) & Chaldean (1-8) systems, Master Numbers (11, 22, 33),
Life Path, Expression, Soul Urge, Personality, Birthday, and Personal Year cycles.
"""

from typing import Dict, Any, List

PYTHAGOREAN_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

CHALDEAN_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5, 'I': 1,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2,
    'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5, 'Y': 1, 'Z': 7
}

VOWELS = set('AEIOU')

MEANINGS = {
    1: {
        "title": "The Independent Leader & Pioneer",
        "keywords": ["Leadership", "Originality", "Ambition", "Independence", "Innovation"],
        "description": "Number 1 represents drive, courage, and self-reliance. You are a natural pioneer motivated to forge new paths and take bold initiative."
    },
    2: {
        "title": "The Intuitive Diplomat & Peacemaker",
        "keywords": ["Harmony", "Cooperation", "Intuition", "Empathy", "Balance"],
        "description": "Number 2 embodies sensitivity, teamwork, and emotional intelligence. You excel at unifying people and mediating solutions."
    },
    3: {
        "title": "The Creative Communicator & Expresser",
        "keywords": ["Creativity", "Optimism", "Self-Expression", "Joy", "Artistic Vision"],
        "description": "Number 3 radiates charisma, artistic inspiration, and magnetic communication. You bring joy, enthusiasm, and light to others."
    },
    4: {
        "title": "The Master Builder & Architect",
        "keywords": ["Stability", "Discipline", "Order", "Pragmatism", "Perseverance"],
        "description": "Number 4 stands for solid foundations, structure, and reliable execution. You turn ambitious blueprints into lasting realities."
    },
    5: {
        "title": "The Freedom Seeker & Explorer",
        "keywords": ["Freedom", "Adaptability", "Adventure", "Versatility", "Curiosity"],
        "description": "Number 5 thrives on change, dynamic experiences, and uninhibited exploration. You learn through direct life immersion."
    },
    6: {
        "title": "The Nurturing Guardian & Healer",
        "keywords": ["Responsibility", "Compassion", "Community", "Harmony", "Healing"],
        "description": "Number 6 represents unconditional love, service, and protective harmony. You build supportive, beautiful environments."
    },
    7: {
        "title": "The Mystical Truth Seeker & Analyst",
        "keywords": ["Wisdom", "Introspection", "Analysis", "Spiritual Depth", "Intuition"],
        "description": "Number 7 searches beneath the surface for universal truths. You possess keen analytical power and deep contemplative intuition."
    },
    8: {
        "title": "The Powerhouse Manifestor & Executive",
        "keywords": ["Abundance", "Authority", "Vision", "Mastery", "Achievement"],
        "description": "Number 8 governs material mastery, executive decision-making, and financial flow. You possess great stamina and goal focus."
    },
    9: {
        "title": "The Compassionate Universalist & Visionary",
        "keywords": ["Global Wisdom", "Humanitarianism", "Transformation", "Generosity", "Completion"],
        "description": "Number 9 embodies universal brotherhood, selfless wisdom, and spiritual completion. You inspire cosmic empathy and elevation."
    },
    11: {
        "title": "Master Number 11: The Illuminated Catalyst",
        "keywords": ["Spiritual Vision", "Intuitive Flash", "Inspiration", "Higher Consciousness"],
        "description": "Master Number 11 is the Illuminator. You possess psychic sensitivity, high spiritual perception, and the power to awaken others."
    },
    22: {
        "title": "Master Number 22: The Master Architect",
        "keywords": ["Global Blueprint", "Practical Vision", "Legacy Creation", "Manifestation"],
        "description": "Master Number 22 bridges high spiritual vision with concrete physical realization. You can build large-scale systems for world benefit."
    },
    33: {
        "title": "Master Number 33: The Master Teacher & Healer",
        "keywords": ["Cosmic Love", "Spiritual Elevation", "Selfless Service", "Mastery of Compassion"],
        "description": "Master Number 33 represents the height of spiritual devotion and unconditional love, guiding humanity toward universal healing."
    }
}

CHALDEAN_COMPOUND_MEANINGS = {
    10: {"name": "Wheel of Fortune", "nature": "Ultra Favorable", "vibe": "Honor, faith, self-confidence, and rising fortune. Highly auspicious for name correction."},
    11: {"name": "Clenched Fist", "nature": "Challenging", "vibe": "Warning of hidden secret enemies, betrayal, trials, and emotional conflicts. Avoid for names."},
    12: {"name": "The Sacrifice / Victim", "nature": "Challenging", "vibe": "Anxiety, self-sacrifice for others, and being victimized by external plans. Avoid for business names."},
    13: {"name": "Rebirth & Transformation", "nature": "Neutral", "vibe": "Symbol of power and upheaval. Demands wise governance; brings major life transformations."},
    14: {"name": "Movement & Commercial Drive", "nature": "Favorable", "vibe": "Magnetic communication, commercial travel, dealing with mass public, though requires financial prudence."},
    15: {"name": "The Magus of High Magnetism", "nature": "Ultra Favorable", "vibe": "Supreme magnetic charm, eloquence, artistic gift, luxury, and attracting influential patrons."},
    16: {"name": "The Shattered Citadel", "nature": "Challenging", "vibe": "Warning of sudden shocks, downfall of pride, or unexpected obstacles. Avoid for name spellings."},
    17: {"name": "The Star of the Magi", "nature": "Ultra Favorable", "vibe": "Immortal hope, high spiritual protection, rising fame, and supreme victory over obstacles."},
    18: {"name": "Spiritual & Material Conflict", "nature": "Challenging", "vibe": "Warning of family friction, deception, or business intrigue. Requires strict ethics."},
    19: {"name": "Prince of Heaven", "nature": "Ultra Favorable", "vibe": "One of the luckiest numbers! Bestows honor, success, happiness, esteem, and high fulfillment."},
    20: {"name": "The Awakening", "nature": "Favorable", "vibe": "Call to higher purpose, awakening of latent talents, public recognition, and noble duty."},
    21: {"name": "Crown of the Magi", "nature": "Ultra Favorable", "vibe": "Supreme advancement, victory, general success, and honors achieved after dedicated effort."},
    22: {"name": "Master Architect / Caution", "nature": "Neutral", "vibe": "High visionary power, but warns of false friends or misplaced trust if ungrounded."},
    23: {"name": "Royal Star of the Lion", "nature": "Ultra Favorable", "vibe": "Supreme protection and luck! Promises success in commercial, legal, and public enterprise."},
    24: {"name": "Love, Money & Favor", "nature": "Ultra Favorable", "vibe": "Attracts key support from high authority, wealth, romantic happiness, and executive favor."},
    25: {"name": "Wisdom Through Experience", "nature": "Favorable", "vibe": "Gained through trial and observation. Excellent for scientific research, analysis, and intellect."},
    26: {"name": "Partnership Warning", "nature": "Challenging", "vibe": "Warns of financial speculation risks and unreliable business partners. Requires strict audit."},
    27: {"name": "The Scepter of Authority", "nature": "Ultra Favorable", "vibe": "Command, creative brilliance, executive power, and leadership in state or enterprise."},
    28: {"name": "Trust & Reorganization", "nature": "Neutral", "vibe": "High potential, but warns of starting over if trust is given blindly to unverified associates."},
    29: {"name": "Uncertainty & Trials", "nature": "Challenging", "vibe": "Warning of unexpected trials, emotional deception, or ungrounded expectations."},
    30: {"name": "The Lonely Scholar", "nature": "Favorable", "vibe": "Intellectual superiority, artistic creation, research, and independent philosophical work."},
    31: {"name": "The Isolated Visionary", "nature": "Neutral", "vibe": "Deep mental brilliance, self-contained, prefers working independently away from public crowds."},
    32: {"name": "Dynamic Commercial Synergy", "nature": "Ultra Favorable", "vibe": "High popularity, mass media success, commercial prosperity, and international trade luck."},
    33: {"name": "Master Teacher & Healing Light", "nature": "Ultra Favorable", "vibe": "Cosmic aura, high public honor, financial abundance, and supreme spiritual/creative influence."},
    34: {"name": "Grounded Realization", "nature": "Favorable", "vibe": "Hard work in early years leading to steady financial security, wisdom, and technical mastery."},
    35: {"name": "Financial Prudence", "nature": "Neutral", "vibe": "Warns against hasty financial speculation; rewards systematic accumulation and steady effort."},
    36: {"name": "Genius Through Effort", "nature": "Favorable", "vibe": "High creative authority, intellectual leadership, and success achieved through hard work."},
    37: {"name": "Friendly Partnerships & Fortune", "nature": "Ultra Favorable", "vibe": "Supreme luck in business partnerships, love, public enterprise, and financial abundance."},
    38: {"name": "Intuitive Caution", "nature": "Neutral", "vibe": "Strong artistic and intuitive gifts, though requires verification of commercial partnerships."},
    39: {"name": "Intellectual Fame", "nature": "Favorable", "vibe": "High mental activity, literature, journalism, public speaking, and health improvement."},
    40: {"name": "Solitude & Introspection", "nature": "Neutral", "vibe": "Focus on spiritual study, introspection, and quiet work away from chaotic public arenas."},
    41: {"name": "Success in Enterprise", "nature": "Ultra Favorable", "vibe": "High commercial luck, leadership, administration, executive power, and wealth growth."},
    42: {"name": "Harmonious Relationships", "nature": "Ultra Favorable", "vibe": "Attracts supportive partnerships, luxury, artistic success, and romantic peace."},
    43: {"name": "Unconventional Path", "nature": "Neutral", "vibe": "Brings unique career pivots and non-traditional success, requiring mental adaptability."},
    44: {"name": "Master Executive", "nature": "Favorable", "vibe": "Tremendous stamina, building physical and corporate infrastructure, lasting security."},
    45: {"name": "Great Fortunes Through Enterprise", "nature": "Ultra Favorable", "vibe": "High commercial prosperity, public recognition, international trade, and wealth."},
    46: {"name": "Crown of Accomplishment", "nature": "Ultra Favorable", "vibe": "High executive power, fame, authority, and financial accomplishment."},
    47: {"name": "Intuitive Mastery", "nature": "Favorable", "vibe": "Deep wisdom, spiritual insight, analytical brilliance, and inner peace."},
    48: {"name": "Pragmatic Governance", "nature": "Favorable", "vibe": "Orderly management, law, corporate structure, and steady wealth accumulation."},
    49: {"name": "Global Visionary", "nature": "Favorable", "vibe": "Humanitarian leadership, international connections, and public influence."},
    50: {"name": "Commercial Expansion", "nature": "Ultra Favorable", "vibe": "High mobility, commercial trade, quick thinking, and financial growth."},
    51: {"name": "Warrior of Victory", "nature": "Ultra Favorable", "vibe": "High courage, military/corporate command, swift execution, and victorious leadership."},
    52: {"name": "Wisdom & Faith", "nature": "Favorable", "vibe": "Overcoming obstacles through faith, strategic intellect, and spiritual integrity."}
}

PLANETARY_FRIENDSHIP_MATRIX = {
    1: {"friends": {1, 2, 3, 5, 9}, "enemies": {4, 8}, "neutrals": {6, 7}}, # Sun
    2: {"friends": {1, 2, 3, 5}, "enemies": {4, 8, 9}, "neutrals": {6, 7}}, # Moon
    3: {"friends": {1, 2, 3, 5, 7, 9}, "enemies": {6}, "neutrals": {4, 8}}, # Jupiter
    4: {"friends": {1, 5, 6, 7}, "enemies": {2, 4, 8, 9}, "neutrals": {3}}, # Rahu
    5: {"friends": {1, 2, 3, 5, 6, 7, 8, 9}, "enemies": set(), "neutrals": set()}, # Mercury (Universal Friend)
    6: {"friends": {1, 5, 6, 7}, "enemies": {3}, "neutrals": {2, 4, 8, 9}}, # Venus
    7: {"friends": {1, 3, 5, 6}, "enemies": {2, 4, 8, 9}, "neutrals": {7}}, # Ketu
    8: {"friends": {3, 5, 6}, "enemies": {1, 2, 4, 8, 9}, "neutrals": {7}}, # Saturn
    9: {"friends": {1, 3, 5, 9}, "enemies": {2, 4, 8}, "neutrals": {6, 7}} # Mars
}


def reduce_number(val: int, keep_master: bool = True) -> int:
    """Reduces a number to a single digit (1-9) or Master Number (11, 22, 33)."""
    while val > 9:
        if keep_master and val in (11, 22, 33):
            return val
        val = sum(int(digit) for digit in str(val))
    return val


def get_reduction_steps(val: int, keep_master: bool = True) -> List[int]:
    """Returns step-by-step reduction array for UI animation."""
    steps = [val]
    current = val
    while current > 9:
        if keep_master and current in (11, 22, 33):
            break
        current = sum(int(digit) for digit in str(current))
        steps.append(current)
    return steps


def calculate_life_path(year: int, month: int, day: int) -> Dict[str, Any]:
    """Calculates Life Path Number from DOB (Year, Month, Day)."""
    reduced_m = reduce_number(month)
    reduced_d = reduce_number(day)
    reduced_y = reduce_number(year)

    raw_sum = reduced_m + reduced_d + reduced_y
    final_number = reduce_number(raw_sum)
    steps = get_reduction_steps(raw_sum)

    return {
        "number": final_number,
        "raw_sum": raw_sum,
        "steps": steps,
        "meaning": MEANINGS.get(final_number, MEANINGS[1])
    }


def is_vowel_char(char: str, prev_char: str = "", next_char: str = "", is_end: bool = False) -> bool:
    c = char.upper()
    if c in ('A', 'E', 'I', 'O', 'U'):
        return True
    if c == 'Y':
        if prev_char and prev_char.upper() not in ('A', 'E', 'I', 'O', 'U', 'Y'):
            return True
        if is_end and prev_char and prev_char.upper() not in ('A', 'E', 'I', 'O', 'U'):
            return True
    return False


def calculate_name_numbers(full_name: str, system: str = "pythagorean") -> Dict[str, Any]:
    """
    Calculates Expression, Soul Urge, and Personality numbers
    for a given name string using Pythagorean or Chaldean mappings,
    with authentic vowel/consonant classification and compound number meanings.
    """
    mapping = CHALDEAN_MAP if system.lower() == "chaldean" else PYTHAGOREAN_MAP
    clean_name = "".join(c.upper() for c in full_name if c.isalpha())

    expression_total = 0
    soul_urge_total = 0
    personality_total = 0

    letter_breakdown = []
    n_len = len(clean_name)

    for idx, char in enumerate(clean_name):
        val = mapping.get(char, 0)
        prev_char = clean_name[idx - 1] if idx > 0 else ""
        next_char = clean_name[idx + 1] if idx < n_len - 1 else ""
        is_end = (idx == n_len - 1)

        is_vowel = is_vowel_char(char, prev_char, next_char, is_end)
        expression_total += val
        if is_vowel:
            soul_urge_total += val
        else:
            personality_total += val

        letter_breakdown.append({
            "char": char,
            "val": val,
            "type": "Vowel" if is_vowel else "Consonant"
        })

    expr_num = reduce_number(expression_total)
    soul_num = reduce_number(soul_urge_total) if soul_urge_total > 0 else 0
    pers_num = reduce_number(personality_total) if personality_total > 0 else 0

    compound_info = CHALDEAN_COMPOUND_MEANINGS.get(expression_total, {
        "name": f"Compound #{expression_total}",
        "nature": "Favorable" if expr_num in (1, 3, 5, 6) else "Neutral",
        "vibe": f"Vibration of Single Digit #{expr_num}."
    })

    return {
        "system": system.capitalize(),
        "compound_number": expression_total,
        "compound_meaning": compound_info,
        "expression": {
            "number": expr_num,
            "raw_sum": expression_total,
            "steps": get_reduction_steps(expression_total),
            "meaning": MEANINGS.get(expr_num, MEANINGS[1])
        },
        "soul_urge": {
            "number": soul_num,
            "raw_sum": soul_urge_total,
            "steps": get_reduction_steps(soul_urge_total) if soul_urge_total > 0 else [0],
            "meaning": MEANINGS.get(soul_num, MEANINGS[2])
        },
        "personality": {
            "number": pers_num,
            "raw_sum": personality_total,
            "steps": get_reduction_steps(personality_total) if personality_total > 0 else [0],
            "meaning": MEANINGS.get(pers_num, MEANINGS[4])
        },
        "letter_breakdown": letter_breakdown
    }


def calculate_personal_year(birth_month: int, birth_day: int, target_year: int) -> Dict[str, Any]:
    """Calculates Personal Year Number for a given target year."""
    reduced_m = reduce_number(birth_month)
    reduced_d = reduce_number(birth_day)
    reduced_y = reduce_number(target_year)

    total = reduced_m + reduced_d + reduced_y
    personal_year_num = reduce_number(total, keep_master=False)

    return {
        "target_year": target_year,
        "personal_year_number": personal_year_num,
        "meaning": MEANINGS.get(personal_year_num, MEANINGS[1])
    }


def calculate_kua_number(year: int, gender: str = "male") -> int:
    """Calculates Feng Shui / Vedic Kua Number from birth year and gender."""
    year_sum = sum(int(d) for d in str(year))
    while year_sum > 9:
        year_sum = sum(int(d) for d in str(year_sum))

    gender_clean = gender.lower()
    if year < 2000:
        if gender_clean in ("female", "f"):
            kua = year_sum + 4
        else:
            kua = 11 - year_sum
    else:  # Born 2000 or later
        if gender_clean in ("female", "f"):
            kua = year_sum + 6
        else:
            kua = 10 - year_sum

    while kua > 9:
        kua = sum(int(d) for d in str(kua))
    if kua <= 0:
        kua = 9
    return kua


def calculate_loshu_grid(day: int, month: int, year: int, gender: str = "male") -> Dict[str, Any]:
    """
    Calculates 100% mathematically precise 3x3 Lo Shu Magic Square Grid.
    Supports Pure DOB Grid and Full Vedic Grid (DOB + Driver + Conductor + Kua).
    Matrix Layout:
      [4 - Wood]  [9 - Fire]  [2 - Earth]   <- Mental Plane
      [3 - Wood]  [5 - Earth] [7 - Metal]   <- Emotional Plane
      [8 - Earth] [1 - Water] [6 - Metal]   <- Practical Plane
    """
    # 1. Extract pure non-zero DOB digits
    dob_digits = []
    for num_val in (day, month, year):
        for ch in str(num_val):
            if ch != '0':
                dob_digits.append(int(ch))

    # 2. Driver / Mulank (Day reduced to single digit)
    driver = day
    while driver > 9:
        driver = sum(int(d) for d in str(driver))

    # 3. Conductor / Bhagyank (Sum of all DOB digits reduced to single digit)
    total_dob_sum = sum(int(d) for d in f"{day:02d}{month:02d}{year:04d}")
    conductor = total_dob_sum
    while conductor > 9:
        conductor = sum(int(d) for d in str(conductor))

    # 4. Kua Number
    kua = calculate_kua_number(year, gender)

    # 5. Full Vedic Grid numbers = Pure DOB digits + Driver + Conductor + Kua
    full_vedic_numbers = dob_digits + [driver, conductor, kua]

    # Frequency counts
    dob_counts = {n: dob_digits.count(n) for n in range(1, 10)}
    vedic_counts = {n: full_vedic_numbers.count(n) for n in range(1, 10)}

    def build_grid_matrix(counts_map):
        return [
            [
                {"num": 4, "element": "Wood", "plane": "Mental", "count": counts_map[4], "str": "4" * counts_map[4] if counts_map[4] > 0 else ""},
                {"num": 9, "element": "Fire", "plane": "Mental", "count": counts_map[9], "str": "9" * counts_map[9] if counts_map[9] > 0 else ""},
                {"num": 2, "element": "Earth", "plane": "Mental", "count": counts_map[2], "str": "2" * counts_map[2] if counts_map[2] > 0 else ""}
            ],
            [
                {"num": 3, "element": "Wood", "plane": "Emotional", "count": counts_map[3], "str": "3" * counts_map[3] if counts_map[3] > 0 else ""},
                {"num": 5, "element": "Earth", "plane": "Emotional", "count": counts_map[5], "str": "5" * counts_map[5] if counts_map[5] > 0 else ""},
                {"num": 7, "element": "Metal", "plane": "Emotional", "count": counts_map[7], "str": "7" * counts_map[7] if counts_map[7] > 0 else ""}
            ],
            [
                {"num": 8, "element": "Earth", "plane": "Practical", "count": counts_map[8], "str": "8" * counts_map[8] if counts_map[8] > 0 else ""},
                {"num": 1, "element": "Water", "plane": "Practical", "count": counts_map[1], "str": "1" * counts_map[1] if counts_map[1] > 0 else ""},
                {"num": 6, "element": "Metal", "plane": "Practical", "count": counts_map[6], "str": "6" * counts_map[6] if counts_map[6] > 0 else ""}
            ]
        ]

    # Evaluate Yogas on full Vedic grid
    c = vedic_counts
    planes = {
        "Mental Plane (4-9-2)": {
            "present": c[4] > 0 and c[9] > 0 and c[2] > 0,
            "desc": "Sharpe memory, intellectual speed, and high analytical power."
        },
        "Emotional / Soul Plane (3-5-7)": {
            "present": c[3] > 0 and c[5] > 0 and c[7] > 0,
            "desc": "Deep intuition, emotional balance, and spiritual empathy."
        },
        "Practical Plane (8-1-6)": {
            "present": c[8] > 0 and c[1] > 0 and c[6] > 0,
            "desc": "Strong physical execution, financial management, and hard work."
        },
        "Thought / Vision Plane (4-3-8)": {
            "present": c[4] > 0 and c[3] > 0 and c[8] > 0,
            "desc": "Strategic foresight, structured planning, and logical analysis."
        },
        "Willpower / Determination Plane (9-5-1)": {
            "present": c[9] > 0 and c[5] > 0 and c[1] > 0,
            "desc": "Unshakable persistence, leadership drive, and resilience under pressure."
        },
        "Action Plane (2-7-6)": {
            "present": c[2] > 0 and c[7] > 0 and c[6] > 0,
            "desc": "Immediate execution, practical drive, and swift physical implementation."
        },
        "Golden Raj Yoga / Success Line (4-5-6)": {
            "present": c[4] > 0 and c[5] > 0 and c[6] > 0,
            "desc": "Supreme Raj Yoga bringing financial prosperity, high status, and luxury."
        },
        "Silver Earth / Property Line (2-5-8)": {
            "present": c[2] > 0 and c[5] > 0 and c[8] > 0,
            "desc": "Strong affinity for real estate accumulation, property growth, and stability."
        }
    }

    # Exhaustive Lo Shu Grid In-Depth Cell Analysis Matrix (Numbers 1 - 9)
    CELL_NUM_DETAILS = {
        1: {
            "name": "Number 1 — Water Element (North Zone)",
            "ruling_planet": "Sun (Surya) / Water Energy",
            "archetype": "Communication, Self-Expression, Ambition & Life Career Path",
            "direction": "North Zone (Feng Shui Water Element)",
            "associated_planes": ["Practical Plane (8-1-6)", "Willpower Plane (9-5-1)"],
            "personality_impact": "Governs how clearly you articulate your inner truth, stand in personal independence, and navigate public career endeavors. Number 1 represents the flow of verbal confidence, clarity of thought, and self-belief.",
            "career_and_wealth": "Essential for public speaking, media, executive leadership, sales, and independent entrepreneurship. Strong 1 energy creates natural leaders who stand out in competitive career landscapes.",
            "relationship_dynamics": "Influences emotional openness in conversation. Balanced 1 fosters active listening and empathetic dialogue, whereas missing 1 creates internal suppression and over-repetition leads to dominating talk.",
            "health_and_vitality": "Governs the circulatory system, vocal cords, kidneys, and fluid balance. Stress manifests as vocal strain or kidney energy exhaustion.",
            "detailed_frequencies": {
                0: "0x (Missing Number 1): Great difficulty expressing personal emotions or speaking up for oneself. May struggle to articulate true desires, experience stage fright, or feel directionless regarding career ambitions. Essential to practice assertive communication.",
                1: "1x (Single Occurrence): Balanced verbal expression. You are an empathetic listener who speaks with clarity, honesty, and composure. You express thoughts without overwhelming others and enjoy steady career growth.",
                2: "2x (Double Occurrence - 11): Heightened eloquence and intuitive communication. Highly articulate, persuasive, and able to understand subtle emotional cues in conversation. Excellent for writers, speakers, and diplomats.",
                3: "3x (Triple Occurrence - 111): Energetic, talkative, and vibrant communicator. Loves sharing ideas, commanding attention in social groups, and expressing thoughts passionately. Must practice active listening so others can speak.",
                4: "4x+ (Quadruple or Higher - 1111+): Intense verbal energy creating a complex inner world. May oscillate between extreme chattiness and deep introspective silence. Highly sensitive to criticism, requiring grounding outlets like creative writing."
            },
            "remedy_suite": {
                "gemstone_and_color": "Aquamarine, Lapis Lazuli, Blue Topaz. Wearing Navy Blue, Royal Blue, or Black.",
                "fengshui_placement": "Place a small indoor water fountain, aquarium, or a clear water glass bowl in the North zone of your room.",
                "daily_affirmation": "'I speak my truth with clarity, confidence, and calm authority.'"
            }
        },
        2: {
            "name": "Number 2 — Earth Element (Southwest Zone)",
            "ruling_planet": "Moon (Chandra) / Earth Energy",
            "archetype": "Intuition, Emotional Sensitivity, Diplomacy & Partnership Harmony",
            "direction": "Southwest Zone (Feng Shui Earth Element)",
            "associated_planes": ["Mental Plane (4-9-2)", "Action Plane (2-7-6)", "Silver Property Line (2-5-8)"],
            "personality_impact": "Governs psychic intuition, emotional intelligence, cooperation, and artistic sensitivity. Number 2 is the peacemaker digit that senses hidden feelings and creates deep interpersonal bonds.",
            "career_and_wealth": "Key digit for counseling, human resources, diplomacy, psychology, fine arts, and team-based business ventures. Brings wealth through real estate partnerships and long-term client trust.",
            "relationship_dynamics": "The ultimate partnership number. Ensures deep empathy, tenderness, and marital stability. When missing, relationships feel cold or hasty; when balanced, it forms lifelong harmonious bonds.",
            "health_and_vitality": "Governs the nervous system, digestive stomach lining, and fluid retention. Emotional stress directly impacts digestion and anxiety levels.",
            "detailed_frequencies": {
                0: "0x (Missing Number 2): May lack emotional patience, struggle with empathy, or find it hard to trust partners. Tendency to act impetuously without consulting others. Needs to cultivate emotional sensitivity.",
                1: "1x (Single Occurrence): Balanced intuition and tact. Gentle, cooperative, considerate, and able to resolve conflicts peacefully. Possesses good instinct regarding people's true intentions.",
                2: "2x (Double Occurrence - 22): Exceptional psychic intuition and acute sensitivity. Deeply empathetic, absorbs ambient energies easily, and possesses brilliant emotional intelligence. Natural counselor or artist.",
                3: "3x+ (Triple or Higher - 222+): Hyper-sensitive emotional radar. Can easily feel overwhelmed by negative environments or public crowds. Needs frequent solitary rest, meditation, and strong energetic boundaries."
            },
            "remedy_suite": {
                "gemstone_and_color": "Rose Quartz, Moonstone, Pearl. Wearing Soft Pink, Cream, or Earthy Ochre.",
                "fengshui_placement": "Keep a pair of Rose Quartz mandarin ducks, earthen clay pottery, or a pink crystal sphere in the Southwest corner.",
                "daily_affirmation": "'I am emotionally grounded, intuitive, and peacefully aligned in all relationships.'"
            }
        },
        3: {
            "name": "Number 3 — Wood Element (East Zone)",
            "ruling_planet": "Jupiter (Guru) / Wood Energy",
            "archetype": "Intellect, Knowledge, Optimism, Memory & Family Harmony",
            "direction": "East Zone (Feng Shui Wood Element)",
            "associated_planes": ["Emotional Plane (3-5-7)", "Thought Plane (4-3-8)"],
            "personality_impact": "Governs intellectual capacity, analytical memory, academic drive, and inherent optimism. Number 3 represents the expanding mind, wisdom, and enthusiasm for lifelong learning.",
            "career_and_wealth": "Crucial for teaching, law, publishing, research, software logic, finance, and creative writing. High 3 presence attracts mentors and academic success.",
            "relationship_dynamics": "Brings joy, intellectual camaraderie, and humor to family life. Helps resolve disputes through wise advice and constructive dialogue.",
            "health_and_vitality": "Governs the liver, gallbladder, nervous system focus, and brain memory centers. Over-intellectualizing can cause insomnia or mental exhaustion.",
            "detailed_frequencies": {
                0: "0x (Missing Number 3): Difficulty maintaining consistent optimism or self-confidence during setbacks. May struggle with academic focus, poor memory retention, or feeling intellectually underrated.",
                1: "1x (Single Occurrence): Excellent memory, positive outlook, sharp analytical mind, and natural intellectual curiosity. Learns quickly and communicates ideas logically.",
                2: "2x (Double Occurrence - 33): Outstanding literary and creative imagination. Brilliant mental focus, artistic flair, and original storytelling ability. Highly suited for authors, lawyers, and teachers.",
                3: "3x+ (Triple or Higher - 333+): Hyper-creative, restless intellect. Mind runs continuously with multiple ideas, making it hard to relax. Requires structured creative discipline to avoid mental burnout."
            },
            "remedy_suite": {
                "gemstone_and_color": "Green Aventurine, Emerald, Yellow Sapphire. Wearing Bright Green or Golden Yellow.",
                "fengshui_placement": "Keep healthy green indoor plants (like Jade or Peace Lily) or wooden decor in the East zone of your room.",
                "daily_affirmation": "'My mind is sharp, creative, and continuously expanding with wisdom and joy.'"
            }
        },
        4: {
            "name": "Number 4 — Wood Element (Southeast Zone)",
            "ruling_planet": "Rahu (North Node) / Wood Energy",
            "archetype": "Discipline, Order, Systematic Structure, Practicality & Wealth",
            "direction": "Southeast Zone (Feng Shui Wood Element)",
            "associated_planes": ["Mental Plane (4-9-2)", "Thought Plane (4-3-8)", "Golden Raj Yoga (4-5-6)"],
            "personality_impact": "Governs practical discipline, methodical organization, hard work, and physical execution. Number 4 grounds lofty dreams into tangible real-world achievements.",
            "career_and_wealth": "Fundamental for real estate development, accounting, engineering, project management, law enforcement, and architecture. Number 4 accumulates lasting wealth through methodical saving.",
            "relationship_dynamics": "Brings reliability, loyalty, and practical support to relationships. Expresses love through helpful actions and building home security.",
            "health_and_vitality": "Governs the skeletal frame, joints, knees, and physical stamina. Rigidity can lead to stiffness, joint pain, or overwork fatigue.",
            "detailed_frequencies": {
                0: "0x (Missing Number 4): Struggle with systematic discipline, time management, or financial budgeting. May leave projects unfinished or feel disorganized. Must cultivate daily routines.",
                1: "1x (Single Occurrence): Practical, reliable, punctual, and organized. Works steadily toward goals, values financial security, and builds strong foundations.",
                2: "2x (Double Occurrence - 44): Exceptional stamina, hard-working, highly methodical, and detail-oriented. Can execute complex long-term projects with flawless precision.",
                3: "3x+ (Triple or Higher - 444+): Over-focused on rules and perfectionism. May display stubbornness or reluctance to accept change. Needs to practice mental flexibility and spontaneous fun."
            },
            "remedy_suite": {
                "gemstone_and_color": "Hessonate Garnet (Gomedh), Green Tourmaline, Wooden Mala. Wearing Emerald Green or Forest Shades.",
                "fengshui_placement": "Keep a vibrant Lucky Bamboo plant or wooden carved artifact in the Southeast wealth corner.",
                "daily_affirmation": "'I build strong, practical, and prosperous foundations for my life with ease.'"
            }
        },
        5: {
            "name": "Number 5 — Earth Element (Center Grid Zone)",
            "ruling_planet": "Mercury (Budh) / Core Earth Energy",
            "archetype": "Emotional Balance, Adaptability, Core Stability & Freedom",
            "direction": "Center of Grid (Brahmasthan / Core Earth Element)",
            "associated_planes": ["Emotional Plane (3-5-7)", "Willpower Plane (9-5-1)", "Raj Yoga (4-5-6)", "Property Line (2-5-8)"],
            "personality_impact": "The central anchor of the entire Lo Shu grid! Governs inner stability, emotional equilibrium, adaptability under pressure, and personal freedom.",
            "career_and_wealth": "Crucial for international business, trading, marketing, travel, public relations, and versatile careers. Central 5 brings financial adaptability and luck.",
            "relationship_dynamics": "Maintains emotional balance in crisis. Prevents extreme mood swings and fosters open-minded freedom in relationships.",
            "health_and_vitality": "Governs the central nervous system, solar plexus, stomach, and overall vitality. Central balance protects against panic and anxiety.",
            "detailed_frequencies": {
                0: "0x (Missing Number 5): Emotional volatility, mood swings, or difficulty maintaining balance during stress. May struggle with consistency, feeling scattered or lacking a solid personal center.",
                1: "1x (Single Occurrence): Perfectly balanced emotional center. Adaptable, confident, versatile, calm under pressure, and able to recover quickly from life challenges.",
                2: "2x (Double Occurrence - 55): High energy drive, intense determination, adventurous spirit, and strong craving for freedom. Great pioneer who thrives on change.",
                3: "3x+ (Triple or Higher - 555+): Hyper-restless energy drive. Needs constant travel, variety, and physical activity to channel intense inner momentum; must guard against impulsiveness."
            },
            "remedy_suite": {
                "gemstone_and_color": "Green Emerald, Peridot, Citrine. Wearing Bright Yellow, Green, or Ochre.",
                "fengshui_placement": "Keep the center of your living space clean, well-lit, free of heavy clutter, and place a yellow quartz cluster or crystal pyramid there.",
                "daily_affirmation": "'I am centered, emotionally balanced, versatile, and anchored in peace.'"
            }
        },
        6: {
            "name": "Number 6 — Metal Element (Northwest Zone)",
            "ruling_planet": "Venus (Shukra) / Metal Energy",
            "archetype": "Family Domesticity, Luxury, Helpful Friends & Cosmic Grace",
            "direction": "Northwest Zone (Feng Shui Metal Element)",
            "associated_planes": ["Practical Plane (8-1-6)", "Action Plane (2-7-6)", "Golden Raj Yoga (4-5-6)"],
            "personality_impact": "Governs luxury lifestyle, artistic taste, helpful mentors, family devotion, and protective care for loved ones.",
            "career_and_wealth": "Essential for luxury goods, fashion, hospitality, interior design, entertainment, and high-end sales. Attracts wealthy benefactors and mentors.",
            "relationship_dynamics": "Deeply devoted to home harmony, marriage, and family comfort. Creates a welcoming, warm aesthetic environment for loved ones.",
            "health_and_vitality": "Governs the kidneys, reproductive system, throat, and skin luster. Over-worrying about family can cause tension.",
            "detailed_frequencies": {
                0: "0x (Missing Number 6): May feel a lack of supportive friends or helpful mentors when in need. Difficulty achieving luxury comforts or managing home stability. Needs to cultivate supportive networks.",
                1: "1x (Single Occurrence): Loving, protective, family-centered, refined taste, and attracts helpful friends. Enjoys decorating the home and taking care of others.",
                2: "2x (Double Occurrence - 66): High perfectionism, romantic idealist, magnetic charm, and deep aesthetic refinement. Loves luxury and creates beautiful surroundings.",
                3: "3x+ (Triple or Higher - 666+): Over-protective instinct toward family. May smother loved ones with concern or become overly critical of home imperfections. Needs healthy boundaries."
            },
            "remedy_suite": {
                "gemstone_and_color": "Diamond, Clear Quartz, White Zircon. Wearing Silver, Off-White, or Metallic Gold.",
                "fengshui_placement": "Hang a 6-rod metal wind chime or place brass accessories / silver coins in the Northwest mentor zone.",
                "daily_affirmation": "'I attract supportive friends, luxury, and loving harmony into my home.'"
            }
        },
        7: {
            "name": "Number 7 — Metal Element (West Zone)",
            "ruling_planet": "Ketu (South Node) / Metal Energy",
            "archetype": "Intuition, Spiritual Research, Experiential Learning & Wisdom",
            "direction": "West Zone (Feng Shui Metal Element)",
            "associated_planes": ["Emotional Plane (3-5-7)", "Action Plane (2-7-6)"],
            "personality_impact": "Governs spiritual depth, analytical investigation, learning through life experiences, and philosophical introspection.",
            "career_and_wealth": "Key for scientific research, data analysis, occult studies, archaeology, technical writing, and medicine. Finds truth beyond surface appearances.",
            "relationship_dynamics": "Seeks deep spiritual and intellectual connection in romance rather than superficial attachment. Enjoys contemplative quiet time.",
            "health_and_vitality": "Governs the spleen, lymphatic system, and psychological depth. Repressed emotions can lead to melancholy.",
            "detailed_frequencies": {
                0: "0x (Missing Number 7): May neglect spiritual reflection or struggle to learn from past mistakes, repeating emotional cycles. Needs to cultivate quiet introspection and analytical research.",
                1: "1x (Single Occurrence): Learns deeply from experience, analytical, curious, intuitive, and philosophical. Possesses a keen eye for underlying truths.",
                2: "2x (Double Occurrence - 77): Deep spiritual seeker, brilliant researcher, intuitive analyst, and contemplative thinker. Highly perceptive in complex mysteries.",
                3: "3x+ (Triple or Higher - 777+): Intense spiritual and philosophical orientation. May feel detached from worldly material concerns; needs grounding practical hobbies."
            },
            "remedy_suite": {
                "gemstone_and_color": "Cat's Eye (Vaiduryam), Clear Quartz, Amethyst. Wearing White, Silver, or Metallic Grey.",
                "fengshui_placement": "Place a silver bowl with clear quartz crystals or metal art objects in the West zone.",
                "daily_affirmation": "'I trust my inner intuition and gain profound wisdom from all life experiences.'"
            }
        },
        8: {
            "name": "Number 8 — Earth Element (Northeast Zone)",
            "ruling_planet": "Saturn (Shani) / Earth Energy",
            "archetype": "Financial Acumen, Executive Power, Meticulous Detail & Property",
            "direction": "Northeast Zone (Feng Shui Earth Element)",
            "associated_planes": ["Practical Plane (8-1-6)", "Thought Plane (4-3-8)", "Property Line (2-5-8)"],
            "personality_impact": "Governs financial prudence, executive discipline, long-term memory, real estate acumen, and commercial perseverance.",
            "career_and_wealth": "Crucial for banking, corporate leadership, stock trading, real estate development, government administration, and auditing. Builds lasting wealth.",
            "relationship_dynamics": "Shows loyalty through financial security, dependability, and practical protection. Takes commitments very seriously.",
            "health_and_vitality": "Governs the bones, teeth, knees, and digestive retention. Workaholism can cause joint stiffness or exhaustion.",
            "detailed_frequencies": {
                0: "0x (Missing Number 8): May struggle with money management, act impulsively with finances, or find long-term financial planning tedious. Must develop financial discipline.",
                1: "1x (Single Occurrence): Financially prudent, detail-oriented, meticulous, commercially sharp, and patient. Manages assets wisely.",
                2: "2x (Double Occurrence - 88): High business ambition, strong executive power, brilliant financial judgement, and real estate growth talent.",
                3: "3x+ (Triple or Higher - 888+): Tremendous financial stamina and intense work ethic. Must balance corporate ambitions with personal rest and relaxation."
            },
            "remedy_suite": {
                "gemstone_and_color": "Blue Sapphire, Amethyst, Black Tourmaline. Wearing Dark Blue, Charcoal, or Earthy Brown.",
                "fengshui_placement": "Place a natural crystal cluster (like Amethyst or Smoky Quartz) or earthenware in the Northeast zone.",
                "daily_affirmation": "'I am financially wise, executive, disciplined, and abundantly prosperous.'"
            }
        },
        9: {
            "name": "Number 9 — Fire Element (South Zone)",
            "ruling_planet": "Mars (Mangal) / Fire Energy",
            "archetype": "Humanitarian Drive, Fame, Energy, Passion & Public Honor",
            "direction": "South Zone (Feng Shui Fire Element)",
            "associated_planes": ["Mental Plane (4-9-2)", "Willpower Plane (9-5-1)"],
            "personality_impact": "Governs public recognition, charisma, humanitarian idealism, energy drive, and courage to stand for noble causes.",
            "career_and_wealth": "Essential for public figures, social leaders, sports, politics, military, performing arts, and philanthropy. Number 9 brings fame and honor.",
            "relationship_dynamics": "Passionate, idealistic, and generous. Desires a partner who shares high ideals and social vision.",
            "health_and_vitality": "Governs the muscular system, blood, head, and vital body heat. High energy can manifest as impatience or inflammation.",
            "detailed_frequencies": {
                0: "0x (Missing Number 9): May lack drive, enthusiasm, or public recognition. Struggle to assert oneself or finish ambitious projects. Needs to cultivate passion.",
                1: "1x (Single Occurrence): Ambitious, energetic, idealist, humanitarian, and highly respected in social circles. Stands for noble ideals.",
                2: "2x (Double Occurrence - 99): Highly competitive, charismatic, passionate, and determined to achieve high goals and social standing.",
                3: "3x+ (Triple or Higher - 999+): Intense Fire energy drive. High passion that must be channeled into noble causes to prevent restlessness or impatience."
            },
            "remedy_suite": {
                "gemstone_and_color": "Red Coral, Carnelian, Ruby. Wearing Crimson Red, Coral, or Warm Orange.",
                "fengshui_placement": "Place bright red candles, red lamps, or awards/trophies in the South fame zone of your space.",
                "daily_affirmation": "'My passion, energy, and humanitarian vision illuminate the world with success.'"
            }
        }
    }

    number_analysis = []
    for num in range(1, 10):
        cnt = vedic_counts[num]
        info = CELL_NUM_DETAILS[num]
        freq_map = info.get("detailed_frequencies", {})
        freq_desc = freq_map.get(min(cnt, 4 if num == 1 else 3), freq_map.get(0, ""))
        number_analysis.append({
            "number": num,
            "count": cnt,
            "details": info,
            "frequency_implication": freq_desc
        })

    # Missing Numbers & Remedies
    missing_remedies = {
        1: {"element": "Water", "remedy": "Place a small water fountain or aquamarine crystal in the North zone of your room."},
        2: {"element": "Earth", "remedy": "Wear rose quartz or keep pink/earthen decor to strengthen emotional partnership energy."},
        3: {"element": "Wood", "remedy": "Keep green indoor plants or wear a green aventurine bracelet."},
        4: {"element": "Wood", "remedy": "Wear wooden beads or keep bamboo plants to enhance discipline and focus."},
        5: {"element": "Earth", "remedy": "Wear green emerald/tourmaline or keep yellow crystals to anchor mental stability."},
        6: {"element": "Metal", "remedy": "Wear silver jewelry or brass accessories to boost luxury and supportive relationships."},
        7: {"element": "Metal", "remedy": "Wear white metallic accessories or clear quartz for research and intuitive depth."},
        8: {"element": "Earth", "remedy": "Wear blue sapphire or black tourmaline to strengthen financial discipline."},
        9: {"element": "Fire", "remedy": "Incorporate warm red/coral accents or bright lighting in the South zone for fame and drive."}
    }

    missing_list = [{"number": n, **missing_remedies[n]} for n in range(1, 10) if vedic_counts[n] == 0]

    return {
        "driver_number": driver,
        "conductor_number": conductor,
        "kua_number": kua,
        "gender": gender.capitalize(),
        "pure_dob_digits": dob_digits,
        "full_vedic_numbers": full_vedic_numbers,
        "pure_dob_grid": build_grid_matrix(dob_counts),
        "grid_layout": build_grid_matrix(vedic_counts),
        "planes": planes,
        "number_analysis": number_analysis,
        "cell_details_map": CELL_NUM_DETAILS,
        "missing_numbers": missing_list
    }


PINNACLE_DESCRIPTIONS = {
    1: {
        "theme": "Leadership & Self-Reliance",
        "desc": "A period demanding bold independence, self-motivation, and pioneering new initiatives.",
        "opportunities": "Career advancement, starting new businesses, developing individuality, and gaining personal authority.",
        "action_plan": "Trust your instincts, take initiative, avoid over-reliance on others, and forge your own path."
    },
    2: {
        "theme": "Harmony & Partnerships",
        "desc": "A cycle focused on collaboration, emotional balance, diplomacy, and relationship growth.",
        "opportunities": "Forming key life partnerships, marriage, diplomatic success, teamwork, and artistic refinement.",
        "action_plan": "Practice patience, listen actively, cultivate cooperation, and avoid rush in decision-making."
    },
    3: {
        "theme": "Creativity & Self-Expression",
        "desc": "A vibrant era for artistic expression, communication, social expansion, and joy.",
        "opportunities": "Writing, speaking, media work, creative arts, social networking, and public recognition.",
        "action_plan": "Channel your creative ideas into structured projects; avoid scattering your focus across too many tasks."
    },
    4: {
        "theme": "Building & Discipline",
        "desc": "A grounded period requiring dedicated effort, financial security, and solid foundations.",
        "opportunities": "Real estate investment, building long-term businesses, establishing financial order, and mastering skills.",
        "action_plan": "Maintain strict work ethic, pay attention to practical details, and build for long-term permanence."
    },
    5: {
        "theme": "Freedom & Transformation",
        "desc": "A dynamic phase of change, adventure, personal freedom, and versatility.",
        "opportunities": "Travel, career pivots, public promotion, embracing innovation, and breaking old restrictions.",
        "action_plan": "Embrace healthy adaptability, stay flexible, but avoid impulsive financial or life risks."
    },
    6: {
        "theme": "Family & Healing Service",
        "desc": "A cycle emphasizing domestic harmony, nurturing loved ones, and community duty.",
        "opportunities": "Home ownership, raising a family, counseling, community leadership, and healing work.",
        "action_plan": "Focus on domestic balance and nurturing others, while setting healthy emotional boundaries."
    },
    7: {
        "theme": "Wisdom & Introspection",
        "desc": "A contemplative period for spiritual growth, analytical study, and inner mastery.",
        "opportunities": "Higher education, scientific research, spiritual awakening, writing, and specialized expertise.",
        "action_plan": "Dedicate time to deep study, meditation, and skill refinement; avoid rushing into loud public arenas."
    },
    8: {
        "theme": "Power & Material Mastery",
        "desc": "An executive phase focused on business success, financial flow, and authority.",
        "opportunities": "Executive promotions, large-scale financial management, commercial expansion, and leadership.",
        "action_plan": "Exercise executive decision-making, maintain absolute financial integrity, and lead with vision."
    },
    9: {
        "theme": "Humanitarianism & Completion",
        "desc": "A global phase of altruism, spiritual wisdom, emotional release, and completion.",
        "opportunities": "Philanthropy, international travel, teaching, arts, and releasing outdated life chapters.",
        "action_plan": "Serve the greater good, practice forgiveness, and prepare for higher spiritual awakenings."
    },
    11: {
        "theme": "Master Intuition & Awakening",
        "desc": "A high-vibration period of spiritual illumination, inspiration, and visionary insight.",
        "opportunities": "Spiritual teaching, intuitive innovation, inspiring large groups, and inventive breakthroughs.",
        "action_plan": "Anchor your high intuitive flashes into practical real-world applications."
    },
    22: {
        "theme": "Master Building & Legacy",
        "desc": "A powerful phase of building large-scale projects that benefit humanity.",
        "opportunities": "Constructing major institutions, international enterprise, and leaving an enduring legacy.",
        "action_plan": "Combine giant idealistic vision with meticulous practical execution."
    }
}

CHALLENGE_DESCRIPTIONS = {
    0: {
        "theme": "Challenge of Choice",
        "desc": "You are free to choose your path; beware of indecision or lack of clear direction.",
        "overcoming_strategy": "Set clear personal goals and make proactive choices rather than drifting passively."
    },
    1: {
        "theme": "Challenge of Independence",
        "desc": "Overcome feelings of self-doubt and avoid being overly defensive or dominating.",
        "overcoming_strategy": "Build genuine self-confidence, stand up for yourself, and respect others' autonomy."
    },
    2: {
        "theme": "Challenge of Sensitivity",
        "desc": "Develop emotional stability; avoid taking things personally or sacrificing your needs for peace.",
        "overcoming_strategy": "Strengthen emotional boundaries, express your needs clearly, and avoid over-sensitivity."
    },
    3: {
        "theme": "Challenge of Focus",
        "desc": "Avoid scattering your energies, superficiality, or suppressing feelings.",
        "overcoming_strategy": "Focus your creative talents on one project at a time and express feelings authentically."
    },
    4: {
        "theme": "Challenge of Practicality",
        "desc": "Overcome impatience or rigid thinking; build discipline and persistence.",
        "overcoming_strategy": "Embrace routine, stay patient, and build step-by-step toward your goals."
    },
    5: {
        "theme": "Challenge of Freedom",
        "desc": "Avoid restlessness, impulsiveness, or fear of commitment; seek balanced freedom.",
        "overcoming_strategy": "Cultivate internal discipline so freedom doesn't turn into chaos."
    },
    6: {
        "theme": "Challenge of Acceptance",
        "desc": "Avoid being overly critical or idealistic in relationships; practice acceptance.",
        "overcoming_strategy": "Accept people as they are, release perfectionism, and offer unconditional support."
    },
    7: {
        "theme": "Challenge of Faith",
        "desc": "Overcome cynicism, isolation, or spiritual skepticism; trust your inner wisdom.",
        "overcoming_strategy": "Balance intellectual analysis with intuitive faith and open communication."
    },
    8: {
        "theme": "Challenge of Authority",
        "desc": "Balance material ambitions with ethics; avoid power struggles or financial obsession.",
        "overcoming_strategy": "Use power and money as tools for good, maintaining complete ethical balance."
    }
}


def calculate_pinnacles_and_challenges(month: int, day: int, year: int, life_path_num: int) -> Dict[str, Any]:
    """
    Calculates the 4 Major Life Pinnacle Cycles and 4 Challenge Numbers.
    """
    # Reduce components
    r_m = reduce_number(month, keep_master=False)
    r_d = reduce_number(day, keep_master=False)
    r_y = reduce_number(year, keep_master=False)

    # Base Life Path (reduced for age calculations)
    base_lp = life_path_num if life_path_num not in (11, 22, 33) else reduce_number(life_path_num, keep_master=False)

    # Age Boundaries
    age1_end = 36 - base_lp
    age2_start = age1_end + 1
    age2_end = age1_end + 9
    age3_start = age2_end + 1
    age3_end = age2_end + 9
    age4_start = age3_end + 1

    # Pinnacle Calculations
    p1 = reduce_number(r_m + r_d)
    p2 = reduce_number(r_d + r_y)
    p3 = reduce_number(p1 + p2)
    p4 = reduce_number(r_m + r_y)

    # Challenge Calculations
    c1 = abs(r_m - r_d)
    c2 = abs(r_d - r_y)
    c3 = abs(c1 - c2)
    c4 = abs(r_m - r_y)

    pinnacles = [
        {
            "pinnacle_phase": "First Pinnacle (Foundation Phase)",
            "age_range": f"Age 0 to {age1_end}",
            "number": p1,
            "interpretation": PINNACLE_DESCRIPTIONS.get(p1, PINNACLE_DESCRIPTIONS[1]),
            "challenge_number": c1,
            "challenge_interpretation": CHALLENGE_DESCRIPTIONS.get(c1, CHALLENGE_DESCRIPTIONS[0])
        },
        {
            "pinnacle_phase": "Second Pinnacle (Productive Phase)",
            "age_range": f"Age {age2_start} to {age2_end}",
            "number": p2,
            "interpretation": PINNACLE_DESCRIPTIONS.get(p2, PINNACLE_DESCRIPTIONS[2]),
            "challenge_number": c2,
            "challenge_interpretation": CHALLENGE_DESCRIPTIONS.get(c2, CHALLENGE_DESCRIPTIONS[0])
        },
        {
            "pinnacle_phase": "Third Pinnacle (Maturity Phase)",
            "age_range": f"Age {age3_start} to {age3_end}",
            "number": p3,
            "interpretation": PINNACLE_DESCRIPTIONS.get(p3, PINNACLE_DESCRIPTIONS[3]),
            "challenge_number": c3,
            "challenge_interpretation": CHALLENGE_DESCRIPTIONS.get(c3, CHALLENGE_DESCRIPTIONS[0])
        },
        {
            "pinnacle_phase": "Fourth Pinnacle (Harvest Phase)",
            "age_range": f"Age {age4_start}+ Onward",
            "number": p4,
            "interpretation": PINNACLE_DESCRIPTIONS.get(p4, PINNACLE_DESCRIPTIONS[4]),
            "challenge_number": c4,
            "challenge_interpretation": CHALLENGE_DESCRIPTIONS.get(c4, CHALLENGE_DESCRIPTIONS[0])
        }
    ]

    return {
        "first_pinnacle_age_end": age1_end,
        "pinnacle_cycles": pinnacles
    }


MOBILE_RULING_PLANETS = {
    1: {"planet": "Sun (Surya)", "vibe": "Executive Authority, Power, Public Leadership", "fav_for": "CEOs, Directors, Politicians, Independent Entrepreneurs"},
    2: {"planet": "Moon (Chandra)", "vibe": "Diplomacy, Sensitivity, Intuition, Partnerships", "fav_for": "Counselors, Mediators, HR Professionals, Artists"},
    3: {"planet": "Jupiter (Guru)", "vibe": "Wisdom, Knowledge, Expansion, Financial Luck", "fav_for": "Teachers, Lawyers, Financial Advisors, Writers"},
    4: {"planet": "Rahu (North Node)", "vibe": "Technology, System Structure, Sudden Opportunities", "fav_for": "Engineers, Software Developers, Project Managers"},
    5: {"planet": "Mercury (Budh)", "vibe": "Business, Commercial Sales, Fast Trading, High Luck", "fav_for": "Traders, Marketers, Sales Executives, Brokers, E-commerce"},
    6: {"planet": "Venus (Shukra)", "vibe": "Luxury, Fashion, Popularity, Supportive Friends", "fav_for": "Fashion Designers, Hospitality, Luxury Goods, Entertainment"},
    7: {"planet": "Ketu (South Node)", "vibe": "Research, Technical Expertise, Deep Intuition", "fav_for": "Data Analysts, Researchers, Occultists, Technical Experts"},
    8: {"planet": "Saturn (Shani)", "vibe": "Meticulous Financial Management, Long-Term Assets", "fav_for": "Accountants, Real Estate Developers, Corporate Leadership"},
    9: {"planet": "Mars (Mangal)", "vibe": "Courage, Passion, Public Fame, High Energy Drive", "fav_for": "Sports Professionals, Public Speakers, Military, Sales Drives"}
}


def analyze_name_spelling_options(full_name: str, driver_num: int, life_path_num: int) -> Dict[str, Any]:
    """
    Provides authentic Chaldean & Pythagorean name analysis, component breakdown,
    planetary enemy check, and recommends Royal Star Master Name Spellings.
    """
    pyth = calculate_name_numbers(full_name, "pythagorean")
    chal = calculate_name_numbers(full_name, "chaldean")

    current_pyth_num = pyth["expression"]["number"]
    current_chal_compound = chal["compound_number"]
    current_chal_num = chal["expression"]["number"]
    current_chal_meaning = chal["compound_meaning"]

    # Component Breakdown
    words = [w.strip() for w in full_name.split() if w.strip()]
    components = []
    for w in words:
        clean_w = "".join(c.upper() for c in w if c.isalpha())
        p_tot = sum(PYTHAGOREAN_MAP.get(c, 0) for c in clean_w)
        c_tot = sum(CHALDEAN_MAP.get(c, 0) for c in clean_w)
        p_sing = reduce_number(p_tot)
        c_sing = reduce_number(c_tot)
        c_info = CHALDEAN_COMPOUND_MEANINGS.get(c_tot, {
            "name": f"Compound #{c_tot}",
            "nature": "Favorable" if c_sing in (1, 3, 5, 6) else "Neutral",
            "vibe": f"Vibration of Single Digit #{c_sing}."
        })
        components.append({
            "component_word": w,
            "pythagorean_sum": p_tot,
            "pythagorean_single": p_sing,
            "chaldean_compound": c_tot,
            "chaldean_single": c_sing,
            "chaldean_meaning": c_info
        })

    # Planetary Enemy Check vs Driver & Life Path
    driver_friends = PLANETARY_FRIENDSHIP_MATRIX.get(driver_num, {}).get("friends", {1, 3, 5, 6})
    driver_enemies = PLANETARY_FRIENDSHIP_MATRIX.get(driver_num, {}).get("enemies", set())
    lp_friends = PLANETARY_FRIENDSHIP_MATRIX.get(life_path_num, {}).get("friends", {1, 3, 5, 6})
    lp_enemies = PLANETARY_FRIENDSHIP_MATRIX.get(life_path_num, {}).get("enemies", set())

    is_enemy = (current_chal_num in driver_enemies) or (current_chal_num in lp_enemies)
    is_friend = (current_chal_num in driver_friends) and (current_chal_num in lp_friends)

    if is_enemy:
        current_harmony = f"🚨 Planetary Enemy Alert — Name Single Digit #{current_chal_num} is hostile to Driver #{driver_num} / LP #{life_path_num}"
    elif is_friend and current_chal_meaning.get("nature") == "Ultra Favorable":
        current_harmony = f"🏆 Royal Star Master Alignment — Chaldean #{current_chal_compound} ({current_chal_meaning.get('name')}) is 100% Synchronized!"
    elif is_friend:
        current_harmony = f"🌟 Highly Favorable Harmony — Chaldean #{current_chal_num} & Pythagorean #{current_pyth_num} align with Driver #{driver_num}"
    else:
        current_harmony = "⚠️ Neutral Vibration — Name Spelling Optimization Recommended"

    # Royal Star & Auspicious Name Spelling Candidate Generator
    base_parts = [w.strip() for w in full_name.split() if w.strip()]
    first_name = base_parts[0] if base_parts else full_name
    middle_name = " ".join(base_parts[1:-1]) if len(base_parts) > 2 else ""
    last_name = base_parts[-1] if len(base_parts) > 1 else ""

    candidate_spellings = [
        full_name,
        f"{first_name} A. {last_name}".strip(),
        f"{first_name} K. {last_name}".strip(),
        f"{first_name} S. {last_name}".strip(),
        f"{first_name} V. {last_name}".strip(),
        f"{first_name}{first_name[-1] if first_name else ''} {last_name}".strip(),
        f"{first_name} {last_name}{last_name[-1] if last_name else ''}".strip(),
        f"{first_name}a {last_name}".strip(),
        f"{first_name}e {last_name}".strip(),
        f"{first_name}i {last_name}".strip(),
        f"{first_name}h {last_name}".strip(),
        f"{first_name} {last_name}h".strip()
    ]

    variations = []
    seen = set()

    for cand in candidate_spellings:
        if not cand or cand in seen:
            continue
        seen.add(cand)

        p_cand = calculate_name_numbers(cand, "pythagorean")
        c_cand = calculate_name_numbers(cand, "chaldean")

        c_expr = p_cand["expression"]["number"]
        ch_comp = c_cand["compound_number"]
        ch_expr = c_cand["expression"]["number"]
        ch_meaning = c_cand["compound_meaning"]

        c_enemy = (ch_expr in driver_enemies) or (ch_expr in lp_enemies)
        c_friend = (ch_expr in driver_friends) and (ch_expr in lp_friends)
        is_royal = ch_meaning.get("nature") == "Ultra Favorable"

        if c_enemy:
            continue # Skip enemy vibrations

        if is_royal and c_friend:
            rating = f"🏆 98% Royal Star Master (#{ch_comp} {ch_meaning.get('name')})"
            reason = f"Chaldean Compound #{ch_comp} ({ch_meaning.get('name')}) — {ch_meaning.get('vibe')} Perfect friend with Driver #{driver_num} & LP #{life_path_num}."
        elif c_friend:
            rating = f"🌟 92% Auspicious Harmony (#{ch_comp})"
            reason = f"Chaldean Expression #{ch_expr} & Pythagorean #{c_expr} creates strong planetary friendship with Driver #{driver_num}."
        else:
            rating = f"✨ 85% Favorable Balance (#{ch_comp})"
            reason = f"Chaldean Compound #{ch_comp} ({ch_meaning.get('name')}) provides balanced energy."

        variations.append({
            "spelling": cand,
            "pythagorean_expression": c_expr,
            "chaldean_compound": ch_comp,
            "chaldean_expression": ch_expr,
            "chaldean_name": ch_meaning.get("name", ""),
            "rating": rating,
            "reason": reason
        })

    # Sort candidates by rating quality
    variations.sort(key=lambda x: ("🏆" in x["rating"], "🌟" in x["rating"]), reverse=True)

    return {
        "current_name": full_name,
        "current_expression": current_pyth_num,
        "current_chaldean_compound": current_chal_compound,
        "current_chaldean_expression": current_chal_num,
        "current_chaldean_meaning": current_chal_meaning,
        "current_harmony_status": current_harmony,
        "components": components,
        "recommended_variations": variations[:6]
    }


def analyze_mobile_numbers(phone_numbers: List[str], driver_num: int, life_path_num: int) -> Dict[str, Any]:
    """Analyzes up to 4 mobile numbers, evaluates ruling planet vibration, and recommends the #1 best mobile number."""
    results = []

    for idx, phone in enumerate(phone_numbers[:4]): # Max 4 mobile numbers
        clean_digits = [int(d) for d in str(phone) if d.isdigit()]
        if not clean_digits:
            continue

        raw_sum = sum(clean_digits)
        reduced = reduce_number(raw_sum, keep_master=False)

        planet_info = MOBILE_RULING_PLANETS.get(reduced, MOBILE_RULING_PLANETS[5])

        if reduced in (5, 6, 1, 3) or reduced in (driver_num, life_path_num):
            compat_score = 95
            compat_label = "🌟 Excellent Commercial & Wealth Harmony"
        elif reduced in (2, 7, 9):
            compat_score = 80
            compat_label = "✨ Favorable Neutral Harmony"
        else: # 4, 8
            compat_score = 65
            compat_label = "⚠️ Requires Hard Work & Strict Financial Discipline"

        results.append({
            "index": idx + 1,
            "mobile_number": str(phone),
            "raw_sum": raw_sum,
            "total_single_digit": reduced,
            "ruling_planet": planet_info["planet"],
            "vibe": planet_info["vibe"],
            "best_suited_for": planet_info["fav_for"],
            "compatibility_score": compat_score,
            "compatibility_label": compat_label
        })

    sorted_res = sorted(results, key=lambda x: x["compatibility_score"], reverse=True)
    best_mobile = sorted_res[0] if sorted_res else None

    return {
        "analyzed_count": len(results),
        "mobile_analysis_list": results,
        "best_recommended_mobile": best_mobile
    }


def generate_full_numerology_profile(full_name: str, year: int, month: int, day: int, gender: str = "male", current_year: int = 2026, mobile_numbers: List[str] = None) -> Dict[str, Any]:
    """Generates complete Numerology Blueprint including Lo Shu Grid, Pinnacles, Name Spelling Analysis, and Mobile Number Inspector."""
    life_path = calculate_life_path(year, month, day)
    birthday_num = reduce_number(day)
    pythagorean_name = calculate_name_numbers(full_name, "pythagorean")
    chaldean_name = calculate_name_numbers(full_name, "chaldean")
    personal_year = calculate_personal_year(month, day, current_year)
    loshu_grid = calculate_loshu_grid(day, month, year, gender)
    pinnacles = calculate_pinnacles_and_challenges(month, day, year, life_path["number"])

    driver_num = loshu_grid["driver_number"]
    lp_num = life_path["number"]

    # Name Spelling Recommendations
    name_analysis = analyze_name_spelling_options(full_name, driver_num, lp_num)

    # Mobile Number Inspector
    if not mobile_numbers:
        mobile_numbers = ["9876543210", "9123456789"]
    mobile_analysis = analyze_mobile_numbers(mobile_numbers, driver_num, lp_num)

    return {
        "full_name": full_name,
        "date_of_birth": f"{year:04d}-{month:02d}-{day:02d}",
        "gender": gender.capitalize(),
        "life_path": life_path,
        "birthday_number": {
            "number": birthday_num,
            "meaning": MEANINGS.get(birthday_num, MEANINGS[1])
        },
        "pythagorean": pythagorean_name,
        "chaldean": chaldean_name,
        "personal_year": personal_year,
        "loshu_grid": loshu_grid,
        "pinnacles": pinnacles,
        "name_spelling_analysis": name_analysis,
        "mobile_analysis": mobile_analysis
    }

