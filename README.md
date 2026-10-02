# CodeLumen AI

CodeLumen AI is an AI-assisted developer workspace for understanding, debugging, and improving source code. Paste a snippet or upload a supported source file and get actionable analysis with line-level findings, quality signals, and suggested fixes.

The project includes a FastAPI backend and a dependency-light static frontend. The default analysis engine runs locally with rule-based checks, so the core workflow does not require an API key or an external model.

## What it does

- **Explain** code in plain English, including language detection, structure, complexity, functions, and classes.
- **Debug** common problems with static-analysis patterns, exact line references, snippets, and fix suggestions.
- **Improve** code quality with recommendations for documentation, error handling, type safety, and testing.
- **Analyze** runs the explanation, debugging, and improvement workflows together and returns a combined quality score.
- **Chat** provides an assistant-style interaction with the analysis service.
- **Upload** accepts supported source files and ZIP archives for analysis.
- **History and user workflows** include authentication, saved entries, sharing, collaboration, subscriptions, and administrative observability routes where enabled.

Supported source languages include Python, JavaScript, TypeScript, Java, and C++.

## Architecture

```text
frontend/index.html       Static browser application
        |
        | HTTP / WebSocket
        v
backend/app/main.py       FastAPI application
        |
        +-- routers          Analysis, chat, auth, history, sharing, and admin flows
        +-- services          Static analysis, caching, LLM integration, and persistence
        +-- tests             Backend unit and integration tests
```

## Quick start

### Requirements

- Python 3.11 or newer
- Node.js 18 or newer for frontend tests
- npm

### 1. Clone and enter the project

```bash
git clone https://github.com/Adityagola003/CodeLumen.git
cd CodeLumen/AI-dev-assistant
```

### 2. Create a Python environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 3. Start the API

From the repository root:

```bash
uvicorn app.main:app --app-dir backend --reload
```

The API is available at `http://localhost:8000`.

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

### 4. Open the frontend

The frontend is a static HTML application. Serve it from a second terminal so browser requests work consistently:

```bash
python -m http.server 5500 --directory frontend
```

Open `http://localhost:5500` and use `http://localhost:8000` as the API URL if it is not already selected.

## API examples

The interactive OpenAPI documentation at `/docs` is the authoritative reference for request and response schemas. A basic full analysis request looks like this:

```bash
curl -X POST http://localhost:8000/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a, b):\n    return a + b",
    "language": "python"
  }'
```

Core routes include:

| Route | Purpose |
| --- | --- |
| `GET /health` | Service health check |
| `GET /ping` | Lightweight availability check |
| `POST /explanation/` | Explain code and identify its structure |
| `POST /debugging/` | Find likely bugs and return line-level findings |
| `POST /suggestions/` | Return improvement recommendations and quality signals |
| `POST /analyze/` | Run the combined analysis workflow |
| `POST /analyze/zip/` | Analyze supported files from a ZIP archive |
| `POST /chat/` | Chat with the assistant service |

Analysis endpoints are rate limited per IP. Responses include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-Process-Time-Ms`, and `X-CodeLumen-Version` headers. The default limit is 30 analysis requests per minute.

## Configuration

Create a `.env` file in the project root when you need to override defaults. Do not commit secrets; `.env` is already excluded by `.gitignore`.

Common settings:

```dotenv
# Analysis and limits
AI_PROVIDER=rule-based
MAX_CODE_CHARS=20000
MAX_REQUEST_BYTES=1048576
RATE_LIMIT_PER_MINUTE=30

# Cache
CACHE_ENABLED=true
CACHE_TTL_SECONDS=300
CACHE_MAX_ENTRIES=100

# Optional LLM support
LLM_ENABLED=false
LLM_PROVIDER=openai-compatible
LLM_API_KEY=
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=https://api.openai.com/v1

# Application security and persistence
JWT_SECRET=replace-with-a-long-random-secret
DATABASE_URL=sqlite:///./assistant.db
ENABLE_DOCS=false
TRUST_PROXY_HEADERS=false
```

LLM support is optional. With `LLM_ENABLED=false`, the local rule-based engine remains the default. Ollama and other OpenAI-compatible providers can be configured through `LLM_PROVIDER`, `LLM_BASE_URL`, `LLM_MODEL`, and the corresponding API key settings.

For production deployments, set a strong `JWT_SECRET`, review CORS and proxy settings, use a production database, and keep API documentation disabled unless it is intentionally exposed.

## Running tests

### Backend

From the repository root:

```bash
pytest
```

Useful focused commands:

```bash
pytest backend/tests/test_python_ast_analyzer.py
pytest backend/tests/test_auth_endpoints.py
pytest tests/test_api_integration.py
```

Formatting and import checks:

```bash
black --check backend tests
isort --check-only backend tests
```

### Frontend

Install the frontend test dependencies:

```bash
cd frontend
npm install
npx playwright install
```

Run static tests:

```bash
npm run test:static
```

Run Playwright end-to-end tests:

```bash
npm run test:e2e
```

The end-to-end suite expects the API and static frontend to be running locally. Use `npm run test:e2e:headed` when you need to inspect the browser session.

## Project layout

```text
backend/
  app/
    routers/       API route modules
    services/      Analysis, cache, AI, and supporting services
    utils/         Upload and validation helpers
  tests/           Backend test suite
frontend/
  index.html       Main browser application
  css/             Syntax styling
  js/              Syntax highlighting
  tests/           Static and Playwright tests
tests/              Cross-project integration tests
```

## Security notes

- Never commit `.env`, API keys, JWT secrets, database files, or production logs.
- Uploaded files are validated by extension, size, and archive safeguards before analysis.
- Keep `TRUST_PROXY_HEADERS=false` unless the application is behind a trusted proxy that sets those headers correctly.
- The default JWT secret is for development only and must be replaced in any deployed environment.
- Review the configured CORS policy before exposing the API beyond local development.

## Contributing

1. Create a focused branch from `main`.
2. Make the smallest change that addresses the issue.
3. Add or update tests for behavior changes.
4. Run the relevant backend and frontend checks.
5. Open a pull request with a concise description of the change and verification performed.

## License

The backend declares an MIT license in its FastAPI metadata. Confirm the repository's intended licensing terms before redistributing or deploying the project.
