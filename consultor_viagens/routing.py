# -*- coding: utf-8 -*-
from typing import Tuple, Literal
import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSRM_URL = "https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"

class RoutingError(RuntimeError): pass

def geocode_address(addr: str) -> Tuple[float,float]:
    r = requests.get(NOMINATIM_URL, params={
        "q": addr, "format": "json", "limit": 1, "addressdetails": 0
    }, headers={"User-Agent":"consultor_viagens"}, timeout=25)
    r.raise_for_status()
    data = r.json()
    if not data: raise RoutingError("Endereço não encontrado")
    return float(data[0]["lat"]), float(data[0]["lon"])

def route_drive_minutes(o_lat: float, o_lon: float, d_lat: float, d_lon: float,
                        provider: Literal["osrm"]="osrm") -> int:
    url = OSRM_URL.format(lon1=o_lon, lat1=o_lat, lon2=d_lon, lat2=d_lat)
    rr = requests.get(url, timeout=25)
    rr.raise_for_status()
    js = rr.json()
    if not js.get("routes"): raise RoutingError("Rota não encontrada (OSRM).")
    sec = js["routes"][0]["duration"]
    return int(round(sec/60))
