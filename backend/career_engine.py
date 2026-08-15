"""
Profession & Vocation Predictions Engine
Analyzes Astrological 10th House/Midheaven, Dominant Elements, and Numerology Lo Shu Driver/Conductor numbers
to generate exhaustive, in-depth career predictions and professional alignment guides.
"""

from typing import Dict, Any, List


DRIVER_CAREER_MAP = {
    1: {
        "title": "Executive Leadership, Politics & Independent Business",
        "match_score": 96,
        "professions": ["CEO / Managing Director", "Government Official / Politician", "Entrepreneur / Founder", "Management Consultant", "Military Officer"],
        "strengths": "Natural authority, high courage, visionary decision-making, and independence. Thrives when leading teams and setting strategic direction.",
        "wealth_vibe": "High potential for independent business ownership and top executive roles. Prefers full autonomy over micromanagement."
    },
    2: {
        "title": "Diplomacy, Counseling, HR & Artistic Production",
        "match_score": 92,
        "professions": ["Psychologist / Marriage Counselor", "Human Resources Director", "Diplomat / Mediator", "Luxury Brand Designer", "Musician / Artist"],
        "strengths": "Deep empathy, emotional intelligence, peacemaking, and intuitive partner handling. Outstanding team mediator.",
        "wealth_vibe": "Thrives in partnerships, collaborative joint ventures, and advisory roles rather than solo aggressive selling."
    },
    3: {
        "title": "Education, Law, Publishing, Media & Financial Advisory",
        "match_score": 95,
        "professions": ["University Professor / Lecturer", "Corporate Lawyer / Judge", "Financial Planner / Wealth Advisor", "Author / Journalist", "Public Speaker"],
        "strengths": "Expansive intellect, inspiring communication, optimism, and deep mastery of complex subjects.",
        "wealth_vibe": "Generates wealth through knowledge-sharing, high-level advisory, publishing, and financial markets."
    },
    4: {
        "title": "Real Estate, Engineering, Accounting & System Architecture",
        "match_score": 94,
        "professions": ["Real Estate Developer", "Chartered Accountant / Auditor", "Civil / Software Engineer", "Project Manager", "Architect"],
        "strengths": "Methodical discipline, stamina, practical organization, and building lasting concrete structures.",
        "wealth_vibe": "Builds substantial long-term assets through property, systematic investments, and disciplined corporate climbing."
    },
    5: {
        "title": "E-Commerce, Trading, Marketing, PR & Travel",
        "match_score": 97,
        "professions": ["Stock / Crypto Trader", "E-Commerce Founder", "Marketing & PR Director", "Travel / Hospitality Mogul", "International Broker"],
        "strengths": "Rapid adaptability, commercial acumen, high networking charisma, and fast decision-making.",
        "wealth_vibe": "Exceptional commercial luck in fast-paced markets, global trade, digital sales, and multi-stream income ventures."
    },
    6: {
        "title": "Luxury Goods, Fashion, Entertainment, Hospitality & Decor",
        "match_score": 95,
        "professions": ["Fashion Designer / Stylist", "Interior Designer / Architect", "Luxury Hotelier / Restaurateur", "Film / Media Producer", "Cosmetics Brand Owner"],
        "strengths": "Refined aesthetic taste, magnetic charm, building luxury environments, and customer devotion.",
        "wealth_vibe": "High financial prosperity through premium branding, beauty, entertainment, and high-end consumer goods."
    },
    7: {
        "title": "Data Science, Research, Technology, Occult & Analytics",
        "match_score": 93,
        "professions": ["AI / Data Research Scientist", "Cybersecurity Specialist", "Scientific Researcher", "Astrologer / Occult Scholar", "Investigative Analyst"],
        "strengths": "Profound analytical focus, research discipline, intuitive deduction, and uncovering hidden truths.",
        "wealth_vibe": "Succeeds through specialized expert knowledge, technical patents, research grants, and high-tech consulting."
    },
    8: {
        "title": "Corporate Power, Banking, Asset Management & Heavy Industry",
        "match_score": 96,
        "professions": ["Investment Banker / Venture Capitalist", "Corporate Chairman / VP", "Mining & Infrastructure Director", "Commercial Lawyer", "Real Estate Investor"],
        "strengths": "Executive stamina, material mastery, handling large capital flows, and long-term strategic patience.",
        "wealth_vibe": "Destined for large-scale financial management, corporate power, and substantial property portfolios."
    },
    9: {
        "title": "Public Defense, Sports, Global Non-Profits, Health & Leadership",
        "match_score": 94,
        "professions": ["Surgeon / Medical Specialist", "Public Advocate / Humanitarian Leader", "Professional Athlete / Coach", "Defense Force Commander", "Social Enterprise Founder"],
        "strengths": "Fierce courage, high stamina, public charisma, and devotion to noble global causes.",
        "wealth_vibe": "Achieves high public fame and financial success through high-impact leadership, healthcare, and sports."
    }
}

ELEMENT_CAREER_SUITABILITY = {
    "Fire": {
        "domain": "Action, Sales, Executive Leadership & Innovation",
        "recommended": ["Tech Startups", "Commercial Sales", "Public Relations", "Emergency Healthcare", "Entertainment & Media"],
        "work_style": "Fast-paced, goal-oriented, competitive, and dynamic environment with opportunity to lead."
    },
    "Earth": {
        "domain": "Finance, Real Estate, Manufacturing & Operations",
        "recommended": ["Banking & Investments", "Real Estate & Construction", "Agriculture & Mining", "Supply Chain Management"],
        "work_style": "Structured, stable, predictable, and rewarded for long-term loyalty and concrete results."
    },
    "Air": {
        "domain": "Software, Communications, Media & Strategic Consulting",
        "recommended": ["Software Engineering & Tech", "Journalism & Media Production", "Legal & Academic Advisory", "Marketing Strategy"],
        "work_style": "Intellectually stimulating, flexible, collaborative, and rich in creative dialogue."
    },
    "Water": {
        "domain": "Healing, Arts, Hospitality, HR & Intuitive Care",
        "recommended": ["Psychology & Counseling", "Healthcare & Nursing", "Hospitality & Culinary Arts", "Artistic Direction"],
        "work_style": "Supportive, empathetic, harmonious, and aligned with personal values and community care."
    }
}


def calculate_profession_predictions(chart_data: Dict[str, Any], num_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes comprehensive profession predictions combining Astrological 10th House/Midheaven & Numerology Lo Shu grid.
    """
    # 1. Numerology Driver & Conductor
    loshu = num_data.get("loshu_grid", {})
    driver_num = loshu.get("driver_number", 1)
    conductor_num = loshu.get("conductor_number", 1)
    life_path_num = num_data.get("life_path", {}).get("number", 1)

    # Primary Career Profile from Driver Number
    driver_career = DRIVER_CAREER_MAP.get(driver_num, DRIVER_CAREER_MAP[1])
    secondary_career = DRIVER_CAREER_MAP.get(conductor_num, DRIVER_CAREER_MAP[5])

    # 2. Astrological Dominant Element & Sun/Moon/Rising
    sun_sign = chart_data.get("sun_sign", "Aries")
    elements = chart_data.get("elements", {"Fire": 2, "Earth": 2, "Air": 2, "Water": 2})

    # Determine dominant element
    dominant_elem = max(elements, key=elements.get)
    elem_career = ELEMENT_CAREER_SUITABILITY.get(dominant_elem, ELEMENT_CAREER_SUITABILITY["Fire"])

    # 3. Entrepreneurship vs Employment Suitability Rating
    if driver_num in (1, 5, 8, 9) or dominant_elem in ("Fire", "Earth"):
        business_rating = 92
        business_verdict = "🚀 Highly Favorable for Business Ownership & Entrepreneurship. You possess natural leadership, financial ambition, and commercial resilience."
    elif driver_num in (3, 4, 6) or dominant_elem == "Air":
        business_rating = 82
        business_verdict = "💼 Excellent for Independent Consulting, Partnerships & Executive Management. Thrives in specialized professional firms."
    else:
        business_rating = 72
        business_verdict = "🤝 Favorable for Strategic Partnerships, Collaborative Advisory & Creative Directorships. Pair with a strong operational partner for business ventures."

    # 4. Top Recommended High-Success Career Sectors
    recommended_sectors = [
        {
            "sector_name": driver_career["title"],
            "match_percentage": driver_career["match_score"],
            "top_job_titles": driver_career["professions"],
            "core_strengths": driver_career["strengths"],
            "financial_outlook": driver_career["wealth_vibe"]
        },
        {
            "sector_name": secondary_career["title"],
            "match_percentage": secondary_career["match_score"] - 3,
            "top_job_titles": secondary_career["professions"],
            "core_strengths": secondary_career["strengths"],
            "financial_outlook": secondary_career["wealth_vibe"]
        },
        {
            "sector_name": f"{dominant_elem} Element Domain: {elem_career['domain']}",
            "match_percentage": 88,
            "top_job_titles": elem_career["recommended"],
            "core_strengths": f"Natural affinity with {dominant_elem} element energy. Thrives in {elem_career['work_style']}",
            "financial_outlook": "High career satisfaction and financial flow when working in alignment with your dominant elemental environment."
        }
    ]

    # 5. Career Sectors to Avoid (Friction Domains)
    avoid_sectors = []
    if driver_num in (1, 8, 9):
        avoid_sectors.append("Highly repetitive, low-autonomy clerical roles without promotion prospects.")
    elif driver_num in (3, 7):
        avoid_sectors.append("Aggressive micro-managed high-volume sales cold-calling without intellectual depth.")
    elif driver_num in (4, 8):
        avoid_sectors.append("Unstructured, speculative get-rich-quick schemes without legal/financial backing.")
    elif driver_num in (5, 6):
        avoid_sectors.append("Isolated, static roles with no client contact or travel flexibility.")
    else:
        avoid_sectors.append("High-conflict, chaotic work environments lacking harmony and stability.")

    # 6. Actionable Career Elevation Remedies
    remedies = {
        "career_colors": "Ice Cyan, Sapphire Blue, Cosmic Gold",
        "office_fengshui": f"Position your executive workspace facing North (for career flow & Mercury) or East (for expansion & Jupiter).",
        "power_days": "Mondays & Thursdays for key contract signings and business launches.",
        "career_affirmation": f"'I am magnetically aligned with extraordinary career opportunities, high financial prosperity, and professional fulfillment.'"
    }

    return {
        "overall_career_title": f"The {driver_career['title'].split(',')[0]} Architect",
        "business_ownership_rating": business_rating,
        "business_verdict": business_verdict,
        "dominant_career_element": dominant_elem,
        "driver_conductor_synergy": f"Driver Number #{driver_num} & Conductor Number #{conductor_num}",
        "top_recommended_sectors": recommended_sectors,
        "sectors_to_avoid": avoid_sectors,
        "work_environment_style": elem_career["work_style"],
        "career_elevation_remedies": remedies
    }
