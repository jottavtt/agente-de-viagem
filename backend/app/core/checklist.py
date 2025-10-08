
import math
from ..models import TripInfo, ClimateSummary

PLUG_TYPES = {
    "Brasil": "Tipo N (às vezes C) • 127/220V",
    "Argentina": "Tipo C/I • 220V",
    "Chile": "Tipo C/L • 220V",
    "Estados Unidos": "Tipo A/B • 120V",
    "Canadá": "Tipo A/B • 120V",
    "México": "Tipo A/B • 127V",
    "Reino Unido": "Tipo G • 230V",
    "Irlanda": "Tipo G • 230V",
    "Portugal": "Tipo C/F • 230V",
    "Espanha": "Tipo C/F • 230V",
    "França": "Tipo C/E • 230V",
    "Alemanha": "Tipo C/F • 230V",
    "Itália": "Tipo C/F/L • 230V",
    "Suíça": "Tipo J • 230V",
    "Áustria": "Tipo C/F • 230V",
    "Países Baixos": "Tipo C/F • 230V",
    "Japão": "Tipo A/B • 100V",
    "Austrália": "Tipo I • 230V",
    "Nova Zelândia": "Tipo I • 230V",
    "China": "Tipo A/C/I • 220V",
}

def qty_by_days(days: int, factor: float, min_items: int = 1, max_items=None) -> int:
    q = max(min_items, int(math.ceil(days * factor)))
    if max_items:
        q = min(q, max_items)
    return q

def build_checklist(trip: TripInfo, climate: ClimateSummary, days: int) -> str:
    quente = climate.temp_class in ["quente", "muito quente"]
    frio = climate.temp_class in ["frio", "muito frio"]
    chuvoso = climate.rainy_class == "chuvoso"
    moderado = climate.rainy_class == "moderado"

    q_meias = qty_by_days(days, 1.0)
    q_cueca = qty_by_days(days, 1.0)
    q_camisas = qty_by_days(days, 0.7, min_items=3)
    q_casual = qty_by_days(days, 0.4, min_items=1)
    q_agasalhos = qty_by_days(days, 0.2, min_items=1, max_items=3)
    q_bermudas = qty_by_days(days, 0.3, min_items=1)
    q_calcas = qty_by_days(days, 0.3, min_items=1)
    q_pijamas = max(1, days // 4)
    q_calcados = 2

    if quente:
        q_bermudas = max(q_bermudas, 2)
    if frio:
        q_agasalhos = max(q_agasalhos, 2)
        q_calcas = max(q_calcas, 2)

    acts = [a.lower() for a in trip.atividades]
    trilha = "trilha" in acts
    praia = "praia" in acts
    academia = "academia" in acts
    negocios = ("negócios" in acts) or ("negocios" in acts)

    adaptador = PLUG_TYPES.get(trip.destino_pais, "Verifique tipo de tomada & voltagem locais")

    lines = []
    lines.append(f"# Checklist de Viagem – {trip.destino_cidade}, {trip.destino_pais}\n")
    lines.append("## Resumo do Clima (médias históricas)")
    lines.append(f"- Meses considerados: {', '.join(climate.month_names)}")
    lines.append(f"- Temperatura média: **{climate.tavg_c:.1f}°C** (mín {climate.tmin_c:.1f}°C • máx {climate.tmax_c:.1f}°C)")
    lines.append(f"- Precipitação média mensal: **{climate.prcp_mm:.0f} mm** → **{climate.rainy_class.upper()}**")
    lines.append(f"- Classificação térmica: **{climate.temp_class.upper()}**\n")

    doc = [
        "## Documentos & Essenciais",
        "[ ] Documento com foto (RG/Passaporte) + cópia digital",
        "[ ] Passagens / cartão de embarque (app e PDF)",
        "[ ] Comprovantes de hospedagem / vouchers",
        "[ ] Seguro viagem (apólice e telefone de emergência)",
        "[ ] Cartões + limite liberado para o exterior (se for o caso)",
        "[ ] Dinheiro em espécie (moeda local) / cartão pré-pago",
        "[ ] Carteira de vacinação (se exigido) • CIVP",
        "[ ] CNH e PID (se for dirigir) • reserva do carro",
        "[ ] Contatos importantes em papel (em caso de perda do celular)",
        f"[ ] Adaptador de tomada: **{adaptador}**",
        "[ ] Cadeado TSA + tags de bagagem",
        ""
    ]
    if trip.internacional:
        doc.insert(2, "[ ] Visto/Autorização eletrônica (se aplicável)")
    lines += doc

    roupas = [
        "## Roupas",
        f"[ ] Camisetas: **{q_camisas}**",
        f"[ ] Camisas casuais: **{q_casual}**",
        f"[ ] Meias: **{q_meias}**",
        f"[ ] Roupas íntimas: **{q_cueca}**",
        f"[ ] Pijama(s): **{q_pijamas}**",
        f"[ ] Agasalhos/Sobrecamadas: **{q_agasalhos}**",
        f"[ ] Calças: **{q_calcas}**",
        f"[ ] Bermudas/shorts: **{q_bermudas}**",
        f"[ ] Calçados (tênis + casual): **{q_calcados}**",
        "[ ] Capa de chuva/Anorak leve" if (chuvoso or moderado) else "[ ] Corta-vento leve (opcional)",
        "[ ] Segunda pele/Thermal" if frio else "[ ] Camiseta dry fit extra",
        ""
    ]
    if praia and quente:
        roupas += ["[ ] Roupas de banho (2)", "[ ] Saída de praia", "[ ] Chinelo"]
    if trilha:
        roupas += ["[ ] Bota de trilha / meia técnica", "[ ] Calça/bermuda de caminhada", "[ ] Boné/chapéu UV"]
    if negocios:
        roupas += ["[ ] 1 terno/blazer", "[ ] 1 calça social", "[ ] 2 camisas sociais", "[ ] 1 sapato social"]
    lines += roupas + [""]

    saude = [
        "## Acessórios & Saúde",
        "[ ] Necessaire completa (escova, pasta, fio dental, desodorante, sabonete, shampoo/cond.)",
        "[ ] Hidratante / protetor labial",
        "[ ] Protetor solar (FPS 30+)",
        "[ ] Remédios de uso contínuo + receita",
        "[ ] Kit primeiros socorros (analgésico, antialérgico, antidiarreico, curativos, termômetro)",
        "[ ] Repelente (se necessário)",
        "[ ] Lenços umedecidos / álcool em gel",
        "[ ] Mini kit costura (linha, agulha, botão, alfinete)",
        ""
    ]
    if frio:
        saude += ["[ ] Protetor térmico (mãos/pés), luvas, gorro, cachecol"]
    lines += saude + [""]

    eletronicos = [
        "## Eletrônicos",
        "[ ] Celular + case resistente",
        "[ ] Carregadores (USB-C/Lightning/USB-A conforme)",
        "[ ] Power bank (≤ 100 Wh, na bagagem de mão)",
        "[ ] Fones de ouvido (com fio e/ou bluetooth)",
        "[ ] Tomada/Benjamim extra / extensão compacta",
        "[ ] eSIM/Chip internacional (se aplicável) + apps offline",
        "[ ] Rastreador de bagagem (ex.: AirTag/Tile) (opcional)",
        ""
    ]
    if academia or trilha:
        eletronicos += ["[ ] Relógio esportivo / cinta cardio", "[ ] Carregador do relógio"]
    lines += eletronicos + [""]

    extras = [
        "## Extras",
        "[ ] Saco a vácuo / organizadores (packing cubes)",
        "[ ] Saco estanque (chuva/trilha)",
        "[ ] Garrafa dobrável",
        "[ ] Óculos de sol",
        "[ ] Lanchinhos para o voo",
        "[ ] Mini guarda-chuva" if (chuvoso or moderado) else "[ ] Óculos de sol reserva",
        ""
    ]
    lines += extras + [""]

    lines += [
        "## Regras de Bagagem (check rápido)",
        "- **Líquidos na MÃO**: frascos ≤ 100 ml dentro de saquinho transparente de 1 L.",
        "- **Power bank**: sempre na bagagem de mão (não despachar).",
        "- **Itens proibidos**: objetos cortantes, inflamáveis, aerossóis fora das regras, etc.",
        ""
    ]

    lines += [
        "## Antes de sair de casa",
        "[ ] Check-in online feito • cartão de embarque salvo offline",
        "[ ] Documento separado e acessível",
        "[ ] Tomar água • pegar garrafa vazia",
        "[ ] Chaves, carteira, celular, carregador portátil",
        "[ ] Apps de transporte instalados, endereço do aeroporto salvo",
        ""
    ]

    return "\n".join(lines)
