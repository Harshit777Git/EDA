import streamlit as st
import pandas as pd
import json
import time

# 📊 Page Configuration
st.set_page_config(
    page_title="Smart Agriculture Dashboard",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Smart Agriculture Monitoring")
st.markdown("Real-time telemetry from **simDevice01**.")

placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            data = []
            with open("processed_data.json", "r") as f:
                for line in f:
                    data.append(json.loads(line.strip()))
            
            df = pd.DataFrame(data)
            
            if not df.empty:
                # Use only the last 20 entries for the chart
                df_chart = df.tail(20)
                latest_data = df.iloc[-1]
                
                # --- 1. Key Metrics Section ---
                col1, col2, col3 = st.columns(3)

                # Temperature Metric
                latest_temp = latest_data["temperature"]
                col1.metric(
                    label="🌡️ Temperature (C)", 
                    value=f"{latest_temp:.2f}"
                )

                # Moisture Metric
                latest_moisture = latest_data["moisture"]
                col2.metric(
                    label="💧 Soil Moisture (%)", 
                    value=f"{latest_moisture:.2f}"
                )
                
                col3.metric(
                    label="📅 Total Readings",
                    value=len(df)
                )

                # --- 2. Alerts Section (based on logic in local_function.py) ---
                st.subheader("⚠️ Current Status Alerts")
                
                temp_alert = latest_temp > 35
                moisture_alert = latest_moisture < 30

                if temp_alert or moisture_alert:
                    if temp_alert:
                        st.error(f"🔥 **HIGH TEMPERATURE ALERT:** The current temperature is **{latest_temp:.2f}°C**, which exceeds the safe threshold (35°C).")
                    if moisture_alert:
                        st.error(f"💧 **LOW MOISTURE ALERT:** The current soil moisture is **{latest_moisture:.2f}%**, which is below the critical level (30%). Immediate irrigation required!")
                else:
                    st.success("✅ **STATUS OK:** All sensor readings are within normal operating parameters.")


                # --- 3. Chart Section ---
                st.subheader("📈 Last 20 Readings Trend")
                st.line_chart(df_chart[["temperature", "moisture"]])
                
                # --- 4. Raw Data Preview ---
                st.subheader("📜 Raw Data Preview (Latest)")
                st.dataframe(df_chart.iloc[::-1]) # show latest data first

            else:
                 st.info("Waiting for data to be processed...")


        except FileNotFoundError:
            st.warning("Waiting for data to be generated and processed...")
        
    time.sleep(3) # Refresh every 3 seconds