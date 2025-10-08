
"use client";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const searchAirports = async (q: string) => {
  const url = new URL(`${API_URL}/airports/search`);
  url.searchParams.set("q", q);
  const res = await fetch(url.toString());
  if (!res.ok) throw new Error("Erro ao buscar aeroportos");
  return res.json();
};



function Autocomplete({ onPick }: { onPick: (a: any) => void }) {
  const [q, setQ] = useState("");
  const [list, setList] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [timer, setTimer] = useState<any>(null);

  const doSearch = async (text: string) => {
    if (!text || text.length < 2) { setList([]); return; }
    try {
      setLoading(true);
      const res = await searchAirports(text);
      setList(res || []);
    } catch (e) {
      setList([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        placeholder="Ex.: SCL, Santiago, Arturo..."
        value={q}
        onChange={(e) => {
          const v = e.target.value;
          setQ(v);
          if (timer) clearTimeout(timer);
          const t = setTimeout(() => doSearch(v), 300);
          setTimer(t);
        }}
      />
      {loading && <div style={{ fontSize: 12, opacity: 0.7 }}>buscando…</div>}
      {list.length > 0 && (
        <div style={{ border: "1px solid #666", borderRadius: 8, padding: 8, marginTop: 4, maxHeight: 200, overflow: "auto" }}>
          {list.map((a, i) => (
            <div key={i}
              onClick={() => onPick(a)}
              style={{ padding: "6px 8px", cursor: "pointer", borderBottom: "1px solid #444" }}>
              <b>{a.iata}</b> — {a.name || "Aeroporto"} {a.city ? `• ${a.city}` : ""} {a.country ? `• ${a.country}` : ""}
              {a.dist_km ? <span style={{ float: "right", opacity: 0.7 }}>{a.dist_km.toFixed(0)} km</span> : null}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function Page() {
  const [form, setForm] = useState({
    origem_cidade: "São Paulo",
    origem_pais: "Brasil",
    origem_tz: "America/Sao_Paulo",
    destino_cidade: "Santiago",
    destino_pais: "Chile",
    destino_tz: "America/Santiago",
    data_ida: "",
    data_volta: "",
    voo_partida_local: "",
    internacional: true,
    bagagem_despachada: false,
    assento_marcado: true,
    tempo_deslocamento_min: 60,
    atividades: "city tour, vinícola"
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const update = (k: string, v: any) => setForm(prev => ({ ...prev, [k]: v }));

  const submit = async () => {
    setLoading(true); setError(null);
    try {
      const payload = {
        ...form,
        atividades: form.atividades.split(",").map(s => s.trim()).filter(Boolean),
      };
      const res = await fetch(`${API_URL}/trip/plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`Erro ${res.status}`);
      const data = await res.json();
      setResult(data);
    } catch (e: any) {
      setError(e.message || "Erro inesperado");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Consultor de Viagens</h1>
      <div className="card">
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          <div>
            <label>Origem - Cidade</label>
            <input value={form.origem_cidade} onChange={e => update("origem_cidade", e.target.value)} />
          </div>
          <div>
            <label>Origem - País</label>
            <input value={form.origem_pais} onChange={e => update("origem_pais", e.target.value)} />
          </div>
          <div>
            <label>Destino - Cidade</label>
            <input value={form.destino_cidade} onChange={e => update("destino_cidade", e.target.value)} />
          </div>

<div style={{ gridColumn: "1 / span 2" }}>
  <label>Buscar aeroporto (IATA, cidade, nome)</label>
  <Autocomplete onPick={(a) => {
    if (a.city) update("destino_cidade", a.city);
    if (a.country) update("destino_pais", a.country);
  }} />
</div>
          <div>
            <label>Destino - País</label>
            <input value={form.destino_pais} onChange={e => update("destino_pais", e.target.value)} />
          </div>
          <div>
            <label>Data de Ida (AAAA-MM-DD)</label>
            <input placeholder="2025-11-19" value={form.data_ida} onChange={e => update("data_ida", e.target.value)} />
          </div>
          <div>
            <label>Data de Volta (AAAA-MM-DD)</label>
            <input placeholder="2025-11-24" value={form.data_volta} onChange={e => update("data_volta", e.target.value)} />
          </div>
          <div style={{ gridColumn: "1 / span 2" }}>
            <label>Horário do Voo (local, ISO) – ex.: 2025-11-19T17:45:00</label>
            <input placeholder="2025-11-19T17:45:00" value={form.voo_partida_local} onChange={e => update("voo_partida_local", e.target.value)} />
          </div>
          <div>
            <label>Internacional</label>
            <select value={String(form.internacional)} onChange={e => update("internacional", e.target.value === "true")}>
              <option value="true">Sim</option>
              <option value="false">Não</option>
            </select>
          </div>
          <div>
            <label>Despacha bagagem?</label>
            <select value={String(form.bagagem_despachada)} onChange={e => update("bagagem_despachada", e.target.value === "true")}>
              <option value="false">Não</option>
              <option value="true">Sim</option>
            </select>
          </div>
          <div>
            <label>Assento marcado?</label>
            <select value={String(form.assento_marcado)} onChange={e => update("assento_marcado", e.target.value === "true")}>
              <option value="true">Sim</option>
              <option value="false">Não</option>
            </select>
          </div>
          <div>
            <label>Deslocamento até o aeroporto (min)</label>
            <input type="number" value={form.tempo_deslocamento_min} onChange={e => update("tempo_deslocamento_min", Number(e.target.value))} />
          </div>
          <div style={{ gridColumn: "1 / span 2" }}>
            <label>Atividades (separadas por vírgula)</label>
            <input value={form.atividades} onChange={e => update("atividades", e.target.value)} />
          </div>
        </div>
        <div style={{ marginTop: 12 }}>
          <button onClick={submit} disabled={loading}>{loading ? "Calculando..." : "Gerar Plano"}</button>
        </div>
        {error && <p style={{ color: "tomato" }}>{error}</p>}
      </div>

      {result && (
        <div className="card">
          <h2>Hora de sair de casa</h2>
          <p><b>{new Date(result.leave_at).toLocaleString()}</b></p>

          <h3>Buffers</h3>
          <pre>{JSON.stringify(result.buffers, null, 2)}</pre>

          <h3>Clima</h3>
          <pre>{JSON.stringify(result.climate, null, 2)}</pre>

          <h3>Checklist</h3>
          <ReactMarkdown>{result.checklist_markdown}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}
