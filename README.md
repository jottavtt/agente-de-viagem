diff --git a/README.md b/README.md
index a5f7f5963e90d8dc23391d795883e4bc6475bde5..de93e22591bea9dae805237b6d665923db86407e 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,91 @@
-# agente-de-viagem
+# Consultor de Viagens
+
+Este repositório contém dois projetos complementares:
+
+- **consultor_viagens** — backend em FastAPI responsável por gerar o plano de viagem, estimar horário de saída, resumir clima e construir checklist.
+- **consultor-ui** — frontend em Next.js + Tailwind que consome a API e apresenta um formulário interativo.
+
+Abaixo estão os passos para executar localmente, versionar no GitHub/GitLab e publicar no Render.
+
+## Requisitos
+
+- Python 3.10+
+- Node.js 18+
+- Git
+
+## Backend (FastAPI)
+
+```bash
+cd consultor_viagens
+python -m venv .venv
+source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
+pip install --upgrade pip
+pip install -r requirements_windows_no_compile.txt
+```
+
+Inicialize a base de aeroportos apontando para o CSV desejado:
+
+```bash
+python -c "from airports_db import init_db_from_csv; init_db_from_csv('airports.csv')"
+```
+
+Suba a API:
+
+```bash
+uvicorn api.app.main:app --reload --port 8000
+```
+
+Teste em `http://localhost:8000/health`.
+
+## Frontend (Next.js)
+
+```bash
+cd consultor-ui
+npm install
+npm run dev
+```
+
+A aplicação fica disponível em `http://localhost:3000`. Ajuste `consultor-ui/.env.local` se for expor o backend em outra URL.
+
+## Subindo para o Git
+
+1. Configure o repositório remoto (exemplo para GitHub):
+   ```bash
+   git remote add origin https://github.com/<usuario>/<repositorio>.git
+   ```
+2. Faça commit das alterações:
+   ```bash
+   git add .
+   git commit -m "feat: adicionar consultor de viagens"
+   ```
+3. Envie para o remoto:
+   ```bash
+   git push -u origin work
+   ```
+   Substitua `work` pelo nome da branch desejada (ex.: `main`).
+
+## Deploy no Render
+
+### Backend (FastAPI)
+1. Crie um novo **Web Service** no Render apontando para o repositório Git.
+2. Nas configurações, defina:
+   - **Runtime**: Python 3
+   - **Build Command**: `pip install -r consultor_viagens/requirements_windows_no_compile.txt`
+   - **Start Command**: `cd consultor_viagens && uvicorn api.app.main:app --host 0.0.0.0 --port $PORT`
+   - **Environment**: `Python Version` = `3.11` (ou compatível)
+3. Se precisar do arquivo `airports.sqlite3`, carregue o CSV em um bucket acessível ou faça upload via Render Disk. Você pode incluir um script de inicialização chamando `init_db_from_csv` no deploy, ou fazer isso manualmente em um shell do serviço.
+
+### Frontend (Next.js)
+1. Crie um **Static Site** (ou outro Web Service) apontando para o mesmo repositório.
+2. Configure:
+   - **Build Command**: `cd consultor-ui && npm install && npm run build`
+   - **Publish Directory**: `consultor-ui/.next`
+3. Defina a variável de ambiente `NEXT_PUBLIC_API_URL` com a URL pública do backend no Render.
+4. Após o deploy, Render servirá o frontend; garanta que o backend esteja acessível via HTTPS.
+
+## Dicas
+
+- Para testes locais simultâneos, execute o backend na porta `8000` e o frontend na `3000`.
+- Utilize `requests` no backend com cabeçalhos `User-Agent` personalizados para evitar bloqueios de API.
+- Mantenha variáveis sensíveis fora do repositório, usando `.env` conforme necessário.
+
