# AI-Based Intrusion Detection & Cybersecurity Monitoring System Runner
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  Starting AI-Based Intrusion Detection & Cybersecurity Platform" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Directory: $PSScriptRoot`n" -ForegroundColor DarkGray

# 1. Check Python virtual environment
$pythonExe = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    Write-Host "[ERROR] Virtual environment (.venv) not found at $pythonExe!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# 2. Check models
$modelFile = Join-Path $PSScriptRoot "ml\models\xgb_model.joblib"
if (-not (Test-Path $modelFile)) {
    Write-Host "[*] Training ML models (XGBoost + Isolation Forest)..." -ForegroundColor Yellow
    & $pythonExe "ml\train.py"
}

# 3. Launch FastAPI Backend
Write-Host "[*] Launching FastAPI Backend on http://localhost:8000..." -ForegroundColor Green
Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-Command",
    "`$host.UI.RawUI.WindowTitle = 'AI-IDS Backend'; Set-Location '$PSScriptRoot'; `$env:PYTHONPATH='backend;.'; & '$pythonExe' -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
)

# 4. Launch Traffic Replay Producer
Write-Host "[*] Launching Traffic Replayer Producer..." -ForegroundColor Green
Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-Command",
    "`$host.UI.RawUI.WindowTitle = 'AI-IDS Traffic Producer'; Set-Location '$PSScriptRoot'; `$env:PYTHONPATH='backend;.'; & '$pythonExe' producer\replay_traffic.py"
)

# 5. Launch Next.js SOC Dashboard
Write-Host "[*] Launching Next.js 14 SOC Dashboard on http://localhost:3000..." -ForegroundColor Green
$frontendDir = Join-Path $PSScriptRoot "frontend"
Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-Command",
    "`$host.UI.RawUI.WindowTitle = 'AI-IDS Frontend'; Set-Location '$frontendDir'; node ./node_modules/next/dist/bin/next dev -p 3000"
)

Write-Host "`n======================================================================" -ForegroundColor Cyan
Write-Host "  All services launched in separate windows!" -ForegroundColor Green
Write-Host "  - SOC Dashboard : http://localhost:3000" -ForegroundColor White
Write-Host "  - Backend API   : http://localhost:8000" -ForegroundColor White
Write-Host "  - API Swagger   : http://localhost:8000/docs" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Keep the spawned terminal windows open while testing." -ForegroundColor Yellow
Start-Sleep -Seconds 3
