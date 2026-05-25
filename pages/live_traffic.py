import cv2
import streamlit as st
import pandas as pd
from ultralytics import YOLO

# ---------------- PAGE ----------------

def show_live_traffic():

    st.title("📹 LIVE TRAFFIC AI DETECTION")

    st.markdown("### 🚦 Smart AI CCTV Monitoring System")

    # ---------------- LOAD MODEL ----------------

    model = YOLO("models/yolov8n.pt")

    # ---------------- DEFAULT VIDEO ----------------

    video_path = "videos/traffic_video.mp4"

    cap = cv2.VideoCapture(video_path)

    frame_placeholder = st.empty()

    # ---------------- METRIC PLACEHOLDERS ----------------

    metric_placeholder = st.empty()

    # ---------------- CLASS LIST ----------------

    vehicle_classes = [
        "car",
        "truck",
        "bus",
        "motorcycle",
        "bicycle"
    ]

    human_classes = [
        "person"
    ]

    animal_classes = [
        "dog",
        "cat",
        "cow",
        "horse"
    ]

    substance_classes = [
        "backpack",
        "suitcase",
        "handbag",
        "bottle"
    ]

    # ---------------- DETECTION LOOP ----------------

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        # Resize for smooth display
        frame = cv2.resize(frame, (1000, 600))

        # ---------------- YOLO DETECTION ----------------

        results = model(frame)

        vehicle_count = 0
        human_count = 0
        animal_count = 0
        substance_count = 0

        for result in results:

            boxes = result.boxes

            for box in boxes:

                cls = int(box.cls[0])

                confidence = float(box.conf[0])

                label = model.names[cls]

                # Skip low confidence
                if confidence < 0.40:
                    continue

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                # ---------------- VEHICLE ----------------

                if label in vehicle_classes:

                    vehicle_count += 1
                    color = (0, 255, 0)

                # ---------------- HUMAN ----------------

                elif label in human_classes:

                    human_count += 1
                    color = (255, 0, 0)

                # ---------------- ANIMAL ----------------

                elif label in animal_classes:

                    animal_count += 1
                    color = (0, 0, 255)

                # ---------------- SUBSTANCE ----------------

                elif label in substance_classes:

                    substance_count += 1
                    color = (255, 255, 0)

                else:
                    continue

                # ---------------- DRAW BOX ----------------

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    color,
                    2
                )

                # ---------------- LABEL ----------------

                text = f"{label} {confidence:.2f}"

                cv2.putText(
                    frame,
                    text,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )

        # ---------------- TRAFFIC ANALYSIS ----------------

        total_traffic = vehicle_count + human_count

        traffic_status = "🟢 LOW"

        if total_traffic > 20:
            traffic_status = "🔴 HEAVY"

        elif total_traffic > 10:
            traffic_status = "🟠 MEDIUM"

        # ---------------- ALERTS ----------------

        alert = "✅ Normal Traffic"

        if animal_count > 0:
            alert = "⚠️ Animal Detected On Road"

        if substance_count > 0:
            alert = "⚠️ Suspicious Object Detected"

        if total_traffic > 20:
            alert = "🚨 Heavy Traffic Congestion"

        # ---------------- METRICS ----------------

        with metric_placeholder.container():

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "🚗 Vehicles",
                vehicle_count
            )

            col2.metric(
                "🧍 Humans",
                human_count
            )

            col3.metric(
                "🐶 Animals",
                animal_count
            )

            col4, col5, col6 = st.columns(3)

            col4.metric(
                "📦 Objects",
                substance_count
            )

            col5.metric(
                "🚦 Traffic",
                traffic_status
            )

            col6.metric(
                "🚨 Alert",
                alert
            )

        # ---------------- FRAME DISPLAY ----------------

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame_placeholder.image(
            frame,
            channels="RGB",
            use_container_width=True
        )

    cap.release()

    # ---------------- AI FEATURES ----------------

    st.markdown("---")

    st.subheader("🚦 Smart Traffic AI Features")

    st.success("✅ Live CCTV Vehicle Detection")

    st.success("✅ Human Detection")

    st.success("✅ Animal Detection")

    st.success("✅ Suspicious Object Detection")

    st.success("✅ Smart Traffic Density Analysis")

    st.success("✅ Congestion Monitoring")

    st.success("✅ Accident Risk Alerts")

    st.success("✅ AI Based Smart Surveillance")