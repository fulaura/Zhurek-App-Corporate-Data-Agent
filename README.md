# Auyrmaidy_zhurek — CASE 6: BI-GPT

Team: Auyrmaidy_zhurek

Hackathon case: #6 — задача: BI-GPT: агент по корпоративной БД (Natural Language → SQL)

This repository contains the server and minimal frontend integration used in the CASE 6 chatflow. Below are notes needed to run the app locally, expose it with ngrok, and the high-level architecture decisions and integrations.

## Quick start (development)

Prerequisites:
- Python 3.10+ installed
- Git (optional)
- `requirements.txt` provided in this repo

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

2. Run the development server (uvicorn) on port 8000:

```powershell
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000 in your browser to access the site.

If you run into issues, make sure `main.py` exposes a FastAPI app named `app` (example: `app = FastAPI()`), and that dependencies from `requirements.txt` are installed.

## Expose locally with ngrok (config only)

We recommend using ngrok when you need an external endpoint for the Shai platform to reach your local server. Do NOT commit your real credentials — use environment variables or the platform secret manager.

Example ngrok configuration (place in `%USERPROFILE%\.ngrok2\ngrok.yml` or `~/.ngrok2/ngrok.yml`):

```yaml
authtoken: "YOUR_NGROK_AUTHTOKEN_GOES_HERE"
region: us
tunnels:
	case6:
		addr: 8000
		proto: http
		host_header: rewrite
```

You can also run a one-off tunnel from PowerShell:

```powershell
ngrok http 8000 --authtoken="YOUR_NGROK_AUTHTOKEN_GOES_HERE" --region=us
```

The public URL shown by ngrok should be registered in the Shai platform as the webhook / callback for your chatflow. Use HTTPS URL and keep your authtoken secret.

## Shai platform integration

- Working space: `auyrmaidy_zurek` (on Shai platform)
- Chatflow name: "CASE 6"

Requests originate from the Shai chatflow and are sent to our server endpoints. Our server embeds incoming user requests using the `all-MiniLM-L6-v2` (allmini) embedding model before searching our knowledge base.

Knowledge base source:
- We use `knowledge/metadata.txt` in this repository as the canonical knowledge base metadata file for this demo. The server code reads and uses data from `knowledge/metadata.txt` (and related files in the `knowledge/` folder) to perform semantic search against stored documents.

Typical flow:
- Shai chatflow (iframe) → POST to our server endpoints → server embeds request (all-MiniLM-L6-v2) → semantic search on knowledge base → produce SQL / chart data → respond to Shai / frontend.

## Frontend

- The frontend integrates an iframe served by the Shai platform for the chatflow interaction.
- We also expose custom routes (for example `/api/plot-data`) which the frontend uses to fetch processed data to render charts.
- Charting is done with Chart.js in the frontend. The server returns JSON data shaped for Chart.js datasets (labels + datasets).

Real endpoints (as implemented in `main.py`):
- `GET /` — redirects to `/v1/embeddings` in the code (root redirect)
- `POST /embeddings` — accepts JSON {"input": [...], "model": "all-MiniLM-L6-v2"} and returns embeddings encoded by `all-MiniLM-L6-v2` in OpenAI-like JSON shape
- `GET /other` — simple route that returns a JSON message
- `POST /data` — receives JSON data from clients, broadcasts it to connected WebSocket clients, and returns status JSON
- `WebSocket /ws` — WebSocket endpoint for clients to connect and receive broadcast messages

Example additional routes you might add (not currently implemented):
- `/api/plot-data` — return time-series or tabular data for Chart.js (example responsibility)
- `/webhook/chatflow` — a webhook-style route to receive Shai chatflow events (example responsibility)

Front-end iframe notes:
- The iframe hosts the Shai chatflow UI. Communication between iframe and parent can be done via postMessage if needed, or the iframe can call our exposed endpoints directly if allowed by the platform.

## Embeddings and knowledge base

- Embeddings model: `all-MiniLM-L6-v2` (short: `allmini`) — used to convert user queries into vector form for semantic search.
- Knowledge base: we store documents and their embeddings in Cloudflare D1 (or we use D1 to store raw documents and metadata; embeddings can be stored as vectors or in a separate vector index if preferred).

Environment variables and config placeholders:
- `D1_DATABASE_URL` — Cloudflare D1 connection string
- `EMBEDDING_MODEL` — `all-MiniLM-L6-v2`

## Database (Cloudflare D1)

We use Cloudflare D1 as our primary datastore for case data and metadata. In production, configure the D1 credentials/secrets in the Shai platform secret manager and never commit them to the repo.

## LLM

- LLM: `LLama4Scout` — we connect it via an OpenAI-compatible plugin or bridge so the rest of our code uses the OpenAI plugin interface.


## Security and secrets

- Do not commit API keys, tokens, or ngrok authtoken to source control.
- Use environment variables or the Shai platform secret manager for:
	- ngrok authtoken
	- Cloudflare D1 credentials
	- OpenAI plugin credentials / Llama4Scout configs

## Troubleshooting

- If uvicorn fails to start, check that `main.py` contains an `app` (FastAPI) object and that no port conflicts exist.
- If Shai cannot reach your local server, confirm ngrok is running and that the public URL is configured in the Shai workspace.

## Notes

- This README contains configuration guidance and placeholders only. Replace placeholders with real secrets in your platform's secret store before deployment.
- Contact the team lead if you need help wiring platform-specific secrets.



