# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import List, Optional

import pytz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from geopy.geocoders import Nominatim
from pydantic import BaseModel, Field

from airports_db import get_airport_by_iata, nearest_airports
from checklist import build_checklist
from climate import summarize_climate
from flight import apply_peak_adjustment, calc_preflight_buffers
from routing import geocode_address, route_drive_minutes

app = FastAPI(title="Consultor de Viagens API")

# CORS para o Next.js em dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripRequest(BaseModel):
    endereco_origem: str
    origem_pais: str = "Brasil"
    destino_cidade: str
    destino_pais: str
    aeroporto_iata: Optional[str] = None
    tz_origem: str = "America/Sao_Paulo"
    datahora_partida_local: str  # "YYYY-MM-DDTHH:mm" (datetime-local)
    internacional: bool = True
    bagagem_despachada: bool = False
    assento_marcado: bool = True
    dias: int = Field(ge=1, le=60, default=6)
    atividades: List[str] = []


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/plan")
def plan(req: TripRequest) -> dict:
    # Parse da data/hora local + timezone
    tz = pytz.timezone(req.tz_origem)
    # Aceita "YYYY-MM-DDTHH:mm" ou ISO
    dt = datetime.fromisoformat(req.datahora_partida_local.replace("Z", ""))
    if dt.tzinfo is None:
        dt = tz.localize(dt)
    partida_local = dt

    # Buffers sem deslocamento
    prevoo_min, det = calc_preflight_buffers(
        req.internacional, req.bagagem_despachada, req.assento_marcado
    )
    leave_est = partida_local - timedelta(minutes=prevoo_min)
    prevoo_min += apply_peak_adjustment(leave_est, req.internacional, det)

    # Geocode origem + aeroporto destino
    o_lat, o_lon = geocode_address(req.endereco_origem)
    geo = Nominatim(user_agent="consultor_viagens_api")
    ap = get_airport_by_iata(req.aeroporto_iata) if req.aeroporto_iata else None
    if not ap:
        loc = geo.geocode(f"{req.destino_cidade}, {req.destino_pais}", language="pt")
        cand = nearest_airports(loc.latitude, loc.longitude, 1)[0]
        iata, icao, name, city, country, d_lat, d_lon = cand
    else:
        iata, icao, name, city, country, d_lat, d_lon = ap

    # Rota (OSRM gratuito)
    drive_min = route_drive_minutes(o_lat, o_lon, d_lat, d_lon, provider="osrm")

    # Hora de sair de casa
    leave_final = partida_local - timedelta(minutes=(prevoo_min + drive_min))

    # Clima + Checklist
    loc = geo.geocode(f"{req.destino_cidade}, {req.destino_pais}", language="pt")
    climate = summarize_climate(
        loc.latitude,
        loc.longitude,
        partida_local.date(),
        partida_local.date() + timedelta(days=req.dias - 1),
    )
    checklist_md = build_checklist(
        req.destino_cidade, req.destino_pais, climate, req.dias, req.atividades
    )

    return {
        "airport": {"iata": iata, "name": name, "city": city, "country": country},
        "departure_advice": {
            "leave_at_local": leave_final.isoformat(),
            "breakdown_min": {"prevoo": prevoo_min, **det, "drive": drive_min},
        },
        "climate_summary": climate,
        "checklist_md": checklist_md,
    }
