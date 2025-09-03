from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api import router

# Create FastAPI app
app = FastAPI(
    title="Breeze Prompter API",
    description="An AI-powered prompt enhancement service that analyzes and improves prompts for maximum effectiveness",
    version="1.0.0"
)

# Configure CORS for GPT custom actions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "*"],  # Allow ChatGPT and all origins for dev
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
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
- **Document Context**: Supports additional context from documents for more accurate enhancements
- **Scoring System**: Rates prompts on clarity, specificity, and completeness
- **Context-Aware**: Tailors enhancements based on domain (coding, writing, analysis, etc.)
- **Style Options**: Supports different output styles (concise, detailed, technical, conversational)
- **GPT Custom Action Support**: Simplified endpoint for ChatGPT custom actions

## Endpoints

### For GPT Custom Actions
- **POST `/api/gpt-enhance`**: Simplified endpoint that returns only the enhanced prompt
  - Accepts document context for additional information
  - Returns a single enhanced prompt string
  - Perfect for ChatGPT custom actions

### For Full Analysis
- **POST `/api/perfect-prompt`**: Full analysis with scores and explanations

## Authentication
API key required in header: `X-API-Key: your-api-key`

## Usage
For GPT custom actions, use `/api/gpt-enhance` to get just the enhanced prompt.
For full analysis, use `/api/perfect-prompt` to get detailed feedback.
""",
        routes=app.routes,
        servers=[
            {"url": "https://breeze-prompter.onrender.com", "description": "Production server (Render)"},
            {"url": "http://localhost:8000", "description": "Development server"},
            {"url": "http://localhost:8002", "description": "Alternative development server"}
        ]
    )
    
    # Add top-level tags for clearer grouping in GPT Actions
    openapi_schema["tags"] = [
        {"name": "GPT Actions", "description": "Endpoints optimized for ChatGPT Custom Actions"},
        {"name": "Analysis", "description": "Full prompt analysis endpoints"},
        {"name": "System", "description": "Operational and health endpoints"},
    ]

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

    # Enhance operationIds, tags, and add media examples to help GPT Actions
    paths = openapi_schema.get("paths", {})

    # /api/perfect-prompt (POST)
    perfect = paths.get("/api/perfect-prompt", {}).get("post")
    if isinstance(perfect, dict):
        perfect["operationId"] = "perfectPrompt"
        perfect["tags"] = ["Analysis"]
        # Request example
        try:
            media = (
                perfect
                .get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
            )
            if isinstance(media, dict):
                media["example"] = {
                    "prompt": "Write a Python function to reverse a string.",
                    "context": "coding",
                    "style": "detailed",
                    "include_examples": False,
                    "fetch_current_knowledge": False,
                }
        except Exception:
            pass
        # Response example
        try:
            media = (
                perfect
                .get("responses", {})
                .get("200", {})
                .get("content", {})
                .get("application/json", {})
            )
            if isinstance(media, dict):
                media["example"] = {
                    "original_prompt": "Write a Python function to reverse a string.",
                    "enhanced_prompt": "You are a helpful Python assistant. Task: Implement a function reverse_string(s: str) -> str that returns the reversed input string. Requirements: handle empty strings; preserve whitespace and punctuation; include 3 doctest-style examples including an empty string, a single-word string, and a sentence with punctuation.",
                    "improvements": [
                        {
                            "category": "Specificity",
                            "description": "Added explicit function signature and requirements",
                            "before": "",
                            "after": "Implement reverse_string(s: str) -> str",
                        }
                    ],
                    "explanation": "The enhanced prompt clarifies the task, provides a signature, and adds testable examples.",
                    "score_before": {"clarity": 55, "specificity": 40, "completeness": 45, "overall": 47},
                    "score_after": {"clarity": 92, "specificity": 90, "completeness": 88, "overall": 90},
                    "tips": ["State explicit inputs/outputs", "Add constraints and examples"],
                }
        except Exception:
            pass

    # /api/gpt-enhance (POST)
    gpt = paths.get("/api/gpt-enhance", {}).get("post")
    if isinstance(gpt, dict):
        gpt["operationId"] = "gptEnhancePrompt"
        gpt["tags"] = ["GPT Actions"]
        # Request example
        try:
            media = (
                gpt
                .get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
            )
            if isinstance(media, dict):
                media["example"] = {
                    "prompt": "Summarize the attached report for an executive audience.",
                    "document_context": "Report: 2024 Q2 performance...",
                    "context": "analysis",
                    "style": "concise",
                    "fetch_current_info": False,
                }
        except Exception:
            pass
        # Response example
        try:
            media = (
                gpt
                .get("responses", {})
                .get("200", {})
                .get("content", {})
                .get("application/json", {})
            )
            if isinstance(media, dict):
                media["example"] = {
                    "enhanced_prompt": "You are a concise analyst. Task: Summarize the 2024 Q2 performance report for executives. Include: topline revenue and growth vs Q1; key wins/losses; 2-3 risks; 2 actionable recommendations. Keep under 120 words.",
                }
        except Exception:
            pass

    # /api/health (GET)
    health = paths.get("/api/health", {}).get("get")
    if isinstance(health, dict):
        health["operationId"] = "healthCheck"
        health["tags"] = ["System"]
        try:
            media = (
                health
                .get("responses", {})
                .get("200", {})
                .get("content", {})
                .get("application/json", {})
            )
            if isinstance(media, dict):
                media.setdefault("schema", {"type": "object", "properties": {"status": {"type": "string"}, "service": {"type": "string"}}})
                media["example"] = {"status": "healthy", "service": "Breeze Prompter API"}
        except Exception:
            pass

    # / (GET)
    root = paths.get("/", {}).get("get")
    if isinstance(root, dict):
        root["operationId"] = "root"
        root["tags"] = ["System"]
        try:
            media = (
                root
                .get("responses", {})
                .get("200", {})
                .get("content", {})
                .get("application/json", {})
            )
            if isinstance(media, dict):
                media.setdefault(
                    "schema",
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "version": {"type": "string"},
                            "description": {"type": "string"},
                            "documentation": {"type": "string"},
                            "openapi": {"type": "string"},
                        },
                    },
                )
                media["example"] = {
                    "name": "Breeze Prompter API",
                    "version": "1.0.0",
                    "description": "AI-powered prompt enhancement service",
                    "documentation": "/docs",
                    "openapi": "/openapi.json",
                }
        except Exception:
            pass
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)