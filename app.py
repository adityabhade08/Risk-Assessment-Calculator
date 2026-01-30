import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Risk Assessment Calculator",
    page_icon="⚠️",
    layout="centered"
)

st.title("⚠️ Risk Assessment Calculator")
st.write("Visual risk assessment using standard GRC methodology (Likelihood × Impact).")

st.divider()

# User inputs
asset = st.text_input("🖥️ Asset / Process Name", placeholder="e.g. Web Application, Customer Database")

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

# Risk level logic with visuals
if risk_score <= 5:
    risk_level = "Low"
    risk_color = "🟢 LOW RISK"
elif 6 <= risk_score <= 12:
    risk_level = "Medium"
    risk_color = "🟡 MEDIUM RISK"
else:
    risk_level = "High"
    risk_color = "🔴 HIGH RISK"

st.divider()

# Visual summary section
st.subheader("📌 Risk Summary")

col1, col2 = st.columns(2)
col1.metric("Risk Score", risk_score)
col2.metric("Risk Level", risk_color)

st.markdown(
    f"""
    ### 🧾 Assessment Overview
    - **Asset / Process:** `{asset if asset else "Not Specified"}`
    - **Likelihood Score:** `{likelihood}`
    - **Impact Score:** `{impact}`
    - **Overall Risk Classification:** **{risk_level}**
    """
)

st.divider()

# Risk register table
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
def generate_pdf(asset, risk_level, explanation, action):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    pdf = SimpleDocTemplate(
        temp_file.name,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    content = []

    # Title
    content.append(Paragraph(
        "<b><font size=18>Risk Assessment Report</font></b>",
        styles["Title"]
    ))
    content.append(Spacer(1, 0.3 * inch))

    # Asset section
    content.append(Paragraph(
        f"<b>What was assessed:</b><br/>{asset if asset else 'Not specified'}",
        styles["Normal"]
    ))
    content.append(Spacer(1, 0.2 * inch))

    # Risk level with color
    if risk_level == "High":
        color = red
        risk_text = "HIGH RISK"
    elif risk_level == "Medium":
        color = orange
        risk_text = "MEDIUM RISK"
    else:
        color = green
        risk_text = "LOW RISK"

    content.append(Paragraph(
        f"<b>Risk Level:</b> <font color='{color.hexval()}'>{risk_text}</font>",
        styles["Normal"]
    ))
    content.append(Spacer(1, 0.2 * inch))

    # Explanation
    content.append(Paragraph(
        "<b>What does this mean?</b>",
        styles["Heading3"]
    ))
    content.append(Paragraph(explanation, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    # Action
    content.append(Paragraph(
        "<b>Recommended Action:</b>",
        styles["Heading3"]
    ))
    content.append(Paragraph(action, styles["Normal"])) 
    from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import red, green, orange, black
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import tempfile


    # Footer
    content.append(Spacer(1, 0.5 * inch))
    content.append(Paragraph(
        "<font size=9 color='grey'>Generated using Risk Assessment Calculator</font>",
        styles["Normal"]
    ))

    pdf.build(content)
    return temp_file.name

