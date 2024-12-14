# Workflow Automation Backend

This FastAPI-based backend service provides an API for executing LLM-based workflow tasks. It's designed to be deployed on Railway and can be easily extended with additional functionality.

## Features

- FastAPI-based REST API
- Endpoint for executing LLM tasks
- Input validation using Pydantic models
- Docker containerization
- Railway deployment configuration

## Setup

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/fsilva7456/workflow-alpha.git
cd workflow-alpha
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Railway Deployment

1. Install the Railway CLI:
```bash
npm i -g @railway/cli
```

2. Login to Railway:
```bash
railway login
```

3. Link your project:
```bash
railway link
```

4. Deploy the application:
```bash
railway up
```

## API Documentation

After starting the server, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Execute LLM Endpoint

**POST** `/api/v1/execute-llm`

Request body:
```json
{
    "prompt": "Your input prompt",
    "model": "Claude",
    "parameters": {
        "temperature": 0.7,
        "max_tokens": 1000
    }
}
```

Response:
```json
{
    "response": "LLM response text"
}
```

## Directory Structure

```
/workflow-alpha
├── /app
│   ├── __init__.py
│   ├── main.py
│   ├── /routes
│   │   ├── __init__.py
│   │   ├── llm.py
│   ├── /services
│   │   ├── __init__.py
│   │   ├── llm_service.py
├── requirements.txt
├── Dockerfile
├── railway.json
├── .env.example
├── README.md
```

## Future Improvements

- Integration with actual LLM APIs (OpenAI, Anthropic)
- Authentication and rate limiting
- Request/response logging
- Error tracking
- Monitoring and analytics