# Speed Test

A lightweight browser-based network speed test that measures **latency**, **download speed**, and **upload speed** between the browser and the server where this app is hosted.

---

## Features

- **Ping / Latency** — averages 10 round-trip probes (ms)
- **Download speed** — streams a configurable payload from server to browser (Mbps)
- **Upload speed** — sends random incompressible data from browser to server (Mbps)
- **Live results** — download speed updates in real time as chunks arrive
- **Reverse proxy aware** — API calls are always rooted at the origin (`/api/speedtest/*`), independent of the frontend path prefix

---

## Project Structure

```
speed-test/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── pyproject.toml   # uv-managed dependencies
│   └── uv.lock          # Locked dependency versions
├── frontend/
│   └── index.html       # Single-file HTML/CSS/JS UI
├── Dockerfile
└── .dockerignore
```

---

## API Endpoints

Both path forms are supported simultaneously:

| Method | Path | Alias | Description |
|--------|------|-------|-------------|
| `GET` | `/ping` | `/api/speedtest/ping` | Latency probe |
| `GET` | `/download?size=10` | `/api/speedtest/download?size=10` | Stream N MB of random bytes (1–100) |
| `POST` | `/upload` | `/api/speedtest/upload` | Receive bytes, return count |
| `GET` | `/` | — | Serve the frontend |

---

## Local Development

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Setup & Run

```bash
cd backend
uv sync
uv run uvicorn main:app --reload --port 8000
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Docker

### Build

```bash
docker build -t speed-test .
```

### Run

```bash
docker run --rm -p 8000:8000 speed-test
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Reverse Proxy Deployment

The frontend and API can be served from different paths. The UI always sends API requests to `/api/speedtest/*` relative to the **origin**, not the page path.

**Example:** frontend at `http://example.com/apps/speedtest`, API at `http://example.com/api/speedtest/ping`.

### Nginx example

```nginx
# Serve the frontend
location /apps/speedtest {
    proxy_pass http://localhost:8000/;
}

# Proxy the API
location /api/speedtest/ {
    proxy_pass http://localhost:8000/api/speedtest/;
}
```
