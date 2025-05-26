# PocketFlow FastAPI Background Job

A minimal example of running PocketFlow workflows as background jobs with real-time progress updates via Server-Sent Events (SSE).

## Features

- Start article generation jobs via REST API
- Real-time granular progress updates via SSE (shows progress for each section)
- Background processing with FastAPI
- Simple three-step workflow: Outline → Content → Style
- Web interface for easy job submission and monitoring

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

3. Run the server:
```bash
python main.py
```

## Usage

### Web Interface (Recommended)

1. Open your browser and go to `http://localhost:8000`
2. Enter an article topic (e.g., "AI Safety", "Climate Change")
3. Click "Generate Article"
4. You'll be redirected to a progress page showing real-time updates
5. The final article will appear when generation is complete

### API Usage

#### Start a Job
```bash
curl -X POST "http://localhost:8000/start-job" -d "topic=AI Safety" -H "Content-Type: application/x-www-form-urlencoded"
```

Response:
```json
{"job_id": "123e4567-e89b-12d3-a456-426614174000", "topic": "AI Safety", "status": "started"}
```

#### Monitor Progress
```bash
curl "http://localhost:8000/progress/123e4567-e89b-12d3-a456-426614174000"
```

SSE Stream:
```
data: {"step": "outline", "progress": 33, "data": {"sections": ["Introduction", "Challenges", "Solutions"]}}
data: {"step": "content", "progress": 44, "data": {"section": "Introduction", "completed_sections": 1, "total_sections": 3}}
data: {"step": "content", "progress": 55, "data": {"section": "Challenges", "completed_sections": 2, "total_sections": 3}}
data: {"step": "content", "progress": 66, "data": {"section": "Solutions", "completed_sections": 3, "total_sections": 3}}
data: {"step": "content", "progress": 66, "data": {"draft_length": 1234, "status": "complete"}}
data: {"step": "complete", "progress": 100, "data": {"final_article": "..."}}
```

## Files

- `main.py` - FastAPI app with background jobs and SSE
- `flow.py` - PocketFlow workflow definition
- `nodes.py` - Workflow nodes (Outline, Content, Style)
- `utils/call_llm.py` - LLM utility function
- `static/index.html` - Main page for starting jobs
- `static/progress.html` - Progress monitoring page with real-time updates 