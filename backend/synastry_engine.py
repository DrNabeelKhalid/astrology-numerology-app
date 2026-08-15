"""
Synastry & Compatibility Engine
Calculates astrological and numerological compatibility between two profiles.
"""

from typing import Dict, Any
from astrology_engine import calculate_natal_chart
from numerology_engine import generate_full_numerology_profile


ELEMENT_CHEMISTRY = {
    ("Fire", "Fire"): {"theme": "Dynamic Flame of Passion", "score": 92, "analysis": "High energy, mutual enthusiasm, and fierce mutual drive. You inspire each other to conquer big goals, but must guard against competitive flare-ups."},
    ("Fire", "Air"): {"theme": "Inspirational Spark & Expansion", "score": 94, "analysis": "Air fuels Fire's ambition while Fire brings Air's ideas to life! Highly creative, intellectually stimulating, and fun partnership."},
    ("Fire", "Earth"): {"theme": "Grounded Power & Execution", "score": 72, "analysis": "Earth provides stability and practical structure to Fire's visions. Fire brings warmth and courage, though Earth must avoid dampening Fire's spontaneity."},
    ("Fire", "Water"): {"theme": "Steam & Deep Transformation", "score": 68, "analysis": "Intensely passionate and transformative! Water softens Fire's edges and Fire energizes Water, requiring emotional patience so steam doesn't cause misunderstandings."},
    ("Earth", "Earth"): {"theme": "Unshakable Mountain of Stability", "score": 95, "analysis": "Solid, dependable, and deeply secure. Excellent for long-term wealth accumulation, home building, and shared practical values."},
    ("Earth", "Water"): {"theme": "Fertile Garden of Nurturing", "score": 92, "analysis": "A deeply supportive match. Water nourishes Earth's roots, and Earth provides safe emotional containment for Water's deep feelings."},
    ("Earth", "Air"): {"theme": "Pragmatic Logic & Intellect", "score": 70, "analysis": "Air brings fresh perspectives and creative ideas, while Earth grounds them into real-world results. Communication is key to bridging abstract and concrete views."},
    ("Air", "Air"): {"theme": "Mental Synergy & Endless Dialogue", "score": 93, "analysis": "A meeting of minds! Intellectual stimulation, brilliant conversations, shared social lives, and mutual freedom."},
    ("Air", "Water"): {"theme": "Intuitive Thought & Sentiment", "score": 65, "analysis": "Air approaches life through logic while Water feels through emotion. When balanced, Air brings clarity and Water brings emotional depth."},
    ("Water", "Water"): {"theme": "Oceanic Soulmate Connection", "score": 96, "analysis": "Profound emotional empathy, psychic understanding, and deep spiritual bonding. You sense each other's feelings without speaking a word."}
}

LIFE_PATH_SYNERGY = {
    1: {1: "Two strong leaders; mutual respect for independence is essential.", 2: "Balanced match; LP 1 leads with vision, LP 2 supports with diplomacy.", 3: "Vibrant combination of drive and creative self-expression.", 4: "Grounded partnership; LP 1 provides vision, LP 4 builds structure.", 5: "Dynamic and adventurous duo; loves freedom and new projects.", 6: "Protective and caring match; balances career drive with home warmth.", 7: "Intellectual connection; combines practical action with deep wisdom.", 8: "High executive power couple; tremendous commercial and wealth drive.", 9: "Global visionary match; unites personal ambition with noble service."},
    2: {2: "Deeply gentle, intuitive, and empathetic bond.", 3: "Joyful and harmonious relationship filled with art and warmth.", 4: "Secure, reliable, and family-oriented connection.", 5: "Requires balance between LP 2's need for closeness and LP 5's freedom.", 6: "Ultimate domestic and loving harmony; ideal for marriage and family.", 7: "Quiet, intuitive, and spiritual connection.", 8: "Powerful team; LP 8 manages material growth, LP 2 manages harmony.", 9: "Compassionate, spiritual, and humanitarian synergy."},
    3: {3: "High creative enthusiasm and social fun.", 4: "LP 4 brings practical discipline to LP 3's creative ideas.", 5: "Exciting, versatile, and fun-loving bond.", 6: "Warm, artistic, and nurturing home life.", 7: "Blends creative expression with deep analytical research.", 8: "Combines creative vision with commercial success.", 9: "Vibrant artistic and philanthropic power duo."},
    4: {4: "Unshakable reliability, financial discipline, and loyalty.", 5: "LP 4 provides stability while LP 5 introduces excitement.", 6: "Outstanding foundation for family, real estate, and financial security.", 7: "Grounded analytical partnership focused on truth and discipline.", 8: "Corporate and financial master team; unstoppable work ethic.", 9: "Combines systematic work with noble humanitarian goals."},
    5: {5: "High-voltage adventure, travel, and mutual freedom.", 6: "LP 6 anchors home stability while LP 5 brings exciting experiences.", 7: "Intellectual and philosophical wanderers.", 8: "Dynamic business expansion team; loves bold enterprise.", 9: "Passionate humanitarian travelers."},
    6: {6: "Deeply loving, family-first relationship filled with luxury and care.", 7: "Blends emotional home warmth with spiritual reflection.", 8: "Prosperous match combining family devotion with executive wealth.", 9: "Altruistic, healing, and community-minded power union."},
    7: {7: "Profound spiritual, philosophical, and meditative soul connection.", 8: "Balances spiritual wisdom with material business mastery.", 9: "Universal wisdom seekers devoted to truth and spiritual growth."},
    8: {8: "Mighty executive power couple; high ambition and wealth potential.", 9: "Combines material abundance with humanitarian purpose."},
    9: {9: "Spiritual, altruistic, and inspiring global soulmates."}
}


def calculate_business_compatibility(p1_name: str, chart1: Dict[str, Any], num1: Dict[str, Any], p2_name: str, chart2: Dict[str, Any], num2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates Business & Financial Partnership Compatibility.
    """
    d1 = num1["loshu_grid"]["driver_number"]
    d2 = num2["loshu_grid"]["driver_number"]
    elem1 = chart1["planets"]["Sun"]["element"]
    elem2 = chart2["planets"]["Sun"]["element"]

    # 1. Financial & Wealth Management Score
    financial_score = 94 if (d1 in (8, 4, 2, 6) and d2 in (8, 4, 2, 6)) else (88 if (d1 in (8, 4, 2, 6) or d2 in (8, 4, 2, 6)) else 76)

    # 2. Executive Leadership & Drive Score
    leadership_score = 92 if (d1 in (1, 9, 5) and d2 in (1, 9, 5)) else (85 if (d1 in (1, 9, 5) or d2 in (1, 9, 5)) else 78)

    # 3. Innovation & Strategy Score
    innovation_score = 90 if (d1 in (3, 5, 7) or d2 in (3, 5, 7)) else 78

    # 4. Trust & Contract Security Score
    trust_score = 92 if (elem1 in ("Earth", "Water") and elem2 in ("Earth", "Water")) else 80

    biz_overall = round((financial_score * 0.30) + (leadership_score * 0.30) + (innovation_score * 0.20) + (trust_score * 0.20))

    if biz_overall >= 88:
        biz_archetype = "🏆 High Empire Building Partners"
    elif biz_overall >= 78:
        biz_archetype = "💼 Strategic Commercial Venture"
    elif biz_overall >= 68:
        biz_archetype = "💡 Innovation & Execution Duo"
    else:
        biz_archetype = "⚠️ High Friction / Strict Contracts Recommended"

    # Business Industry Recommendations
    recommended_fields = []
    if elem1 == "Earth" or elem2 == "Earth":
        recommended_fields.append("Real Estate Development, Banking & Asset Management")
    if elem1 == "Fire" or elem2 == "Fire":
        recommended_fields.append("Tech Startups, Executive Consulting & Commercial Sales")
    if elem1 == "Air" or elem2 == "Air":
        recommended_fields.append("Media, Digital Marketing & Software Platforms")
    if elem1 == "Water" or elem2 == "Water":
        recommended_fields.append("Healthcare, Hospitality, Luxury Goods & Creative Arts")

    return {
        "business_score": biz_overall,
        "business_archetype": biz_archetype,
        "pillars": {
            "financial_management": financial_score,
            "executive_leadership": leadership_score,
            "innovation_strategy": innovation_score,
            "trust_security": trust_score
        },
        "recommended_industries": recommended_fields,
        "financial_pitfall_warning": "Define clear written equity agreements, profit-sharing ratios, and distinct executive responsibilities early to prevent overlap.",
        "business_advice": f"{p1_name} (Driver {d1}) & {p2_name} (Driver {d2}) possess a solid commercial foundation. Unify {p1_name}'s leadership strengths with {p2_name}'s financial execution for optimum business growth."
    }


def calculate_compatibility(p1_name: str, p1_birth: str, p2_name: str, p2_birth: str) -> Dict[str, Any]:
    """
    Computes exhaustive 4-Pillar compatibility score, astrological synastry aspects, and business partnership analysis.
    p1_birth & p2_birth format: 'YYYY-MM-DD'
    """
    # Parse dates
    y1, m1, d1 = map(int, p1_birth.split('-'))
    y2, m2, d2 = map(int, p2_birth.split('-'))

    # Calculate individual charts
    chart1 = calculate_natal_chart(y1, m1, d1, 12.0, 0.0, 0.0, 0.0)
    chart2 = calculate_natal_chart(y2, m2, d2, 12.0, 0.0, 0.0, 0.0)

    num1 = generate_full_numerology_profile(p1_name, y1, m1, d1)
    num2 = generate_full_numerology_profile(p2_name, y2, m2, d2)

    # Element compatibility weights
    elem1 = chart1["planets"]["Sun"]["element"]
    elem2 = chart2["planets"]["Sun"]["element"]

    pair_key = (elem1, elem2) if (elem1, elem2) in ELEMENT_CHEMISTRY else (elem2, elem1)
    elem_info = ELEMENT_CHEMISTRY.get(pair_key, ELEMENT_CHEMISTRY[("Fire", "Fire")])

    # Numerology Life Path compatibility
    lp1 = num1["life_path"]["number"]
    lp2 = num2["life_path"]["number"]

    # Normalize LP numbers to single digit 1-9 for matrix lookup
    base_lp1 = lp1 if lp1 not in (11, 22, 33) else (2 if lp1 == 11 else 4)
    base_lp2 = lp2 if lp2 not in (11, 22, 33) else (2 if lp2 == 11 else 4)

    lp_pair = (min(base_lp1, base_lp2), max(base_lp1, base_lp2))
    lp_analysis = LIFE_PATH_SYNERGY.get(lp_pair[0], {}).get(lp_pair[1], "Harmonious Life Path connection fostering mutual growth.")

    # Calculate 4 Compatibility Pillars
    romantic_score = min(99, max(60, elem_info["score"] + (5 if abs(lp1 - lp2) in (0, 2, 4) else -2)))
    passion_score = min(99, max(55, 85 if elem1 in ("Fire", "Air") and elem2 in ("Fire", "Air") else 78))
    communication_score = min(99, max(62, 88 if abs(num1["birthday_number"]["number"] - num2["birthday_number"]["number"]) <= 3 else 75))
    security_score = min(99, max(65, 92 if elem1 in ("Earth", "Water") and elem2 in ("Earth", "Water") else 80))

    overall_score = round((romantic_score * 0.35) + (passion_score * 0.25) + (communication_score * 0.20) + (security_score * 0.20))

    # Determine Synergy Badge & Title
    if overall_score >= 88:
        synergy_title = "🔥 High Soulmate Connection"
        synergy_badge = "Platinum Harmony"
    elif overall_score >= 78:
        synergy_title = "✨ Harmonious Growth Partners"
        synergy_badge = "Gold Synergy"
    elif overall_score >= 68:
        synergy_title = "⚡ Dynamic Catalyst Connection"
        synergy_badge = "Silver Balance"
    else:
        synergy_title = "🌊 Transformative Growth Union"
        synergy_badge = "Bronze Awakening"

    # Astrological Synastry Inter-Chart Aspects
    astrological_aspects = [
        {
            "aspect": f"Sun-Sun Alignment ({chart1['sun_sign']} & {chart2['sun_sign']})",
            "type": "Identity & Ego Synergy",
            "analysis": f"{p1_name}'s {chart1['sun_sign']} Sun and {p2_name}'s {chart2['sun_sign']} Sun create a shared {elem1}-{elem2} vitality connection."
        },
        {
            "aspect": f"Moon & Emotional Harmony ({chart1['moon_sign']} & {chart2['moon_sign']})",
            "type": "Subconscious Connection",
            "analysis": f"Emotions align through {chart1['moon_sign']} and {chart2['moon_sign']} lunar placements."
        },
        {
            "aspect": f"Mercury Mental Dialogue ({chart1['planets']['Mercury']['sign']} & {chart2['planets']['Mercury']['sign']})",
            "type": "Communication Style",
            "analysis": f"Intellectual exchange between {chart1['planets']['Mercury']['sign']} and {chart2['planets']['Mercury']['sign']} Mercury placements."
        }
    ]

    # Calculate Business Partnership Analysis
    business_partnership = calculate_business_compatibility(p1_name, chart1, num1, p2_name, chart2, num2)

    strengths = [
        f"Strong elemental chemistry between {elem1} and {elem2}.",
        f"Complementary Life Path energy (Life Path {lp1} & Life Path {lp2}).",
        "Mutual capacity for personal growth and shared life goals."
    ]

    friction_points = [
        "Be mindful of individual communication styles during high-stress periods.",
        "Ensure balance between personal independence and togetherness."
    ]

    advice = f"Nurture your relationship by leaning into your shared {elem_info['theme']}. Focus on open dialogue and appreciate your complementary strengths."

    return {
        "person1": {
            "name": p1_name,
            "sun_sign": chart1["sun_sign"],
            "moon_sign": chart1["moon_sign"],
            "element": elem1,
            "life_path": lp1,
            "driver_number": num1["loshu_grid"]["driver_number"]
        },
        "person2": {
            "name": p2_name,
            "sun_sign": chart2["sun_sign"],
            "moon_sign": chart2["moon_sign"],
            "element": elem2,
            "life_path": lp2,
            "driver_number": num2["loshu_grid"]["driver_number"]
        },
        "overall_compatibility_score": overall_score,
        "synergy_title": synergy_title,
        "synergy_badge": synergy_badge,
        "four_pillars": {
            "romantic_score": romantic_score,
            "passion_score": passion_score,
            "communication_score": communication_score,
            "security_score": security_score
        },
        "astrological_aspects": astrological_aspects,
        "business_partnership": business_partnership,
        "elemental_harmony": {
            "score": elem_info["score"],
            "theme": elem_info["theme"],
            "analysis": elem_info["analysis"]
        },
        "numerology_synergy": {
            "score": 90 if abs(lp1 - lp2) in (0, 2, 4) else 80,
            "analysis": lp_analysis
        },
        "strengths": strengths,
        "friction_points": friction_points,
        "actionable_advice": advice
    }
