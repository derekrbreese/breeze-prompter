from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api import router

# Create FastAPI app
app = FastAPI(
    title="Breeze Prompter API",
    description="An AI-powered prompt enhancement service that analyzes and improves prompts for maximum effectiveness",
    version="1.0.0",
    servers=[
        {"url": "https://breeze-prompter.onrender.com", "description": "Production server"},
        {"url": "http://localhost:8000", "description": "Development server"}
    ]
)

# Configure CORS for GPT custom actions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "*"],  # Allow ChatGPT and all origins for dev
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "Breeze Prompter API",
        "version": "1.0.0",
        "description": "AI-powered prompt enhancement service",
        "documentation": "/docs",
        "openapi": "/openapi.json"
    }

# Custom OpenAPI schema for GPT
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Breeze Prompter API",
        version="1.0.0",
        description="""
# Breeze Prompter API

An AI-powered service that analyzes and enhances prompts to make them more effective for AI systems.

## Features
- **Prompt Analysis**: Identifies ambiguities, missing information, and areas for improvement
- **Smart Enhancement**: Generates optimized versions with better clarity and specificity
- **Scoring System**: Rates prompts on clarity, specificity, and completeness
- **Context-Aware**: Tailors enhancements based on domain (coding, writing, analysis, etc.)
- **Style Options**: Supports different output styles (concise, detailed, technical, conversational)

## Authentication
API key required in header: `X-API-Key: your-api-key`

## Usage
Send a POST request to `/api/perfect-prompt` with your prompt and optional parameters.
""",
        routes=app.routes,
    )
    
    # Add security scheme for GPT custom actions
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }
    
    # Apply security to all endpoints
    for path in openapi_schema.get("paths", {}).values():
        for operation in path.values():
            if isinstance(operation, dict):
                operation["security"] = [{"ApiKeyAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)