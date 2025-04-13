# 设置环境变量
$env:PYTHONPATH = "."

# 启动应用
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 