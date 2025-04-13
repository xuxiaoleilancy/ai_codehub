@echo off
echo Starting AI CodeHub application...
set PYTHONPATH=.
set AI_CODEHUB_HOST=localhost
set AI_CODEHUB_PORT=8000
python -c "from config.config import settings; print(f'Starting server on {settings.HOST}:{settings.PORT}')"
python -m uvicorn src.main:app --reload --host localhost --port 8000 