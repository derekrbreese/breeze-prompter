# Breese Prompter - AI Prompt Enhancement API

An AI-powered service that analyzes and enhances prompts to make them more effective for AI systems. Perfect for use as a custom GPT action.

## Features

- **Prompt Analysis**: Identifies ambiguities, missing information, and improvement opportunities
- **Smart Enhancement**: Generates optimized versions with better clarity and specificity
- **Scoring System**: Rates prompts on clarity, specificity, and completeness (0-100)
- **Context-Aware**: Tailors enhancements based on domain (coding, writing, analysis, etc.)
- **Style Options**: Supports different output styles (concise, detailed, technical, conversational)
- **GPT-Ready**: Includes OpenAPI spec for easy integration as a ChatGPT custom action

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your OpenRouter API key:

```bash
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

Get your API key from [OpenRouter](https://openrouter.ai/keys)

### 3. Run the Server

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Interactive docs: `http://localhost:8000/docs`
- OpenAPI schema: `http://localhost:8000/openapi.json`

## Using as a GPT Custom Action

1. Deploy the API to a public server (Vercel, Railway, Render, etc.)
2. In ChatGPT, create a new GPT or edit an existing one
3. Go to "Actions" and click "Create new action"
4. Import the OpenAPI schema from `https://your-api-url/openapi.json`
5. Configure authentication if needed
6. Test the action with sample prompts

## API Endpoints

### POST /api/perfect-prompt

Enhance a prompt to make it more effective.

**Request Body:**
```json
{
  "prompt": "write code for sorting",
  "context": "coding",
  "style": "detailed",
  "include_examples": false
}
```

**Response:**
```json
{
  "original_prompt": "write code for sorting",
  "enhanced_prompt": "Write a Python function that implements the quicksort algorithm...",
  "improvements": [...],
  "explanation": "The enhanced version adds specificity...",
  "score_before": {"clarity": 40, "specificity": 30, ...},
  "score_after": {"clarity": 95, "specificity": 90, ...},
  "tips": ["Always specify the programming language", ...]
}
```

## Context Options

- `coding` - For programming and technical prompts
- `writing` - For creative and content writing
- `analysis` - For data analysis and research
- `creative` - For creative tasks
- `technical` - For technical documentation
- `general` - Default, for any type of prompt

## Style Options

- `concise` - Brief and to the point
- `detailed` - Comprehensive with full context
- `technical` - Technical language and terminology
- `conversational` - Natural, friendly tone

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Project Structure

```
breese-prompter/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── services/
│   │   └── prompt_enhancer.py  # Core enhancement logic
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   └── utils/
│       └── openrouter.py    # OpenRouter API client
├── requirements.txt
├── .env
└── README.md
```

## Deployment

### Render (Recommended)

1. Fork/clone this repository to your GitHub account
2. Connect your GitHub account to Render
3. Create a new Web Service on Render
4. Connect your repository
5. Render will auto-detect the `render.yaml` configuration
6. Add your `OPENROUTER_API_KEY` in the Environment Variables section
7. Deploy!

The service will be available at: `https://your-service-name.onrender.com`

### Manual Render Setup

If not using `render.yaml`:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**: Add `OPENROUTER_API_KEY`

### Railway

1. Connect your GitHub repo to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

### Heroku

1. Install Heroku CLI
2. Create app: `heroku create your-app-name`
3. Set config: `heroku config:set OPENROUTER_API_KEY=your-key`
4. Deploy: `git push heroku main`

## License

MIT