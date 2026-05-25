# SMART TRAFFIC AI

A Streamlit-based AI traffic monitoring dashboard that uses Ultralytics YOLOv8 to estimate traffic density from uploaded images and videos, then saves results for reports and alerts.

## Features

- Live dashboard with map-based traffic indicators
- AI-powered traffic prediction using image and video uploads
- Alerts page driven by saved predictions
- Reports page with summary KPIs, charts, and CSV export

## Setup

1. Create and activate a virtual environment
2. Install dependencies
3. Run the app

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## How it works

- The prediction page accepts PNG, JPG, JPEG, MP4, AVI, MOV, and MKV files.
- The AI model analyzes the uploaded media and estimates:
  - detected vehicles
  - traffic level (Low, Moderate, Heavy)
  - congestion percentage
  - average speed
- Results are saved to `data/traffic.csv` and can be viewed in Reports and Alerts.

## Notes

- If `models/yolov8n.pt` is missing or empty, the app will download `yolov8n.pt` automatically on first run.
- For best results, use clear traffic images/videos with visible vehicles.
