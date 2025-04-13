# Create scripts directory if it doesn't exist
$scriptsDir = Join-Path $PSScriptRoot ".."
if (-not (Test-Path $scriptsDir)) {
    New-Item -ItemType Directory -Force -Path $scriptsDir
}

Write-Host "Running environment and GPU tests..." -ForegroundColor Green
python -m pytest tests/test_environment.py tests/test_gpu_environment.py -v

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Tests failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "`nGenerating HTML report..." -ForegroundColor Green
python scripts/generate_report.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Report generation failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "`nAll done! Check the reports directory for test results." -ForegroundColor Green 