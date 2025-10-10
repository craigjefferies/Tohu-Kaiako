# Tohu Kaiako — “Teacher’s Sign”

Tohu Kaiako is a single-page application that generates a printable NZSL learning pack using OpenRouter text and image models.

## Features

- FastAPI backend that issues concurrent text and image requests via OpenRouter.
- Tailwind-inspired frontend powered by Alpine.js for interactivity.
- Download/print ready learning packs with provocation image, NZSL prompt, and activity web.
- Structured logging, graceful error handling, and environment-based configuration.

## Prerequisites

- Python 3.11+
- Node.js 18+
- An OpenRouter API key (`OPENROUTER_API_KEY`).

## Quickstart

```bash
make install
cp .env.example .env  # populate with your keys
make dev
```

Visit `http://localhost:8000` to load the interface.

## Testing

```bash
make test
```

## Environment Variables

See `.env.example` for the available configuration options.

## Deployment

- `infra/Dockerfile` builds a production-ready API container.
- `infra/docker-compose.yml` runs the API locally with Docker.
- `infra/vercel.json` configures deployment to Vercel.
