# FurtherAI SQL Agent

A reference implementation of a conversational AI agent that can reason over multiple data sources and produce SQL for analytics workflows. The project includes a lightweight HTML interface, a FastAPI backend with PostgreSQL persistence, and an OpenAI-powered reasoning loop that can be extended with MCP and tool-calling capabilities.

## Features

- 💬 Conversational UI built with vanilla HTML/CSS/JS
- 🗂️ CRUD APIs for managing conversations and message history
- 🧠 Agent endpoint capable of invoking OpenAI models with configurable reasoning loops
- 🗃️ PostgreSQL persistence layer with automatic table creation
- 🔌 Extensible data-source abstraction supporting PostgreSQL plus stubs for BigQuery, HiveSQL, and MySQL
- ⚙️ Prompt blocks extracted for easy maintenance
- 🔐 Environment configuration managed through `.env`

## Project Structure

```
backend/
  app/
    agents/         # Agent loop and OpenAI integration
    datasources/    # Data-source abstraction
    prompts/        # Prompt templates
    routers/        # FastAPI routers
    services/       # Conversation + agent services
    config.py       # Environment loader
    db.py           # SQLAlchemy session + metadata
    main.py         # FastAPI entry point
    models.py       # SQLAlchemy models
    schemas.py      # Pydantic schemas
  requirements.txt
frontend/
  index.html        # Static single-page UI
```

## Getting Started

### 1. Install dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Required variables:

- `DATABASE_URL`: PostgreSQL connection string (SQLAlchemy format)
- `OPENAI_API_KEY`: API key for the OpenAI capability API
- `OPENAI_MODEL`: Model name (defaults to `gpt-4o-mini`)
- `MAX_REASONING_STEPS`: Maximum thinking loop iterations
- `ALLOW_MCP` / `ALLOW_TOOL_CALLING`: Feature toggles for agent behavior

### 3. Apply database migrations (optional)

The service will automatically create tables on startup. For production deployments consider managing migrations with Alembic.

### 4. Run the backend

```bash
uvicorn app.main:app --reload
```

The server starts on `http://localhost:8000` by default and exposes:

- `GET /health`
- `GET/POST/PATCH/DELETE /api/conversations`
- `POST /api/conversations/{id}/messages`
- `POST /api/agent/ask`

### 5. Open the UI

Serve `frontend/index.html` with any static file server (e.g. `npx serve frontend`) and interact with the agent.

## Extending the Agent

- Prompts live in `backend/app/prompts` to simplify experimentation.
- Additional data-source implementations can extend `BaseDataSource` and be registered in `datasources/factory.py`.
- MCP and tool-calling toggles are surfaced via request payloads and forwarded to the OpenAI client metadata for future customization.

## Database Schema

The backend auto-creates two tables on startup:

- `conversations(id, title, created_at, updated_at)`
- `messages(id, conversation_id, role, content, metadata, created_at)`

## License

MIT
