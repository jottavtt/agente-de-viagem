# -*- coding: utf-8 -*-
from datetime import datetime

def calc_preflight_buffers(internacional: bool, bagagem: bool, assento: bool) -> tuple[int, dict]:
    base = 180 if internacional else 120
    extras = 15
    det = {"base": base, "despacho": 0, "sem_assento": 0, "contingencia": 15, "pico": 0}
    if bagagem: extras += 30; det["despacho"] = 30
    if not assento: extras += 20; det["sem_assento"] = 20
    return base + extras, det

def apply_peak_adjustment(leave_estimate: datetime, internacional: bool, det: dict) -> int:
    h = leave_estimate.hour
    pico = 30 if (7 <= h <= 10 or 17 <= h <= 20) and internacional else (20 if 7 <= h <= 10 or 17 <= h <= 20 else 0)
    det["pico"] = pico
    return pico
