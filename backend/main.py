"""
FastAPI Microservice Main Entrypoint
Serves Astrology Ephemeris, Numerology Engines, Synastry Matcher, and Web Frontend.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
import os

from astrology_engine import calculate_natal_chart
from numerology_engine import generate_full_numerology_profile
from synastry_engine import calculate_compatibility
from career_engine import calculate_profession_predictions
from pdf_engine import generate_pdf_report

app = FastAPI(
    title="Numerology & Astrology Cosmic Engine API",
    description="High-precision ephemeris natal chart calculations & Pythagorean/Chaldean numerology API",
    version="1.0.0"
)

# Enable CORS for Next.js / External web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Models
class BirthProfileRequest(BaseModel):
    full_name: str
    year: int
    month: int
    day: int
    gender: str = "male"
    hour: float = 12.0
    minute: float = 0.0
    latitude: float = 40.7128   # Default: NYC
    longitude: float = -74.0060
    mobile_numbers: list[str] = ["9876543210", "9123456789"]
    synastry: dict | None = None


class SynastryRequest(BaseModel):
    person1_name: str
    person1_birth: str  # YYYY-MM-DD
    person2_name: str
    person2_birth: str  # YYYY-MM-DD


# API Endpoints
@app.post("/api/astrology/natal-chart")
def get_natal_chart(req: BirthProfileRequest):
    try:
        chart_data = calculate_natal_chart(
            req.year, req.month, req.day,
            req.hour, req.minute,
            req.latitude, req.longitude
        )
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/numerology/calculate")
def get_numerology_profile(req: BirthProfileRequest):
    try:
        profile = generate_full_numerology_profile(
            req.full_name, req.year, req.month, req.day, req.gender,
            mobile_numbers=req.mobile_numbers
        )
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compatibility")
def get_compatibility(req: SynastryRequest):
    try:
        result = calculate_compatibility(
            req.person1_name, req.person1_birth,
            req.person2_name, req.person2_birth
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/career/predictions")
def get_career_predictions(req: BirthProfileRequest):
    try:
        chart_data = calculate_natal_chart(
            req.year, req.month, req.day,
            req.hour, req.minute,
            req.latitude, req.longitude
        )
        num_data = generate_full_numerology_profile(
            req.full_name, req.year, req.month, req.day, req.gender,
            mobile_numbers=req.mobile_numbers
        )
        predictions = calculate_profession_predictions(chart_data, num_data)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/report/pdf")
def generate_pdf_blueprint(req: BirthProfileRequest):
    try:
        chart_data = calculate_natal_chart(
            req.year, req.month, req.day,
            req.hour, req.minute,
            req.latitude, req.longitude
        )
        num_data = generate_full_numerology_profile(
            req.full_name, req.year, req.month, req.day, req.gender,
            mobile_numbers=req.mobile_numbers
        )
        career_data = calculate_profession_predictions(chart_data, num_data)

        horoscope_data = {
            "cosmic_vibe": "Harmonious Trine between Sun and Jupiter brings clarity, strategic wisdom, and executive momentum today.",
            "lucky_numbers": [3, 7, 11, 21],
            "power_color": "Cosmic Gold (#ffd700)"
        }

        combined_payload = {
            "full_name": req.full_name,
            "birth_date": f"{int(req.year):04d}-{int(req.month):02d}-{int(req.day):02d}",
            "birth_time": f"{int(req.hour):02d}:{int(req.minute):02d} UTC",
            "gender": req.gender,
            "location": "Specified Coordinates",
            "astrology": chart_data,
            "numerology": num_data,
            "career": career_data,
            "horoscope": horoscope_data,
            "synastry": req.synastry
        }

        pdf_bytes = generate_pdf_report(combined_payload)
        filename = f"Cosmic_Blueprint_{req.full_name.replace(' ', '_')}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/horoscope/daily")
def get_daily_horoscope():
    return {
        "cosmic_vibe": "Harmonious Trine between Sun and Jupiter brings clarity and creative breakthroughs today.",
        "lucky_numbers": [3, 7, 11, 21],
        "power_color": "Cosmic Gold (#ffd700)"
    }


# Serve Frontend Web App
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_frontend():
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "Numerology & Astrology API is active. Open /docs for API documentation."}

    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend_root")

    @app.get("/favicon.ico", include_in_schema=False)
    def favicon_ico():
        fav_path = os.path.join(FRONTEND_DIR, "favicon.ico")
        if os.path.exists(fav_path):
            return FileResponse(fav_path, media_type="image/x-icon")
        return Response(status_code=404)

    @app.get("/favicon.png", include_in_schema=False)
    def favicon_png():
        fav_path = os.path.join(FRONTEND_DIR, "favicon.png")
        if os.path.exists(fav_path):
            return FileResponse(fav_path, media_type="image/png")
        return Response(status_code=404)

    @app.get("/favicon.svg", include_in_schema=False)
    def favicon_svg():
        fav_path = os.path.join(FRONTEND_DIR, "favicon.svg")
        if os.path.exists(fav_path):
            return FileResponse(fav_path, media_type="image/svg+xml")
        return Response(status_code=404)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
