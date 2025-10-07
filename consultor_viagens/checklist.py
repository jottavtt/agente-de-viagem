# -*- coding: utf-8 -*-
import math
PLUG_TYPES = {
  "Brasil":"Tipo N (às vezes C) • 127/220V","Argentina":"Tipo C/I • 220V","Chile":"Tipo C/L • 220V",
  "Estados Unidos":"Tipo A/B • 120V","Portugal":"Tipo C/F • 230V","Espanha":"Tipo C/F • 230V",
  "França":"Tipo C/E • 230V","Alemanha":"Tipo C/F • 230V","Itália":"Tipo C/F/L • 230V","Japão":"Tipo A/B • 100V"
}
def _q(days,f,min_i=1,max_i=None):
    q=max(min_i,int(math.ceil(days*f))); return min(q,max_i) if max_i else q

def build_checklist(dest_city: str, dest_country: str, climate: dict, days: int, atividades: list[str]) -> str:
    quente = climate and climate["temp_class"] in ["quente","muito quente"]
    frio = climate and climate["temp_class"] in ["frio","muito frio"]
    chuvoso = climate and climate["rainy_class"]=="chuvoso"
    moderado = climate and climate["rainy_class"]=="moderado"
    trilha = any(a.lower()=="trilha" for a in atividades)
    praia = any(a.lower()=="praia" for a in atividades)
    academia = any(a.lower()=="academia" for a in atividades)
    negocios = any(a.lower() in ("negócios","negocios") for a in atividades)
    adapt = PLUG_TYPES.get(dest_country, "Verifique tipo de tomada & voltagem locais")
    q_meias=_q(days,1); q_cueca=_q(days,1); q_cam=_q(days,0.7,3); q_cas=_q(days,0.4,1)
    q_ag=_q(days,0.2,1,3); q_ber=_q(days,0.3,1); q_cal=_q(days,0.3,1); q_pj=max(1,days//4); q_shoes=2
    if quente: q_ber=max(q_ber,2)
    if frio: q_ag=max(q_ag,2); q_cal=max(q_cal,2)
    md=[]
    md.append(f"# Checklist – {dest_city}, {dest_country}\n")
    if climate:
        md += [
            "## Clima (médias)", 
            f"- Meses: {', '.join(climate['month_names'])}",
            f"- Temp média: **{climate['tavg_c']:.1f}°C** (mín {climate['tmin_c']:.1f}°C • máx {climate['tmax_c']:.1f}°C)",
            f"- Chuva (mês): **{climate['prcp_mm']:.0f} mm** → **{climate['rainy_class'].upper()}**",
            f"- Classificação térmica: **{climate['temp_class'].upper()}**\n"
        ]
    md += [
        "## Documentos & Essenciais",
        "[ ] RG/Passaporte + cópia digital","[ ] Cartão de embarque (app/PDF)","[ ] Vouchers hospedagem/seguro",
        f"[ ] Adaptador de tomada: **{adapt}**","[ ] Cartões de crédito/dinheiro","[ ] Cadeado TSA\n",
        "## Roupas",
        f"[ ] Camisetas: **{q_cam}**", f"[ ] Camisas casuais: **{q_cas}**",
        f"[ ] Meias: **{q_meias}**", f"[ ] Roupas íntimas: **{q_cueca}**",
        f"[ ] Pijama(s): **{q_pj}**", f"[ ] Agasalhos: **{q_ag}**",
        f"[ ] Calças: **{q_cal}**", f"[ ] Bermudas/shorts: **{q_ber}**",
        f"[ ] Calçados (tênis+casual): **{q_shoes}**",
        "[ ] Capa de chuva/Anorak" if (chuvoso or moderado) else "[ ] Corta-vento (opcional)",
        "[ ] Segunda pele/Thermal" if frio else "[ ] Camiseta dry-fit extra",
    ]
    if praia and quente: md += ["[ ] Roupas de banho (2)", "[ ] Chinelo"]
    if trilha: md += ["[ ] Bota/Meia técnica", "[ ] Calça de caminhada", "[ ] Boné/chapéu UV"]
    if negocios: md += ["[ ] Blazer/Terno", "[ ] Camisa social (2)", "[ ] Sapato social"]
    md += [
        "\n## Eletrônicos",
        "[ ] Celular + carregadores","[ ] Power bank (≤100Wh — bagagem de mão)","[ ] Fones",
        "[ ] Extensão/benjamim compacto","[ ] eSIM/Chip internacional\n",
        "## Regras de Bagagem (check rápido)",
        "- Líquidos na mão: frascos ≤100 ml dentro de saquinho de 1 L.",
        "- Power bank: sempre na bagagem de mão.",
        "- Proibidos: cortantes/ inflamáveis etc.\n",
        "## Antes de sair de casa",
        "[ ] Check-in feito e cartão salvo offline","[ ] Documentos acessíveis",
        "[ ] Garrafa vazia p/ água pós raio-x","[ ] Chaves, carteira, celular, power bank\n"
    ]
    return "\n".join(md)
