/**
 * Interactive 360° Vector SVG Natal Wheel Renderer — Cold Professional Palette
 * Renders Zodiac Ring, House Division Cusps, Planetary Glyphs, and Aspect Lines.
 */

const ZODIAC_SYMBOLS = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"];
const ZODIAC_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];

// Professional Cold Element Colors: Fire (Cool Coral), Earth (Teal Mint), Air (Ice Cyan), Water (Sapphire Blue)
const ZODIAC_COLORS = [
    "#f87171", "#2dd4bf", "#38bdf8", "#60a5fa",
    "#f87171", "#2dd4bf", "#38bdf8", "#60a5fa",
    "#f87171", "#2dd4bf", "#38bdf8", "#60a5fa"
];

function renderNatalWheel(svgContainer, chartData) {
    const size = 460;
    const center = size / 2;
    const rOuter = 210;
    const rInner = 170;
    const rPlanets = 135;
    const rAspects = 100;

    const ascendantDeg = (chartData && chartData.planets && chartData.planets.Ascendant && typeof chartData.planets.Ascendant.longitude === 'number') 
        ? chartData.planets.Ascendant.longitude 
        : 0;

    // Convert ecliptic degree to SVG wheel angle (ASC set to left 180°)
    function degToRad(deg) {
        const d = typeof deg === 'number' ? deg : 0;
        const adjustedDeg = (d - ascendantDeg + 180) % 360;
        return (adjustedDeg * Math.PI) / 180;
    }

    let svg = `<svg width="100%" height="100%" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">`;

    // 1. Background Circles (Cold Platinum & Ice Cyan Strokes)
    svg += `<circle cx="${center}" cy="${center}" r="${rOuter}" fill="rgba(15, 23, 42, 0.7)" stroke="#38bdf8" stroke-width="2" />`;
    svg += `<circle cx="${center}" cy="${center}" r="${rInner}" fill="none" stroke="rgba(226, 232, 240, 0.2)" stroke-width="1.5" />`;
    svg += `<circle cx="${center}" cy="${center}" r="${rAspects}" fill="rgba(7, 10, 18, 0.88)" stroke="rgba(56, 189, 248, 0.25)" stroke-width="1" />`;

    // 2. Render 12 Zodiac Segments (30° each)
    for (let i = 0; i < 12; i++) {
        const startAngle = degToRad(i * 30);
        const midAngle = degToRad(i * 30 + 15);

        // Divider lines
        const x1 = center + rOuter * Math.cos(startAngle);
        const y1 = center + rOuter * Math.sin(startAngle);
        const x2 = center + rInner * Math.cos(startAngle);
        const y2 = center + rInner * Math.sin(startAngle);

        svg += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="rgba(226, 232, 240, 0.15)" stroke-width="1" />`;

        // Zodiac Symbol text with click action
        const symbolX = center + ((rOuter + rInner) / 2) * Math.cos(midAngle);
        const symbolY = center + ((rOuter + rInner) / 2) * Math.sin(midAngle);

        svg += `
            <g class="natal-zodiac-node" data-zodiac="${ZODIAC_NAMES[i]}" style="cursor: pointer;">
                <text x="${symbolX}" y="${symbolY + 5}" font-size="16" fill="${ZODIAC_COLORS[i]}" text-anchor="middle" font-family="Outfit">${ZODIAC_SYMBOLS[i]}</text>
                <title>Zodiac Sign: ${ZODIAC_NAMES[i]} (Click for sign guide)</title>
            </g>
        `;
    }

    // 3. Render House Cusps with click action
    if (chartData && chartData.houses) {
        chartData.houses.forEach((h) => {
            const cDeg = typeof h.cusp_longitude === 'number' ? h.cusp_longitude : ((h.house - 1) * 30);
            const angle = degToRad(cDeg);
            const x1 = center + rInner * Math.cos(angle);
            const y1 = center + rInner * Math.sin(angle);
            const x2 = center + rAspects * Math.cos(angle);
            const y2 = center + rAspects * Math.sin(angle);

            const isMainAxis = h.house === 1 || h.house === 10;
            const color = isMainAxis ? "#38bdf8" : "rgba(226, 232, 240, 0.25)";
            const width = isMainAxis ? 2.5 : 1.5;

            svg += `
                <g class="natal-house-node" data-house="${h.house}" style="cursor: pointer;">
                    <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}" />
                    <title>${h.name || 'House'} (${h.domain || ''}) - Click for House Guide</title>
                </g>
            `;
        });
    }

    // 4. Render Aspect Lines (Cool Ice Cyan & Sapphire Blue)
    if (chartData && chartData.aspects && chartData.planets) {
        chartData.aspects.forEach((asp, idx) => {
            const p1 = chartData.planets[asp.body1];
            const p2 = chartData.planets[asp.body2];

            if (p1 && p2) {
                const a1 = degToRad(p1.longitude);
                const a2 = degToRad(p2.longitude);

                const x1 = center + rAspects * Math.cos(a1);
                const y1 = center + rAspects * Math.sin(a1);
                const x2 = center + rAspects * Math.cos(a2);
                const y2 = center + rAspects * Math.sin(a2);

                let strokeColor = "rgba(148, 163, 184, 0.3)";
                if (asp.nature && asp.nature.includes("Harmonious")) strokeColor = "rgba(56, 189, 248, 0.6)";
                if (asp.nature && asp.nature.includes("Challenging")) strokeColor = "rgba(129, 140, 248, 0.7)";

                svg += `
                    <g class="natal-aspect-node" data-aspect-index="${idx}" style="cursor: pointer;">
                        <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${strokeColor}" stroke-width="1.6" stroke-dasharray="${asp.aspect === 'Sextile' ? '3,3' : 'none'}"></line>
                        <title>Aspect: ${asp.body1} ${asp.symbol || ''} ${asp.body2} (${asp.aspect}) - Click for Aspect Guide</title>
                    </g>
                `;
            }
        });
    }

    // 5. Render Planet Glyphs (Interactive Planet Nodes)
    if (chartData && chartData.planets) {
        Object.values(chartData.planets).forEach((p) => {
            const pDeg = typeof p.longitude === 'number' ? p.longitude : 0;
            const angle = degToRad(pDeg);
            const px = center + rPlanets * Math.cos(angle);
            const py = center + rPlanets * Math.sin(angle);

            svg += `
                <g class="natal-planet-node" data-planet="${p.name}" style="cursor: pointer;">
                    <circle cx="${px}" cy="${py}" r="14" fill="rgba(15, 23, 42, 0.95)" stroke="#38bdf8" stroke-width="2" />
                    <text x="${px}" y="${py + 4}" font-size="13" fill="#e2e8f0" text-anchor="middle" font-weight="bold">${p.symbol || '☉'}</text>
                    <title>${p.name}: ${p.formatted || p.sign} (${p.house_name || ''}) - Click for Planet Guide</title>
                </g>
            `;
        });
    }

    svg += `</svg>`;
    svgContainer.innerHTML = svg;

    // Attach Click Event Listener to SVG elements
    bindNatalWheelClickEvents(svgContainer, chartData);
}

function bindNatalWheelClickEvents(svgContainer, chartData) {
    const svgEl = svgContainer.querySelector("svg");
    if (!svgEl) return;

    svgEl.querySelectorAll(".natal-planet-node").forEach(node => {
        node.addEventListener("click", (e) => {
            e.stopPropagation();
            const pName = node.getAttribute("data-planet");
            const pData = chartData.planets[pName];
            if (pData && typeof openAstrologyGuideModal === "function") {
                openAstrologyGuideModal("planet", pData);
            }
        });
    });

    svgEl.querySelectorAll(".natal-house-node").forEach(node => {
        node.addEventListener("click", (e) => {
            e.stopPropagation();
            const hNum = parseInt(node.getAttribute("data-house"));
            const hData = chartData.houses.find(h => h.house === hNum);
            if (hData && typeof openAstrologyGuideModal === "function") {
                openAstrologyGuideModal("house", hData);
            }
        });
    });

    svgEl.querySelectorAll(".natal-aspect-node").forEach(node => {
        node.addEventListener("click", (e) => {
            e.stopPropagation();
            const aspIdx = parseInt(node.getAttribute("data-aspect-index"));
            const aspData = chartData.aspects[aspIdx];
            if (aspData && typeof openAstrologyGuideModal === "function") {
                openAstrologyGuideModal("aspect", aspData);
            }
        });
    });

    svgEl.querySelectorAll(".natal-zodiac-node").forEach(node => {
        node.addEventListener("click", (e) => {
            e.stopPropagation();
            const zName = node.getAttribute("data-zodiac");
            if (zName && typeof openAstrologyGuideModal === "function") {
                openAstrologyGuideModal("zodiac", { name: zName });
            }
        });
    });
}
