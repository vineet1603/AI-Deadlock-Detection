#!/bin/bash
echo "Starting AI-Powered Deadlock Detection System..."
python3 deadlock_detector/detector.py &
python3 ai_model/model.py &
python3 gui/app.py
