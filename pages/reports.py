from pathlib import Path

import pandas as pd
import streamlit as st

DATA_PATH = Path("data/traffic.csv")


def build_sample_data() -> pd.DataFrame:
    dates = pd.date_range("2026-05-01", periods=7, freq="D")
    areas = ["Pune", "Mumbai", "Delhi", "Bengaluru"]

    rows = []

    for area in areas:
        for idx, date in enumerate(dates):
            traffic = 45 + (idx * 4) + (len(area) % 5)
            avg_speed = max(35, 80 - (traffic * 0.4))
            incidents = max(0, int((traffic - 55) / 10))

            rows.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "area": area,
                    "traffic": round(traffic, 1),
                    "avg_speed": round(avg_speed, 1),
                    "incidents": incidents,
                }
            )

    return pd.DataFrame(rows)


def load_report_data() -> pd.DataFrame:
    if not DATA_PATH.exists() or DATA_PATH.stat().st_size == 0:
        return build_sample_data()

    try:
        df = pd.read_csv(DATA_PATH)

        required_cols = {"date", "area", "traffic"}
        if not required_cols.issubset(df.columns):
            return build_sample_data()

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

        if df.empty:
            return build_sample_data()

        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

        if "avg_speed" not in df.columns:
            df["avg_speed"] = 0.0

        if "incidents" not in df.columns:
            df["incidents"] = 0

        return df
    except Exception:
        return build_sample_data()


def show_reports():
    st.title("📊 Traffic Reports")
    st.caption("Analyze congestion patterns, hotspots, and traffic incidents across monitored areas.")

    df = load_report_data()
    df["date"] = pd.to_datetime(df["date"])

    area_options = ["All Areas"] + sorted(df["area"].dropna().unique().tolist())
    selected_area = st.selectbox("Filter by area", area_options)

    if selected_area != "All Areas":
        filtered_df = df[df["area"] == selected_area].copy()
    else:
        filtered_df = df.copy()

    if filtered_df.empty:
        st.warning("No traffic data is available for the selected filter.")
        return

    filtered_df["date"] = filtered_df["date"].dt.strftime("%Y-%m-%d")

    avg_traffic = float(filtered_df["traffic"].mean())
    avg_speed = float(filtered_df["avg_speed"].mean()) if "avg_speed" in filtered_df.columns else 0.0
    total_incidents = int(filtered_df["incidents"].sum()) if "incidents" in filtered_df.columns else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Average congestion", f"{avg_traffic:.1f}%")
    col2.metric("Average speed", f"{avg_speed:.1f} km/h")
    col3.metric("Reported incidents", total_incidents)

    chart_col, table_col = st.columns([2, 1])

    with chart_col:
        st.subheader("Traffic trend")
        trend_df = filtered_df.groupby("date")["traffic"].mean().reset_index()
        st.line_chart(trend_df.set_index("date"))

        st.subheader("Area comparison")
        comparison_df = filtered_df.groupby("area")["traffic"].mean().reset_index()
        st.bar_chart(comparison_df.set_index("area"))

    with table_col:
        st.subheader("Top hotspots")
        top_hotspots = (
            filtered_df.sort_values("traffic", ascending=False)
            .drop_duplicates(subset=["area", "date"])
            .head(5)
        )
        st.dataframe(top_hotspots[["date", "area", "traffic", "avg_speed", "incidents"]])

    st.subheader("Detailed report")
    st.dataframe(filtered_df.sort_values("date", ascending=False)[["date", "area", "traffic", "avg_speed", "incidents"]])

    csv_data = filtered_df[["date", "area", "traffic", "avg_speed", "incidents"]].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download report CSV",
        data=csv_data,
        file_name="traffic_reports.csv",
        mime="text/csv",
    )