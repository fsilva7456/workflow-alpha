# Workflow Automation Backend

This FastAPI-based backend service provides an API for executing LLM-based workflow tasks. It's designed to be deployed on Railway and can be easily extended with additional functionality.

## Features

- FastAPI-based REST API with input validation
- Endpoint for executing LLM tasks
- Health check endpoint
- Comprehensive logging
- Docker containerization
- Railway deployment configuration

## Testing the Live API

The API is deployed and can be tested using the following endpoints:

### Health Check

```bash
curl https://your-railway-url/api/v1/health-check
```

Expected response:
```json
{
    "status": "ok"
}
```

### Execute LLM Task

```bash
curl -X POST https://your-railway-url/api/v1/execute-llm \
     -H "Content-Type: application/json" \
     -d '{
         "prompt": "Write a short story about a robot",
         "model": "claude",
         "parameters": {
             "temperature": 0.7,
             "max_tokens": 1000
         }
     }'
```

Expected response:
```json
{
    "response": "Mock response from claude: Based on your prompt 'Write a short story about a robot', here is a simulated response."
}
```

### Error Handling Examples

1. Invalid model:
```bash
curl -X POST https://your-railway-url/api/v1/execute-llm \
     -H "Content-Type: application/json" \
     -d '{
         "prompt": "Test prompt",
         "model": "invalid-model",
         "parameters": {}
     }'
```

2. Empty prompt:
```bash
curl -X POST https://your-railway-url/api/v1/execute-llm \
     -H "Content-Type: application/json" \
     -d '{
         "prompt": "",
         "model": "claude",
         "parameters": {}
     }'
```

## Local Development

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

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

After starting the server, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Validation Steps

1. Verify the service is running:
```bash
curl https://your-railway-url/api/v1/health-check
```

2. Test input validation:
```bash
# Test with valid input
curl -X POST https://your-railway-url/api/v1/execute-llm \
     -H "Content-Type: application/json" \
     -d '{
         "prompt": "Test prompt",
         "model": "claude",
         "parameters": {}
     }'

# Test with invalid model
curl -X POST https://your-railway-url/api/v1/execute-llm \
     -H "Content-Type: application/json" \
     -d '{
         "prompt": "Test prompt",
         "model": "invalid-model",
         "parameters": {}
     }'
```

3. Check logs in Railway dashboard for request tracking

## Error Codes

- 200: Successful request
- 400: Bad request (invalid input)
- 500: Internal server error

## Deployment

The application is configured for automatic deployment on Railway. Any push to the main branch will trigger a new deployment.

To deploy manually:

```bash
railway up
```

## Environment Variables

- `PORT`: Port number (default: 8000)
- `ENVIRONMENT`: Runtime environment (development/production)
