import streamlit as st
import tempfile

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import red, green, orange
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Risk Assessment Report",
    page_icon="⚠️",
    layout="centered"
)

st.title("⚠️ Risk Assessment Report")
st.write("A simple, human-readable cybersecurity risk report.")

st.divider()

# ---------------- USER INPUT ----------------
asset = st.text_input(
    "🖥️ What are you assessing?",
    placeholder="Example: Customer Database, Web Application, Employee Laptop"
)

likelihood = st.selectbox(
    "📊 How likely is the risk?",
    {
        1: "Very unlikely",
        2: "Unlikely",
        3: "Possible",
        4: "Likely",
        5: "Very likely"
    }
)

impact = st.selectbox(
    "🔥 If it happens, how bad will it be?",
    {
        1: "Very small impact",
        2: "Minor impact",
        3: "Moderate impact",
        4: "Serious impact",
        5: "Very serious impact"
    }
)

# ---------------- RISK LOGIC ----------------
risk_score = likelihood * impact

if risk_score <= 5:
    risk_level = "Low"
    explanation = (
        "This risk is unlikely to occur and would cause minimal damage. "
        "It does not require immediate attention."
    )
    action = "🟢 No urgent action required. Monitor occasionally."
    color = green

elif 6 <= risk_score <= 12:
    risk_level = "Medium"
    explanation = (
        "This risk could occur and may cause noticeable impact. "
        "Some preventive controls should be planned."
    )
    action = "🟡 Plan and apply basic risk controls."
    color = orange

else:
    risk_level = "High"
    explanation = (
        "This risk is likely to occur and could cause serious damage. "
        "Immediate corrective action is strongly recommended."
    )
    action = "🔴 Immediate action required to reduce the risk."
    color = red

# ---------------- REPORT DISPLAY ----------------
st.divider()
st.subheader("📄 Final Risk Summary")

st.markdown(
    f"""
    **Asset / Process Assessed:** {asset if asset else "Not specified"}  

    **Risk Level:** {risk_level} Risk  

    **What does this mean?**  
    {explanation}

    **What should be done next?**  
    {action}
    """
)

# ---------------- PDF FUNCTION ----------------
def generate_pdf(asset, risk_level, explanation, action, color):
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
        "<b><font size=20>Cybersecurity Risk Assessment Report</font></b>",
        styles["Title"]
    ))
    content.append(Spacer(1, 0.4 * inch))

    # Asset
    content.append(Paragraph(
        f"<b>Asset / Process Assessed:</b><br/>{asset if asset else 'Not specified'}",
        styles["Normal"]
    ))
    content.append(Spacer(1, 0.25 * inch))

    # Risk level
    content.append(Paragraph(
        f"<b>Risk Level:</b> <font color='{color.hexval()}'><b>{risk_level.upper()} RISK</b></font>",
        styles["Normal"]
    ))
    content.append(Spacer(1, 0.25 * inch))

    # Explanation
    content.append(Paragraph("<b>What does this mean?</b>", styles["Heading3"]))
    content.append(Paragraph(explanation, styles["Normal"]))
    content.append(Spacer(1, 0.25 * inch))

    # Action
    content.append(Paragraph("<b>Recommended Action</b>", styles["Heading3"]))
    content.append(Paragraph(action, styles["Normal"]))
    content.append(Spacer(1, 0.4 * inch))

    # ---------------- RISK ASSESSMENT STEPS ----------------
    content.append(Paragraph("<b>Risk Assessment Steps Used</b>", styles["Heading2"]))
    content.append(Spacer(1, 0.2 * inch))

    steps = [
        "1. Identify the asset or process that needs protection.",
        "2. Identify the potential cybersecurity risk related to the asset.",
        "3. Assess how likely the risk is to occur.",
        "4. Assess the impact if the risk occurs.",
        "5. Calculate the overall risk level based on likelihood and impact.",
        "6. Interpret the risk in simple terms for better understanding.",
        "7. Recommend appropriate actions based on the risk level.",
        "8. Generate a clear and easy-to-read risk report."
    ]

    for step in steps:
        content.append(Paragraph(step, styles["Normal"]))
        content.append(Spacer(1, 0.1 * inch))

    # Footer
    content.append(Spacer(1, 0.5 * inch))
    content.append(Paragraph(
        "<font size=9 color='grey'>Generated using Risk Assessment Calculator</font>",
        styles["Normal"]
    ))

    pdf.build(content)
    return temp_file.name

# ---------------- DOWNLOAD SECTION ----------------
st.divider()
st.subheader("📥 Download Report")

if st.button("Generate Styled PDF Report"):
    pdf_path = generate_pdf(asset, risk_level, explanation, action, color)
    with open(pdf_path, "rb") as file:
        st.download_button(
            label="⬇ Download PDF Report",
            data=file,
            file_name="risk_assessment_report.pdf",
            mime="application/pdf"
        )

st.success("✔ Risk assessment report generated successfully")
