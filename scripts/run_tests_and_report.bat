@echo off
echo Running environment and GPU tests...
python -m pytest tests/test_environment.py tests/test_gpu_environment.py -v

if %ERRORLEVEL% NEQ 0 (
    echo Error: Tests failed!
    exit /b %ERRORLEVEL%
)

echo.
echo Generating HTML report...
python scripts/generate_report.py

if %ERRORLEVEL% NEQ 0 (
    echo Error: Report generation failed!
    exit /b %ERRORLEVEL%
)

echo.
echo All done! Check the reports directory for test results. 