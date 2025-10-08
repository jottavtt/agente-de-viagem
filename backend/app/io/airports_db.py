
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import math

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "airports.csv"

def _load():
    df = pd.read_csv(DATA_PATH)
    cols = {c.lower(): c for c in df.columns}
    # Tentamos identificar colunas comuns
    iata_col = cols.get("iata") or cols.get("iata_code") or cols.get("IATA".lower())
    lat_col = cols.get("lat") or cols.get("latitude") or cols.get("Latitude".lower())
    lon_col = cols.get("lon") or cols.get("longitude") or cols.get("Longitude".lower())
    name_col = cols.get("name") or cols.get("airport") or cols.get("Nome".lower())
    city_col = cols.get("city") or cols.get("municipality") or cols.get("cidade")
    country_col = cols.get("country") or cols.get("iso_country") or cols.get("pais")
    if not all([iata_col, lat_col, lon_col]):
        raise RuntimeError("airports.csv precisa ter colunas IATA, latitude e longitude.")
    return df, iata_col, lat_col, lon_col, name_col, city_col, country_col

def get_airport_by_iata(iata: str) -> Optional[Dict]:
    df, iata_col, lat_col, lon_col, name_col, city_col, country_col = _load()
    row = df[df[iata_col].str.upper() == iata.upper()].head(1)
    if row.empty:
        return None
    r = row.iloc[0]
    return {
        "iata": r[iata_col],
        "lat": float(r[lat_col]),
        "lon": float(r[lon_col]),
        "name": r[name_col] if name_col else None,
        "city": r[city_col] if city_col else None,
        "country": r[country_col] if country_col else None
    }

def _haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def nearest_airports(lat: float, lon: float, n: int = 5) -> List[Dict]:
    df, iata_col, lat_col, lon_col, name_col, city_col, country_col = _load()
    df = df.copy()
    df["dist_km"] = df.apply(lambda r: _haversine(lat, lon, float(r[lat_col]), float(r[lon_col])), axis=1)
    df = df.sort_values("dist_km").head(n)
    out = []
    for _, r in df.iterrows():
        out.append({
            "iata": r[iata_col],
            "lat": float(r[lat_col]),
            "lon": float(r[lon_col]),
            "name": r[name_col] if name_col else None,
            "city": r[city_col] if city_col else None,
            "country": r[country_col] if country_col else None,
            "dist_km": float(r["dist_km"])
        })
    return out


def search_airports(query: str, limit: int = 10, lat: float = None, lon: float = None):
    """
    Pesquisa simples por IATA, nome, cidade ou país (case-insensitive).
    Se lat/lon forem fornecidos, ordena por distância; caso contrário, por match e nome.
    """
    df, iata_col, lat_col, lon_col, name_col, city_col, country_col = _load()
    q = str(query).strip().lower()
    if not q:
        return []

    def _match(row):
        fields = [
            str(row.get(iata_col, "")).lower(),
            str(row.get(name_col, "")).lower() if name_col else "",
            str(row.get(city_col, "")).lower() if city_col else "",
            str(row.get(country_col, "")).lower() if country_col else "",
        ]
        return any(q in f for f in fields)

    matches = df[df.apply(_match, axis=1)].copy()
    if matches.empty:
        return []

    if lat is not None and lon is not None:
        matches["dist_km"] = matches.apply(lambda r: _haversine(lat, lon, float(r[lat_col]), float(r[lon_col])), axis=1)
        matches = matches.sort_values("dist_km")
    else:
        # ordenação simples: IATA exata primeiro, depois por nome
        exact = matches[matches[iata_col].str.lower() == q]
        rest = matches[matches[iata_col].str.lower() != q]
        matches = pd.concat([exact, rest]).sort_values(name_col if name_col else iata_col)

    out = []
    for _, r in matches.head(limit).iterrows():
        out.append({
            "iata": r[iata_col],
            "name": r[name_col] if name_col else None,
            "city": r[city_col] if city_col else None,
            "country": r[country_col] if country_col else None,
            "lat": float(r[lat_col]),
            "lon": float(r[lon_col]),
            "dist_km": float(r["dist_km"]) if "dist_km" in matches.columns else None
        })
    return out
