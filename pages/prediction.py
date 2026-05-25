import streamlit as st
import plotly.graph_objects as go
import numpy as np
from backend.prediction_ai import generate_ai_prediction

# =========================================
# MAIN FUNCTION
# =========================================

def show_prediction():

    # =====================================
    # PAGE STYLE
    # =====================================

    st.markdown("""
    <style>

    .main-title{
        font-size:38px;
        font-weight:700;
        color:white;
        margin-bottom:5px;
    }

    .sub-title{
        color:#94a3b8;
        margin-bottom:30px;
    }

    .pred-card{
        background:#0b132b;
        padding:22px;
        border-radius:20px;
        border:1px solid rgba(255,255,255,0.05);
        margin-bottom:20px;
    }

    .small-card{
        background:#111827;
        padding:18px;
        border-radius:16px;
        margin-bottom:15px;
    }

    .metric{
        color:white;
        font-size:34px;
        font-weight:700;
    }

    .label{
        color:#94a3b8;
        font-size:14px;
    }

    .insight-box{
        background:#111827;
        padding:18px;
        border-radius:16px;
        color:white;
        min-height:120px;
    }

    table{
        width:100%;
        color:white;
    }

    td{
        padding:10px;
        border-bottom:1px solid rgba(255,255,255,0.05);
    }

    </style>
    """, unsafe_allow_html=True)

    # =====================================
    # HEADER
    # =====================================

    st.markdown("""
    <div class="main-title">
    🚦 AI TRAFFIC PREDICTION
    </div>

    <div class="sub-title">
    Advanced AI models predict future traffic conditions and help better route planning.
    </div>
    """, unsafe_allow_html=True)

    # =====================================
    # TOP BAR
    # =====================================

    c1,c2,c3,c4 = st.columns([1,1,1,2])

    with c1:
        st.button("24 Hours", use_container_width=True)

    with c2:
        st.button("7 Days", use_container_width=True)

    with c3:
        st.button("30 Days", use_container_width=True)

    with c4:

        area = st.selectbox(
            "🇮🇳 Select City",
            [

            # Maharashtra
            "Mumbai",
            "Pune",
            "Nagpur",
            "Nashik",
            "Thane",
            "Aurangabad",
            "Solapur",

            # Delhi
            "New Delhi",

            # Karnataka
            "Bengaluru",
            "Mysore",
            "Hubli",

            # Telangana
            "Hyderabad",
            "Warangal",

            # Tamil Nadu
            "Chennai",
            "Coimbatore",
            "Madurai",

            # Gujarat
            "Ahmedabad",
            "Surat",
            "Vadodara",
            "Rajkot",

            # Rajasthan
            "Jaipur",
            "Udaipur",
            "Jodhpur",

            # Uttar Pradesh
            "Lucknow",
            "Kanpur",
            "Noida",
            "Varanasi",
            "Agra",

            # West Bengal
            "Kolkata",
            "Howrah",

            # Madhya Pradesh
            "Indore",
            "Bhopal",
            "Gwalior",

            # Punjab
            "Chandigarh",
            "Ludhiana",
            "Amritsar",

            # Bihar
            "Patna",
            "Gaya",

            # Odisha
            "Bhubaneswar",
            "Cuttack",

            # Kerala
            "Kochi",
            "Thiruvananthapuram",
            "Kozhikode",

            # Andhra Pradesh
            "Vijayawada",
            "Visakhapatnam",

            # Assam
            "Guwahati",

            # Jharkhand
            "Ranchi",

            # Chhattisgarh
            "Raipur",

            # Jammu & Kashmir
            "Srinagar",

            # Goa
            "Panaji",

           # Himachal Pradesh
           "Shimla",

           # Uttarakhand
           "Dehradun"
        ]
        )

    # =====================================
    # AI DATA
    # =====================================

    ai_data = generate_ai_prediction(area)

    # =====================================
    # MAIN ROW
    # =====================================

    left,right = st.columns([3,1])

    # =====================================
    # AI PREDICTION GRAPH
    # =====================================

    with left:

        x = list(range(24))

        y = np.random.randint(10,90,24)

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode='lines+markers',
                line=dict(
                    color='#8b5cf6',
                    width=4
                ),
                fill='tozeroy'
            )
        )

        fig.update_layout(

            paper_bgcolor='#0b132b',

            plot_bgcolor='#0b132b',

            font=dict(color='white'),

            height=420,

            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            ),

            xaxis=dict(
                showgrid=False
            ),

            yaxis=dict(
                showgrid=False
            )
        )

        st.markdown('<div class="pred-card">', unsafe_allow_html=True)

        st.subheader("CONGESTION PREDICTION")

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================
    # RIGHT SIDE SUMMARY
    # =====================================

    with right:

        st.markdown(f"""
        <div class="pred-card">

        <h3 style="color:white;">
        Prediction Summary
        </h3>

        <div class="small-card">

        <div class="label">
        Congestion Level
        </div>

        <div class="metric">
        {ai_data["congestion_percent"]}
        </div>

        </div>

        <div class="small-card">

        <div class="label">
        Best Time To Travel
        </div>

        <div class="metric">
        {ai_data["best_travel_time"]}
        </div>

        </div>

        <div class="small-card">

        <div class="label">
        Avoid Route
        </div>

        <div class="metric">
        {ai_data["avoid_route"]}
        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    # =====================================
    # SECOND ROW
    # =====================================

    col1,col2,col3 = st.columns(3)

    # =====================================
    # AREA PREDICTION
    # =====================================

    with col1:

        st.markdown(f"""
        <div class="pred-card">

        <h3 style="color:white;">
        Area Prediction
        </h3>

        <table>

        <tr>
        <td>{area}</td>
        <td>{ai_data["congestion_percent"]}</td>
        <td style="color:red;">
        {ai_data["congestion_level"]}
        </td>
        </tr>

        <tr>
        <td>Baner</td>
        <td>45%</td>
        <td style="color:orange;">
        Moderate
        </td>
        </tr>

        <tr>
        <td>Hinjewadi</td>
        <td>28%</td>
        <td style="color:lime;">
        Low
        </td>
        </tr>

        </table>

        </div>
        """, unsafe_allow_html=True)

    # =====================================
    # TRAVEL TIME
    # =====================================

    with col2:

        st.markdown(f"""
        <div class="pred-card">

        <h3 style="color:white;">
        Travel Time Prediction
        </h3>

        <div class="small-card">

        Current Time

        <h2 style="color:white;">
        32 mins
        </h2>

        </div>

        <div class="small-card">

        Predicted Time

        <h2 style="color:#8b5cf6;">
        {ai_data["predicted_travel_time"]}
        </h2>

        </div>

        </div>
        """, unsafe_allow_html=True)

    # =====================================
    # DEMAND FORECAST
    # =====================================

    with col3:

        x = np.arange(24)

        high = np.random.randint(40,100,24)

        medium = np.random.randint(20,80,24)

        low = np.random.randint(10,50,24)

        fig2 = go.Figure()

        fig2.add_trace(
            go.Scatter(
                x=x,
                y=high,
                mode='lines',
                name='High',
                line=dict(color='#8b5cf6')
            )
        )

        fig2.add_trace(
            go.Scatter(
                x=x,
                y=medium,
                mode='lines',
                name='Medium',
                line=dict(color='#f59e0b')
            )
        )

        fig2.add_trace(
            go.Scatter(
                x=x,
                y=low,
                mode='lines',
                name='Low',
                line=dict(color='#38bdf8')
            )
        )

        fig2.update_layout(

            paper_bgcolor='#0b132b',

            plot_bgcolor='#0b132b',

            font=dict(color='white'),

            height=320,

            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            )
        )

        st.markdown('<div class="pred-card">', unsafe_allow_html=True)

        st.subheader("Traffic Demand Forecast")

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================
    # PEAK HOURS + INSIGHTS
    # =====================================

    c1,c2 = st.columns([1,2])

    # =====================================
    # PEAK HOURS
    # =====================================

    with c1:

        st.markdown(f"""
        <div class="pred-card">

        <h3 style="color:white;">
        Peak Congestion Hours
        </h3>

        <div class="small-card">

        <div class="label">
        Today's Peak
        </div>

        <div class="metric">
        {ai_data["peak_hours"]}
        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    # =====================================
    # AI INSIGHTS
    # =====================================

    with c2:

        st.markdown(f"""
        <div class="pred-card">

        <h3 style="color:white;">
        AI Prediction Insights
        </h3>

        <div style="
        display:grid;
        grid-template-columns:repeat(4,1fr);
        gap:15px;
        ">

        <div class="insight-box">
        🚨<br><br>
        {ai_data["ai_alert"]}
        </div>

        <div class="insight-box">
        🛣<br><br>
        Avoid:
        <br><br>
        {ai_data["avoid_route"]}
        </div>

        <div class="insight-box">
        🌦<br><br>
        Weather Impact:
        <br><br>
        {ai_data["weather_impact"]}
        </div>

        <div class="insight-box">
        ⏰<br><br>
        Best Travel:
        <br><br>
        {ai_data["best_travel_time"]}
        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    # =====================================
    # FOOTER
    # =====================================

    st.markdown("""
    <div style="
    text-align:center;
    color:#94a3b8;
    padding:20px;
    ">

    Predictions are generated using AI traffic analysis models.

    </div>
    """, unsafe_allow_html=True)