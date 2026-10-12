# AI Music Lab — Python backend starter

This project keeps the existing single-file HTML interface and adds a modular FastAPI backend.

## Implemented in this version

- `GET /health` and compatibility endpoint `GET /api/health`
- `POST /api/v1/prompts/build`: validated, rule-based prompt construction
- `POST /api/v1/prompts/enhance`: honest offline fallback (normalizes whitespace; not an AI model)
- `POST /api/v1/music/generations`: returns a structured `503` until a real music provider is configured
- `POST /api/separate`: validates audio uploads and invokes the Demucs CLI if installed
- Pytest tests for health, prompt building, validation, fallback transparency, and unconfigured generation
- Existing frontend copied to `frontend/index.html`; served at `/ui/`

## Windows setup

Use Python 3.11 or 3.12.

From the project root in PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
Copy-Item .env.example .env
```

Run the backend from the project root:

```powershell
python -m uvicorn app.main:app --app-dir backend --reload
```

Open:
- Frontend: http://127.0.0.1:8000/ui/
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

Run tests:

```powershell
$env:PYTHONPATH = "backend"
python -m pytest backend\tests -q
```

Or use the included `run_dev.bat` after creating `.venv` at the project root and installing dependencies.

## API example

```powershell
$body = @{
  mode = "instrumental"
  idea = "A peaceful fantasy landscape that gradually becomes emotional"
  genre = "cinematic orchestral"
  mood = @("peaceful", "emotional")
  instruments = @("piano", "strings")
  tempo_bpm = 85
  structure = @("soft intro", "gradual build", "emotional climax", "gentle ending")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/prompts/build" -Method Post -ContentType "application/json" -Body $body
```

## Audio separation (optional dependency)

The API does not pretend to separate audio unless the `demucs` command exists and returns real output. Demucs and its audio dependencies can be heavy and may have platform/Python compatibility constraints. Install and test it separately in a compatible environment before using `/api/separate`. CPU processing can be slow. The endpoint currently processes synchronously with a 30-minute timeout; production should move this work to a task queue/worker and use persistent job IDs.

Upload limit defaults to 100 MB and can be changed with `MAX_AUDIO_UPLOAD_MB`. Supported filename extensions are MP3, WAV, FLAC, M4A, OGG, AAC. File extension alone does not guarantee that the codec is readable.

## Important honest limitations

- Prompt building is template/rule-based, not a language model.
- No real music-generation provider is configured; no fake audio or fake job IDs are returned.
- Audio separation only works if Demucs is installed and verified.
- Karaoke recording in the provided HTML runs locally in the browser. It is not an online account or multiplayer system.
- Battle Arena is a preview, not a live competition.
- This is a local development baseline, not a public production deployment. Before deployment add authentication, rate limits, persistent job tracking, quotas, file retention policies, monitoring, and security review.

## Project layout

```text
ai_music_lab/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/config.py
│   │   ├── schemas/prompts.py
│   │   ├── services/prompt_builder.py
│   │   ├── services/prompt_enhancer.py
│   │   ├── services/audio_processor.py
│   │   └── api/routes/{health,prompts,music,audio}.py
│   ├── tests/
│   └── requirements.txt
├── frontend/index.html
├── storage/{uploads,outputs}/
├── .env.example
├── .gitignore
└── README.md
```
