
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import TripInfo, PlanResponse
from .core.time_to_leave import calc_saida_de_casa
from .core.climate import get_climate_summary
from .core.checklist import build_checklist
from datetime import date

app = FastAPI(title="Consultor de Viagens – API", version="0.1.0")

# CORS (ajuste a origem no Render se quiser restringir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/trip/plan", response_model=PlanResponse)
def plan_trip(trip: TripInfo):
    climate = get_climate_summary(trip.destino_cidade, trip.destino_pais, trip.data_ida, trip.data_volta)
    days = (trip.data_volta - trip.data_ida).days + 1
    leave_at, details = calc_saida_de_casa(
        trip.voo_partida_local, trip.internacional,
        trip.bagagem_despachada, trip.assento_marcado,
        trip.tempo_deslocamento_min
    )
    checklist_md = build_checklist(trip, climate, days)

    return {
        "leave_at": leave_at,
        "buffers": details,
        "climate": climate,
        "checklist_markdown": checklist_md
    }


from fastapi import Query
from typing import Optional
from .io.airports_db import get_airport_by_iata, nearest_airports, search_airports

@app.get("/airports/by_iata")
def airport_by_iata(code: str = Query(..., description="Código IATA (ex.: GRU)")):
    res = get_airport_by_iata(code)
    return res or {}

@app.get("/airports/search")
def airports_search(
    q: str = Query(..., description="Termo para buscar por IATA, nome, cidade ou país"),
    limit: int = Query(10, ge=1, le=50),
    lat: Optional[float] = None,
    lon: Optional[float] = None
):
    return search_airports(q, limit=limit, lat=lat, lon=lon)
