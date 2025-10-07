# -*- coding: utf-8 -*-
from datetime import date
from meteostat import Stations, Normals, Daily, Point

def month_name_pt(m: int) -> str:
    return [
        "","janeiro","fevereiro","março","abril","maio","junho","julho",
        "agosto","setembro","outubro","novembro","dezembro"
    ][m]

def _temp_class(tmax: float) -> str:
    if tmax >= 31: return "muito quente"
    if tmax >= 25: return "quente"
    if tmax >= 18: return "ameno"
    if tmax >= 10: return "frio"
    return "muito frio"

def _rain_class(prcp: float) -> str:
    if prcp >= 120: return "chuvoso"
    if prcp >= 60: return "moderado"
    return "seco"

def summarize_climate(lat: float, lon: float, start: date, end: date) -> dict:
    trip_months = sorted({start.month, end.month})
    st = Stations().nearby(lat, lon).fetch(3)
    normals = None
    for sid in st.index:
        try:
            df = Normals(sid, monthly=True).fetch()
            if df is not None and not df.empty:
                normals = df
                break
        except Exception:
            continue
    if normals is None or normals.empty:
        end_dt = date.today().replace(day=1)
        start_dt = end_dt.replace(year=end_dt.year-10)
        daily = Daily(Point(lat, lon), start_dt, end_dt).fetch().dropna(how="all")
        if daily.empty:
            return None
        daily["month"] = daily.index.month
        agg = daily.groupby("month").agg(
            tmin=("tmin", "mean"),
            tavg=("tavg", "mean"),
            tmax=("tmax", "mean"),
            prcp=("prcp", "sum"),
        )
        normals = agg
    rows = normals.loc[trip_months]
    tmin = float(rows["tmin"].mean())
    tavg = float(rows["tavg"].mean())
    tmax = float(rows["tmax"].mean())
    prcp = float((rows["prcp"] if "prcp" in rows.columns else rows.iloc[:, 0]).mean())
    return {
        "month_names": [month_name_pt(m) for m in trip_months],
        "tmin_c": tmin,
        "tavg_c": tavg,
        "tmax_c": tmax,
        "prcp_mm": prcp,
        "rainy_class": _rain_class(prcp),
        "temp_class": _temp_class(tmax),
    }
