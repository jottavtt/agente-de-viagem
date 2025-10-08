
from datetime import datetime, timedelta

def calc_saida_de_casa(voo_partida_local: datetime,
                       internacional: bool,
                       bagagem_despachada: bool,
                       assento_marcado: bool,
                       tempo_deslocamento_min: int):
    base = 180 if internacional else 120
    extras = 0
    detalhes = {"base": base, "despacho": 0, "sem_assento": 0, "pico": 0, "contingencia": 15}

    if bagagem_despachada:
        extras += 30
        detalhes["despacho"] = 30
    if not assento_marcado:
        extras += 20
        detalhes["sem_assento"] = 20

    estimativa_saida = voo_partida_local - timedelta(minutes=base + extras + tempo_deslocamento_min)
    hora = estimativa_saida.hour
    if 7 <= hora <= 10 or 17 <= hora <= 20:
        pico = 30 if internacional else 20
        extras += pico
        detalhes["pico"] = pico

    extras += 15
    total_prevoo = base + extras
    detalhes["total_prevoo"] = total_prevoo

    sair_quando = voo_partida_local - timedelta(minutes=total_prevoo + tempo_deslocamento_min)
    return sair_quando, detalhes
