@echo off
REM 设置环境变量
set PYTHONPATH=.

REM 启动应用
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 