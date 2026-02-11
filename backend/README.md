# ElevateAI Backend

FastAPI backend for the ElevateAI career enhancement platform.

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update with your credentials:

```env
GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_token
```

### 3. Run Server

```bash
# Development mode (with auto-reload)
python -m uvicorn app.main:app --reload

# Or using the main.py directly
python app/main.py
```

Server will start at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

## API Endpoints

### Analysis

- `POST /api/v1/analyze/complete` - Analyze complete profile
- `GET /api/v1/analyze/github/{username}` - Analyze GitHub only
- `GET /api/v1/analyze/leetcode/{username}` - Analyze LeetCode only
- `GET /api/v1/analyze/health` - Service health check

### Health

- `GET /` - Root endpoint
- `GET /health` - Application health check

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── analysis.py      # Analysis endpoints
│   ├── core/
│   │   └── config.py            # Configuration
│   ├── schemas/
│   │   └── profile.py           # Pydantic models
│   ├── services/
│   │   ├── github_service.py    # GitHub integration
│   │   ├── leetcode_service.py  # LeetCode integration
│   │   └── ai_service.py        # Gemini AI integration
│   └── main.py                  # FastAPI app
├── requirements.txt
└── .env
```

## Testing

```bash
# Test GitHub analysis
curl http://localhost:8000/api/v1/analyze/github/torvalds

# Test LeetCode analysis
curl http://localhost:8000/api/v1/analyze/leetcode/leetcode

# Test complete analysis
curl -X POST http://localhost:8000/api/v1/analyze/complete \
  -H "Content-Type: application/json" \
  -d '{
    "github_username": "torvalds",
    "leetcode_username": "leetcode",
    "target_role": "Senior Software Engineer"
  }'
```

## Development

- Python 3.10+
- FastAPI 0.109.0
- PyGithub for GitHub API
- Gemini AI for recommendations

## License

MIT
