import streamlit as st
import cv2
from ultralytics import YOLO
import pandas as pd
import time

# ---------------- PAGE ----------------

def show_alerts():

    st.title("🚨 LIVE AI TRAFFIC ALERT SYSTEM")

    st.caption(
        "Real-time smart traffic monitoring & emergency alerts"
    )

    st.markdown("---")

    # ---------------- LOAD AI MODEL ----------------

    model = YOLO("models/yolov8n.pt")

    # ---------------- VIDEO ----------------

    video_path = "Videos/traffic_video.mp4"

    cap = cv2.VideoCapture(video_path)

    # ---------------- PLACEHOLDERS ----------------

    frame_placeholder = st.empty()

    alert_placeholder = st.empty()

    metric_placeholder = st.empty()

    chart_placeholder = st.empty()

    # ---------------- HISTORY ----------------

    traffic_history = []

    # ---------------- CLASSES ----------------

    vehicle_classes = [
        "car",
        "truck",
        "bus",
        "motorcycle"
    ]

    human_classes = [
        "person"
    ]

    # ---------------- LOOP ----------------

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        # ---------------- YOLO ----------------

        results = model(frame)

        vehicle_count = 0

        human_count = 0

        for result in results:

            boxes = result.boxes

            for box in boxes:

                cls = int(box.cls[0])

                label = model.names[cls]

                confidence = float(box.conf[0])

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                # ---------------- VEHICLES ----------------

                if label in vehicle_classes:

                    vehicle_count += 1

                    color = (0,255,0)

                # ---------------- HUMANS ----------------

                elif label in human_classes:

                    human_count += 1

                    color = (255,0,0)

                else:

                    continue

                # ---------------- DRAW ----------------

                cv2.rectangle(
                    frame,
                    (x1,y1),
                    (x2,y2),
                    color,
                    2
                )

                cv2.putText(
                    frame,
                    f"{label} {confidence:.2f}",
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )

        # ---------------- AI ALERT ENGINE ----------------

        total_density = vehicle_count + human_count

        if total_density > 50:

            alert_level = "🔴 HIGH ALERT"

            alert_message = (
                "Heavy congestion detected"
            )

            signal = "RED"

        elif total_density > 25:

            alert_level = "🟠 MEDIUM ALERT"

            alert_message = (
                "Traffic increasing rapidly"
            )

            signal = "YELLOW"

        else:

            alert_level = "🟢 NORMAL"

            alert_message = (
                "Traffic flow stable"
            )

            signal = "GREEN"

        # ---------------- HISTORY ----------------

        traffic_history.append(total_density)

        if len(traffic_history) > 20:

            traffic_history.pop(0)

        # ---------------- METRICS ----------------

        with metric_placeholder.container():

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "🚗 Vehicles",
                vehicle_count
            )

            col2.metric(
                "🧍 Humans",
                human_count
            )

            col3.metric(
                "🚦 Density",
                total_density
            )

            col4.metric(
                "🚨 Alert",
                signal
            )

        # ---------------- ALERT BOX ----------------

        with alert_placeholder.container():

            if total_density > 50:

                st.error(
                    f"""
🚨 {alert_level}

{alert_message}

⚠️ AI recommends alternate route immediately
"""
                )

            elif total_density > 25:

                st.warning(
                    f"""
⚠️ {alert_level}

{alert_message}

🚦 Smart signals activated
"""
                )

            else:

                st.success(
                    f"""
✅ {alert_level}

{alert_message}

🚗 Traffic moving smoothly
"""
                )

        # ---------------- LIVE CHART ----------------

        chart_data = pd.DataFrame({

            "Traffic Density": traffic_history

        })

        chart_placeholder.line_chart(
            chart_data,
            use_container_width=True
        )

        # ---------------- FRAME ----------------

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame_placeholder.image(
            frame,
            channels="RGB",
            use_container_width=True
        )

        time.sleep(0.03)

    cap.release()

    st.success(
        "✅ AI Alert Monitoring Completed"
    )