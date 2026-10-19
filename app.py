import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime

# ReportLab imports for professional multi-page PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Set page configuration
st.set_page_config(
    page_title="Ethiopian Capital Market & Impact Analytics Engine",
    page_icon="🇪🇹",
    layout="wide"
)

# Custom Header Section
st.title("🇪🇹 Ethiopian Capital Market & Development M&E Analytics Engine")
st.markdown("""
**A Comprehensive Macroeconomic, Fixed Income Yield & Social Impact Evaluation Platform**  
*Designed for Commercial Banks, Institutional Investors, Planning Commissions, and International Development Partners.*
""")
st.divider()

# Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "📈 Capital Market & Treasury Yield Engine", 
    "🎯 Development M&E & Impact Scorecard", 
    "📊 Executive Report Generator & Strategic Advisor"
])

# ==============================================================================
# TAB 1: ETHIOPIAN CAPITAL MARKET & TREASURY YIELD ENGINE
# ==============================================================================
with tab1:
    st.header("1. Ethiopian Fixed Income & Money Market Analytics")
    st.caption("Modeled for National Bank of Ethiopia (NBE) Auctions, Treasury Bills, Sovereign Bonds, and ESX Markets.")
    
    col_in, col_out = st.columns([1, 1])
    
    with col_in:
        st.subheader("⚙️ Macro & Instrument Inputs")
        headline_inflation = st.number_input("Ethiopian Headline Inflation Rate (%)", min_value=0.0, max_value=100.0, value=22.50, step=0.50)
        withholding_tax_rate = st.number_input("Applicable Withholding / Capital Tax (%)", min_value=0.0, max_value=30.0, value=0.0, step=1.0)
        
        security_type = st.radio("Select Financial Instrument", ["Treasury Bill (Discount Security)", "Sovereign / Infrastructure Bond (Coupon Security)"])
        
        if security_type == "Treasury Bill (Discount Security)":
            tenor_days = st.selectbox("NBE T-Bill Tenor (Days)", [28, 91, 182, 364], index=3)
            nominal_yield = st.number_input("Auction Cut-off Yield / Nominal Rate (%)", min_value=0.0, max_value=100.0, value=18.50, step=0.25)
            target_outlay = st.number_input("Target Face Value Investment (ETB)", min_value=10000.0, value=1000000.0, step=100000.0)
            
            # T-Bill Calculations
            discount_price = 100 / (1 + (nominal_yield / 100) * (tenor_days / 365))
            required_cash = (target_outlay * discount_price) / 100
            gross_profit = target_outlay - required_cash
            tax_deduction = gross_profit * (withholding_tax_rate / 100)
            net_profit = gross_profit - tax_deduction
            
            # Effective Annual Yield (EAY)
            eay = (((1 + (nominal_yield / 100) * (tenor_days / 365))) ** (365 / tenor_days) - 1) * 100
            
            # Fisher Real Return Rate
            net_yield = (net_profit / required_cash) * (365 / tenor_days) * 100
            real_return = (((1 + (net_yield / 100)) / (1 + (headline_inflation / 100))) - 1) * 100

        else:
            bond_years = st.selectbox("Bond Maturity Tenor (Years)", [3, 5, 7, 10], index=1)
            coupon_rate = st.number_input("Annual Coupon Interest Rate (%)", min_value=0.0, max_value=50.0, value=18.00, step=0.50)
            principal_amount = st.number_input("Principal Capital Commitment (ETB)", min_value=100000.0, value=5000000.0, step=500000.0)
            
            # Bond Calculations
            annual_coupon = principal_amount * (coupon_rate / 100)
            total_interest = annual_coupon * bond_years
            tax_deduction = total_interest * (withholding_tax_rate / 100)
            net_profit = total_interest - tax_deduction
            
            discount_price = 100.00
            required_cash = principal_amount
            gross_profit = total_interest
            eay = coupon_rate
            real_return = (((1 + (coupon_rate / 100)) / (1 + (headline_inflation / 100))) - 1) * 100

    with col_out:
        st.subheader("📈 Institutional Yield Outputs")
        
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric("Discount Price / 100 Birr", f"{discount_price:.2f} ETB")
            st.metric("Upfront Cash Required", f"{required_cash:,.2f} ETB")
            st.metric("Gross Maturity Profit", f"{gross_profit:,.2f} ETB")
        with m_col2:
            st.metric("Effective Annual Yield (EAY)", f"{eay:.2f}%")
            st.metric("Net Earnings Post-Tax", f"{net_profit:,.2f} ETB")
            st.metric("Inflation Gap", f"{(nominal_yield - headline_inflation):.2f}%")
        
        st.divider()
        if real_return >= 0:
            st.success(f"**Real Return Rate (Purchasing Power Growth):** +{real_return:.2f}%\n\n*The investment yield successfully protects capital against local inflation.*")
        else:
            st.error(f"**Real Return Rate (Purchasing Power Loss):** {real_return:.2f}%\n\n*Nominal gains are eclipsed by domestic price inflation, leading to real capital dilution.*")

# ==============================================================================
# TAB 2: DEVELOPMENT IMPACT & M&E SCORECARD
# ==============================================================================
with tab2:
    st.header("2. Project M&E, Social Return & Cost-Efficiency Engine")
    st.caption("Aligned with Planning and Development Commission & International Donor Monitoring Frameworks.")
    
    col_m1, col_m2 = st.columns([1, 1])
    
    with col_m1:
        st.subheader("📋 Project Parameters")
        project_title = st.text_input("Project Name / Initiative Title", "National Agricultural Productivity Enhancement Project")
        implementing_agency = st.text_input("Implementing Organization / Bureau", "Ministry of Agriculture / Planning Commission")
        project_budget = st.number_input("Total Financial Investment (ETB)", value=10000000.0, step=500000.0)
        
        st.subheader("👥 Beneficiary Metrics")
        direct_beneficiaries = st.number_input("Direct Beneficiaries Reached", value=15000, step=1000)
        indirect_beneficiaries = st.number_input("Indirect Beneficiaries Reached", value=45000, step=2500)
        
        st.subheader("💡 Monetized Impact Evaluation")
        monetized_social_value = st.number_input("Monetized Value of Social Benefits Created (ETB)", value=18500000.0, step=500000.0)

    with col_m2:
        st.subheader("📊 M&E Performance Diagnostics")
        
        cost_per_direct = project_budget / direct_beneficiaries if direct_beneficiaries > 0 else 0
        total_beneficiaries = direct_beneficiaries + indirect_beneficiaries
        cost_per_total = project_budget / total_beneficiaries if total_beneficiaries > 0 else 0
        sroi_ratio = monetized_social_value / project_budget if project_budget > 0 else 0
        net_social_value = monetized_social_value - project_budget
        
        kpi_col1, kpi_col2 = st.columns(2)
        with kpi_col1:
            st.metric("Cost per Direct Beneficiary", f"{cost_per_direct:,.2f} ETB")
            st.metric("Total Beneficiary Reach", f"{total_beneficiaries:,}")
            st.metric("Cost per Combined Beneficiary", f"{cost_per_total:,.2f} ETB")
        with kpi_col2:
            st.metric("Social Return on Investment (SROI)", f"{sroi_ratio:.2f}:1")
            st.metric("Net Social Value Created", f"{net_social_value:,.2f} ETB")
            
        st.divider()
        if sroi_ratio >= 1.5:
            st.success(f"**High Impact Performance (SROI: {sroi_ratio:.2f}:1)**\n\nFor every 1.00 ETB invested, {sroi_ratio:.2f} ETB of monetized socio-economic value is generated.")
        elif sroi_ratio >= 1.0:
            st.info(f"**Moderate Impact Efficiency (SROI: {sroi_ratio:.2f}:1)**\n\nSocial returns cover initial financial outlays, but resource optimization is recommended.")
        else:
            st.warning(f"**Low Impact Efficiency (SROI: {sroi_ratio:.2f}:1)**\n\nFinancial outlay exceeds monetized benefits. Project workflow requires restructuring.")

# ==============================================================================
# TAB 3: EXECUTIVE REPORT GENERATOR & STRATEGIC ADVISOR
# ==============================================================================
with tab3:
    st.header("3. Executive PDF Report & Strategic Decision Advisor")
    st.markdown("Compile all financial, macroeconomic, and impact metrics into a formal **Publication-Ready PDF Executive Briefing**.")
    
    st.subheader("📝 Strategic Narrative Settings")
    report_title = st.text_input("Document Title", "Ethiopian Capital Market & Impact Performance Evaluation Briefing")
    prepared_by = st.text_input("Prepared By (Author / Analyst)", "Economic Planning & Financial Analytics Division")
    exec_comments = st.text_area("Custom Executive Remarks & Directives", "This analysis evaluates capital allocation efficiency, inflation adjustments, and social impact returns for executive review and policy decision-making.")
    
    st.divider()
    
    if st.button("🚀 Generate Comprehensive PDF Briefing", type="primary"):
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        
        # Custom PDF Styles
        title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1A365D'), spaceAfter=8, leading=22)
        subtitle_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#4A5568'), spaceAfter=14)
        heading_style = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1A365D'), spaceBefore=12, spaceAfter=6, leading=16)
        body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#2D3748'), spaceAfter=6, leading=13)
        bold_body = ParagraphStyle('BoldBody', parent=body_style, fontName='Helvetica-Bold')
        
        story = []
        
        # Header Banner
        story.append(Paragraph("<b>ETHIOPIAN CAPITAL MARKET & DEVELOPMENT M&E ENGINE</b>", title_style))
        story.append(Paragraph(f"<b>Document Title:</b> {report_title} | <b>Date:</b> {datetime.now().strftime('%Y-%m-%d')} | <b>Author:</b> {prepared_by}", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1A365D'), spaceAfter=12))
        
        # Executive Summary Section
        story.append(Paragraph("1. Executive Summary & Macroeconomic Outlook", heading_style))
        summary_text = f"""
        This analytical briefing provides a unified evaluation of capital market yields and development impact within the Ethiopian national economic context. 
        Evaluating market instruments against a baseline headline inflation rate of <b>{headline_inflation:.2f}%</b> reveals a real purchasing power yield of <b>{real_return:.2f}%</b> for the selected instrument (<b>{security_type}</b>). 
        Concurrently, social investment modeling for <b>{project_title}</b> indicates an SROI ratio of <b>{sroi_ratio:.2f}:1</b>, delivering a net social return of <b>{net_social_value:,.2f} ETB</b> across <b>{total_beneficiaries:,}</b> total beneficiaries.
        """
        story.append(Paragraph(summary_text, body_style))
        story.append(Spacer(1, 8))
        
        # Section 2: Capital Market Performance Table
        story.append(Paragraph("2. Financial Yield & Fixed Income Performance Scorecard", heading_style))
        fin_data = [
            [Paragraph("<b>Metric / Parameter</b>", bold_body), Paragraph("<b>Quantitative Value</b>", bold_body), Paragraph("<b>Strategic Benchmark / Context</b>", bold_body)],
            ["Headline Inflation Rate", f"{headline_inflation:.2f}%", "National Macroeconomic Baseline"],
            ["Selected Security Instrument", security_type, "Money Market / Debt Capital Instrument"],
            ["Instrument Tenor / Duration", f"{tenor_days} Days" if security_type.startswith("Treasury") else f"{bond_years} Years", "Maturity Cycle"],
            ["Nominal Cut-off Rate / Yield", f"{nominal_yield:.2f}%", "Gross Annualized Return"],
            ["Effective Annual Yield (EAY)", f"{eay:.2f}%", "Annualized Compounded Metric"],
            ["Upfront Outlay Required", f"{required_cash:,.2f} ETB", "Capital Allocation Commitment"],
            ["Net Maturity Earnings", f"{net_profit:,.2f} ETB", f"Post-{withholding_tax_rate:.1f}% Tax Profit"],
            ["Real Purchasing Power Return", f"{real_return:.2f}%", "Fisher Real Return Valuation"]
        ]
        
        t_fin = Table(fin_data, colWidths=[180, 140, 220])
        t_fin.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')]),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_fin)
        story.append(Spacer(1, 10))
        
        # Section 3: M&E & Impact Table
        story.append(Paragraph("3. Development M&E & Impact Performance Table", heading_style))
        me_data = [
            [Paragraph("<b>Impact Performance Indicator</b>", bold_body), Paragraph("<b>Evaluated Metric</b>", bold_body), Paragraph("<b>Institutional Assessment</b>", bold_body)],
            ["Project / Initiative Name", project_title, f"Agency: {implementing_agency}"],
            ["Total Financial Outlay", f"{project_budget:,.2f} ETB", "Total Resource Commitment"],
            ["Direct Beneficiary Reach", f"{direct_beneficiaries:,} Individuals", f"Cost: {cost_per_direct:,.2f} ETB / Person"],
            ["Indirect Beneficiary Reach", f"{indirect_beneficiaries:,} Individuals", "Broader Community Spillover"],
            ["Monetized Social Benefits", f"{monetized_social_value:,.2f} ETB", "Quantified Socio-Economic Benefit"],
            ["Social Return on Investment (SROI)", f"{sroi_ratio:.2f} : 1", "Social Efficiency Ratio"],
            ["Net Value Creation", f"{net_social_value:,.2f} ETB", "Value Above Financial Outlay"]
        ]
        
        t_me = Table(me_data, colWidths=[180, 140, 220])
        t_me.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')]),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_me)
        story.append(Spacer(1, 10))
        
        # Section 4: Actionable Recommendations
        story.append(Paragraph("4. Actionable Institutional Recommendations", heading_style))
        
        rec_financial = f"• <b>Treasury & Liquidity Management:</b> Nominal returns currently yield <b>{nominal_yield:.2f}%</b> against inflation of <b>{headline_inflation:.2f}%</b>. "
        if real_return < 0:
            rec_financial += "Treasury managers are advised to negotiate higher auction cut-off yields or diversify into inflation-indexed assets to prevent real capital erosion."
        else:
            rec_financial += "The selected security effectively locks in positive real capital gains, making it a viable allocation for portfolio preservation."
            
        rec_impact = f"<br/><br/>• <b>Impact Efficiency Directive:</b> With an SROI of <b>{sroi_ratio:.2f}:1</b>, the initiative demonstrates "
        if sroi_ratio >= 1.2:
            rec_impact += "strong social efficiency. It is recommended for scale-up and institutional expansion."
        else:
            rec_impact += "moderate social leverage. M&E teams should audit operational cost structures to reduce per-beneficiary expenditure."
            
        story.append(Paragraph(rec_financial + rec_impact, body_style))
        story.append(Spacer(1, 8))
        
        # Section 5: Executive Remarks
        if exec_comments:
            story.append(Paragraph("5. Directives & Executive Remarks", heading_style))
            story.append(Paragraph(f"<i>\"{exec_comments}\"</i>", body_style))
            
        # Build Document
        doc.build(story)
        pdf_buffer.seek(0)
        
        st.success("✅ Executive Briefing PDF Generated Successfully!")
        st.download_button(
            label="📥 Download Publication-Ready PDF Briefing",
            data=pdf_buffer,
            file_name=f"Ethiopia_Capital_Market_Impact_Briefing_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            type="primary"
        )
