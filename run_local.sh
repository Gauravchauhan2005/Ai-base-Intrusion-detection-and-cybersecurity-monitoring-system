#!/usr/bin/env bash
set -e

echo "======================================================================"
echo "  Starting AI-Based Intrusion Detection & Cybersecurity Platform"
echo "======================================================================"

# 1. Train models if missing
if [ ! -f "ml/models/xgb_model.joblib" ]; then
    echo "[*] Training ML models (XGBoost + Isolation Forest)..."
    python3 ml/train.py
fi

# 2. Launch backend
echo "[*] Launching FastAPI Backend on http://localhost:8000..."
PYTHONPATH=backend:. python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# 3. Launch producer
echo "[*] Launching Traffic Replay Producer..."
PYTHONPATH=backend:. python3 producer/replay_traffic.py &
PRODUCER_PID=$!

# 4. Launch Next.js Dashboard
echo "[*] Launching Next.js 14 SOC Dashboard on http://localhost:3000..."
cd frontend && npm run dev -- -p 3000 &
FRONTEND_PID=$!

echo "======================================================================"
echo "  System running!"
echo "  - SOC Dashboard : http://localhost:3000"
echo "  - Backend API   : http://localhost:8000"
echo "  - API Swagger   : http://localhost:8000/docs"
echo "======================================================================"

trap "kill $BACKEND_PID $PRODUCER_PID $FRONTEND_PID" EXIT
wait
