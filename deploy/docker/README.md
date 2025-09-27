# Docker Deployment

This directory contains a reference Docker Compose stack for running the FurtherAI SQL Agent, including:

- **PostgreSQL** for conversation storage
- **FastAPI backend** serving the API and agent endpoints
- **Nginx frontend** that hosts the static UI and proxies `/api` traffic to the backend

## Prerequisites

- [Docker Engine](https://docs.docker.com/engine/install/) 20.10+
- [Docker Compose](https://docs.docker.com/compose/install/) V2 (usually bundled with modern Docker Desktop / CLI)

## Quick start

1. Copy the example environment file and edit it to suit your environment:

   ```bash
   cp .env.example .env
   # update .env with your OPENAI_API_KEY, etc.
   ```

2. Build and launch the stack:

   ```bash
   docker compose up --build
   ```

   The command exposes:

   - Frontend UI on [http://localhost:8080](http://localhost:8080)
   - Backend API on [http://localhost:8000](http://localhost:8000)

3. (Optional) Run the services in the background:

   ```bash
   docker compose up --build -d
   ```

4. Tear everything down (containers + named volume):

   ```bash
   docker compose down -v
   ```

## Notes

- The backend automatically runs database migrations via SQLAlchemy metadata creation at startup.
- The default database credentials are intended for local development only. Update them before deploying to production.
- To adjust the OpenAI model or reasoning parameters, edit the values in `.env` or override them when running `docker compose`.
