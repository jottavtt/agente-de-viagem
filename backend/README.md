
# Consultor de Viagens – Backend (FastAPI)

## Rodando local
```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints
- `GET /health`
- `POST /trip/plan` – payload TripInfo, retorna horário de saída, buffers, clima e checklist Markdown

## Deploy no Render
Use o `render.yaml` na raiz do projeto (pasta /backend). Variáveis comuns:
- `PORT` é gerenciado pelo Render.
- Considere setar `ALLOWED_ORIGINS` se quiser restringir o CORS.
