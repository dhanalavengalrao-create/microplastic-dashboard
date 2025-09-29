# ------------------------------
# dashboard.py
# ------------------------------

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="Microplastic Sensor Dashboard", layout="wide")
st.title("Microplastic Detection Sensor Dashboard (Simulated Data)")

# ------------------------------
# Simulate Dataset
# ------------------------------
num_readings = 10
timestamps = [datetime.now() - timedelta(minutes=i*1) for i in reversed(range(num_readings))]
concentrations = np.random.randint(50, 200, size=num_readings)
particle_sizes = np.round(np.random.uniform(0.1, 1.0, size=num_readings), 2)

data = pd.DataFrame({
    "timestamp": timestamps,
    "concentration": concentrations,
    "particle_size": particle_sizes
})

# ------------------------------
# Alerts for Readings
# ------------------------------
def get_alert(conc):
    if conc < 100:
        return "Safe ✅"
    elif conc < 150:
        return "Moderate ⚠️"
    else:
        return "High ❌"

data["Alert"] = data["concentration"].apply(get_alert)

# ------------------------------
# KPIs for Latest Reading
# ------------------------------
st.subheader("Current Reading (Latest)")
latest = data.iloc[-1]
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
kpi_col1.metric("Concentration (particles/L)", latest["concentration"])
kpi_col2.metric("Avg Particle Size (mm)", latest["particle_size"])
kpi_col3.metric("Status", latest["Alert"])

# ------------------------------
# Charts
# ------------------------------
st.subheader("Concentration Over Time")
fig1 = px.line(data, x="timestamp", y="concentration", markers=True,
               title="Microplastic Concentration Over Time")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Particle Size Distribution")
fig2 = px.histogram(data, x="particle_size", nbins=10,
                    title="Particle Size Distribution")
st.plotly_chart(fig2, use_container_width=True)

# ------------------------------
# Table with Alerts
# ------------------------------
st.subheader("All Readings with Alerts")
st.table(data)

# ------------------------------
# CSV Download Button
# ------------------------------
st.download_button("Download Data as CSV", data.to_csv(), file_name="microplastics.csv")
