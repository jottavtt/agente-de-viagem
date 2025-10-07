"use client";
import { useState } from "react";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

const schema = z.object({
  endereco_origem: z.string().min(5, "Digite um endereço válido"),
  origem_pais: z.string().min(2).default("Brasil"),
  destino_cidade: z.string().min(2),
  destino_pais: z.string().min(2),
  aeroporto_iata: z.string().optional(),
  tz_origem: z.string().min(3).default("America/Sao_Paulo"),
  datahora_partida_local: z.string().min(10, "Informe data e hora"),
  internacional: z.boolean().default(true),
  bagagem_despachada: z.boolean().default(false),
  assento_marcado: z.boolean().default(true),
  dias: z.coerce.number().int().min(1).max(60).default(6),
  atividades: z.string().optional(),
});
type FormData = z.infer<typeof schema>;
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Page() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } =
    useForm<FormData>({ resolver: zodResolver(schema), defaultValues: {
      origem_pais: "Brasil", tz_origem: "America/Sao_Paulo",
      internacional: true, bagagem_despachada: false, assento_marcado: true, dias: 6,
    }});
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (data: FormData) => {
    setError(null); setResult(null);
    try {
      const payload = {
        endereco_origem: data.endereco_origem,
        origem_pais: data.origem_pais,
        destino_cidade: data.destino_cidade,
        destino_pais: data.destino_pais,
        aeroporto_iata: data.aeroporto_iata || null,
        tz_origem: data.tz_origem,
        datahora_partida_local: data.datahora_partida_local,
        internacional: data.internacional,
        bagagem_despachada: data.bagagem_despachada,
        assento_marcado: data.assento_marcado,
        dias: data.dias,
        atividades: (data.atividades || "").split(",").map(s=>s.trim()).filter(Boolean),
      };
      const res = await fetch(`${API_URL}/plan`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`Falha no backend: ${res.status}`);
      setResult(await res.json());
    } catch (e:any) { setError(e.message || "Erro inesperado"); }
  };

  const Label = ({ children }: { children: React.ReactNode }) => (
    <span className="block text-sm font-medium text-neutral-700 dark:text-neutral-200">{children}</span>
  );

  return (
    <main className="min-h-screen bg-gradient-to-b from-white to-slate-50 dark:from-neutral-900 dark:to-neutral-950">
      <div className="mx-auto max-w-5xl px-4 py-10">
        <header className="mb-8 flex items-center gap-3">
          <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">Consultor de Viagens</h1>
          <span className="ml-auto rounded-full bg-sky-100 px-3 py-1 text-xs text-sky-700 dark:bg-sky-900/40 dark:text-sky-200">Next.js UI</span>
        </header>

        <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div className="space-y-4">
            <div>
              <Label>Endereço de origem</Label>
              <input {...register("endereco_origem")} placeholder="Av. Paulista, 1000, São Paulo"
                className="mt-1 w-full rounded-xl border border-slate-300 bg-white/70 px-3 py-2 shadow-sm outline-none focus:ring-2 focus:ring-sky-400 dark:bg-neutral-900 dark:border-neutral-700"/>
              {errors.endereco_origem && <p className="text-red-600 text-xs mt-1">{errors.endereco_origem.message}</p>}
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <Label>Cidade de destino</Label>
                <input {...register("destino_cidade")} placeholder="Santiago"
                  className="mt-1 w-full rounded-xl border border-slate-300 bg-white/70 px-3 py-2 shadow-none focus:ring-2 focus:ring-sky-400 dark:bg-neutral-900 dark:border-neutral-700"/>
                {errors.destino_cidade && <p className="text-red-600 text-xs mt-1">{errors.destino_cidade.message}</p>}
              </div>
              <div>
                <Label>País de destino</Label>
                <input {...register("destino_pais")} placeholder="Chile"
                  className="mt-1 w-full rounded-xl border border-slate-300 bg-white/70 px-3 py-2 shadow-none focus:ring-2 focus:ring-sky-400 dark:bg-neutral-900 dark:border-neutral-700"/>
                {errors.destino_pais && <p className="text-red-600 text-xs mt-1">{errors.destino_pais.message}</p>}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <Label>Aeroporto (IATA) — opcional</Label>
                <input {...register("aeroporto_iata")} placeholder="SCL"
                  className="mt-1 w-full rounded-xl border border-slate-300 bg-white/70 px-3 py-2 shadow-none focus:ring-2 focus:ring-sky-400 dark:bg-neutral-900 dark:border-neutral-700"/>
              </div>
              <div>
                <Label>Timezone de origem (IANA)</Label>
                <input {...register("tz_origem")} defaultValue="America/Sao_Paulo"
                  className="mt-1 w-full rounded-xl border border-slate-300 bg-white/70 px-3 py-2 shadow-none focus:ring-2 focus:ring-sky-400 dark:bg-neutral-900 dark:border-neutral-700"/>
              </div>
            </div>
            <div>
              <Label>Data/hora do voo (origem)</Label>
              <input type="datetime-local" {...register("datahora_partida_local")}
                className="mt-1 w-full rounded-xl border border-slate-300 bg-white/70 px-3 py-2 shadow-none focus:ring-2 focus:ring-sky-400 dark:bg-neutral-900 dark:border-neutral-700"/>
              {errors.datahora_partida_local && <p className="text-red-600 text-xs mt-1">{errors.datahora_partida_local.message}</p>}
            </div>
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <label className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white/70 p-3 dark:bg-neutral-900 dark:border-neutral-700">
                <input type="checkbox" {...register("internacional")} /><span>Voo internacional</span>
              </label>
              <label className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white/70 p-3 dark:bg-neutral-900 dark:border-neutral-700">
                <input type="checkbox" {...register("bagagem_despachada")} /><span>Despacha bagagem</span>
              </label>
              <label className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white/70 p-3 dark:bg-neutral-900 dark:border-neutral-700">
                <input defaultChecked type="checkbox" {...register("assento_marcado")} /><span>Assento marcado</span>
              </label>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <Label>Duração (dias)</Label>
                <input type="number" min={1} max={60} {...register("dias", { valueAsNumber: true })}
                  className="mt-1 w-full rounded-xl border border-slate-300 bg-white/70 px-3 py-2 shadow-none focus:ring-2 focus:ring-sky-400 dark:bg-neutral-900 dark:border-neutral-700"/>
              </div>
              <div>
                <Label>Atividades (vírgulas)</Label>
                <input {...register("atividades")} placeholder="trilha,praia,academia,negocios"
                  className="mt-1 w-full rounded-xl border border-slate-300 bg-white/70 px-3 py-2 shadow-none focus:ring-2 focus:ring-sky-400 dark:bg-neutral-900 dark:border-neutral-700"/>
              </div>
            </div>
            <button disabled={isSubmitting} className="w-full rounded-2xl bg-sky-600 px-4 py-3 text-white font-medium shadow hover:bg-sky-700 disabled:opacity-60">
              {isSubmitting ? "Gerando..." : "Gerar plano e checklist"}
            </button>
            {error && <p className="text-red-600 text-sm">{error}</p>}
          </div>
        </form>

        {result && (
          <section className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="rounded-2xl border border-slate-200 bg-white/70 p-5 shadow-sm dark:bg-neutral-900 dark:border-neutral-700">
              <h2 className="text-lg font-semibold mb-3">Resumo</h2>
              <ul className="space-y-2 text-sm">
                <li><strong>Aeroporto:</strong> {result.airport?.iata || "(desconhecido)"} — {result.airport?.city || ""}</li>
                <li><strong>Dirija-se de casa às:</strong> {result.departure_advice?.leave_at_local ? new Date(result.departure_advice.leave_at_local).toLocaleString() : "-"}</li>
                <li><strong>Tempo de deslocamento:</strong> ~{result.departure_advice?.breakdown_min?.drive} min</li>
                <li><strong>Buffers pré-voo:</strong> {result.departure_advice?.breakdown_min?.prevoo} min</li>
              </ul>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white/70 p-5 shadow-sm dark:bg-neutral-900 dark:border-neutral-700">
              <h2 className="text-lg font-semibold mb-3">Clima (médias)</h2>
              {result.climate_summary ? (
                <ul className="space-y-1 text-sm">
                  <li>Meses: {result.climate_summary.month_names?.join(", ")}</li>
                  <li>Temp média: {result.climate_summary.tavg_c?.toFixed?.(1)}°C (mín {result.climate_summary.tmin_c?.toFixed?.(1)}°C • máx {result.climate_summary.tmax_c?.toFixed?.(1)}°C)</li>
                  <li>Chuva: {Math.round(result.climate_summary.prcp_mm || 0)} mm — {result.climate_summary.rainy_class?.toUpperCase?.()}</li>
                  <li>Classificação: {result.climate_summary.temp_class?.toUpperCase?.()}</li>
                </ul>
              ) : <p className="text-sm">Clima indisponível.</p>}
            </div>
          </section>
        )}

        {result?.checklist_md && (
          <section className="mt-8">
            <h2 className="text-lg font-semibold mb-3">Checklist (Markdown)</h2>
            <pre className="rounded-xl border border-slate-200 bg-white/70 p-5 text-xs whitespace-pre-wrap dark:bg-neutral-900 dark:border-neutral-700">
{result.checklist_md}
            </pre>
          </section>
        )}

        <footer className="mt-14 text-center text-xs text-neutral-500">Configure <code>NEXT_PUBLIC_API_URL</code> para apontar ao FastAPI</footer>
      </div>
    </main>
  );
}
