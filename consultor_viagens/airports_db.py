# -*- coding: utf-8 -*-
import sqlite3, csv, math
from pathlib import Path
from typing import Optional, Tuple, List

DB_PATH = Path("data/airports.sqlite3")

def init_db_from_csv(csv_path: str) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS airports(
        iata TEXT, icao TEXT, name TEXT, city TEXT, country TEXT,
        lat REAL, lon REAL
    )""")
    cur.execute("DELETE FROM airports")
    with open(csv_path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        rows = []
        for row in r:
            iata = (row.get("iata_code") or row.get("iata") or "").strip() or None
            icao = (row.get("ident") or row.get("icao") or "").strip() or None
            lat_s = row.get("latitude_deg") or row.get("lat") or row.get("latitude")
            lon_s = row.get("longitude_deg") or row.get("lon") or row.get("longitude")
            try:
                lat = float(lat_s) if lat_s not in (None, "") else None
                lon = float(lon_s) if lon_s not in (None, "") else None
            except Exception:
                lat, lon = None, None
            name = (row.get("name") or "").strip()
            city = (row.get("municipality") or row.get("city") or "").strip()
            country = (row.get("iso_country") or row.get("country") or "").strip()
            if lat is not None and lon is not None:
                rows.append((iata, icao, name, city, country, lat, lon))
        if rows:
            cur.executemany("INSERT INTO airports VALUES (?,?,?,?,?,?,?)", rows)
    con.commit(); con.close()

def get_airport_by_iata(iata: str) -> Optional[Tuple[str,str,str,str,str,float,float]]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT iata, icao, name, city, country, lat, lon FROM airports WHERE iata = ?", (iata.upper(),))
    row = cur.fetchone()
    con.close()
    return row

def nearest_airports(lat: float, lon: float, limit: int = 5) -> List[Tuple]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT iata, icao, name, city, country, lat, lon FROM airports WHERE lat IS NOT NULL")
    rows = cur.fetchall(); con.close()
    def hav(a,b,c,d):
        import math
        R=6371.0
        p1=math.radians(a); p2=math.radians(c)
        dphi=math.radians(c-a); dl=math.radians(d-b)
        h=math.sin(dphi/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
        return 2*R*math.asin(math.sqrt(h))
    scored=[(hav(lat,lon,x[5],x[6]), x) for x in rows]
    scored.sort(key=lambda t:t[0])
    return [x for _,x in scored[:limit]]
