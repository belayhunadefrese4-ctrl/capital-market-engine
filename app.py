import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

# Set Page Config for Mobile App Look
st.set_page_config(
    page_title="Impact & Capital Yield Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application Title
st.title("🏛️ Capital Market & Development M&E Engine")
st.caption("A Centralized Framework for Yield Analytics, Project Planning, and Impact Modeling")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📈 Capital Market & Yields", "🎯 Development M&E & Impact", "📊 Integrated Planning"])

# -------------------------------------------------------------------
# TAB 1: CAPITAL MARKET & YIELD ENGINE
# -------------------------------------------------------------------
with tab1:
    st.header("Ethiopian Capital Market & Treasury Yield Engine")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Market Inputs")
        inflation = st.number_input("Headline Inflation Rate (%)", value=28.5, step=0.5) / 100
        tenor = st.selectbox("T-Bill Tenor (Days)", [28, 91, 182, 364], index=3)
        nominal_yield = st.number_input("Nominal Yield / Cut-off Rate (%)", value=18.5, step=0.25) / 100
        capital = st.number_input("Investment / Treasury Outlay (ETB)", value=1000000, step=50000)

    with col2:
        # Mathematical Formulas
        discount_price_per_100 = 100 / (1 + (nominal_yield * (tenor / 365)))
        upfront_cost = (discount_price_per_100 / 100) * capital
        yield_earned = capital - upfront_cost
        real_return = ((1 + nominal_yield) / (1 + inflation)) - 1
        
        st.subheader("Yield Analysis Output")
        st.metric("Discount Buying Price / 100 Birr", f"{discount_price_per_100:.2f} ETB")
        st.metric("Required Outlay (Upfront Investment)", f"{upfront_cost:,.2f} ETB")
        st.metric("Maturity Earnings (Profit)", f"{yield_earned:,.2f} ETB")
        
        if real_return < 0:
            st.error(f"**Real Return Rate (Purchasing Power):** `{real_return*100:.2f}%` (Negative Real Yield)")
        else:
            st.success(f"**Real Return Rate (Purchasing Power):** `{real_return*100:.2f}%` (Positive Real Yield)")

        # PDF Report Generator for Treasury Yields
        def generate_treasury_pdf():
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
            story = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor("#1A365D"), spaceAfter=12)
            normal_style = styles['Normal']
            
            story.append(Paragraph("<b>Capital Market & Treasury Yield Executive Report</b>", title_style))
            story.append(Paragraph(f"<b>Tenor:</b> {tenor} Days | <b>Nominal Yield:</b> {nominal_yield*100:.2f}%", normal_style))
            story.append(Paragraph(f"<b>Inflation Rate:</b> {inflation*100:.2f}% | <b>Capital Outlay:</b> {capital:,.2f} ETB", normal_style))
            story.append(Spacer(1, 12))
            
            data = [
                ["Metric / Indicator", "Calculated Output"],
                ["Discount Buying Price per 100 Birr", f"{discount_price_per_100:.2f} ETB"],
                ["Upfront Investment Outlay", f"{upfront_cost:,.2f} ETB"],
                ["Maturity Earnings (Profit)", f"{yield_earned:,.2f} ETB"],
                ["Real Return Rate (Fisher Adjusted)", f"{real_return*100:.2f}%"]
            ]
            
            t = Table(data, colWidths=[250, 250])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (1,0), colors.HexColor("#2B6CB0")),
                ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#EDF2F7")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            story.append(t)
            doc.build(story)
            buffer.seek(0)
            return buffer

        st.download_button(
            label="📄 Download Treasury Executive Report (PDF)",
            data=generate_treasury_pdf(),
            file_name="Treasury_Yield_Report.pdf",
            mime="application/pdf"
        )

# -------------------------------------------------------------------
# TAB 2: IMPACT & M&E CONSULTING ENGINE
# -------------------------------------------------------------------
with tab2:
    st.header("Project M&E, SROI & Development Impact Model")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Project Inputs")
        project_cost = st.number_input("Total Project Investment / NGO Budget (ETB)", value=5000000, step=100000)
        social_value = st.number_input("Monetized Social / Economic Benefit (ETB)", value=8500000, step=100000)
        beneficiaries = st.number_input("Total Target Beneficiaries", value=2500, step=100)
        project_name = st.text_input("Project Name / Grant Identifier", value="Rural Financial Inclusion Initiative")

    with col_b:
        cost_per_beneficiary = project_cost / beneficiaries if beneficiaries > 0 else 0
        sroi_ratio = social_value / project_cost if project_cost > 0 else 0
        net_social_benefit = social_value - project_cost

        st.subheader("Impact Indicators")
        st.metric("Unit Cost per Beneficiary", f"{cost_per_beneficiary:,.2f} ETB")
        st.metric("Social Return on Investment (SROI)", f"{sroi_ratio:.2f}x")
        st.metric("Net Economic Benefit Created", f"{net_social_benefit:,.2f} ETB")
        
        st.info(f"**Interpretation:** Every 1 ETB invested creates **{sroi_ratio:.2f} ETB** of verified social-economic value.")

        # PDF Report Generator for M&E Impact
        def generate_impact_pdf():
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
            story = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor("#2C5282"), spaceAfter=12)
            normal_style = styles['Normal']
            
            story.append(Paragraph(f"<b>Development M&E & Impact Report</b>", title_style))
            story.append(Paragraph(f"<b>Project Identifier:</b> {project_name}", normal_style))
            story.append(Paragraph(f"<b>Total Budget:</b> {project_cost:,.2f} ETB | <b>Beneficiaries:</b> {beneficiaries:,}", normal_style))
            story.append(Spacer(1, 12))
            
            data = [
                ["M&E / Impact Indicator", "Evaluated Output"],
                ["Total Investment Outlay", f"{project_cost:,.2f} ETB"],
                ["Monetized Social Value", f"{social_value:,.2f} ETB"],
                ["Cost per Beneficiary", f"{cost_per_beneficiary:,.2f} ETB"],
                ["Social Return on Investment (SROI)", f"{sroi_ratio:.2f}x"],
                ["Net Economic Benefit", f"{net_social_benefit:,.2f} ETB"]
            ]
            
            t = Table(data, colWidths=[250, 250])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (1,0), colors.HexColor("#3182CE")),
                ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#EDF2F7")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            story.append(t)
            doc.build(story)
            buffer.seek(0)
            return buffer

        st.download_button(
            label="📄 Download Impact & M&E Report (PDF)",
            data=generate_impact_pdf(),
            file_name="Impact_ME_Report.pdf",
            mime="application/pdf"
        )

# -------------------------------------------------------------------
# TAB 3: INTEGRATED MACRO PLANNING
# -------------------------------------------------------------------
with tab3:
    st.header("Strategic Macro-Planning & Portfolio Allocation")
    st.markdown("Automated asset distribution balancing risk-free government securities with high-impact development projects.")
    
    total_portfolio = st.number_input("Total Capital Allocation (ETB)", value=10000000, step=500000)
    tbill_pct = st.slider("Treasury Bills Allocation (%)", 0, 100, 60)
    impact_pct = 100 - tbill_pct
    
    tbill_amount = total_portfolio * (tbill_pct / 100)
    impact_amount = total_portfolio * (impact_pct / 100)
    
    st.write("---")
    res_col1, res_col2 = st.columns(2)
    res_col1.metric("Capital Market Treasury Allocation", f"{tbill_amount:,.2f} ETB ({tbill_pct}%)")
    res_col2.metric("Impact / Project Investment Allocation", f"{impact_amount:,.2f} ETB ({impact_pct}%)")
