import streamlit as st
import cv2
import time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from ultralytics import YOLO

# =========================================================
# DASHBOARD
# =========================================================

def show_dashboard():

    # =========================================================
    # CSS
    # =========================================================

    st.markdown("""
    <style>

    html, body, [class*="css"]{
        overflow:hidden;
    }

    .block-container{
        padding-top:0.5rem;
        padding-bottom:0rem;
        max-width:100%;
    }

    .main{
        background:#050816;
        color:white;
    }

    .card{
        background:#0b1220;
        border:1px solid #1b2a41;
        border-radius:18px;
        padding:18px;
        height:140px;
    }

    .metric-title{
        color:#9ca3af;
        font-size:14px;
        font-weight:600;
    }

    .metric-value{
        color:white;
        font-size:38px;
        font-weight:800;
    }

    .metric-sub{
        color:#22c55e;
        font-size:14px;
    }

    .section-card{
        background:#0b1220;
        border:1px solid #1b2a41;
        border-radius:18px;
        padding:16px;
    }

    .alert-box{
        background:#1a0f16;
        border-left:5px solid red;
        border-radius:14px;
        padding:14px;
        margin-top:10px;
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # MODEL
    # =========================================================

    model = YOLO("models/yolov8n.pt")

    vehicle_classes = [
        "car",
        "truck",
        "bus",
        "motorcycle"
    ]

    # =========================================================
    # VIDEO
    # =========================================================

    cap = cv2.VideoCapture(
        "videos/traffic_video.mp4"
    )

    if not cap.isOpened():

        st.error("❌ traffic_video.mp4 not found")
        return

    # =========================================================
    # TOP METRICS
    # =========================================================

    m1, m2, m3, m4, m5 = st.columns(5)

    metric_1 = m1.empty()
    metric_2 = m2.empty()
    metric_3 = m3.empty()
    metric_4 = m4.empty()
    metric_5 = m5.empty()

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================================
    # MAIN GRID
    # =========================================================

    left, center, right = st.columns([1.3,1.7,0.8])

    # =========================================================
    # LEFT
    # =========================================================

    with left:

        st.markdown("""
        <div class="section-card">
        <h4>📹 LIVE TRAFFIC CAMERA</h4>
        </div>
        """, unsafe_allow_html=True)

        video_placeholder = st.empty()

        st.markdown("<br>", unsafe_allow_html=True)

        pie_placeholder = st.empty()

    # =========================================================
    # CENTER
    # =========================================================

    with center:

        chart_placeholder = st.empty()

        st.markdown("<br>", unsafe_allow_html=True)

        area_placeholder = st.empty()

        st.markdown("<br>", unsafe_allow_html=True)

        map_placeholder = st.empty()

    # =========================================================
    # RIGHT
    # =========================================================

    with right:

        prediction_placeholder = st.empty()

        alert_placeholder = st.empty()

    # =========================================================
    # HISTORY
    # =========================================================

    history = []

    # =========================================================
    # LOOP
    # =========================================================

    while True:

        ret, frame = cap.read()

        if not ret:

            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            continue

        results = model(frame)

        vehicle_count = 0

        car_count = 0
        bike_count = 0
        bus_count = 0
        truck_count = 0

        # =========================================================
        # DETECTION
        # =========================================================

        for result in results:

            for box in result.boxes:

                cls = int(box.cls[0])

                label = model.names[cls]

                conf = float(box.conf[0])

                if label in vehicle_classes:

                    vehicle_count += 1

                    if label == "car":
                        car_count += 1

                    elif label == "motorcycle":
                        bike_count += 1

                    elif label == "bus":
                        bus_count += 1

                    elif label == "truck":
                        truck_count += 1

                    x1, y1, x2, y2 = map(
                        int,
                        box.xyxy[0]
                    )

                    cv2.rectangle(
                        frame,
                        (x1,y1),
                        (x2,y2),
                        (0,255,255),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"{label} {conf:.2f}",
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255,255,255),
                        2
                    )

        # =========================================================
        # AI VALUES
        # =========================================================

        congestion = min(
            vehicle_count * 3,
            100
        )

        avg_speed = max(
            20,
            80 - vehicle_count
        )

        alerts = np.random.randint(2,15)

        optimized = np.random.randint(90,200)

        # =========================================================
        # METRICS
        # =========================================================

        metric_1.markdown(f"""
        <div class="card">
        <div class="metric-title">TOTAL VEHICLES</div>
        <div class="metric-value">{vehicle_count}</div>
        <div class="metric-sub">↑ 18% from last hour</div>
        </div>
        """, unsafe_allow_html=True)

        metric_2.markdown(f"""
        <div class="card">
        <div class="metric-title">TRAFFIC DENSITY</div>
        <div class="metric-value">{congestion}%</div>
        <div class="metric-sub">High Density</div>
        </div>
        """, unsafe_allow_html=True)

        metric_3.markdown(f"""
        <div class="card">
        <div class="metric-title">AVERAGE SPEED</div>
        <div class="metric-value">{avg_speed}</div>
        <div class="metric-sub">km/h</div>
        </div>
        """, unsafe_allow_html=True)

        metric_4.markdown(f"""
        <div class="card">
        <div class="metric-title">ACTIVE ALERTS</div>
        <div class="metric-value">{alerts}</div>
        <div class="metric-sub">High Priority</div>
        </div>
        """, unsafe_allow_html=True)

        metric_5.markdown(f"""
        <div class="card">
        <div class="metric-title">SIGNALS OPTIMIZED</div>
        <div class="metric-value">{optimized}</div>
        <div class="metric-sub">AI Controlled</div>
        </div>
        """, unsafe_allow_html=True)

        # =========================================================
        # VIDEO FRAME
        # =========================================================

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        video_placeholder.image(
            frame,
            channels="RGB",
            width="stretch"
        )

        # =========================================================
        # HISTORY
        # =========================================================

        history.append(congestion)

        if len(history) > 24:
            history.pop(0)

        # =========================================================
        # TRAFFIC CHART
        # =========================================================

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                y=history,
                mode="lines+markers",
                line=dict(
                    color="#8b5cf6",
                    width=4
                )
            )
        )

        fig.update_layout(
            title="TRAFFIC DENSITY OVER TIME",
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            font_color="white",
            height=320,
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10
            )
        )

        chart_placeholder.plotly_chart(
            fig,
            width="stretch",
            key=f"chart_{time.time()}"
        )

        # =========================================================
        # PIE CHART
        # =========================================================

        pie = go.Figure(
            data=[
                go.Pie(
                    labels=[
                        "Cars",
                        "Bikes",
                        "Buses",
                        "Trucks"
                    ],
                    values=[
                        car_count,
                        bike_count,
                        bus_count,
                        truck_count
                    ],
                    hole=.5
                )
            ]
        )

        pie.update_layout(
            title="TRAFFIC STATUS",
            paper_bgcolor="#0b1220",
            font_color="white",
            height=320
        )

        pie_placeholder.plotly_chart(
            pie,
            width="stretch",
            key=f"pie_{time.time()}"
        )

        # =========================================================
        # AREA SECTION
        # =========================================================

        area_placeholder.markdown(f"""
        <div class="section-card">

        <h4>TOP CONGESTED AREAS</h4>

        <p>1️⃣ Mumbai-Pune Expressway — 85%</p>
        <p>2️⃣ Hinjewadi IT Park — 72%</p>
        <p>3️⃣ Katraj Road — 68%</p>
        <p>4️⃣ Swargate Area — 65%</p>
        <p>5️⃣ Baner Road — 60%</p>

        </div>
        """, unsafe_allow_html=True)

        # =========================================================
        # MAP
        # =========================================================

        map_data = pd.DataFrame({
            "lat": np.random.normal(
                18.5204,
                0.01,
                200
            ),
            "lon": np.random.normal(
                73.8567,
                0.01,
                200
            )
        })

        map_placeholder.map(
            map_data,
            width="stretch"
        )

        # =========================================================
        # AI PREDICTION
        # =========================================================

        prediction_placeholder.markdown(f"""
        <div class="section-card">

        <h3>AI PREDICTION</h3>

        <h1 style='color:red;font-size:58px;'>
        {congestion}%
        </h1>

        <p style='color:#ef4444;'>
        High Congestion
        </p>

        </div>
        """, unsafe_allow_html=True)

        # =========================================================
        # ALERT
        # =========================================================

        alert_placeholder.markdown(f"""
        <div class="alert-box">

        <h4>🚨 AI RECOMMENDATION</h4>

        <p>
        Heavy traffic detected in
        Hinjewadi IT Park.
        Consider alternate routes.
        </p>

        </div>
        """, unsafe_allow_html=True)

        time.sleep(0.03)