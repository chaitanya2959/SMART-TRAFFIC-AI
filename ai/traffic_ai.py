from pathlib import Path
import tempfile
import uuid

import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO

MODEL_PATH = Path("models/yolov8n.pt")
DATA_PATH = Path("data/traffic.csv")
VEHICLE_LABELS = {"car", "truck", "bus", "motorcycle", "bicycle", "van", "train"}
_MODEL_CACHE = None


def get_model() -> YOLO:
    global _MODEL_CACHE

    if _MODEL_CACHE is not None:
        return _MODEL_CACHE

    if MODEL_PATH.exists() and MODEL_PATH.stat().st_size > 0:
        _MODEL_CACHE = YOLO(str(MODEL_PATH))
    else:
        _MODEL_CACHE = YOLO("yolov8n.pt")

    return _MODEL_CACHE


def frame_to_png_bytes(frame: np.ndarray) -> bytes:
    success, encoded = cv2.imencode(".png", frame)

    if not success:
        raise ValueError("Unable to encode the annotated frame.")

    return encoded.tobytes()


def save_temp_upload(uploaded_file) -> Path:
    suffix = Path(uploaded_file.name).suffix or ".tmp"
    temp_path = Path(tempfile.gettempdir()) / f"smart_traffic_ai_{uuid.uuid4().hex}{suffix}"

    with temp_path.open("wb") as buffer:
        buffer.write(uploaded_file.getvalue())

    return temp_path


def detect_vehicles(model: YOLO, frame: np.ndarray):
    results = model(frame, conf=0.35, iou=0.45)
    detection = results[0]

    vehicle_count = 0
    labels = []

    for box in detection.boxes:
        label = detection.names[int(box.cls[0])]

        if label in VEHICLE_LABELS:
            vehicle_count += 1
            labels.append(label)

    annotated = detection.plot()

    return vehicle_count, labels, annotated


def analyze_image(uploaded_file, model: YOLO):
    image_bytes = np.frombuffer(uploaded_file.getvalue(), dtype=np.uint8)
    frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    if frame is None:
        raise ValueError("The uploaded image could not be decoded.")

    vehicle_count, labels, annotated = detect_vehicles(model, frame)

    return {
        "source": "image",
        "vehicle_count": int(vehicle_count),
        "labels": labels,
        "preview": frame_to_png_bytes(annotated),
    }


def analyze_video(uploaded_file, model: YOLO):
    video_path = save_temp_upload(uploaded_file)
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise ValueError("The uploaded video could not be opened.")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        raise ValueError("The uploaded video does not contain readable frames.")

    max_frames = min(8, total_frames)
    sample_indices = np.linspace(0, total_frames - 1, max_frames, dtype=int)

    counts = []
    labels = []
    preview = None

    for frame_idx in sample_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_idx))
        success, frame = cap.read()

        if not success or frame is None:
            continue

        vehicle_count, frame_labels, annotated = detect_vehicles(model, frame)
        counts.append(vehicle_count)
        labels.extend(frame_labels)

        if preview is None:
            preview = frame_to_png_bytes(annotated)

    cap.release()

    if not counts:
        raise ValueError("No valid frames were available for analysis.")

    return {
        "source": "video",
        "vehicle_count": int(round(float(np.mean(counts)))),
        "labels": labels,
        "preview": preview,
    }


def analyze_uploaded_file(uploaded_file, model: YOLO):
    filename = uploaded_file.name.lower()

    if filename.endswith((".png", ".jpg", ".jpeg")):
        return analyze_image(uploaded_file, model)

    if filename.endswith((".mp4", ".avi", ".mov", ".mkv")):
        return analyze_video(uploaded_file, model)

    raise ValueError("Unsupported file type. Upload an image or video file.")


def classify_traffic(vehicle_count: int) -> str:
    if vehicle_count >= 25:
        return "Heavy"

    if vehicle_count >= 10:
        return "Moderate"

    return "Low"


def estimate_congestion(vehicle_count: int) -> int:
    return int(min(100, max(10, round(vehicle_count * 3.5))))


def estimate_speed(vehicle_count: int) -> int:
    return int(max(15, round(90 - vehicle_count * 1.5)))


def build_prediction_record(area: str, source: str, vehicle_count: int, traffic_level: str):
    congestion = estimate_congestion(vehicle_count)
    avg_speed = estimate_speed(vehicle_count)

    return {
        "date": pd.Timestamp.utcnow().strftime("%Y-%m-%d"),
        "area": area.strip() or "Unknown Area",
        "source": source,
        "vehicle_count": int(vehicle_count),
        "traffic": congestion,
        "avg_speed": avg_speed,
        "incidents": 1 if traffic_level == "Heavy" else 0,
        "traffic_level": traffic_level,
    }


def save_prediction_record(record: dict) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DATA_PATH.exists() and DATA_PATH.stat().st_size > 0:
        existing = pd.read_csv(DATA_PATH)
        updated = pd.concat([existing, pd.DataFrame([record])], ignore_index=True)
    else:
        updated = pd.DataFrame([record])

    updated.to_csv(DATA_PATH, index=False)


def load_latest_alerts(limit: int = 5):
    if not DATA_PATH.exists() or DATA_PATH.stat().st_size == 0:
        return []

    try:
        df = pd.read_csv(DATA_PATH)
    except Exception:
        return []

    if df.empty:
        return []

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.sort_values("date", ascending=False, na_position="last")

    return df.head(limit).to_dict("records")
