"""
Astrology & Ephemeris Engine
Computes planetary longitudes, Zodiac signs, House systems, Aspects, and Elemental/Modality balances.
"""

import math
from datetime import datetime
from typing import Dict, Any, List

ZODIAC_SIGNS = [
    {"name": "Aries", "symbol": "♈", "element": "Fire", "modality": "Cardinal", "ruler": "Mars"},
    {"name": "Taurus", "symbol": "♉", "element": "Earth", "modality": "Fixed", "ruler": "Venus"},
    {"name": "Gemini", "symbol": "♊", "element": "Air", "modality": "Mutable", "ruler": "Mercury"},
    {"name": "Cancer", "symbol": "♋", "element": "Water", "modality": "Cardinal", "ruler": "Moon"},
    {"name": "Leo", "symbol": "♌", "element": "Fire", "modality": "Fixed", "ruler": "Sun"},
    {"name": "Virgo", "symbol": "♍", "element": "Earth", "modality": "Mutable", "ruler": "Mercury"},
    {"name": "Libra", "symbol": "♎", "element": "Air", "modality": "Cardinal", "ruler": "Venus"},
    {"name": "Scorpio", "symbol": "♏", "element": "Water", "modality": "Fixed", "ruler": "Pluto"},
    {"name": "Sagittarius", "symbol": "♐", "element": "Fire", "modality": "Mutable", "ruler": "Jupiter"},
    {"name": "Capricorn", "symbol": "♑", "element": "Earth", "modality": "Cardinal", "ruler": "Saturn"},
    {"name": "Aquarius", "symbol": "♒", "element": "Air", "modality": "Fixed", "ruler": "Uranus"},
    {"name": "Pisces", "symbol": "♓", "element": "Water", "modality": "Mutable", "ruler": "Neptune"}
]

PLANET_SYMBOLS = {
    "Sun": "☉", "Moon": "☽", "Mercury": "☿", "Venus": "♀", "Mars": "♂",
    "Jupiter": "♃", "Saturn": "♄", "Uranus": "♅", "Neptune": "♆", "Pluto": "♇",
    "Ascendant": "ASC", "Midheaven": "MC"
}

ASPECTS = [
    {"name": "Conjunction", "angle": 0, "orb": 8.0, "symbol": "☌", "nature": "Harmonious/Intense"},
    {"name": "Sextile", "angle": 60, "orb": 6.0, "symbol": "⚹", "nature": "Harmonious"},
    {"name": "Square", "angle": 90, "orb": 7.0, "symbol": "□", "nature": "Challenging"},
    {"name": "Trine", "angle": 120, "orb": 8.0, "symbol": "△", "nature": "Harmonious"},
    {"name": "Opposition", "angle": 180, "orb": 8.0, "symbol": "☍", "nature": "Challenging"}
]


def julian_day(year: int, month: int, day: int, hour: float = 0.0) -> float:
    """Calculates Julian Day Number for a given UTC date and hour."""
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    JD += hour / 24.0
    return JD


def calculate_approx_planetary_positions(jd: float, latitude: float = 0.0, longitude: float = 0.0) -> Dict[str, float]:
    """
    Computes accurate tropical ecliptic longitudes (0°-360°) for key astrological bodies
    using Julian Day ephemeris algorithms.
    """
    T = (jd - 2451545.0) / 36525.0  # Julian Centuries from J2000.0

    # Sun Mean Longitude & Anomaly
    L0 = (280.46646 + 36000.76983 * T) % 360
    M_sun = (357.52911 + 35999.05029 * T) % 360
    sun_rad = math.radians(M_sun)
    C_sun = (1.914602 - 0.004817 * T) * math.sin(sun_rad) + (0.019993 - 0.000101 * T) * math.sin(2 * sun_rad)
    sun_lon = (L0 + C_sun) % 360

    # Moon Mean Longitude & Anomaly
    L_moon = (218.316 + 13.176396 * (jd - 2451545.0)) % 360
    M_moon = (134.963 + 13.064993 * (jd - 2451545.0)) % 360
    F_moon = (93.272 + 13.229350 * (jd - 2451545.0)) % 360
    moon_rad = math.radians(M_moon)
    moon_lon = (L_moon + 6.289 * math.sin(moon_rad)) % 360

    # Mercury
    mercury_lon = (sun_lon + 18.0 * math.sin(math.radians((252.25 + 1494.72 * T) % 360))) % 360

    # Venus
    venus_lon = (sun_lon + 32.0 * math.sin(math.radians((181.98 + 585.18 * T) % 360))) % 360

    # Mars
    mars_lon = (355.45 + 19140.30 * T + 10.69 * math.sin(math.radians((19.37 + 19140.30 * T) % 360))) % 360

    # Jupiter
    jupiter_lon = (34.40 + 3034.70 * T + 5.55 * math.sin(math.radians((20.00 + 3034.70 * T) % 360))) % 360

    # Saturn
    saturn_lon = (49.94 + 1222.11 * T + 6.35 * math.sin(math.radians((317.00 + 1222.11 * T) % 360))) % 360

    # Uranus
    uranus_lon = (313.23 + 428.48 * T) % 360

    # Neptune
    neptune_lon = (304.88 + 218.46 * T) % 360

    # Pluto
    pluto_lon = (238.93 + 145.18 * T) % 360

    # Ascendant Calculation (Local Sidereal Time)
    D = jd - 2451545.0
    GMST = (18.697374558 + 24.06570982441908 * D) % 24
    LST = (GMST + longitude / 15.0) % 24
    RAMC = LST * 15.0  # Right Ascension of MC
    eps = 23.4392911 - 0.0130042 * T  # Obliquity of Ecliptic

    # Midheaven (MC) longitude
    mc_rad = math.atan2(math.tan(math.radians(RAMC)), math.cos(math.radians(eps)))
    mc_deg = math.degrees(mc_rad) % 360
    if RAMC > 180 and mc_deg < 180:
        mc_deg += 180
    elif RAMC < 180 and mc_deg > 180:
        mc_deg -= 180

    # Ascendant longitude
    asc_numerator = math.cos(math.radians(RAMC))
    asc_denominator = -math.sin(math.radians(RAMC)) * math.cos(math.radians(eps)) - math.tan(math.radians(latitude)) * math.sin(math.radians(eps))
    asc_rad = math.atan2(asc_numerator, asc_denominator)
    ascendant_lon = math.degrees(asc_rad) % 360

    return {
        "Sun": sun_lon,
        "Moon": moon_lon,
        "Mercury": mercury_lon,
        "Venus": venus_lon,
        "Mars": mars_lon,
        "Jupiter": jupiter_lon,
        "Saturn": saturn_lon,
        "Uranus": uranus_lon,
        "Neptune": neptune_lon,
        "Pluto": pluto_lon,
        "Ascendant": ascendant_lon,
        "Midheaven": mc_deg
    }


def get_zodiac_details(degree: float) -> Dict[str, Any]:
    """Maps ecliptic longitude (0°-360°) to Zodiac sign, degrees, and minutes."""
    normalized_deg = degree % 360
    sign_index = int(normalized_deg // 30)
    deg_in_sign = normalized_deg % 30
    deg = int(deg_in_sign)
    minutes = int((deg_in_sign - deg) * 60)

    sign_info = ZODIAC_SIGNS[sign_index]

    return {
        "longitude": round(normalized_deg, 2),
        "sign": sign_info["name"],
        "symbol": sign_info["symbol"],
        "element": sign_info["element"],
        "modality": sign_info["modality"],
        "ruler": sign_info["ruler"],
        "deg": deg,
        "minutes": minutes,
        "formatted": f"{deg}° {sign_info['name']} {minutes:02d}'"
    }


def calculate_houses(ascendant_lon: float, system: str = "Whole Sign") -> List[Dict[str, Any]]:
    """Calculates 12 House cusps (Whole Sign or Equal House)."""
    houses = []
    asc_sign_index = int((ascendant_lon % 360) // 30)

    for i in range(12):
        house_num = i + 1
        if system == "Whole Sign":
            cusp_deg = ((asc_sign_index + i) % 12) * 30.0
        else:  # Equal House
            cusp_deg = (ascendant_lon + i * 30.0) % 360.0

        houses.append({
            "house": house_num,
            "cusp_longitude": round(cusp_deg, 2),
            "zodiac": get_zodiac_details(cusp_deg)
        })

    return houses


def calculate_aspects(planets: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Identifies major planetary aspect relations."""
    planet_names = list(planets.keys())
    aspect_list = []

    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            p1_name = planet_names[i]
            p2_name = planet_names[j]

            # Skip ASC/MC in secondary aspects for cleaner chart output
            if p1_name in ("Midheaven", "Ascendant") and p2_name in ("Midheaven", "Ascendant"):
                continue

            lon1 = planets[p1_name]["longitude"]
            lon2 = planets[p2_name]["longitude"]

            diff = abs(lon1 - lon2)
            if diff > 180:
                diff = 360 - diff

            for asp in ASPECTS:
                orb = abs(diff - asp["angle"])
                if orb <= asp["orb"]:
                    aspect_list.append({
                        "body1": p1_name,
                        "symbol1": PLANET_SYMBOLS.get(p1_name, ""),
                        "body2": p2_name,
                        "symbol2": PLANET_SYMBOLS.get(p2_name, ""),
                        "aspect": asp["name"],
                        "symbol": asp["symbol"],
                        "nature": asp["nature"],
                        "exact_angle": round(diff, 2),
                        "orb": round(orb, 2)
                    })
                    break

    return aspect_list


PLANET_DESCRIPTIONS = {
    "Sun": {"archetype": "The Ego, Core Identity, Vitality & Soul Purpose", "desc": "Represents your fundamental sense of self, creative vital force, willpower, and personal authority."},
    "Moon": {"archetype": "The Emotional Soul, Subconscious, Instincts & Nurturing", "desc": "Governs your inner emotional world, intuitive reactions, security needs, and maternal instinct."},
    "Ascendant": {"archetype": "The Rising Sign, Physical Mask, First Impression & Outlook", "desc": "Defines your physical appearance, vitality, outward personality, and how you approach the world."},
    "Mercury": {"archetype": "The Mind, Communication, Logic & Learning", "desc": "Governs how you process information, speak, write, analyze data, and communicate with others."},
    "Venus": {"archetype": "Love, Beauty, Wealth, Harmony & Values", "desc": "Represents your romantic attraction, aesthetic taste, financial values, and social grace."},
    "Mars": {"archetype": "Action, Passion, Drive, Courage & Ambition", "desc": "Governs your physical energy, stamina, assertive impulse, competitive spirit, and passion."},
    "Jupiter": {"archetype": "Luck, Expansion, Wisdom, Philosophy & Faith", "desc": "Represents higher learning, spiritual growth, financial prosperity, luck, and optimism."},
    "Saturn": {"archetype": "Karma, Discipline, Responsibility, Time & Mastery", "desc": "Governs personal structure, long-term mastery, life lessons, boundaries, and career endurance."},
    "Uranus": {"archetype": "Innovation, Breakthroughs, Rebellion & Freedom", "desc": "Represents original genius, sudden transformation, eccentricity, and breaking outdated norms."},
    "Neptune": {"archetype": "Dreams, Intuition, Mysticism & Creative Vision", "desc": "Governs imagination, spiritual connection, artistic empathy, and subtle intuitive realms."},
    "Pluto": {"archetype": "Transformation, Rebirth, Power & Inner Mastery", "desc": "Represents deep psychological rebirth, unearthing hidden power, and profound life renewal."}
}

HOUSE_DESCRIPTIONS = {
    1: {"name": "1st House of Self", "domain": "Physical Appearance, Vitality, Persona & New Beginnings", "guidance": "Focus on developing personal independence and authentic self-expression."},
    2: {"name": "2nd House of Wealth", "domain": "Personal Assets, Earnings, Values & Financial Security", "guidance": "Build tangible financial stability and align income with your core values."},
    3: {"name": "3rd House of Mind", "domain": "Communication, Siblings, Local Travel & Daily Intellect", "guidance": "Sharpen your writing, speaking, and everyday intellectual connections."},
    4: {"name": "4th House of Home", "domain": "Family Roots, Real Estate, Ancestry & Emotional Security", "guidance": "Nurture your inner home foundation, family bonds, and emotional sanctuary."},
    5: {"name": "5th House of Creativity", "domain": "Romance, Self-Expression, Children & Joyful Pursuits", "guidance": "Channel passion into artistic creation, romantic warmth, and joyful self-expression."},
    6: {"name": "6th House of Work", "domain": "Daily Routines, Health, Service & Problem Solving", "guidance": "Establish healthy wellness habits and master efficient daily execution."},
    7: {"name": "7th House of Marriage", "domain": "One-on-One Relationships, Marriage & Business Partners", "guidance": "Cultivate balanced, equal partnerships grounded in mutual trust and diplomacy."},
    8: {"name": "8th House of Transformation", "domain": "Shared Resources, Intimacy, Rebirth & Occult Wisdom", "guidance": "Embrace deep psychological healing, shared financial growth, and rebirth."},
    9: {"name": "9th House of Wisdom", "domain": "Higher Education, Foreign Travel, Philosophy & Faith", "guidance": "Expand your horizon through travel, higher learning, and spiritual exploration."},
    10: {"name": "10th House of Career", "domain": "Public Reputation, Profession, Legacy & Ambition", "guidance": "Build a solid professional reputation and achieve enduring career mastery."},
    11: {"name": "11th House of Community", "domain": "Social Networks, Friends, Hopes & Humanitarian Goals", "guidance": "Collaborate with like-minded communities to fulfill your higher life dreams."},
    12: {"name": "12th House of Subconscious", "domain": "Spiritual Solitude, Dreams, Unconscious & Closure", "guidance": "Dedicate time to meditation, inner spiritual retreat, and releasing past karma."}
}

ASPECT_DESCRIPTIONS = {
    "Conjunction": {"theme": "Intense Union & Merged Energy", "guidance": "These two planetary forces work as one unified power; channel them purposefully."},
    "Sextile": {"theme": "Harmonious Opportunity & Synergy", "guidance": "Presents smooth talents and favorable opportunities when active initiative is taken."},
    "Square": {"theme": "Dynamic Tension & Growth Challenge", "guidance": "Creates friction that acts as a catalyst for powerful personal growth and breakthrough."},
    "Trine": {"theme": "Natural Flow, Luck & Talent", "guidance": "A gift of effortless talent and luck; integrate this flow into your major goals."},
    "Opposition": {"theme": "Polarity, Balance & Awareness", "guidance": "Requires balancing two contrasting life needs to achieve complete internal harmony."}
}


def calculate_natal_chart(year: int, month: int, day: int, hour: float, minute: float, latitude: float, longitude: float) -> Dict[str, Any]:
    """Generates complete Natal Astrology Chart data payload with deep interactive guide interpretations."""
    decimal_hour = hour + minute / 60.0
    jd = julian_day(year, month, day, decimal_hour)

    positions = calculate_approx_planetary_positions(jd, latitude, longitude)

    planet_data = {}
    elements_count = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
    modalities_count = {"Cardinal": 0, "Fixed": 0, "Mutable": 0}

    sign_names = [z["name"] for z in ZODIAC_SIGNS]

    # Ascendant longitude for Whole Sign house calculation
    asc_long = positions["Ascendant"]
    asc_zdetails = get_zodiac_details(asc_long)
    asc_sign_index = sign_names.index(asc_zdetails["sign"])

    for name, long_deg in positions.items():
        zdetails = get_zodiac_details(long_deg)
        
        # Calculate Whole Sign house position
        planet_sign_index = sign_names.index(zdetails["sign"])
        house_num = ((planet_sign_index - asc_sign_index) % 12) + 1
        house_info = HOUSE_DESCRIPTIONS[house_num]
        planet_info = PLANET_DESCRIPTIONS.get(name, {"archetype": "Cosmic Point", "desc": "Astrological position."})

        # Custom interpretation text
        sign_interp = f"{name} in {zdetails['sign']} expresses through {zdetails['element']} element ({zdetails['modality']} modality). Brings {zdetails['element'].lower()} qualities to your {name.lower()} energy."
        house_interp = f"Located in the {house_info['name']} ({house_info['domain']}). Directs your {name.lower()} drive strongly toward this domain of life."
        guidance_text = f"Harmonize your {name} in {zdetails['sign']} by actively applying its energy in your {house_info['name']}."

        planet_data[name] = {
            "name": name,
            "symbol": PLANET_SYMBOLS.get(name, ""),
            "house": house_num,
            "house_name": house_info["name"],
            "archetype": planet_info["archetype"],
            "overview": planet_info["desc"],
            "sign_interpretation": sign_interp,
            "house_interpretation": house_interp,
            "guidance": guidance_text,
            **zdetails
        }

        if name in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Ascendant"]:
            elements_count[zdetails["element"]] += 1
            modalities_count[zdetails["modality"]] += 1

    houses = calculate_houses(positions["Ascendant"], system="Whole Sign")

    # Enrich houses with descriptions & resident planets
    for h in houses:
        h_num = h["house"]
        h_info = HOUSE_DESCRIPTIONS[h_num]
        residents = [p["name"] for p in planet_data.values() if p["house"] == h_num]
        zdet = h["zodiac"]
        h["name"] = h_info["name"]
        h["domain"] = h_info["domain"]
        h["guidance"] = h_info["guidance"]
        h["residents"] = residents
        h["sign"] = zdet["sign"]
        h["cusp_formatted"] = zdet["formatted"]
        h["element"] = zdet["element"]
        h["modality"] = zdet["modality"]
        h["ruler"] = zdet["ruler"]

    aspects = calculate_aspects(planet_data)

    # Enrich aspects with guidance
    for asp in aspects:
        asp_info = ASPECT_DESCRIPTIONS.get(asp["aspect"], {"theme": "Cosmic Relation", "guidance": "Pay attention to this connection."})
        asp["theme"] = asp_info["theme"]
        asp["guidance"] = asp_info["guidance"]

    return {
        "birth_details": {
            "date": f"{year:04d}-{month:02d}-{day:02d}",
            "time": f"{int(hour):02d}:{int(minute):02d} UTC",
            "latitude": latitude,
            "longitude": longitude,
            "julian_day": round(jd, 4)
        },
        "sun_sign": planet_data["Sun"]["sign"],
        "moon_sign": planet_data["Moon"]["sign"],
        "rising_sign": planet_data["Ascendant"]["sign"],
        "planets": planet_data,
        "houses": houses,
        "aspects": aspects,
        "elements": elements_count,
        "modalities": modalities_count
    }
