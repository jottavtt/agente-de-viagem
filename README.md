
# Consultor de Viagens – Monorepo (Backend + Web)

## Estrutura
- `/backend`: FastAPI (Python)
- `/web`: Next.js (TypeScript)

## Como rodar localmente
### Backend
```bash
cd backend
pip install -e .
uvicorn app.main:app --reload --port 8000
```

### Web
```bash
cd web
npm install
export NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

## Deploy no Render
Use `render.yaml` dentro de `/backend` (já define dois serviços: API e Web).
- Ajuste `NEXT_PUBLIC_API_URL` do serviço web para a URL do backend após o primeiro deploy.
