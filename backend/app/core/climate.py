
from datetime import date
from typing import Optional, List
import pandas as pd
from meteostat import Stations, Normals, Daily, Point
from ..models import ClimateSummary

def month_name_pt(m: int) -> str:
    return ["","janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"][m]

def _find_stations(lat: float, lon: float):
    st = Stations().nearby(lat, lon)
    return st.fetch(3)

def _normals_for_station(station_id: str) -> Optional[pd.DataFrame]:
    try:
        df = Normals(station_id, monthly=True).fetch()
        return df
    except Exception:
        return None

def _fallback_monthly(lat: float, lon: float) -> pd.DataFrame:
    end_dt = date.today().replace(day=1)
    start_dt = end_dt.replace(year=end_dt.year - 10)
    point = Point(lat, lon)
    daily = Daily(point, start_dt, end_dt).fetch().dropna(how="all")
    daily["month"] = daily.index.month
    agg = daily.groupby("month").agg(
        tmin=("tmin", "mean"),
        tavg=("tavg", "mean"),
        tmax=("tmax", "mean"),
        prcp=("prcp", "sum")
    )
    return agg

def _geocode(city: str, country: str):
    # Para reduzir dependências no backend, usamos uma lookup leve via Nominatim somente quando necessário.
    # Se quiser trocar por um dataset próprio, injete aqui.
    from geopy.geocoders import Nominatim
    geo = Nominatim(user_agent="consultor_viagens_api")
    loc = geo.geocode(f"{city}, {country}", language="pt")
    if not loc:
        raise RuntimeError(f"Não encontrei coordenadas para {city}, {country}.")
    return loc.latitude, loc.longitude

def get_climate_summary(city: str, country: str, start: date, end: date) -> ClimateSummary:
    lat, lon = _geocode(city, country)
    trip_months = sorted({start.month, end.month})

    stations = _find_stations(lat, lon)
    normals = None
    for sid in stations.index if not stations.empty else []:
        normals = _normals_for_station(sid)
        if normals is not None and not normals.empty:
            break

    if normals is None or normals.empty:
        normals = _fallback_monthly(lat, lon)

    rows = normals.loc[trip_months]
    tmin = float(rows["tmin"].mean())
    tavg = float(rows["tavg"].mean())
    tmax = float(rows["tmax"].mean())
    prcp_col = "prcp" if "prcp" in rows.columns else rows.columns[0]
    prcp = float(rows[prcp_col].mean())

    if tmax >= 31: temp_class = "muito quente"
    elif tmax >= 25: temp_class = "quente"
    elif tmax >= 18: temp_class = "ameno"
    elif tmax >= 10: temp_class = "frio"
    else: temp_class = "muito frio"

    if prcp >= 120: rainy_class = "chuvoso"
    elif prcp >= 60: rainy_class = "moderado"
    else: rainy_class = "seco"

    month_names = [month_name_pt(m) for m in trip_months]
    return ClimateSummary(
        month_names=month_names,
        tmin_c=tmin, tavg_c=tavg, tmax_c=tmax,
        prcp_mm=prcp,
        rainy_class=rainy_class,
        temp_class=temp_class
    )
