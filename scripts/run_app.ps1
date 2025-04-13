# 启动FastAPI应用程序
Write-Output "Starting AI CodeHub application..."
$env:PYTHONPATH = "."
$env:AI_CODEHUB_HOST = "localhost"
$env:AI_CODEHUB_PORT = "8000"
python -c "from config.config import settings; print(f'Starting server on {settings.HOST}:{settings.PORT}')"
python -m uvicorn src.main:app --reload --host localhost --port 8000 