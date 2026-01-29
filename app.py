import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Risk Assessment Calculator",
    page_icon="⚠️",
    layout="centered"
)

st.title("⚠️ Risk Assessment Calculator")
st.write("Calculate risk levels based on Likelihood and Impact (GRC Methodology).")

st.divider()

# User inputs
asset = st.text_input("🖥️ Asset / Process Name")

likelihood = st.selectbox(
    "📊 Likelihood",
    {
        1: "Rare",
        2: "Unlikely",
        3: "Possible",
        4: "Likely",
        5: "Almost Certain"
    }
)

impact = st.selectbox(
    "🔥 Impact",
    {
        1: "Negligible",
        2: "Minor",
        3: "Moderate",
        4: "Major",
        5: "Severe"
    }
)

# Risk calculation
risk_score = likelihood * impact

# Risk level logic
if risk_score <= 5:
    risk_level = "Low"
elif 6 <= risk_score <= 12:
    risk_level = "Medium"
else:
    risk_level = "High"

st.divider()

st.subheader("📈 Risk Assessment Result")

st.metric("Risk Score", risk_score)
st.metric("Risk Level", risk_level)

# Risk table
data = {
    "Asset / Process": [asset if asset else "Not Specified"],
    "Likelihood": [likelihood],
    "Impact": [impact],
    "Risk Score": [risk_score],
    "Risk Level": [risk_level]
}

df = pd.DataFrame(data)

st.subheader("📋 Risk Register Entry")
st.dataframe(df, use_container_width=True)

# Download report
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇ Download Risk Assessment Report (CSV)",
    data=csv,
    file_name="risk_assessment_report.csv",
    mime="text/csv"
)

st.success("✔ Risk assessment completed successfully")
