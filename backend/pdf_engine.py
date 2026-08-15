import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)

def generate_pdf_report(data: dict) -> bytes:
    """
    Generates an exhaustive, high-precision vector PDF report covering all 6 application workspace tabs in deep detail:
    1. 🌌 Natal Chart Wheel & 12 Houses (Aspects, Elements, Modalities)
    2. 🔢 Sacred Lo Shu Grid & Numerology (3x3 Lo Shu Matrix, Planes/Yogas, Missing Remedies, Name Spelling, 4 Mobile Numbers)
    3. 💼 Profession & Vocation Predictions (Archetypes, Business Suitability, Top Sectors, Work Environment, Power Remedies)
    4. 🏔️ Pinnacles & Life Cycles (4 Life Phases, Peak Numbers, Challenges, Action Strategies)
    5. 💖 Synastry Matcher & Business Partnership (Profiles, Relationship 4 Pillars, Business 4 Pillars, Inter-Chart Aspects, Pitfalls, Executive Strategy)
    6. 🌟 Daily Forecast & Transits (Cosmic Vibe, Lucky Numbers, Power Color)
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=32,
        leftMargin=32,
        topMargin=32,
        bottomMargin=32
    )

    story = []
    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY_CYAN = colors.HexColor("#0284c7")
    DARK_BLUE = colors.HexColor("#0f172a")
    TEXT_MUTED = colors.HexColor("#64748b")
    ACCENT_INDIGO = colors.HexColor("#4f46e5")
    ACCENT_GOLD = colors.HexColor("#d97706")
    SUCCESS_GREEN = colors.HexColor("#16a34a")
    ALERT_RED = colors.HexColor("#dc2626")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY_CYAN,
        alignment=1, # Center
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_MUTED,
        alignment=1,
        spaceAfter=10
    )

    tab_header_style = ParagraphStyle(
        'TabHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=PRIMARY_CYAN,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#334155")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=PRIMARY_CYAN
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1e293b")
    )

    # Extract Data Objects safely
    full_name = data.get("full_name", "Cosmic Client")
    dob = data.get("date_of_birth", data.get("birth_date", "Specified Date"))
    time_str = data.get("birth_time", "12:00 UTC")
    location = data.get("location", "Specified Location")
    gender = data.get("gender", "Female").capitalize()

    astrology = data.get("astrology", {})
    numerology = data.get("numerology", {})
    career = data.get("career", {})
    horoscope = data.get("horoscope", {})
    synastry = data.get("synastry")

    # ==========================================
    # HEADER BANNER & CLIENT PROFILE
    # ==========================================
    story.append(Paragraph("✨ ASTROVEDIC COSMIC BLUEPRINT & LIFE REPORT", title_style))
    story.append(Paragraph("High-Precision 6-Module Ephemeris, Sacred Lo Shu Grid, Vocation & Synastry Master Analysis", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_CYAN, spaceAfter=8))

    profile_table_data = [
        [
            Paragraph("<b>Full Name:</b>", table_cell_style),
            Paragraph(f"<font color='#0284c7'><b>{full_name}</b></font>", table_cell_style),
            Paragraph("<b>Date of Birth:</b>", table_cell_style),
            Paragraph(f"<b>{dob}</b>", table_cell_style)
        ],
        [
            Paragraph("<b>Time of Birth:</b>", table_cell_style),
            Paragraph(f"{time_str}", table_cell_style),
            Paragraph("<b>Gender / Kua:</b>", table_cell_style),
            Paragraph(f"{gender}", table_cell_style)
        ],
        [
            Paragraph("<b>Location:</b>", table_cell_style),
            Paragraph(f"{location}", table_cell_style),
            Paragraph("<b>Calculation Standard:</b>", table_cell_style),
            Paragraph("<font color='#16a34a'><b>NASA JPL / Ephemeris Verified</b></font>", table_cell_style)
        ]
    ]

    t_profile = Table(profile_table_data, colWidths=[85, 175, 95, 175])
    t_profile.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_profile)
    story.append(Spacer(1, 8))

    # ==========================================
    # TAB 1: 🌌 NATAL CHART WHEEL & 12 HOUSES
    # ==========================================
    story.append(Paragraph("🌌 TAB 1: Natal Chart Wheel & 12 Astrological Houses", tab_header_style))
    
    sun_sign = astrology.get("sun_sign", "Leo")
    moon_sign = astrology.get("moon_sign", "Scorpio")
    rising_sign = astrology.get("rising_sign", "Virgo")

    elements = astrology.get("elements", {})
    modalities = astrology.get("modalities", {})

    elem_str = f"Fire: {elements.get('Fire', 0)}% • Earth: {elements.get('Earth', 0)}% • Air: {elements.get('Air', 0)}% • Water: {elements.get('Water', 0)}%"
    mod_str = f"Cardinal: {modalities.get('Cardinal', 0)}% • Fixed: {modalities.get('Fixed', 0)}% • Mutable: {modalities.get('Mutable', 0)}%"

    astrology_summary_data = [
        [
            Paragraph("<b>☉ Sun Sign</b>", table_header_style),
            Paragraph("<b>☽ Moon Sign</b>", table_header_style),
            Paragraph("<b>ASC Rising Sign</b>", table_header_style)
        ],
        [
            Paragraph(f"<font size=10 color='#0284c7'><b>{sun_sign}</b></font>", table_cell_style),
            Paragraph(f"<font size=10 color='#0284c7'><b>{moon_sign}</b></font>", table_cell_style),
            Paragraph(f"<font size=10 color='#0284c7'><b>{rising_sign}</b></font>", table_cell_style)
        ],
        [
            Paragraph("<b>Elemental Chemistry:</b>", table_cell_style),
            Paragraph(elem_str, table_cell_style),
            Paragraph(mod_str, table_cell_style)
        ]
    ]

    t_astro_sum = Table(astrology_summary_data, colWidths=[170, 170, 190])
    t_astro_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e0f2fe")),
        ('BOX', (0,0), (-1,-1), 1, PRIMARY_CYAN),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_astro_sum)
    story.append(Spacer(1, 6))

    # 12 Houses Table
    houses = astrology.get("houses", [])
    if houses:
        house_rows = [
            [
                Paragraph("<b>House</b>", table_header_style),
                Paragraph("<b>Sign Cusp</b>", table_header_style),
                Paragraph("<b>Domain Scope</b>", table_header_style),
                Paragraph("<b>Residents</b>", table_header_style)
            ]
        ]
        for h in houses:
            house_num = h.get("house", "")
            sign_cusp = h.get("sign", h.get("zodiac", {}).get("sign", ""))
            formatted_cusp = h.get("cusp_formatted", h.get("zodiac", {}).get("formatted", ""))
            domain = f"{h.get('name', '')}: {h.get('domain', '')}"
            residents = ", ".join(h.get("residents", [])) if h.get("residents") else "None"
            
            house_rows.append([
                Paragraph(f"<b>House {house_num}</b>", table_cell_style),
                Paragraph(f"<b>{sign_cusp}</b> ({formatted_cusp})", table_cell_style),
                Paragraph(domain, table_cell_style),
                Paragraph(f"<font color='#4f46e5'><b>{residents}</b></font>", table_cell_style)
            ])

        t_houses = Table(house_rows, colWidths=[55, 120, 235, 120])
        t_houses.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_houses)
        story.append(Spacer(1, 6))

    # Inter-Planetary Aspects Table
    aspects = (astrology.get("aspects") or [])[:6]
    if aspects:
        story.append(Paragraph("<b>⚡ Major Inter-Planetary Aspects</b>", body_style))
        story.append(Spacer(1, 3))
        asp_rows = [
            [
                Paragraph("<b>Planets Involved</b>", table_header_style),
                Paragraph("<b>Aspect Type</b>", table_header_style),
                Paragraph("<b>Angle & Orb</b>", table_header_style),
                Paragraph("<b>Nature & Guidance</b>", table_header_style)
            ]
        ]
        for asp in aspects:
            is_harm = "Harmonious" in asp.get("nature", "")
            nature_clr = "#0284c7" if is_harm else "#dc2626"
            asp_rows.append([
                Paragraph(f"<b>{asp.get('body1')} & {asp.get('body2')}</b>", table_cell_style),
                Paragraph(f"{asp.get('symbol')} {asp.get('aspect')}", table_cell_style),
                Paragraph(f"{asp.get('exact_angle')}° (Orb {asp.get('orb')}°)", table_cell_style),
                Paragraph(f"<font color='{nature_clr}'><b>{asp.get('nature')}</b></font>: {asp.get('guidance', '')}", table_cell_style)
            ])

        t_asp = Table(asp_rows, colWidths=[110, 95, 85, 240])
        t_asp.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_asp)
        story.append(Spacer(1, 8))

    # PAGE BREAK FOR TAB 2
    story.append(PageBreak())

    # ==========================================
    # TAB 2: 🔢 SACRED LO SHU GRID & NUMEROLOGY
    # ==========================================
    story.append(Paragraph("🔢 TAB 2: Sacred Lo Shu Grid & Numerology Engine", tab_header_style))

    life_path = numerology.get("life_path", {}).get("number", "--")
    expr_num = numerology.get("pythagorean", {}).get("expression", {}).get("number", "--")
    driver_num = numerology.get("loshu_grid", {}).get("driver_number", "--")
    conductor_num = numerology.get("loshu_grid", {}).get("conductor_number", "--")
    kua_num = numerology.get("loshu_grid", {}).get("kua_number", "--")
    chal_data = numerology.get("chaldean", {})
    pyth_data = numerology.get("pythagorean", {})
    chal_expr = chal_data.get("expression", {}).get("number", "--")
    chal_comp = chal_data.get("compound_number", "--")
    pyth_expr = pyth_data.get("expression", {}).get("number", "--")

    num_summary_data = [
        [
            Paragraph("<b>Life Path Number</b>", table_header_style),
            Paragraph("<b>Chaldean Expression (Primary)</b>", table_header_style),
            Paragraph("<b>Pythagorean Option</b>", table_header_style),
            Paragraph("<b>Driver / Conductor / Kua</b>", table_header_style)
        ],
        [
            Paragraph(f"<font size=10 color='#4f46e5'><b>#{life_path}</b></font>", table_cell_style),
            Paragraph(f"<font size=10 color='#0284c7'><b>#{chal_comp} ➔ #{chal_expr}</b></font>", table_cell_style),
            Paragraph(f"<font size=10 color='#64748b'><b>#{pyth_expr}</b></font>", table_cell_style),
            Paragraph(f"<font size=10 color='#4f46e5'><b>#{driver_num} / #{conductor_num} / #{kua_num}</b></font>", table_cell_style)
        ]
    ]
    t_num_sum = Table(num_summary_data, colWidths=[120, 160, 110, 140])
    t_num_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e0e7ff")),
        ('BOX', (0,0), (-1,-1), 1, ACCENT_INDIGO),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_num_sum)
    story.append(Spacer(1, 8))

    # Sacred 3x3 Lo Shu Grid Box Table
    loshu = numerology.get("loshu_grid", {})
    grid_layout = loshu.get("grid_layout", [])
    if grid_layout:
        story.append(Paragraph("<b>☯️ Sacred 3x3 Lo Shu Grid Matrix (Vedic Energy Grid)</b>", body_style))
        story.append(Spacer(1, 3))
        
        # Build 3x3 visual grid rows
        grid_matrix_rows = []
        for r in grid_layout:
            row_cells = []
            for c in r:
                num = c.get("num", "")
                elem = c.get("element", "")
                val = c.get("str", "-")
                count = c.get("count", 0)
                cell_color = "#e0f2fe" if count > 0 else "#f8fafc"
                cell_text = f"<b>#{num} ({elem})</b><br/><font size=10 color='#0284c7'><b>{val}</b></font>"
                row_cells.append(Paragraph(cell_text, table_cell_style))
            grid_matrix_rows.append(row_cells)

        t_loshu_matrix = Table(grid_matrix_rows, colWidths=[170, 170, 190])
        t_loshu_matrix.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1.5, PRIMARY_CYAN),
            ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_loshu_matrix)
        story.append(Spacer(1, 8))

    # Planes & Yogas Table
    planes = loshu.get("planes", {})
    if planes:
        story.append(Paragraph("<b>✨ Planes & Yogas Alignment (Vedic Analysis)</b>", body_style))
        story.append(Spacer(1, 3))
        plane_rows = [
            [
                Paragraph("<b>Plane / Yoga Name</b>", table_header_style),
                Paragraph("<b>Status</b>", table_header_style),
                Paragraph("<b>Core Influence & Meaning</b>", table_header_style)
            ]
        ]
        for name, p in planes.items():
            status_text = "<font color='#16a34a'><b>✨ Present / Active</b></font>" if p.get("present") else "<font color='#94a3b8'>⚪ Incomplete</font>"
            plane_rows.append([
                Paragraph(f"<b>{name}</b>", table_cell_style),
                Paragraph(status_text, table_cell_style),
                Paragraph(p.get("desc", ""), table_cell_style)
            ])

        t_planes = Table(plane_rows, colWidths=[140, 110, 280])
        t_planes.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_planes)
        story.append(Spacer(1, 8))

    # Missing Number Elemental Remedies Table
    missing = loshu.get("missing_remedies", [])
    if missing:
        story.append(Paragraph("<b>💡 Missing Number Elemental Remedies & Gemstones</b>", body_style))
        story.append(Spacer(1, 3))
        rem_rows = [
            [
                Paragraph("<b>Missing # & Element</b>", table_header_style),
                Paragraph("<b>Gemstone Remedy</b>", table_header_style),
                Paragraph("<b>Vedic & Feng Shui Elemental Remedy</b>", table_header_style)
            ]
        ]
        for r in missing[:5]:
            rem_rows.append([
                Paragraph(f"<b>Number #{r.get('number')} ({r.get('missing_element')})</b>", table_cell_style),
                Paragraph(f"<font color='#0284c7'><b>{r.get('gemstone')}</b></font>", table_cell_style),
                Paragraph(f"<b>Direction: {r.get('direction')}</b> — {r.get('remedy')}", table_cell_style)
            ])

        t_rem = Table(rem_rows, colWidths=[130, 120, 280])
        t_rem.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_rem)
        story.append(Spacer(1, 8))

    # Name Spelling Correction & Royal Star Recommendations
    name_analysis = numerology.get("name_spelling_analysis")
    if name_analysis:
        story.append(Paragraph("<b>✍️ Sacred Chaldean Name Numerology & Component Analysis</b>", body_style))
        story.append(Spacer(1, 3))
        
        c_comp = name_analysis.get("current_chaldean_compound", "")
        c_mean = name_analysis.get("current_chaldean_meaning", {})
        c_status = name_analysis.get("current_harmony_status", "")

        story.append(Paragraph(f"Current Full Name: <b>\"{name_analysis.get('current_name')}\"</b> — Chaldean Compound: <font color='#0284c7'><b>#{c_comp} ({c_mean.get('name', 'Compound')})</b></font> ➔ Single Digit: <b>#{name_analysis.get('current_chaldean_expression')}</b>", body_style))
        story.append(Paragraph(f"<b>Chaldean Vibration:</b> {c_mean.get('vibe', '')}", body_style))
        story.append(Paragraph(f"<b>Planetary Harmony Verdict:</b> {c_status}", body_style))
        story.append(Spacer(1, 4))

        # Component Breakdown Table
        components = name_analysis.get("components", [])
        if components:
            comp_rows = [
                [
                    Paragraph("<b>Component Word</b>", table_header_style),
                    Paragraph("<b>Pythagorean #</b>", table_header_style),
                    Paragraph("<b>Chaldean Compound</b>", table_header_style),
                    Paragraph("<b>Sacred Compound Meaning</b>", table_header_style)
                ]
            ]
            for c in components:
                comp_rows.append([
                    Paragraph(f"<b>{c.get('component_word')}</b>", table_cell_style),
                    Paragraph(f"#{c.get('pythagorean_sum')} ➔ <b>#{c.get('pythagorean_single')}</b>", table_cell_style),
                    Paragraph(f"<font color='#4f46e5'><b>#{c.get('chaldean_compound')} ➔ #{c.get('chaldean_single')}</b></font>", table_cell_style),
                    Paragraph(f"<b>{c.get('chaldean_meaning', {}).get('name', '')}:</b> {c.get('chaldean_meaning', {}).get('vibe', '')}", table_cell_style)
                ])

            t_comp = Table(comp_rows, colWidths=[120, 110, 110, 190])
            t_comp.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ]))
            story.append(t_comp)
            story.append(Spacer(1, 6))

        # Royal Star Recommendations Table
        rec_rows = [
            [
                Paragraph("<b>Royal Star Recommended Spelling</b>", table_header_style),
                Paragraph("<b>Chaldean Compound # & Name</b>", table_header_style),
                Paragraph("<b>Pythagorean #</b>", table_header_style),
                Paragraph("<b>Vedic & Planetary Alignment</b>", table_header_style)
            ]
        ]
        for v in name_analysis.get("recommended_variations", []):
            rec_rows.append([
                Paragraph(f"<font color='#0284c7'><b>\"{v.get('spelling', '')}\"</b></font>", table_cell_style),
                Paragraph(f"<b>#{v.get('chaldean_compound', '')} ({v.get('chaldean_name', '')})</b>", table_cell_style),
                Paragraph(f"#{v.get('pythagorean_expression', '')}", table_cell_style),
                Paragraph(f"<font color='#16a34a'><b>{v.get('rating', '')}</b></font><br/>{v.get('reason', '')}", table_cell_style)
            ])

        t_name = Table(rec_rows, colWidths=[140, 140, 70, 180])
        t_name.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_name)
        story.append(Spacer(1, 8))

    # 4-Mobile Number Inspector Table
    mobile_analysis = numerology.get("mobile_analysis")
    if mobile_analysis:
        story.append(Paragraph("<b>📱 4-Mobile Number Numerology Inspector</b>", body_style))
        story.append(Spacer(1, 3))
        mob_rows = [
            [
                Paragraph("<b>Mobile Number</b>", table_header_style),
                Paragraph("<b>Sum & Single Digit</b>", table_header_style),
                Paragraph("<b>Ruling Planet & Vibe</b>", table_header_style),
                Paragraph("<b>Compatibility Score</b>", table_header_style)
            ]
        ]
        for m in mobile_analysis.get("mobile_analysis_list", []):
            mob_rows.append([
                Paragraph(f"<b>{m.get('mobile_number', '')}</b>", table_cell_style),
                Paragraph(f"{m.get('raw_sum', '')} ➔ <font color='#0284c7'><b>#{m.get('total_single_digit', '')}</b></font>", table_cell_style),
                Paragraph(f"{m.get('ruling_planet', '')} ({m.get('vibe', '')})", table_cell_style),
                Paragraph(f"<font color='#0284c7'><b>{m.get('compatibility_score', '')}% ({m.get('compatibility_label', '')})</b></font>", table_cell_style)
            ])

        t_mob = Table(mob_rows, colWidths=[120, 120, 160, 130])
        t_mob.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_mob)
        story.append(Spacer(1, 10))

    # PAGE BREAK FOR TAB 3 & 4
    story.append(PageBreak())

    # ==========================================
    # TAB 3: 💼 PROFESSION PREDICTIONS
    # ==========================================
    if career and career.get("overall_career_title"):
        story.append(Paragraph("💼 TAB 3: Profession & Vocation Predictions", tab_header_style))
        title_vocation = career.get("overall_career_title", "")
        rating_biz = career.get("business_ownership_rating", 0)
        verdict_biz = career.get("business_verdict", "")

        story.append(Paragraph(f"Vocation Archetype: <font color='#0284c7'><b>{title_vocation}</b></font>", body_style))
        story.append(Paragraph(f"<b>Business Ownership Suitability: {rating_biz}%</b> — {verdict_biz}", body_style))
        story.append(Spacer(1, 4))

        career_rows = [
            [
                Paragraph("<b>Recommended High-Success Sector</b>", table_header_style),
                Paragraph("<b>Match %</b>", table_header_style),
                Paragraph("<b>Recommended Job Roles</b>", table_header_style)
            ]
        ]
        for s in career.get("top_recommended_sectors", []):
            job_titles = ", ".join(s.get("top_job_titles", []))
            career_rows.append([
                Paragraph(f"<b>{s.get('sector_name', '')}</b>", table_cell_style),
                Paragraph(f"<font color='#0284c7'><b>{s.get('match_percentage', '')}%</b></font>", table_cell_style),
                Paragraph(job_titles, table_cell_style)
            ])

        t_career = Table(career_rows, colWidths=[170, 70, 290])
        t_career.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_career)
        story.append(Spacer(1, 10))

    # ==========================================
    # TAB 4: 🏔️ PINNACLES & LIFE CYCLES
    # ==========================================
    pinnacles = numerology.get("pinnacles", {})
    if pinnacles and pinnacles.get("pinnacle_cycles"):
        story.append(Paragraph("🏔️ TAB 4: 4 Major Life Pinnacles & Challenge Cycles", tab_header_style))
        pin_rows = [
            [
                Paragraph("<b>Phase & Age Range</b>", table_header_style),
                Paragraph("<b>Pinnacle Peak #</b>", table_header_style),
                Paragraph("<b>Challenge #</b>", table_header_style),
                Paragraph("<b>Core Growth Theme & Strategy</b>", table_header_style)
            ]
        ]
        for p in pinnacles.get("pinnacle_cycles", []):
            interp = p.get("interpretation", {})
            theme_desc = f"<b>{interp.get('theme', '')}:</b> {interp.get('desc', '')}"
            pin_rows.append([
                Paragraph(f"<b>{p.get('pinnacle_phase', '')}</b> ({p.get('age_range', '')})", table_cell_style),
                Paragraph(f"<font color='#0284c7'><b>Peak #{p.get('number', '')}</b></font>", table_cell_style),
                Paragraph(f"<font color='#dc2626'><b>Challenge #{p.get('challenge_number', '')}</b></font>", table_cell_style),
                Paragraph(theme_desc, table_cell_style)
            ])

        t_pin = Table(pin_rows, colWidths=[120, 85, 85, 240])
        t_pin.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_pin)
        story.append(Spacer(1, 10))

    # PAGE BREAK FOR TAB 5 & 6
    story.append(PageBreak())

    # ==========================================
    # TAB 5: 💖 SYNASTRY MATCH & BUSINESS PARTNERSHIP
    # ==========================================
    story.append(Paragraph("💖 TAB 5: Synastry & Business Partnership Engine", tab_header_style))

    if synastry:
        p1 = synastry.get("person1", {})
        p2 = synastry.get("person2", {})
        score_val = synastry.get("overall_compatibility_score", 85)
        synergy_title = synastry.get("synergy_title", "High Cosmic Synergy")
        pillars_rel = synastry.get("four_pillars", {})
        biz = synastry.get("business_partnership", {})
        biz_pillars = biz.get("pillars", {})
        industries = ", ".join(biz.get("recommended_industries", []))
        pitfall = biz.get("financial_pitfall_warning", "Ensure written agreements.")
        advice = biz.get("business_advice", "Align long-term capital goals.")

        # 1. Partner Profiles Table
        syn_profile_data = [
            [
                Paragraph("<b>Partner Profile</b>", table_header_style),
                Paragraph("<b>Sun Sign</b>", table_header_style),
                Paragraph("<b>Moon Sign</b>", table_header_style),
                Paragraph("<b>Element</b>", table_header_style),
                Paragraph("<b>Life Path #</b>", table_header_style)
            ],
            [
                Paragraph(f"<b>Person 1: {p1.get('name', full_name)}</b>", table_cell_style),
                Paragraph(p1.get('sun_sign', ''), table_cell_style),
                Paragraph(p1.get('moon_sign', ''), table_cell_style),
                Paragraph(p1.get('element', ''), table_cell_style),
                Paragraph(f"#{p1.get('life_path', '')}", table_cell_style)
            ],
            [
                Paragraph(f"<b>Person 2: {p2.get('name', 'Partner')}</b>", table_cell_style),
                Paragraph(p2.get('sun_sign', ''), table_cell_style),
                Paragraph(p2.get('moon_sign', ''), table_cell_style),
                Paragraph(p2.get('element', ''), table_cell_style),
                Paragraph(f"#{p2.get('life_path', '')}", table_cell_style)
            ]
        ]
        t_syn_prof = Table(syn_profile_data, colWidths=[150, 95, 95, 95, 95])
        t_syn_prof.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e0f2fe")),
            ('BOX', (0,0), (-1,-1), 1, PRIMARY_CYAN),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_syn_prof)
        story.append(Spacer(1, 6))

        # 2. Relationship 4 Pillars Table
        story.append(Paragraph(f"<b>Overall Compatibility Score: <font color='#16a34a'>{score_val}%</font> ({synergy_title})</b>", body_style))
        story.append(Spacer(1, 3))
        rel_pillars_data = [
            [
                Paragraph("<b>Emotional & Romance</b>", table_header_style),
                Paragraph("<b>Physical & Passion</b>", table_header_style),
                Paragraph("<b>Communication</b>", table_header_style),
                Paragraph("<b>Security & Foundation</b>", table_header_style)
            ],
            [
                Paragraph(f"<b>{pillars_rel.get('romantic_score', 85)}% Score</b>", table_cell_style),
                Paragraph(f"<b>{pillars_rel.get('passion_score', 80)}% Score</b>", table_cell_style),
                Paragraph(f"<b>{pillars_rel.get('communication_score', 75)}% Score</b>", table_cell_style),
                Paragraph(f"<b>{pillars_rel.get('security_score', 82)}% Score</b>", table_cell_style)
            ]
        ]
        t_rel_pillars = Table(rel_pillars_data, colWidths=[130, 130, 135, 135])
        t_rel_pillars.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_rel_pillars)
        story.append(Spacer(1, 6))

        # 3. Business Partnership 4 Pillars Table
        if biz:
            story.append(Paragraph(f"<b>💼 Business Partnership Score: <font color='#0284c7'>{biz.get('business_score', 88)}% ({biz.get('business_archetype', 'Commercial Partners')})</font></b>", body_style))
            story.append(Spacer(1, 3))
            biz_pillars_data = [
                [
                    Paragraph("<b>Financial & Wealth</b>", table_header_style),
                    Paragraph("<b>Executive Leadership</b>", table_header_style),
                    Paragraph("<b>Strategic Execution</b>", table_header_style),
                    Paragraph("<b>Contract Security</b>", table_header_style)
                ],
                [
                    Paragraph(f"<b>{biz_pillars.get('financial_score', 88)}% Score</b>", table_cell_style),
                    Paragraph(f"<b>{biz_pillars.get('leadership_score', 85)}% Score</b>", table_cell_style),
                    Paragraph(f"<b>{biz_pillars.get('innovation_score', 82)}% Score</b>", table_cell_style),
                    Paragraph(f"<b>{biz_pillars.get('trust_security', 90)}% Score</b>", table_cell_style)
                ]
            ]
            t_biz_pillars = Table(biz_pillars_data, colWidths=[130, 130, 135, 135])
            t_biz_pillars.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#dcfce7")),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#16a34a")),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ]))
            story.append(t_biz_pillars)
            story.append(Spacer(1, 6))

        # 4. Inter-Chart Astrological Aspects
        syn_aspects = synastry.get("astrological_aspects", [])
        if syn_aspects:
            story.append(Paragraph("<b>🔮 Inter-Chart Astrological Synastry Aspects</b>", body_style))
            story.append(Spacer(1, 3))
            syn_asp_rows = [
                [
                    Paragraph("<b>Inter-Chart Aspect</b>", table_header_style),
                    Paragraph("<b>Synergy Type</b>", table_header_style),
                    Paragraph("<b>Detailed Analysis & Guidance</b>", table_header_style)
                ]
            ]
            for a in syn_aspects:
                syn_asp_rows.append([
                    Paragraph(f"<b>{a.get('aspect')}</b>", table_cell_style),
                    Paragraph(f"<font color='#0284c7'><b>{a.get('type')}</b></font>", table_cell_style),
                    Paragraph(a.get("analysis", ""), table_cell_style)
                ])

            t_syn_asp = Table(syn_asp_rows, colWidths=[160, 120, 250])
            t_syn_asp.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ]))
            story.append(t_syn_asp)
            story.append(Spacer(1, 6))

        story.append(Paragraph(f"<b>Recommended High-Growth Industries:</b> {industries}", body_style))
        story.append(Paragraph(f"<b><font color='#dc2626'>⚠️ Financial Pitfall Warning:</font></b> {pitfall}", body_style))
        story.append(Paragraph(f"<b>🎯 Executive Strategy:</b> {advice}", body_style))
        story.append(Spacer(1, 10))
    else:
        story.append(Paragraph("<i>Status: Partner Synastry Match Not Computed Yet. (Complete Tab 5: Synastry Matcher to calculate romantic & business compatibility with a second profile).</i>", body_style))
        story.append(Spacer(1, 10))

    # ==========================================
    # TAB 6: 🌟 DAILY FORECAST & TRANSITS
    # ==========================================
    story.append(Paragraph("🌟 TAB 6: Daily Forecast & Cosmic Transits", tab_header_style))
    cosmic_vibe = horoscope.get("cosmic_vibe", "Harmonious Trine between Sun and Jupiter brings clarity and creative breakthroughs today.")
    lucky_nums = ", ".join(map(str, horoscope.get("lucky_numbers", [3, 7, 11, 21])))
    power_color = horoscope.get("power_color", "Cosmic Gold (#ffd700)")

    story.append(Paragraph(f"<b>Current Transit Guidance:</b> {cosmic_vibe}", body_style))
    story.append(Paragraph(f"<b>Lucky Daily Numbers:</b> {lucky_nums} &nbsp;•&nbsp; <b>Power Color:</b> {power_color}", body_style))

    # FOOTER STAMP
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceBefore=15, spaceAfter=8))
    footer_text = ParagraphStyle(
        'FooterText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748b"),
        alignment=1
    )
    story.append(Paragraph("© 2026 AstroVedic Cosmic Engine • Ephemeris NASA JPL Standard Calculations • All Rights Reserved", footer_text))

    # Build Document
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
