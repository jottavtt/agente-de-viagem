
from pydantic import BaseModel, Field, conint
from typing import List, Dict
from datetime import date, datetime

class ClimateSummary(BaseModel):
    month_names: List[str]
    tmin_c: float
    tavg_c: float
    tmax_c: float
    prcp_mm: float
    rainy_class: str
    temp_class: str

class TripInfo(BaseModel):
    origem_cidade: str
    origem_pais: str
    origem_tz: str = "America/Sao_Paulo"
    destino_cidade: str
    destino_pais: str
    destino_tz: str = "America/Santiago"
    data_ida: date
    data_volta: date
    voo_partida_local: datetime
    internacional: bool = True
    bagagem_despachada: bool = False
    assento_marcado: bool = True
    tempo_deslocamento_min: conint(gt=0) = 60
    atividades: List[str] = []

class PlanResponse(BaseModel):
    leave_at: datetime
    buffers: Dict[str, int]
    climate: ClimateSummary
    checklist_markdown: str
