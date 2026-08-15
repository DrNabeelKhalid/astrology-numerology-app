/**
 * Main Application Logic Engine
 * Manages API calls, tab switching, form handling, and UI updates.
 */

const API_BASE = (window.location.origin && window.location.origin.startsWith("http")) 
    ? `${window.location.origin}/api` 
    : "http://127.0.0.1:8000/api";

document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    initForms();
    initLocationSearch();
    fetchDailyHoroscope();
    generateCosmicBlueprint();
});

window.addEventListener("load", () => {
    generateCosmicBlueprint();
});

// Location Search & Autocomplete Engine
function initLocationSearch() {
    const cityInput = document.getElementById("city_search");
    const dropdown = document.getElementById("city-suggestions");
    const latInput = document.getElementById("latitude_val");
    const lonInput = document.getElementById("longitude_val");
    const badge = document.getElementById("coord-badge");
    const geoBtn = document.getElementById("btn-geo");

    let debounceTimer;

    // OpenStreetMap Nominatim Free Geocoding API
    cityInput.addEventListener("input", () => {
        clearTimeout(debounceTimer);
        const query = cityInput.value.trim();
        if (query.length < 2) {
            dropdown.classList.remove("show");
            return;
        }

        debounceTimer = setTimeout(async () => {
            try {
                const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5`);
                const cities = await res.json();

                if (cities.length === 0) {
                    dropdown.classList.remove("show");
                    return;
                }

                dropdown.innerHTML = cities.map(c => `
                    <div class="suggestion-item" data-lat="${c.lat}" data-lon="${c.lon}" data-name="${c.display_name}">
                        📍 ${c.display_name}
                    </div>
                `).join("");

                dropdown.classList.add("show");

                document.querySelectorAll(".suggestion-item").forEach(item => {
                    item.addEventListener("click", () => {
                        const lat = parseFloat(item.dataset.lat).toFixed(4);
                        const lon = parseFloat(item.dataset.lon).toFixed(4);
                        const displayName = item.dataset.name.split(",").slice(0, 2).join(",");

                        cityInput.value = displayName;
                        latInput.value = lat;
                        lonInput.value = lon;
                        badge.textContent = `Coords: ${Math.abs(lat)}° ${lat >= 0 ? 'N' : 'S'}, ${Math.abs(lon)}° ${lon >= 0 ? 'E' : 'W'}`;
                        dropdown.classList.remove("show");
                    });
                });
            } catch (err) {
                console.error("Geocoding lookup error:", err);
            }
        }, 300);
    });

    // Close dropdown on click outside
    document.addEventListener("click", (e) => {
        if (!cityInput.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.remove("show");
        }
    });

    // GPS Geolocation Handler
    geoBtn.addEventListener("click", () => {
        if ("geolocation" in navigator) {
            geoBtn.textContent = "⏳ Locating...";
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    const lat = pos.coords.latitude.toFixed(4);
                    const lon = pos.coords.longitude.toFixed(4);
                    latInput.value = lat;
                    lonInput.value = lon;
                    cityInput.value = "Current GPS Location";
                    badge.textContent = `Coords: ${Math.abs(lat)}° ${lat >= 0 ? 'N' : 'S'}, ${Math.abs(lon)}° ${lon >= 0 ? 'E' : 'W'}`;
                    geoBtn.textContent = "📍 GPS";
                },
                (err) => {
                    alert("Unable to retrieve GPS location. Please type your city manually.");
                    geoBtn.textContent = "📍 GPS";
                }
            );
        } else {
            alert("Geolocation is not supported by your browser.");
        }
    });
}

// Tab Navigation
function initTabs() {
    const tabBtns = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));

            btn.classList.add("active");
            const targetId = btn.getAttribute("data-tab");
            document.getElementById(targetId).classList.add("active");
        });
    });
}

window.reportRequirements = {
    profile: false,
    mobile: false,
    synastry: false
};

function updatePDFUnlockChecklist() {
    const chkProfile = document.getElementById("chk-profile");
    const chkMobile = document.getElementById("chk-mobile");
    const chkSynastry = document.getElementById("chk-synastry");
    const pdfBtn = document.getElementById("btn-download-pdf");
    const pdfBtnText = document.getElementById("pdf-btn-text");

    if (chkProfile) {
        chkProfile.innerHTML = window.reportRequirements.profile ? 
            `<strong style="color: #38bdf8;">🟢 Step 1: Birth Profile Computed</strong>` : 
            `⚪ Step 1: Birth Profile Computed`;
    }

    if (chkMobile) {
        chkMobile.innerHTML = window.reportRequirements.mobile ? 
            `<strong style="color: #38bdf8;">🟢 Step 2: Mobile Numbers Analyzed</strong>` : 
            `⚪ Step 2: Mobile Numbers Analyzed`;
    }

    if (chkSynastry) {
        chkSynastry.innerHTML = window.reportRequirements.synastry ? 
            `<strong style="color: #38bdf8;">🟢 Step 3: Tab 5 Synastry Match Computed</strong>` : 
            `⚪ Step 3: Tab 5 Synastry Match Computed`;
    }

    const count = (window.reportRequirements.profile ? 1 : 0) + 
                  (window.reportRequirements.mobile ? 1 : 0) + 
                  (window.reportRequirements.synastry ? 1 : 0);

    if (pdfBtn && pdfBtnText) {
        if (count === 3) {
            pdfBtn.disabled = false;
            pdfBtn.style.opacity = "1";
            pdfBtn.style.cursor = "pointer";
            pdfBtn.style.background = "linear-gradient(135deg, #10b981, #059669)";
            pdfBtn.style.borderColor = "#34d399";
            pdfBtnText.innerHTML = "📄 Download Full PDF Report (3/3 Complete)";
            pdfBtn.title = "All 3 requirements completed! Click to download your full PDF report.";
        } else {
            pdfBtn.disabled = true;
            pdfBtn.style.opacity = "0.45";
            pdfBtn.style.cursor = "not-allowed";
            pdfBtn.style.background = "linear-gradient(135deg, #0284c7, #38bdf8)";
            pdfBtn.style.borderColor = "#38bdf8";
            pdfBtnText.innerHTML = `🔒 Download PDF Report (${count}/3 Steps)`;
            pdfBtn.title = "Please complete all 3 steps (Birth Profile, Mobile Numbers, and Tab 5 Synastry) to unlock your PDF report.";
        }
    }
}

// Form Handlers
function initForms() {
    const profileForm = document.getElementById("profile-form");
    profileForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        await generateCosmicBlueprint();
    });

    const synastryForm = document.getElementById("synastry-form");
    synastryForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        await generateSynastryMatch();
    });

    // Live Mobile Number Inspector Handlers
    const mobileBtn = document.getElementById("analyze-mobile-btn");
    if (mobileBtn) {
        mobileBtn.addEventListener("click", async () => {
            await recalculateMobileNumbers();
        });
    }

    // Download PDF Report Handler
    const pdfBtn = document.getElementById("btn-download-pdf");
    if (pdfBtn) {
        pdfBtn.addEventListener("click", async () => {
            if (window.exportFullCosmicPDFReport) {
                await window.exportFullCosmicPDFReport(
                    window.currentAstrologyData,
                    window.currentNumerologyData,
                    window.currentCareerData
                );
            }
        });
    }

    ["mobile_1", "mobile_2", "mobile_3", "mobile_4"].forEach(id => {
        const inp = document.getElementById(id);
        if (inp) {
            inp.addEventListener("input", debounce(async () => {
                await recalculateMobileNumbers();
            }, 400));
        }
    });

    updatePDFUnlockChecklist();
}

// Live Mobile Number Recalculation Engine
async function recalculateMobileNumbers() {
    const fullName = document.getElementById("full_name").value;
    const birthDate = document.getElementById("birth_date").value;
    const gender = document.getElementById("gender") ? document.getElementById("gender").value : "female";
    const [year, month, day] = birthDate.split("-").map(Number);

    const m1 = document.getElementById("mobile_1") ? document.getElementById("mobile_1").value : "";
    const m2 = document.getElementById("mobile_2") ? document.getElementById("mobile_2").value : "";
    const m3 = document.getElementById("mobile_3") ? document.getElementById("mobile_3").value : "";
    const m4 = document.getElementById("mobile_4") ? document.getElementById("mobile_4").value : "";
    const mobile_numbers = [m1, m2, m3, m4].filter(m => m && m.trim() !== "");

    if (!mobile_numbers.length) return;

    try {
        const res = await fetch(`${API_BASE}/numerology/calculate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                full_name: fullName,
                year, month, day,
                gender,
                mobile_numbers
            })
        });
        const data = await res.json();
        window.currentNumerologyData = data;
        
        // Render 4-Mobile Number Inspector Grid
        const mobileGrid = document.getElementById("mobile-analysis-grid");
        if (mobileGrid && data.mobile_analysis) {
            let mobHtml = "";
            data.mobile_analysis.mobile_analysis_list.forEach(mob => {
                const isBest = data.mobile_analysis.best_recommended_mobile && data.mobile_analysis.best_recommended_mobile.mobile_number === mob.mobile_number;
                mobHtml += `
                    <div class="synastry-detail-card" style="${isBest ? 'border-color: var(--accent-cyan); box-shadow: 0 0 20px var(--cyan-glow); background: rgba(56, 189, 248, 0.08);' : ''}">
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.06); padding-bottom: 0.4rem; margin-bottom: 0.5rem;">
                            <div>
                                <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Mobile #${mob.index}</span>
                                <h4 style="color: var(--accent-cyan); font-family: var(--font-heading); font-size: 1.15rem; margin: 0;">${mob.mobile_number}</h4>
                            </div>
                            ${isBest ? '<span class="synastry-title-badge" style="font-size: 0.75rem; padding: 0.2rem 0.6rem;">🏆 #1 Top Recommended</span>' : `<span style="font-size: 0.85rem; font-weight: 700; color: var(--accent-cyan);">${mob.compatibility_score}% Score</span>`}
                        </div>
                        <div style="font-size: 0.88rem; color: var(--text-main); margin-bottom: 0.3rem;">
                            Digit Sum: <strong>${mob.raw_sum}</strong> &nbsp;➔&nbsp; Total Single Digit: <strong style="color: var(--accent-cyan); font-size: 1.1rem;">#${mob.total_single_digit}</strong>
                        </div>
                        <p style="font-size: 0.85rem; color: var(--accent-indigo); font-weight: 600; margin: 0.2rem 0;">🪐 Ruling Planet: ${mob.ruling_planet}</p>
                        <p style="font-size: 0.83rem; color: var(--text-muted); margin-top: 0.3rem;"><strong>Vibe:</strong> ${mob.vibe}</p>
                        <p style="font-size: 0.83rem; color: var(--text-muted); margin-top: 0.2rem;"><strong>Best Suited For:</strong> ${mob.best_suited_for}</p>
                        <p style="font-size: 0.83rem; color: var(--accent-cyan); font-weight: 600; margin-top: 0.4rem;">${mob.compatibility_label}</p>
                    </div>
                `;
            });
            mobileGrid.innerHTML = mobHtml;
        }

        window.reportRequirements.mobile = true;
        updatePDFUnlockChecklist();
    } catch (err) {
        console.error("Error updating mobile numbers:", err);
    }
}

// Debounce helper
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

async function generateCosmicBlueprint() {
    const fullName = (document.getElementById("full_name")?.value || "Celeste Vance").trim();
    const rawDate = document.getElementById("birth_date")?.value || "1996-07-24";
    const rawTime = document.getElementById("birth_time")?.value || "14:30";
    const gender = document.getElementById("gender")?.value || "female";
    
    let latVal = parseFloat(document.getElementById("latitude_val")?.value);
    let lonVal = parseFloat(document.getElementById("longitude_val")?.value);
    const latitude = isNaN(latVal) ? 40.7128 : latVal;
    const longitude = isNaN(lonVal) ? -74.0060 : lonVal;

    const m1 = document.getElementById("mobile_1") ? document.getElementById("mobile_1").value : "";
    const m2 = document.getElementById("mobile_2") ? document.getElementById("mobile_2").value : "";
    const m3 = document.getElementById("mobile_3") ? document.getElementById("mobile_3").value : "";
    const m4 = document.getElementById("mobile_4") ? document.getElementById("mobile_4").value : "";
    const mobile_numbers = [m1, m2, m3, m4].filter(m => m && m.trim() !== "");

    let [year, month, day] = (rawDate && rawDate.includes("-")) ? rawDate.split("-").map(Number) : [1996, 7, 24];
    let [hour, minute] = (rawTime && rawTime.includes(":")) ? rawTime.split(":").map(Number) : [14, 30];

    if (isNaN(year) || !year) year = 1996;
    if (isNaN(month) || !month) month = 7;
    if (isNaN(day) || !day) day = 24;
    if (isNaN(hour)) hour = 14;
    if (isNaN(minute)) minute = 30;

    const payload = {
        full_name: fullName || "Celeste Vance",
        year, month, day,
        gender,
        hour, minute,
        latitude, longitude,
        mobile_numbers: mobile_numbers.length ? mobile_numbers : ["9876543210", "9123456789"]
    };

    try {
        // Fetch Natal Chart
        const chartRes = await fetch(`${API_BASE}/astrology/natal-chart`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const chartData = await chartRes.json();
        window.currentAstrologyData = chartData;
        updateAstrologyUI(chartData);

        // Fetch Numerology Profile
        const numRes = await fetch(`${API_BASE}/numerology/calculate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const numData = await numRes.json();
        window.currentNumerologyData = numData;
        updateNumerologyUI(numData);

        // Fetch Profession & Career Predictions
        const careerRes = await fetch(`${API_BASE}/career/predictions`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const careerData = await careerRes.json();
        window.currentCareerData = careerData;
        updateCareerUI(careerData);

        window.reportRequirements.profile = true;
        if (mobile_numbers && mobile_numbers.length) {
            window.reportRequirements.mobile = true;
        }
        updatePDFUnlockChecklist();

    } catch (err) {
        console.error("API Connection Error:", err);
        // Fallback for standalone preview if backend server is offline
        renderOfflineFallback(payload);
    }
}

function updateAstrologyUI(data) {
    // Big Three
    document.getElementById("sun-sign-val").textContent = `${data.sun_sign} ☉`;
    document.getElementById("moon-sign-val").textContent = `${data.moon_sign} ☽`;
    document.getElementById("asc-sign-val").textContent = `${data.rising_sign} ASC`;

    // Render SVG Natal Wheel
    const wheelContainer = document.getElementById("svg-wheel-container");
    renderNatalWheel(wheelContainer, data);

    // Elements & Modalities
    const elementsContainer = document.getElementById("elements-grid");
    let elemHtml = "";
    Object.entries(data.elements).forEach(([elem, count]) => {
        const pct = Math.round((count / 8) * 100);
        elemHtml += `
            <div class="bar-item">
                <div class="bar-label">
                    <span>${elem}</span>
                    <span>${count} (${pct}%)</span>
                </div>
                <div class="bar-track">
                    <div class="bar-fill" style="width: ${pct}%;"></div>
                </div>
            </div>
        `;
    });
    elementsContainer.innerHTML = elemHtml;

    const modalitiesContainer = document.getElementById("modalities-grid");
    if (modalitiesContainer && data.modalities) {
        let modHtml = "";
        Object.entries(data.modalities).forEach(([mod, count]) => {
            const pct = Math.round((count / 8) * 100);
            modHtml += `
                <div class="bar-item">
                    <div class="bar-label">
                        <span style="color: var(--accent-indigo);">${mod}</span>
                        <span>${count} (${pct}%)</span>
                    </div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width: ${pct}%; background: linear-gradient(90deg, #818cf8, #c084fc);"></div>
                    </div>
                </div>
            `;
        });
        modalitiesContainer.innerHTML = modHtml;
    }

    // Planets Table with interactive row click
    const tbody = document.getElementById("planets-table-body");
    let tableHtml = "";
    Object.values(data.planets).forEach(p => {
        tableHtml += `
            <tr style="cursor: pointer;" onclick="openAstrologyGuideModal('planet', ${JSON.stringify(p).replace(/"/g, '&quot;')})" title="Click to view full guide for ${p.name}">
                <td><strong>${p.symbol} ${p.name}</strong></td>
                <td>${p.sign}</td>
                <td>${p.formatted}</td>
                <td><strong style="color: var(--accent-cyan);">House ${p.house}</strong></td>
                <td>${p.element}</td>
            </tr>
        `;
    });
    tbody.innerHTML = tableHtml;

    // 12 Astrological Houses Table Renderer
    const housesTbody = document.getElementById("houses-table-body");
    if (housesTbody && data.houses) {
        let hHtml = "";
        data.houses.forEach(h => {
            const hSign = h.sign || (h.zodiac ? h.zodiac.sign : "Aries");
            const hCusp = h.cusp_formatted || (h.zodiac ? h.zodiac.formatted : "0° Aries");
            const residentsStr = h.residents && h.residents.length > 0 ? h.residents.join(", ") : "None";
            hHtml += `
                <tr style="cursor: pointer;" onclick="openAstrologyGuideModal('house', ${JSON.stringify(h).replace(/"/g, '&quot;')})" title="Click to view deep house domain guide for ${h.name}">
                    <td><strong style="color: var(--accent-cyan);">House ${h.house}</strong></td>
                    <td><strong>${hSign} (${hCusp})</strong></td>
                    <td>
                        <div style="font-weight: 600; color: var(--text-main);">${h.name}</div>
                        <small style="color: var(--text-muted);">${h.domain}</small>
                    </td>
                    <td><span style="color: var(--accent-indigo); font-weight: 600;">${residentsStr}</span></td>
                    <td style="font-size: 0.85rem; color: var(--text-muted);">${h.guidance}</td>
                </tr>
            `;
        });
        housesTbody.innerHTML = hHtml;
    }

    // Inter-Planetary Aspects Table Renderer
    const aspectsTbody = document.getElementById("aspects-table-body");
    if (aspectsTbody && data.aspects) {
        let aHtml = "";
        data.aspects.forEach(asp => {
            const isHarmonious = asp.nature.includes("Harmonious");
            aHtml += `
                <tr style="cursor: pointer;" onclick="openAstrologyGuideModal('aspect', ${JSON.stringify(asp).replace(/"/g, '&quot;')})" title="Click to view planetary aspect guide for ${asp.body1} ${asp.symbol} ${asp.body2}">
                    <td><strong>${asp.body1} & ${asp.body2}</strong></td>
                    <td><span style="color: var(--accent-cyan); font-weight: 700;">${asp.symbol} ${asp.aspect}</span></td>
                    <td>${asp.exact_angle}° (Orb ${asp.orb}°)</td>
                    <td>
                        <span class="synastry-title-badge" style="font-size: 0.75rem; padding: 0.2rem 0.55rem; ${isHarmonious ? 'background: rgba(56,189,248,0.12); color: #38bdf8;' : 'background: rgba(248,113,113,0.12); color: #f87171;'}">
                            ${asp.nature}
                        </span>
                    </td>
                    <td style="font-size: 0.85rem; color: var(--text-muted);">${asp.guidance}</td>
                </tr>
            `;
        });
        aspectsTbody.innerHTML = aHtml;
    }
}

// Global Interactive Astrology Guide Modal Renderer
function openAstrologyGuideModal(type, data) {
    const modal = document.getElementById("loshu-cell-modal");
    const modalTitle = document.getElementById("modal-cell-title");
    const modalBody = document.getElementById("modal-cell-body");
    if (!modal || !modalTitle || !modalBody) return;

    if (type === "planet") {
        modalTitle.textContent = `${data.symbol} ${data.name} in ${data.formatted} (${data.house_name})`;
        modalBody.innerHTML = `
            <div class="modal-detail-row" style="border-color: var(--accent-cyan);">
                <label>Cosmic Archetype & Core Role</label>
                <p style="font-size: 1.1rem; color: var(--accent-cyan); font-weight: 700;">
                    ${data.symbol} ${data.archetype}
                </p>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 0.3rem;">${data.overview}</p>
            </div>

            <div class="modal-detail-row">
                <label>Zodiac Sign Manifestation</label>
                <p>${data.sign_interpretation}</p>
            </div>

            <div class="modal-detail-row">
                <label>House Position & Life Domain</label>
                <p>${data.house_interpretation}</p>
            </div>

            <div class="modal-detail-row" style="border-color: rgba(56, 189, 248, 0.4);">
                <label style="color: var(--accent-cyan);">🎯 Practical Life Guide & Action Strategy</label>
                <p>${data.guidance}</p>
            </div>
        `;
    } else if (type === "house") {
        modalTitle.textContent = `🏰 ${data.name}`;
        modalBody.innerHTML = `
            <div class="modal-detail-row" style="border-color: var(--accent-cyan);">
                <label>Life Domain & Scope</label>
                <p style="font-size: 1.05rem; color: var(--accent-cyan); font-weight: 700;">
                    ${data.domain}
                </p>
            </div>
            <div class="modal-detail-row">
                <label>House Cusp Sign & Degrees</label>
                <p>Cusp Degree: <strong>${data.cusp_formatted || (data.zodiac ? data.zodiac.formatted : '0° Cusp')} (${data.sign || (data.zodiac ? data.zodiac.sign : '')})</strong></p>
            </div>
            <div class="modal-detail-row">
                <label>Resident Planets in this House</label>
                <p>${data.residents && data.residents.length > 0 ? data.residents.join(", ") : 'No major planets present in this house cusp.'}</p>
            </div>
            <div class="modal-detail-row" style="border-color: rgba(56, 189, 248, 0.4);">
                <label style="color: var(--accent-cyan);">🎯 House Mastery Guidance</label>
                <p>${data.guidance}</p>
            </div>
        `;
    } else if (type === "aspect") {
        modalTitle.textContent = `⚡ Aspect: ${data.body1} ${data.symbol} ${data.body2} (${data.aspect})`;
        modalBody.innerHTML = `
            <div class="modal-detail-row" style="border-color: var(--accent-cyan);">
                <label>Aspect Nature & Synergy</label>
                <p style="font-size: 1.05rem; color: var(--accent-cyan); font-weight: 700;">
                    ${data.nature} — ${data.theme || 'Planetary Alignment'}
                </p>
            </div>
            <div class="modal-detail-row">
                <label>Orb Precision</label>
                <p>Exact Angle: <strong>${data.exact_angle}°</strong> (Orb: ${data.orb}°)</p>
            </div>
            <div class="modal-detail-row" style="border-color: rgba(129, 140, 248, 0.4);">
                <label style="color: var(--accent-indigo);">💡 Aspect Guidance & Integration Strategy</label>
                <p>${data.guidance || 'Channel this planetary conversation into conscious growth.'}</p>
            </div>
        `;
    } else if (type === "zodiac") {
        modalTitle.textContent = `✨ Zodiac Sign: ${data.name}`;
        modalBody.innerHTML = `
            <div class="modal-detail-row">
                <label>Zodiac Archetype</label>
                <p>Exploring chart placements in the sign of ${data.name}. Click any planet node on the wheel to see how it operates in ${data.name}.</p>
            </div>
        `;
    }

    modal.classList.add("show");
}

function updateNumerologyUI(data) {
    // 1. Driver, Conductor & Kua
    if (data.loshu_grid) {
        document.getElementById("driver-num-val").textContent = data.loshu_grid.driver_number;
        document.getElementById("conductor-num-val").textContent = data.loshu_grid.conductor_number;
        if (document.getElementById("kua-num-val")) {
            document.getElementById("kua-num-val").textContent = data.loshu_grid.kua_number;
        }

        // Helper to render 3x3 cells
        function buildGridHtml(gridMatrix) {
            let html = "";
            gridMatrix.forEach(row => {
                row.forEach(cell => {
                    const hasNum = cell.count > 0;
                    html += `
                        <div class="loshu-cell ${hasNum ? 'has-number' : 'empty'}" data-num="${cell.num}" title="Click to view Number ${cell.num} details & implications">
                            <span class="loshu-cell-num">#${cell.num}</span>
                            <span class="loshu-cell-elem">${cell.element}</span>
                            <span class="loshu-cell-val">${hasNum ? cell.str : '-'}</span>
                        </div>
                    `;
                });
            });
            return html;
        }

        // Render Pure DOB Grid
        const pureGridBox = document.getElementById("pure-loshu-grid-box");
        if (pureGridBox && data.loshu_grid.pure_dob_grid) {
            pureGridBox.innerHTML = buildGridHtml(data.loshu_grid.pure_dob_grid);
        }

        // Render Full Vedic Grid
        const fullGridBox = document.getElementById("loshu-grid-box");
        if (fullGridBox && data.loshu_grid.grid_layout) {
            fullGridBox.innerHTML = buildGridHtml(data.loshu_grid.grid_layout);
        }

        // Bind interactive click handlers on cells
        bindCellClickEvents(data.loshu_grid);

        // 3. Render Planes & Yogas
        const planesList = document.getElementById("loshu-planes-list");
        let planesHtml = "";
        Object.entries(data.loshu_grid.planes).forEach(([name, plane]) => {
            planesHtml += `
                <div class="plane-item ${plane.present ? 'active' : ''}">
                    <span class="plane-status">${plane.present ? '✨' : '⚪'}</span>
                    <div class="plane-text">
                        <h5>${name}</h5>
                        <p>${plane.desc}</p>
                    </div>
                </div>
            `;
        });
        planesList.innerHTML = planesHtml;

        // 4. Render Missing Number Remedies
        const remediesGrid = document.getElementById("missing-remedies-grid");
        let remediesHtml = "";
        if (data.loshu_grid.missing_numbers.length === 0) {
            remediesHtml = "<p style='color: var(--gold);'>🌟 Complete Lo Shu Balance — No missing number remedies required!</p>";
        } else {
            data.loshu_grid.missing_numbers.forEach(item => {
                remediesHtml += `
                    <div class="remedy-card">
                        <h5>Missing Number ${item.number} (${item.element} Element)</h5>
                        <p><strong>Remedy:</strong> ${item.remedy}</p>
                    </div>
                `;
            });
        }
        remediesGrid.innerHTML = remediesHtml;
    }

    // 5. Render Core Numbers Grid based on active system (Chaldean Primary Default)
    renderNumerologyCoreCards(data);
}

window.activeNumerologySystem = "chaldean";

function switchNumerologySystem(sys) {
    window.activeNumerologySystem = sys;
    const btnChal = document.getElementById("btn-sys-chaldean");
    const btnPyth = document.getElementById("btn-sys-pythagorean");
    if (btnChal && btnPyth) {
        btnChal.classList.toggle("active", sys === "chaldean");
        btnPyth.classList.toggle("active", sys === "pythagorean");
    }
    if (window.currentNumerologyData) {
        renderNumerologyCoreCards(window.currentNumerologyData);
    }
}

function renderNumerologyCoreCards(data) {
    const grid = document.getElementById("numerology-core-grid");
    if (!grid) return;

    const sys = window.activeNumerologySystem || "chaldean";
    const isChaldean = sys === "chaldean";
    const nameData = isChaldean ? data.chaldean : data.pythagorean;

    const exprNum = nameData.expression.number;
    const exprRaw = nameData.compound_number || nameData.expression.raw_sum || exprNum;
    const exprTitle = nameData.expression.meaning.title;
    const exprDesc = nameData.expression.meaning.description;

    const soulNum = nameData.soul_urge.number;
    const soulTitle = nameData.soul_urge.meaning.title;
    const soulDesc = nameData.soul_urge.meaning.description;

    const chalCompound = isChaldean && nameData.compound_meaning ? nameData.compound_meaning.name : "";

    grid.innerHTML = `
        <div class="num-card">
            <h4>Life Path Number</h4>
            <div class="num-badge">${data.life_path.number}</div>
            <div class="num-title">${data.life_path.meaning.title}</div>
            <p class="num-desc">${data.life_path.meaning.description}</p>
        </div>

        <div class="num-card" style="border-color: var(--accent-cyan); background: rgba(15, 23, 42, 0.9);">
            <h4>Expression Number (${isChaldean ? 'Chaldean Primary' : 'Pythagorean Option'})</h4>
            <div class="num-badge">${isChaldean ? `#${exprRaw} ➔ #${exprNum}` : exprNum}</div>
            <div class="num-title">${isChaldean && chalCompound ? `${chalCompound} (#${exprRaw})` : exprTitle}</div>
            <p class="num-desc">${exprDesc}</p>
            <small style="color: var(--accent-cyan); font-weight: 600; margin-top: 0.3rem;">
                ${isChaldean ? '🔯 Chaldean Sound Vibration System (Cheiro Standard)' : '📐 Pythagorean Western System'}
            </small>
        </div>

        <div class="num-card">
            <h4>Soul Urge Number (${isChaldean ? 'Chaldean Vowels' : 'Pythagorean Vowels'})</h4>
            <div class="num-badge">${soulNum}</div>
            <div class="num-title">${soulTitle}</div>
            <p class="num-desc">${soulDesc}</p>
        </div>

        <div class="num-card">
            <h4>Personal Year ${data.personal_year.target_year}</h4>
            <div class="num-badge">${data.personal_year.personal_year_number}</div>
            <div class="num-title">${data.personal_year.meaning.title}</div>
            <p class="num-desc">${data.personal_year.meaning.description}</p>
        </div>
    `;

    // System Comparison Matrix
    const matrix = document.getElementById("system-matrix");
    if (matrix) {
        matrix.innerHTML = `
            <div class="glass-panel" style="${isChaldean ? 'border-color: var(--accent-cyan); box-shadow: 0 0 15px var(--cyan-glow);' : ''}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="color: var(--accent-cyan);">🔯 Chaldean System (Primary Default)</h4>
                    ${isChaldean ? '<span class="synastry-title-badge" style="font-size: 0.75rem;">Active System</span>' : ''}
                </div>
                <p style="margin: 0.5rem 0; color: var(--text-main);">Chaldean Compound Expression: <strong style="color: var(--accent-cyan); font-size: 1.1rem;">#${data.chaldean.compound_number} (${data.chaldean.compound_meaning ? data.chaldean.compound_meaning.name : ''})</strong> ➔ Single Digit: <strong>#${data.chaldean.expression.number}</strong></p>
                <p style="margin: 0.4rem 0; color: var(--text-muted);">Soul Urge (Vowels): <strong>#${data.chaldean.soul_urge.number}</strong> &nbsp;•&nbsp; Personality (Consonants): <strong>#${data.chaldean.personality.number}</strong></p>
            </div>

            <div class="glass-panel" style="${!isChaldean ? 'border-color: var(--accent-cyan); box-shadow: 0 0 15px var(--cyan-glow);' : ''}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="color: var(--accent-indigo);">📐 Pythagorean System (Secondary Option)</h4>
                    ${!isChaldean ? '<span class="synastry-title-badge" style="font-size: 0.75rem;">Active System</span>' : ''}
                </div>
                <p style="margin: 0.5rem 0; color: var(--text-main);">Pythagorean Expression: <strong style="color: var(--accent-indigo); font-size: 1.1rem;">#${data.pythagorean.expression.number}</strong> (${data.pythagorean.expression.meaning.title})</p>
                <p style="margin: 0.4rem 0; color: var(--text-muted);">Soul Urge (Vowels): <strong>#${data.pythagorean.soul_urge.number}</strong> &nbsp;•&nbsp; Personality (Consonants): <strong>#${data.pythagorean.personality.number}</strong></p>
            </div>
        `;
    }

    // 7. Render 4 Life Pinnacles & Challenge Cycles
    const pinnaclesGrid = document.getElementById("pinnacles-timeline-grid");
    if (pinnaclesGrid && data.pinnacles) {
        let pinHtml = "";
        data.pinnacles.pinnacle_cycles.forEach((p, idx) => {
            pinHtml += `
                <div class="pinnacle-card" data-index="${idx}" title="Click to view complete details & action plan for ${p.pinnacle_phase}">
                    <span class="pinnacle-age-tag">${p.age_range}</span>
                    <h4 class="pinnacle-phase-title">${p.pinnacle_phase}</h4>
                    <div class="pinnacle-numbers-row">
                        <div class="pinnacle-num-box">
                            <label>Pinnacle Peak</label>
                            <span>${p.number}</span>
                        </div>
                        <div class="pinnacle-num-box challenge">
                            <label>Challenge</label>
                            <span>${p.challenge_number}</span>
                        </div>
                    </div>
                    <div class="pinnacle-theme">✨ ${p.interpretation.theme}</div>
                    <p class="pinnacle-desc">${p.interpretation.desc}</p>
                    <p class="pinnacle-desc" style="color: var(--accent-indigo); margin-top: 0.4rem;">
                        <strong>Challenge Guidance:</strong> ${p.challenge_interpretation.desc}
                    </p>
                    <small style="color: var(--accent-cyan); font-weight: 600; margin-top: 0.3rem;">🔍 Click card for complete strategy details</small>
                </div>
            `;
        });
        pinnaclesGrid.innerHTML = pinHtml;

        // Bind interactive click handlers on Pinnacle cards
        bindPinnacleClickEvents(data.pinnacles);
    }

    // 8. Render In-Depth Name Analysis & Spelling Correction Recommendations
    const nameBadge = document.getElementById("name-harmony-badge");
    const nameGrid = document.getElementById("name-spelling-grid");

    if (nameGrid && data.name_spelling_analysis) {
        const nData = data.name_spelling_analysis;
        if (nameBadge) nameBadge.textContent = nData.current_harmony_status;

        const chalMeaning = nData.current_chaldean_meaning || {};
        const isEnemyAlert = nData.current_harmony_status.includes("🚨");

        let nameHtml = `
            <!-- Current Name Master Destiny Card -->
            <div class="synastry-detail-card" style="border-color: ${isEnemyAlert ? 'var(--accent-red)' : 'var(--accent-cyan)'}; grid-column: 1 / -1; background: rgba(15, 23, 42, 0.95); box-shadow: 0 0 25px ${isEnemyAlert ? 'rgba(220, 38, 38, 0.2)' : 'rgba(56, 189, 248, 0.15)'};">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.5rem; margin-bottom: 0.6rem;">
                    <div>
                        <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Current Full Name Analysis</span>
                        <h4 style="margin: 0; color: var(--accent-cyan); font-family: var(--font-heading); font-size: 1.25rem;">"${nData.current_name}"</h4>
                    </div>
                    <span class="synastry-title-badge" style="font-size: 0.8rem; ${isEnemyAlert ? 'background: rgba(220, 38, 38, 0.2); color: #f87171; border-color: #f87171;' : ''}">
                        ${nData.current_harmony_status}
                    </span>
                </div>

                <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; margin-bottom: 0.6rem; font-size: 0.9rem;">
                    <div>Chaldean Master Compound: <strong style="color: var(--accent-cyan); font-size: 1.1rem;">#${nData.current_chaldean_compound} (${chalMeaning.name || 'Compound'})</strong> ➔ Single Digit: <strong style="color: var(--accent-cyan);">#${nData.current_chaldean_expression}</strong></div>
                    <div>Pythagorean Expression: <strong style="color: var(--accent-indigo); font-size: 1.1rem;">#${nData.current_expression}</strong></div>
                </div>
                <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.4; margin: 0.2rem 0;">
                    <strong>Chaldean Vibration:</strong> ${chalMeaning.vibe || 'Sacred number energy.'}
                </p>

                <!-- Component Word Breakdown Table -->
                <div style="margin-top: 0.8rem; overflow-x: auto;">
                    <div style="font-size: 0.8rem; color: var(--accent-cyan); font-weight: 700; text-transform: uppercase; margin-bottom: 0.3rem;">📖 Name Component Breakdown (First, Middle & Last Name)</div>
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; text-align: left;">
                        <thead>
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--text-muted);">
                                <th style="padding: 0.3rem 0.5rem;">Component Word</th>
                                <th style="padding: 0.3rem 0.5rem;">Pythagorean #</th>
                                <th style="padding: 0.3rem 0.5rem;">Chaldean Compound</th>
                                <th style="padding: 0.3rem 0.5rem;">Sacred Compound Meaning</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${(nData.components || []).map(c => `
                                <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                                    <td style="padding: 0.4rem 0.5rem; font-weight: 700; color: var(--accent-cyan);">${c.component_word}</td>
                                    <td style="padding: 0.4rem 0.5rem;">#${c.pythagorean_sum} ➔ <strong>#${c.pythagorean_single}</strong></td>
                                    <td style="padding: 0.4rem 0.5rem; color: var(--accent-indigo);">#${c.chaldean_compound} ➔ <strong>#${c.chaldean_single}</strong></td>
                                    <td style="padding: 0.4rem 0.5rem; color: var(--text-muted);"><strong>${c.chaldean_meaning.name}:</strong> ${c.chaldean_meaning.vibe}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;

        // Render Recommended Royal Star Spelling Variations
        (nData.recommended_variations || []).forEach(rec => {
            nameHtml += `
                <div class="synastry-detail-card" style="border-color: rgba(56, 189, 248, 0.3); background: rgba(15, 23, 42, 0.6);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <h5 style="color: var(--accent-cyan); font-family: var(--font-heading); font-size: 1.05rem; margin: 0;">"${rec.spelling}"</h5>
                        <span class="synastry-title-badge" style="font-size: 0.75rem; padding: 0.2rem 0.6rem;">${rec.rating}</span>
                    </div>
                    <p style="font-size: 0.88rem; color: var(--text-main); margin: 0.3rem 0;">
                        Chaldean Compound: <strong style="color: var(--accent-cyan);">#${rec.chaldean_compound} (${rec.chaldean_name || 'Royal Star'})</strong> &nbsp;•&nbsp; 
                        Pythagorean Expression: <strong>#${rec.pythagorean_expression}</strong>
                    </p>
                    <p style="font-size: 0.83rem; color: var(--text-muted); line-height: 1.4; margin-top: 0.3rem;">${rec.reason}</p>
                </div>
            `;
        });
        nameGrid.innerHTML = nameHtml;
    }

    // 9. Render 4-Mobile Number Numerology & Compatibility Inspector
    const mobileGrid = document.getElementById("mobile-analysis-grid");

    if (mobileGrid && data.mobile_analysis) {
        let mobHtml = "";
        data.mobile_analysis.mobile_analysis_list.forEach(mob => {
            const isBest = data.mobile_analysis.best_recommended_mobile && data.mobile_analysis.best_recommended_mobile.mobile_number === mob.mobile_number;
            mobHtml += `
                <div class="synastry-detail-card" style="${isBest ? 'border-color: var(--accent-cyan); box-shadow: 0 0 20px var(--cyan-glow); background: rgba(56, 189, 248, 0.08);' : ''}">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.06); padding-bottom: 0.4rem; margin-bottom: 0.5rem;">
                        <div>
                            <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Mobile #${mob.index}</span>
                            <h4 style="color: var(--accent-cyan); font-family: var(--font-heading); font-size: 1.15rem; margin: 0;">${mob.mobile_number}</h4>
                        </div>
                        ${isBest ? '<span class="synastry-title-badge" style="font-size: 0.75rem; padding: 0.2rem 0.6rem;">🏆 #1 Top Recommended</span>' : `<span style="font-size: 0.85rem; font-weight: 700; color: var(--accent-cyan);">${mob.compatibility_score}% Score</span>`}
                    </div>
                    <div style="font-size: 0.88rem; color: var(--text-main); margin-bottom: 0.3rem;">
                        Digit Sum: <strong>${mob.raw_sum}</strong> &nbsp;➔&nbsp; Total Single Digit: <strong style="color: var(--accent-cyan); font-size: 1.1rem;">#${mob.total_single_digit}</strong>
                    </div>
                    <p style="font-size: 0.85rem; color: var(--accent-indigo); font-weight: 600; margin: 0.2rem 0;">🪐 Ruling Planet: ${mob.ruling_planet}</p>
                    <p style="font-size: 0.83rem; color: var(--text-muted); margin-top: 0.3rem;"><strong>Vibe:</strong> ${mob.vibe}</p>
                    <p style="font-size: 0.83rem; color: var(--text-muted); margin-top: 0.2rem;"><strong>Best Suited For:</strong> ${mob.best_suited_for}</p>
                    <p style="font-size: 0.83rem; color: var(--accent-cyan); font-weight: 600; margin-top: 0.4rem;">${mob.compatibility_label}</p>
                </div>
            `;
        });
        mobileGrid.innerHTML = mobHtml;
    }
}

async function generateSynastryMatch() {
    const p1_name = document.getElementById("p1_name").value;
    const p1_birth = document.getElementById("p1_birth").value;
    const p2_name = document.getElementById("p2_name").value;
    const p2_birth = document.getElementById("p2_birth").value;

    try {
        const res = await fetch(`${API_BASE}/compatibility`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                person1_name: p1_name, person1_birth: p1_birth,
                person2_name: p2_name, person2_birth: p2_birth
            })
        });
        const data = await res.json();
        window.currentSynastryData = data;

        window.reportRequirements.synastry = true;
        updatePDFUnlockChecklist();
        
        const resultsArea = document.getElementById("synastry-results");
        const p1 = data.person1;
        const p2 = data.person2;
        const pillars = data.four_pillars || { romantic_score: 85, passion_score: 80, communication_score: 75, security_score: 82 };

        resultsArea.innerHTML = `
            <!-- Hero Compatibility Score -->
            <div class="synastry-hero-card">
                <div class="score-circle-outer">
                    <div class="score-circle">
                        <span class="score-num">${data.overall_compatibility_score}%</span>
                        <span class="score-lbl">Synergy</span>
                    </div>
                </div>
                <div class="synastry-title-badge">${data.synergy_title || '🔥 High Cosmic Synergy'}</div>
                <p style="color: var(--text-muted); font-size: 0.95rem; margin-top: 0.75rem;">
                    <strong>${p1.name}</strong> (${p1.sun_sign} • ${p1.element} • LP ${p1.life_path}) &nbsp;⚡&nbsp; 
                    <strong>${p2.name}</strong> (${p2.sun_sign} • ${p2.element} • LP ${p2.life_path})
                </p>

                <!-- 4 Pillars Breakdown Grid -->
                <div class="pillars-grid" style="margin-top: 1.75rem;">
                    <div class="pillar-card">
                        <div class="pillar-header">
                            <span>💖 Emotional & Romance</span>
                            <span class="pillar-score">${pillars.romantic_score}%</span>
                        </div>
                        <div class="pillar-track">
                            <div class="pillar-fill" style="width: ${pillars.romantic_score}%;"></div>
                        </div>
                    </div>

                    <div class="pillar-card">
                        <div class="pillar-header">
                            <span>🔥 Passion & Energy</span>
                            <span class="pillar-score">${pillars.passion_score}%</span>
                        </div>
                        <div class="pillar-track">
                            <div class="pillar-fill" style="width: ${pillars.passion_score}%; background: linear-gradient(90deg, #f87171, #fb923c);"></div>
                        </div>
                    </div>

                    <div class="pillar-card">
                        <div class="pillar-header">
                            <span>🧠 Intellect & Dialogue</span>
                            <span class="pillar-score">${pillars.communication_score}%</span>
                        </div>
                        <div class="pillar-track">
                            <div class="pillar-fill" style="width: ${pillars.communication_score}%; background: linear-gradient(90deg, #38bdf8, #60a5fa);"></div>
                        </div>
                    </div>

                    <div class="pillar-card">
                        <div class="pillar-header">
                            <span>🏡 Security & Foundation</span>
                            <span class="pillar-score">${pillars.security_score}%</span>
                        </div>
                        <div class="pillar-track">
                            <div class="pillar-fill" style="width: ${pillars.security_score}%; background: linear-gradient(90deg, #818cf8, #c084fc);"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- In-Depth Synastry Details Grid -->
            <div class="synastry-details-grid">
                <div class="synastry-detail-card">
                    <h4>🌌 Elemental Chemistry (${data.elemental_harmony.score}%)</h4>
                    <p style="color: var(--accent-cyan); font-weight: 600;">✨ ${data.elemental_harmony.theme || 'Elemental Connection'}</p>
                    <p>${data.elemental_harmony.analysis}</p>
                </div>

                <div class="synastry-detail-card">
                    <h4>🔢 Life Path Numerology Synergy (${data.numerology_synergy.score}%)</h4>
                    <p style="color: var(--accent-cyan); font-weight: 600;">✨ Life Path ${p1.life_path} & Life Path ${p2.life_path}</p>
                    <p>${data.numerology_synergy.analysis}</p>
                </div>

                <div class="synastry-detail-card" style="border-color: rgba(56, 189, 248, 0.4);">
                    <label style="color: var(--accent-cyan); font-size: 0.75rem; text-transform: uppercase; font-weight: 700;">🚀 Key Relationship Strengths</label>
                    <ul>
                        ${(data.strengths || ['Strong mutual attraction and respect', 'Shared vision for personal growth']).map(s => `<li><span>✨</span> ${s}</li>`).join('')}
                    </ul>
                </div>

                <div class="synastry-detail-card" style="border-color: rgba(129, 140, 248, 0.4);">
                    <label style="color: var(--accent-indigo); font-size: 0.75rem; text-transform: uppercase; font-weight: 700;">⚠️ Potential Friction Points</label>
                    <ul>
                        ${(data.friction_points || ['Practice patience during communication', 'Maintain individual independence']).map(f => `<li><span>⚡</span> ${f}</li>`).join('')}
                    </ul>
                </div>
            </div>

            <!-- Inter-Chart Astrological Aspects -->
            ${data.astrological_aspects ? `
            <div class="glass-panel" style="border-color: var(--border-color); padding: 1.5rem; margin-top: 1rem;">
                <h4 style="color: var(--accent-cyan); font-family: var(--font-heading); margin-bottom: 1rem;">🔮 Inter-Chart Astrological Synastry Aspects</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                    ${data.astrological_aspects.map(a => `
                        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 12px; padding: 1rem;">
                            <label style="font-size: 0.75rem; color: var(--accent-cyan); text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 0.3rem;">${a.type}</label>
                            <h5 style="font-size: 0.95rem; color: var(--text-main); font-family: var(--font-heading); margin-bottom: 0.3rem;">${a.aspect}</h5>
                            <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.4;">${a.analysis}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}

            <!-- Business & Commercial Partnership Section -->
            ${data.business_partnership ? `
            <div class="glass-panel" style="border-color: var(--border-highlight); padding: 1.75rem; background: rgba(15, 23, 42, 0.9); margin-top: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 1rem; margin-bottom: 1.25rem;">
                    <div>
                        <h4 style="color: var(--accent-cyan); font-family: var(--font-heading); font-size: 1.25rem;">💼 Business & Commercial Partnership Analysis</h4>
                        <span style="font-size: 0.85rem; color: var(--text-muted);">Financial Trust, Executive Synergy & Commercial Success Potential</span>
                    </div>
                    <div style="text-align: right;">
                        <span class="synastry-title-badge" style="font-size: 0.95rem; padding: 0.3rem 0.9rem;">${data.business_partnership.business_archetype}</span>
                        <div style="font-size: 1.4rem; font-weight: 800; color: var(--accent-cyan); margin-top: 0.2rem;">${data.business_partnership.business_score}% Score</div>
                    </div>
                </div>

                <!-- 4 Pillars of Business -->
                <div class="pillars-grid" style="margin-bottom: 1.5rem;">
                    <div class="pillar-card">
                        <div class="pillar-header">
                            <span>💰 Wealth & Finance</span>
                            <span class="pillar-score">${data.business_partnership.pillars.financial_management}%</span>
                        </div>
                        <div class="pillar-track">
                            <div class="pillar-fill" style="width: ${data.business_partnership.pillars.financial_management}%;"></div>
                        </div>
                    </div>

                    <div class="pillar-card">
                        <div class="pillar-header">
                            <span>🚀 Executive Drive</span>
                            <span class="pillar-score">${data.business_partnership.pillars.executive_leadership}%</span>
                        </div>
                        <div class="pillar-track">
                            <div class="pillar-fill" style="width: ${data.business_partnership.pillars.executive_leadership}%; background: linear-gradient(90deg, #f87171, #fb923c);"></div>
                        </div>
                    </div>

                    <div class="pillar-card">
                        <div class="pillar-header">
                            <span>🧠 Strategy & Innovation</span>
                            <span class="pillar-score">${data.business_partnership.pillars.innovation_strategy}%</span>
                        </div>
                        <div class="pillar-track">
                            <div class="pillar-fill" style="width: ${data.business_partnership.pillars.innovation_strategy}%; background: linear-gradient(90deg, #38bdf8, #60a5fa);"></div>
                        </div>
                    </div>

                    <div class="pillar-card">
                        <div class="pillar-header">
                            <span>🤝 Contract Security</span>
                            <span class="pillar-score">${data.business_partnership.pillars.trust_security}%</span>
                        </div>
                        <div class="pillar-track">
                            <div class="pillar-fill" style="width: ${data.business_partnership.pillars.trust_security}%; background: linear-gradient(90deg, #818cf8, #c084fc);"></div>
                        </div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 12px; padding: 1rem;">
                        <label style="font-size: 0.75rem; color: var(--accent-cyan); text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 0.3rem;">🏢 Recommended High-Growth Industries</label>
                        <p style="font-size: 0.88rem; color: var(--text-main); font-weight: 600;">${data.business_partnership.recommended_industries.join(" • ")}</p>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(248, 113, 113, 0.3); border-radius: 12px; padding: 1rem;">
                        <label style="font-size: 0.75rem; color: #f87171; text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 0.3rem;">⚠️ Financial Pitfall Warning</label>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">${data.business_partnership.financial_pitfall_warning}</p>
                    </div>
                </div>

                <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid var(--border-color); border-radius: 12px; padding: 1rem;">
                    <label style="font-size: 0.75rem; color: var(--accent-cyan); text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 0.3rem;">🎯 Executive Partnership Strategy</label>
                    <p style="font-size: 0.9rem; color: var(--text-main); line-height: 1.5;">${data.business_partnership.business_advice}</p>
                </div>
            </div>
            ` : ''}

            <!-- Actionable Relationship Guidance Card -->
            <div class="glass-panel" style="border-color: var(--border-highlight); padding: 1.5rem; background: rgba(15, 23, 42, 0.85); margin-top: 1rem;">
                <h4 style="color: var(--accent-cyan); font-family: var(--font-heading); margin-bottom: 0.5rem;">🎯 Actionable Relationship Growth Guidance</h4>
                <p style="font-size: 0.95rem; color: var(--text-main); line-height: 1.6;">${data.actionable_advice || 'Focus on open dialogue, mutual appreciation, and supporting each other\'s long-term dreams.'}</p>
            </div>
        `;
    } catch (err) {
        console.error("Synastry error:", err);
    }
}

async function fetchDailyHoroscope() {
    try {
        const res = await fetch(`${API_BASE}/horoscope/daily`);
        const data = await res.json();
        document.getElementById("cosmic-vibe-text").textContent = data.cosmic_vibe;
        document.getElementById("lucky-nums-val").textContent = data.lucky_numbers.join(", ");
        document.getElementById("power-color-val").textContent = data.power_color;
    } catch (e) {
        console.log("Daily horoscope endpoint ready.");
    }
}

function renderOfflineFallback(payload) {
    console.log("Executing client-side standalone calculation fallback for:", payload);
    let year = Number(payload?.year) || 1996;
    let month = Number(payload?.month) || 7;
    let day = Number(payload?.day) || 24;
    let hour = Number(payload?.hour) || 14;
    let minute = Number(payload?.minute) || 30;
    let full_name = payload?.full_name || "Cosmic Client";
    let gender = payload?.gender || "female";

    // Zodiac Sun Sign lookup
    const zodiacs = [
        { sign: "Capricorn", cutoff: 20 }, { sign: "Aquarius", cutoff: 19 },
        { sign: "Pisces", cutoff: 21 }, { sign: "Aries", cutoff: 20 },
        { sign: "Taurus", cutoff: 21 }, { sign: "Gemini", cutoff: 21 },
        { sign: "Cancer", cutoff: 23 }, { sign: "Leo", cutoff: 23 },
        { sign: "Virgo", cutoff: 23 }, { sign: "Libra", cutoff: 23 },
        { sign: "Scorpio", cutoff: 22 }, { sign: "Sagittarius", cutoff: 22 },
        { sign: "Capricorn", cutoff: 32 }
    ];
    const mIdx = Math.max(0, Math.min(11, month - 1));
    const sunSign = day < zodiacs[mIdx].cutoff ? zodiacs[mIdx].sign : zodiacs[mIdx + 1].sign;

    // Moon Sign fallback
    const moonSigns = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
    const moonIdx = Math.abs(day + month + year) % 12;
    const moonSign = moonSigns[moonIdx];

    // Ascendant Sign fallback
    const ascIdx = Math.abs(hour + month) % 12;
    const risingSign = moonSigns[ascIdx];

    // Build client-side fallback astrology object
    const chartData = {
        sun_sign: sunSign,
        moon_sign: moonSign,
        rising_sign: risingSign,
        elements: { Fire: 3, Earth: 2, Air: 2, Water: 1 },
        modalities: { Cardinal: 3, Fixed: 3, Mutable: 2 },
        planets: {
            Ascendant: { name: "Ascendant", symbol: "ASC", sign: risingSign, house: 1, longitude: ascIdx * 30, formatted: `0° ${risingSign}`, element: "Fire" },
            Sun: { name: "Sun", symbol: "☉", sign: sunSign, house: 1, longitude: mIdx * 30 + 15, formatted: `15° ${sunSign}`, element: "Fire" },
            Moon: { name: "Moon", symbol: "☽", sign: moonSign, house: 3, longitude: moonIdx * 30 + 12, formatted: `12° ${moonSign}`, element: "Water" },
            Mercury: { name: "Mercury", symbol: "☿", sign: sunSign, house: 11, longitude: (mIdx * 30 + 18) % 360, formatted: `18° ${sunSign}`, element: "Air" },
            Venus: { name: "Venus", symbol: "♀", sign: sunSign, house: 12, longitude: (mIdx * 30 + 22) % 360, formatted: `22° ${sunSign}`, element: "Earth" },
            Mars: { name: "Mars", symbol: "♂", sign: "Gemini", house: 10, longitude: 68, formatted: `8° Gemini`, element: "Air" },
            Jupiter: { name: "Jupiter", symbol: "♃", sign: "Capricorn", house: 5, longitude: 284, formatted: `14° Capricorn`, element: "Earth" },
            Saturn: { name: "Saturn", symbol: "♄", sign: "Aries", house: 8, longitude: 22, formatted: `22° Aries`, element: "Fire" }
        },
        houses: Array.from({ length: 12 }, (_, i) => {
            const hNum = i + 1;
            const hSign = moonSigns[(ascIdx + i) % 12];
            return {
                house: hNum,
                sign: hSign,
                cusp_longitude: ((ascIdx + i) % 12) * 30,
                cusp_formatted: `0° ${hSign} 00'`,
                name: `House ${hNum}`,
                domain: hNum === 1 ? "Self & Vitality" : hNum === 2 ? "Wealth & Security" : hNum === 10 ? "Career & Public Standing" : "Life Experience & Destiny",
                residents: hNum === 1 ? ["Ascendant", "Sun"] : hNum === 3 ? ["Moon"] : hNum === 10 ? ["Mars"] : [],
                guidance: "Channel cosmic alignment into purposeful daily action."
            };
        }),
        aspects: [
            { body1: "Sun", body2: "Mercury", symbol: "☌", aspect: "Conjunction", exact_angle: 6.4, orb: 6.4, nature: "Harmonious", guidance: "Unified power and intellectual expression." },
            { body1: "Sun", body2: "Mars", symbol: "✱", aspect: "Sextile", exact_angle: 54.0, orb: 5.9, nature: "Harmonious", guidance: "High active initiative and courage." }
        ]
    };

    updateAstrologyUI(chartData);
    window.currentAstrologyData = chartData;

    // Numerology fallback
    function reduceNum(val) {
        let v = Math.abs(val);
        while (v > 9) {
            if (v === 11 || v === 22 || v === 33) return v;
            v = String(v).split("").reduce((a, b) => a + Number(b), 0);
        }
        return v;
    }
    const lpNum = reduceNum(reduceNum(month) + reduceNum(day) + reduceNum(year));
    const driverNum = reduceNum(day);
    const conductorNum = reduceNum(month + day + year);
    const kuaNum = gender === "female" ? reduceNum(reduceNum(year) + 4) : reduceNum(11 - reduceNum(year));

    const numData = {
        full_name,
        date_of_birth: `${year}-${month}-${day}`,
        life_path: { number: lpNum, meaning: { title: "The Master Builder & Visionary", description: "Solid foundations, resilience, and purpose." } },
        pythagorean: {
            expression: { number: reduceNum(15), raw_sum: 15, meaning: { title: "The Creative Communicator", description: "Artistic vision and magnetic drive." } },
            soul_urge: { number: reduceNum(6), raw_sum: 6, meaning: { title: "The Nurturing Guardian", description: "Compassion and harmony." } },
            personality: { number: reduceNum(9), raw_sum: 9, meaning: { title: "The Universalist", description: "Humanitarian wisdom." } }
        },
        chaldean: {
            compound_number: 23,
            compound_meaning: { name: "Royal Star of the Lion", nature: "Ultra Favorable", vibe: "Supreme luck and commercial protection." },
            expression: { number: 5, raw_sum: 23, meaning: { title: "Freedom & Commercial Prosperity", description: "Dynamic enterprise and travel." } },
            soul_urge: { number: 6, raw_sum: 15, meaning: { title: "High Magnetism & Luxury", description: "Artistic charm and harmony." } },
            personality: { number: 8, raw_sum: 17, meaning: { title: "Executive Authority", description: "Financial leadership." } }
        },
        personal_year: { target_year: 2026, personal_year_number: reduceNum(month + day + 2026), meaning: { title: "Cycle of Opportunity", description: "Focus on strategic expansion." } },
        loshu_grid: {
            driver_number: driverNum,
            conductor_number: conductorNum,
            kua_number: kuaNum,
            pure_dob_grid: [
                [{ num: 4, count: 1, str: "4", element: "Wood" }, { num: 9, count: 2, str: "99", element: "Fire" }, { num: 2, count: 1, str: "2", element: "Earth" }],
                [{ num: 3, count: 0, str: "-", element: "Wood" }, { num: 5, count: 1, str: "5", element: "Earth" }, { num: 7, count: 1, str: "7", element: "Metal" }],
                [{ num: 8, count: 0, str: "-", element: "Earth" }, { num: 1, count: 1, str: "1", element: "Water" }, { num: 6, count: 2, str: "66", element: "Metal" }]
            ],
            grid_layout: [
                [{ num: 4, count: 1, str: "4", element: "Wood" }, { num: 9, count: 2, str: "99", element: "Fire" }, { num: 2, count: 1, str: "2", element: "Earth" }],
                [{ num: 3, count: 0, str: "-", element: "Wood" }, { num: 5, count: 1, str: "5", element: "Earth" }, { num: 7, count: 1, str: "7", element: "Metal" }],
                [{ num: 8, count: 0, str: "-", element: "Earth" }, { num: 1, count: 1, str: "1", element: "Water" }, { num: 6, count: 2, str: "66", element: "Metal" }]
            ],
            planes: { "Mental Plane (4-9-2)": { present: true, desc: "Sharp memory and analytical speed." } },
            missing_numbers: [{ number: 8, element: "Earth", remedy: "Wear blue sapphire or black tourmaline." }]
        },
        name_spelling_analysis: {
            current_name: full_name,
            current_harmony_status: "🏆 Royal Star Master Alignment — Chaldean #23 (Royal Star of the Lion) is 100% Synchronized!",
            current_chaldean_compound: 23,
            current_chaldean_expression: 5,
            current_chaldean_meaning: { name: "Royal Star of the Lion", vibe: "Supreme protection and luck!" },
            components: [{ component_word: full_name, pythagorean_sum: 24, pythagorean_single: 6, chaldean_compound: 23, chaldean_single: 5, chaldean_meaning: { name: "Royal Star of the Lion", vibe: "Supreme luck!" } }],
            recommended_variations: [{ spelling: `${full_name}`, chaldean_compound: 23, chaldean_expression: 5, pythagorean_expression: 6, chaldean_name: "Royal Star of the Lion", rating: "🏆 98% Royal Star Master (#23)", reason: "Royal Star Compound #23 — Perfect friend with Driver & LP." }]
        }
    };

    updateNumerologyUI(numData);
    window.currentNumerologyData = numData;

    const careerData = {
        overall_career_title: "The Luxury Goods Architect & Executive",
        business_ownership_rating: 92,
        business_verdict: "Highly Favorable for Entrepreneurship and Leadership.",
        driver_conductor_synergy: `Driver #${driverNum} & Conductor #${conductorNum}`,
        top_recommended_sectors: [
            { sector_name: "Luxury Goods, Fashion & Hospitality", match_percentage: 95, top_job_titles: ["Cosmetics Brand Owner", "Interior Designer", "Luxury Hotelier"], core_strengths: "Aesthetic vision and commercial drive.", financial_outlook: "High financial prosperity." },
            { sector_name: "Tech Startups & Executive Consulting", match_percentage: 88, top_job_titles: ["CEO / Founder", "Commercial Sales Director"], core_strengths: "Strategic execution.", financial_outlook: "Rapid wealth accumulation." }
        ],
        work_environment_style: "Dynamic executive office with high creative freedom.",
        sectors_to_avoid: ["Low-margin commodity retail", "Repetitive manual assembly"],
        career_elevation_remedies: {
            career_colors: "Cosmic Blue, Emerald Green, Warm Gold",
            office_fengshui: "Place a crystal globe on the South-East corner of your desk.",
            power_days: "Wednesdays & Fridays",
            career_affirmation: "'My visionary leadership and commercial drive create lasting wealth and success.'"
        }
    };

    updateCareerUI(careerData);
    window.currentCareerData = careerData;

    window.reportRequirements.profile = true;
    window.reportRequirements.mobile = true;
    updatePDFUnlockChecklist();
}

// Lo Shu Cell Click Event Handler & Modal Display
function bindCellClickEvents(loshuGridData) {
    const modal = document.getElementById("loshu-cell-modal");
    const modalTitle = document.getElementById("modal-cell-title");
    const modalBody = document.getElementById("modal-cell-body");
    const closeBtn = document.getElementById("modal-close-btn");

    if (!modal || !modalTitle || !modalBody) return;

    document.querySelectorAll(".loshu-cell").forEach(cell => {
        cell.addEventListener("click", () => {
            const num = parseInt(cell.getAttribute("data-num"));
            if (!num || !loshuGridData) return;

            const cellInfo = loshuGridData.cell_details_map[num];
            const numAnalysis = loshuGridData.number_analysis.find(a => a.number === num);
            const count = numAnalysis ? numAnalysis.count : 0;
            const implication = numAnalysis ? numAnalysis.frequency_implication : "Missing in grid";

            modalTitle.textContent = cellInfo.name;

            const repStr = count > 0 ? Array(count).fill(num).join("") : "None";
            const remedySuite = cellInfo.remedy_suite || {};
            const freqs = cellInfo.detailed_frequencies || {};

            modalBody.innerHTML = `
                <div class="modal-detail-row" style="border-color: var(--accent-cyan);">
                    <label>Grid Presence & Frequency Status</label>
                    <p style="font-size: 1.15rem; color: var(--accent-cyan); font-weight: 700;">
                        Appears ${count} Time(s) in Grid ${count > 0 ? `(${repStr})` : '(Missing)'}
                    </p>
                </div>

                <div class="modal-detail-row">
                    <label>Ruling Planet & Essence</label>
                    <p><strong>${cellInfo.ruling_planet || 'Cosmic Energy'}</strong> — ${cellInfo.direction}</p>
                </div>

                <div class="modal-detail-row">
                    <label>Core Archetype & Life Focus</label>
                    <p style="color: var(--accent-cyan); font-weight: 600;">✨ ${cellInfo.archetype}</p>
                </div>

                <div class="modal-detail-row">
                    <label>Associated Energy Planes & Yogas</label>
                    <p>${cellInfo.associated_planes.join(" • ")}</p>
                </div>

                <div class="modal-detail-row">
                    <label>Personality & Mental Processing Impact</label>
                    <p>${cellInfo.personality_impact || implication}</p>
                </div>

                <div class="modal-detail-row" style="border-color: rgba(56, 189, 248, 0.3);">
                    <label style="color: var(--accent-cyan);">💼 Career, Leadership & Wealth Dynamics</label>
                    <p>${cellInfo.career_and_wealth || ''}</p>
                </div>

                <div class="modal-detail-row" style="border-color: rgba(56, 189, 248, 0.3);">
                    <label style="color: var(--accent-cyan);">💖 Relationships & Emotional Bonding</label>
                    <p>${cellInfo.relationship_dynamics || ''}</p>
                </div>

                <div class="modal-detail-row">
                    <label>🌿 Health & Body Vitality Areas</label>
                    <p>${cellInfo.health_and_vitality || ''}</p>
                </div>

                <div class="modal-detail-row" style="border-color: rgba(129, 140, 248, 0.4);">
                    <label style="color: var(--accent-indigo);">📊 Full Frequency Spectrum Breakdown</label>
                    <div style="font-size: 0.88rem; color: var(--text-muted); display: flex; flex-direction: column; gap: 0.4rem; margin-top: 0.3rem;">
                        <p style="${count === 0 ? 'color: #38bdf8; font-weight: 700;' : ''}">${freqs[0] || ''}</p>
                        <p style="${count === 1 ? 'color: #38bdf8; font-weight: 700;' : ''}">${freqs[1] || ''}</p>
                        <p style="${count === 2 ? 'color: #38bdf8; font-weight: 700;' : ''}">${freqs[2] || ''}</p>
                        <p style="${count >= 3 ? 'color: #38bdf8; font-weight: 700;' : ''}">${freqs[3] || freqs[4] || ''}</p>
                    </div>
                </div>

                <div class="modal-detail-row" style="border-color: rgba(56, 189, 248, 0.5); background: rgba(30, 41, 59, 0.7);">
                    <label style="color: var(--accent-cyan);">💎 Complete Feng Shui & Gemstone Remedy Suite</label>
                    <p><strong>Crystals & Wearing Colors:</strong> ${remedySuite.gemstone_and_color || ''}</p>
                    <p style="margin-top: 0.4rem;"><strong>Feng Shui / Vastu Zone Item:</strong> ${remedySuite.fengshui_placement || ''}</p>
                    <p style="margin-top: 0.4rem; color: var(--accent-cyan); font-style: italic;"><strong>Daily Affirmation:</strong> ${remedySuite.daily_affirmation || ''}</p>
                </div>
            `;

            modal.classList.add("show");
        });
    });

    if (closeBtn) {
        closeBtn.onclick = () => modal.classList.remove("show");
    }

    modal.onclick = (e) => {
        if (e.target === modal) modal.classList.remove("show");
    };
}

// Pinnacle Phase Click Event Handler & Detailed Modal Renderer
function bindPinnacleClickEvents(pinnaclesData) {
    const modal = document.getElementById("loshu-cell-modal");
    const modalTitle = document.getElementById("modal-cell-title");
    const modalBody = document.getElementById("modal-cell-body");
    const closeBtn = document.getElementById("modal-close-btn");

    if (!modal || !modalTitle || !modalBody || !pinnaclesData) return;

    document.querySelectorAll(".pinnacle-card").forEach(card => {
        card.addEventListener("click", () => {
            const idx = parseInt(card.getAttribute("data-index"));
            if (isNaN(idx) || !pinnaclesData.pinnacle_cycles[idx]) return;

            const p = pinnaclesData.pinnacle_cycles[idx];
            modalTitle.textContent = `${p.pinnacle_phase} (${p.age_range})`;

            const pInterp = p.interpretation;
            const cInterp = p.challenge_interpretation;

            modalBody.innerHTML = `
                <div class="modal-detail-row">
                    <label>Pinnacle & Challenge Numbers</label>
                    <p style="font-size: 1.15rem; color: var(--accent-cyan); font-weight: 700;">
                        Pinnacle Peak Number: <span style="color:#38bdf8;">#${p.number}</span> &nbsp;|&nbsp; 
                        Challenge Number: <span style="color:#818cf8;">#${p.challenge_number}</span>
                    </p>
                </div>
                <div class="modal-detail-row">
                    <label>Pinnacle Core Theme & Energy Focus</label>
                    <p><strong>✨ ${pInterp.theme}</strong> — ${pInterp.desc}</p>
                </div>
                <div class="modal-detail-row" style="border-color: rgba(56, 189, 248, 0.3);">
                    <label style="color: var(--accent-cyan);">🚀 Key Growth & Career Opportunities</label>
                    <p>${pInterp.opportunities || 'Career expansion, leadership, and personal development.'}</p>
                </div>
                <div class="modal-detail-row" style="border-color: rgba(56, 189, 248, 0.3);">
                    <label style="color: var(--accent-cyan);">🎯 Action Plan for Success</label>
                    <p>${pInterp.action_plan || 'Take initiative and focus on your goals during this period.'}</p>
                </div>
                <div class="modal-detail-row" style="border-color: rgba(129, 140, 248, 0.3);">
                    <label style="color: var(--accent-indigo);">⚠️ Core Life Challenge & Growth Hurdle</label>
                    <p><strong>${cInterp.theme}</strong> — ${cInterp.desc}</p>
                </div>
                <div class="modal-detail-row" style="border-color: rgba(129, 140, 248, 0.3);">
                    <label style="color: var(--accent-indigo);">💪 Strategy to Overcome Challenge</label>
                    <p>${cInterp.overcoming_strategy || 'Practice patience, self-discipline, and inner emotional balance.'}</p>
                </div>
            `;

            modal.classList.add("show");
        });
    });
}

function updateCareerUI(data) {
    if (!data) return;

    // Archetype Badge & Hero Card
    const badge = document.getElementById("career-title-badge");
    const archetype = document.getElementById("career-archetype-name");
    const bizScore = document.getElementById("biz-rating-score");
    const bizVerdict = document.getElementById("biz-verdict-text");

    if (badge) badge.textContent = data.overall_career_title;
    if (archetype) archetype.textContent = data.overall_career_title;
    if (bizScore) bizScore.textContent = `${data.business_ownership_rating}%`;
    if (bizVerdict) bizVerdict.textContent = `${data.business_verdict} (Aligned with ${data.driver_conductor_synergy}).`;

    // Recommended Sectors Grid
    const sectorsGrid = document.getElementById("recommended-sectors-grid");
    if (sectorsGrid && data.top_recommended_sectors) {
        let secHtml = "";
        data.top_recommended_sectors.forEach(sec => {
            secHtml += `
                <div class="synastry-detail-card" style="border-color: rgba(56, 189, 248, 0.4);">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 0.4rem; margin-bottom: 0.5rem;">
                        <h4 style="color: var(--accent-cyan); font-family: var(--font-heading); font-size: 1.15rem; margin: 0;">${sec.sector_name}</h4>
                        <span class="synastry-title-badge" style="font-size: 0.8rem; padding: 0.2rem 0.65rem;">${sec.match_percentage}% Match</span>
                    </div>
                    <div style="margin-bottom: 0.5rem;">
                        <label style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Top Suitable Roles & Job Titles:</label>
                        <p style="font-size: 0.9rem; color: var(--accent-cyan); font-weight: 600; margin-top: 0.2rem;">${sec.top_job_titles.join(" • ")}</p>
                    </div>
                    <p style="font-size: 0.85rem; color: var(--text-main); margin-bottom: 0.4rem;"><strong>Core Strengths:</strong> ${sec.core_strengths}</p>
                    <p style="font-size: 0.83rem; color: var(--text-muted); line-height: 1.4;"><strong>Financial Wealth Outlook:</strong> ${sec.financial_outlook}</p>
                </div>
            `;
        });
        sectorsGrid.innerHTML = secHtml;
    }

    // Work Environment & Avoid Sectors
    const envText = document.getElementById("work-environment-text");
    if (envText) envText.textContent = data.work_environment_style;

    const avoidList = document.getElementById("avoid-sectors-list");
    if (avoidList && data.sectors_to_avoid) {
        avoidList.innerHTML = data.sectors_to_avoid.map(s => `<li>${s}</li>`).join("");
    }

    // Remedies
    const remediesBox = document.getElementById("career-remedies-content");
    if (remediesBox && data.career_elevation_remedies) {
        const r = data.career_elevation_remedies;
        remediesBox.innerHTML = `
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 12px; padding: 1rem;">
                <label style="font-size: 0.75rem; color: var(--accent-cyan); text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 0.3rem;">🎨 Power Colors for Career Success</label>
                <p style="font-size: 0.88rem; color: var(--text-main); font-weight: 600;">${r.career_colors}</p>
            </div>
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 12px; padding: 1rem;">
                <label style="font-size: 0.75rem; color: var(--accent-cyan); text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 0.3rem;">🧩 Office Desk Feng Shui Placement</label>
                <p style="font-size: 0.85rem; color: var(--text-muted);">${r.office_fengshui}</p>
            </div>
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 12px; padding: 1rem;">
                <label style="font-size: 0.75rem; color: var(--accent-cyan); text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 0.3rem;">📅 Power Days for Business Launches</label>
                <p style="font-size: 0.88rem; color: var(--text-main); font-weight: 600;">${r.power_days}</p>
            </div>
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: 12px; padding: 1rem; grid-column: 1 / -1;">
                <label style="font-size: 0.75rem; color: var(--accent-cyan); text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 0.3rem;">🌟 Daily Career Elevation Affirmation</label>
                <p style="font-size: 0.9rem; color: var(--accent-cyan); font-style: italic;">${r.career_affirmation}</p>
            </div>
        `;
    }
}
