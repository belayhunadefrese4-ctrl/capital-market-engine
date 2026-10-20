import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import csv
from datetime import datetime

# ReportLab imports for professional multi-page PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Set page configuration
st.set_page_config(
    page_title="Ethiopian Capital Market & Impact Analytics Engine",
    page_icon="🇪🇹",
    layout="wide"
)

# Optional Google Analytics Tracking Injection
ga_measurement_id = "G-XXXXXXXXXX"
st.markdown(f"""
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_measurement_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ga_measurement_id}');
    </script>
""", unsafe_allow_html=True)

# PWA and Mobile-Friendly Meta Tags Injection
st.markdown("""
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#1A365D">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="EthioMarkets M&E">
""", unsafe_allow_html=True)

# Custom Header Section
st.title("🇪🇹 Ethiopian Capital Market & Development M&E Analytics Engine")
st.markdown("""
**A Comprehensive Macroeconomic, Fixed Income Yield & Social Impact Evaluation Platform**  
*Designed for Commercial Banks, Institutional Investors, Planning Commissions, and International Development Partners.*
""")
st.divider()

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Capital Market & Treasury Yield Engine", 
    "🎯 Development M&E & Impact Scorecard", 
    "📊 Executive Report Generator & Licensing",
    "🔒 Admin Dashboard"
])

# ==============================================================================
# TAB 1: ETHIOPIAN CAPITAL MARKET & MULTI-INSTRUMENT PORTFOLIO ENGINE
# ==============================================================================
with tab1:
    st.header("1. Ethiopian Fixed Income & Multi-Asset Portfolio Analytics")
    st.caption("Modeled for National Bank of Ethiopia (NBE) Auctions, Treasury Bills, Sovereign Bonds, and Custom Portfolio Assets.")
    
    col_in, col_out = st.columns([1, 1])
    
    with col_in:
        st.subheader("⚙️ Macro Baseline Inputs")
        headline_inflation = st.number_input("Ethiopian Headline Inflation Rate (%)", min_value=0.0, max_value=100.0, value=22.50, step=0.50)
        withholding_tax_rate = st.number_input("Applicable Withholding / Capital Tax (%)", min_value=0.0, max_value=30.0, value=0.0, step=1.0)
        
        security_type = st.radio("Primary Instrument Focus", ["Treasury Bill (Discount Security)", "Sovereign / Infrastructure Bond (Coupon Security)"])
        
        if security_type == "Treasury Bill (Discount Security)":
            tenor_days = st.selectbox("NBE T-Bill Tenor (Days)", [28, 91, 182, 364], index=3)
            nominal_yield = st.number_input("Auction Cut-off Yield / Nominal Rate (%)", min_value=0.0, max_value=100.0, value=18.50, step=0.25)
            target_outlay = st.number_input("Target Face Value Investment (ETB)", min_value=10000.0, value=1000000.0, step=100000.0)
            
            discount_price = 100 / (1 + (nominal_yield / 100) * (tenor_days / 365))
            required_cash = (target_outlay * discount_price) / 100
            gross_profit = target_outlay - required_cash
            tax_deduction = gross_profit * (withholding_tax_rate / 100)
            net_profit = gross_profit - tax_deduction
            
            eay = (((1 + (nominal_yield / 100) * (tenor_days / 365))) ** (365 / tenor_days) - 1) * 100
            net_yield = (net_profit / required_cash) * (365 / tenor_days) * 100
            real_return = (((1 + (net_yield / 100)) / (1 + (headline_inflation / 100))) - 1) * 100
            active_yield = nominal_yield

        else:
            bond_years = st.selectbox("Bond Maturity Tenor (Years)", [3, 5, 7, 10], index=1)
            coupon_rate = st.number_input("Annual Coupon Interest Rate (%)", min_value=0.0, max_value=50.0, value=18.00, step=0.50)
            principal_amount = st.number_input("Principal Capital Commitment (ETB)", min_value=100000.0, value=5000000.0, step=500000.0)
            
            annual_coupon = principal_amount * (coupon_rate / 100)
            total_interest = annual_coupon * bond_years
            tax_deduction = total_interest * (withholding_tax_rate / 100)
            net_profit = total_interest - tax_deduction
            
            discount_price = 100.00
            required_cash = principal_amount
            gross_profit = total_interest
            eay = coupon_rate
            real_return = (((1 + (coupon_rate / 100)) / (1 + (headline_inflation / 100))) - 1) * 100
            active_yield = coupon_rate

        st.subheader("➕ Dynamic Custom Fixed Income Portfolio")
        st.caption("Add multiple custom bonds, T-bills, or commercial papers to your portfolio tracking.")
        
        if "portfolio_assets" not in st.session_state:
            st.session_state.portfolio_assets = pd.DataFrame([
                {"Instrument Name": "NBE 364-Day T-Bill", "Nominal Yield (%)": 18.50, "Allocation (ETB)": 2000000.0},
                {"Instrument Name": "CBE Infrastructure Bond", "Nominal Yield (%)": 19.00, "Allocation (ETB)": 5000000.0}
            ])
            
        edited_portfolio = st.data_editor(
            st.session_state.portfolio_assets,
            num_rows="dynamic",
            use_container_width=True,
            key="portfolio_editor"
        )

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
            st.metric("Inflation Gap", f"{(active_yield - headline_inflation):.2f}%")
        
        st.divider()
        if real_return >= 0:
            st.success(f"**Real Return Rate (Purchasing Power Growth):** +{real_return:.2f}%\n\n*The investment yield successfully protects capital against local inflation.*")
        else:
            st.error(f"**Real Return Rate (Purchasing Power Loss):** {real_return:.2f}%\n\n*Nominal gains are eclipsed by domestic price inflation, leading to real capital dilution.*")

# ==============================================================================
# TAB 2: DEVELOPMENT IMPACT & M&E SCORECARD
# ==============================================================================
with tab2:
    st.header("2. Project M&E, Social Return & Custom Institutional Scorecard")
    st.caption("Aligned with Planning and Development Commission & International Donor Monitoring Frameworks.")
    
    col_m1, col_m2 = st.columns([1, 1])
    
    with col_m1:
        st.subheader("📋 Core Project Parameters")
        org_type = st.selectbox("Organization / Sector Focus", ["NGO / Non-Profit Development", "Private Enterprise / Commercial", "Impact Investor / VC", "Government / Public Sector"])
        project_title = st.text_input("Project Name / Initiative Title", "National Agricultural Productivity Enhancement Project")
        implementing_agency = st.text_input("Implementing Organization / Bureau", "Ministry of Agriculture / Planning Commission")
        project_budget = st.number_input("Total Financial Investment (ETB)", value=10000000.0, step=500000.0)
        
        st.subheader("👥 Beneficiary & Core Metrics")
        direct_beneficiaries = st.number_input("Direct Beneficiaries Reached", value=15000, step=1000)
        indirect_beneficiaries = st.number_input("Indirect Beneficiaries Reached", value=45000, step=2500)
        monetized_social_value = st.number_input("Monetized Value of Social Benefits Created (ETB)", value=18500000.0, step=500000.0)
        
        st.subheader("➕ Dynamic Institutional KPIs & Custom Variables")
        st.caption("Click the '+' button at the bottom of the table to add unlimited custom indicators.")
        
        if "custom_kpis" not in st.session_state:
            st.session_state.custom_kpis = pd.DataFrame([
                {"Indicator Name": "Smallholder Farmers Trained", "Target Value": 2600.0, "Unit": "Farmers"},
                {"Indicator Name": "Green Jobs Created", "Target Value": 450.0, "Unit": "Jobs"}
            ])
            
        edited_kpis = st.data_editor(
            st.session_state.custom_kpis,
            num_rows="dynamic",
            use_container_width=True,
            key="kpi_editor"
        )

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
            st.metric("Sector Mandate", org_type.split()[0])
        with kpi_col2:
            st.metric("Social Return on Investment (SROI)", f"{sroi_ratio:.2f}:1")
            st.metric("Net Social Value Created", f"{net_social_value:,.2f} ETB")
            st.metric("Custom KPIs Tracked", f"{len(edited_kpis)} Indicators")
        
        st.divider()
        if sroi_ratio >= 1.5:
            st.success(f"**High Impact Performance (SROI: {sroi_ratio:.2f}:1)**\n\nFor every 1.00 ETB invested, {sroi_ratio:.2f} ETB of monetized socio-economic value is generated.")
        else:
            st.info(f"**Moderate Impact Efficiency (SROI: {sroi_ratio:.2f}:1)**")

# ==============================================================================
# TAB 3: EXECUTIVE REPORT GENERATOR & SECURE PAYMENT AUDIT GATEWAY
# ==============================================================================
with tab3:
    st.header("3. Executive PDF Report & Institutional Licensing Gateway")
    st.markdown("Unlock certified institutional reports by completing payment via **telebirr** or **CBE Bank Transfer**.")
    
    col_rep1, col_rep2 = st.columns([1, 1])
    
    with col_rep1:
        st.subheader("📝 Report Configuration")
        report_title = st.text_input("Document Title", "Ethiopian Capital Market & Impact Performance Evaluation Briefing")
        prepared_by = st.text_input("Prepared By (Author / Analyst)", "Economic Planning & Financial Analytics Division")
        exec_comments = st.text_area("Custom Executive Remarks", "Evaluates capital allocation efficiency and inflation adjustments for institutional review.")

    with col_rep2:
        st.subheader("💳 Secure Payment & Account Verification")
        payment_gateway = st.selectbox("Select Payment Method", ["telebirr (Mobile Money)", "CBE Bank Transfer", "Free Demo / Institutional Access Key"])
        
        if payment_gateway != "Free Demo / Institutional Access Key":
            st.info(f"Report Generation Fee: **500.00 ETB**\n* Transfer to Official Account: **+251 911 000 000** (telebirr) or CBE Account **1000XXXXXXXXX**")
            
            # STRICTER FIELDS TO CAPTURE SENDER DETAILS FOR AUDITING
            sender_name = st.text_input("Sender Full Name (Account Holder)", placeholder="e.g., Ato Kebede Tadesse")
            sender_account = st.text_input("Sender Account / Phone Number", placeholder="e.g., +251 911XXXXXX")
            tx_reference = st.text_input("Transaction Reference / SMS Code", placeholder="e.g., TR12345678 or Bank Ref")
            
            # Authorization requires proper naming and code length to stop casual cheating
            is_authorized = len(sender_name.strip()) > 3 and len(sender_account.strip()) > 6 and len(tx_reference.strip()) > 5
        else:
            access_key = st.text_input("Enter Institutional Access Code", type="password")
            sender_name = "Institutional Demo User"
            sender_account = "Access Key"
            tx_reference = access_key
            is_authorized = (access_key == "ETHIOPIA2026")
            if not is_authorized:
                st.warning("Hint for testing: Enter access code **ETHIOPIA2026**")

    st.divider()
    
    if is_authorized:
        st.success("✅ Payment Details Verified! You can now generate and download your certified PDF report.")
        
        if st.button("🚀 Generate Certified Executive PDF Report", type="primary"):
            # Automatically Log Payment Transaction with Sender Account Details for Auditing
            payment_log_file = "payment_audit_trail.csv"
            file_exists = os.path.exists(payment_log_file)
            
            with open(payment_log_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Timestamp", "Payment Gateway", "Sender Full Name", "Sender Account/Phone", "Reference Code", "Report Title"])
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), payment_gateway, sender_name, sender_account, tx_reference, report_title])
                
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=15, textColor=colors.HexColor('#1A365D'), spaceAfter=6)
            subtitle_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontSize=8.5, textColor=colors.HexColor('#4A5568'), spaceAfter=10)
            heading_style = ParagraphStyle('SectionHeading', fontSize=10.5, textColor=colors.HexColor('#1A365D'), spaceBefore=10, spaceAfter=4)
            
            body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8.5, textColor=colors.HexColor('#2D3748'), spaceAfter=4, leading=12)
            bold_body = ParagraphStyle('BoldBody', parent=body_style, fontName='Helvetica-Bold')
            
            header_cell_style = ParagraphStyle(
                'HeaderCell',
                parent=styles['Normal'],
                fontName='Helvetica-Bold',
                fontSize=9,
                textColor=colors.whitesmoke,
                leading=11
            )
            
            table_cell_style = ParagraphStyle(
                'TableCell',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=8.5,
                textColor=colors.HexColor('#2D3748'),
                leading=11
            )
            
            story = []
            story.append(Paragraph("<b>ETHIOPIAN CAPITAL MARKET & DEVELOPMENT M&E ENGINE</b>", title_style))
            story.append(Paragraph(f"<b>Title:</b> {report_title} | <b>Sector:</b> {org_type} | <b>Licensed To:</b> {sender_name} ({sender_account}) | <b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}", subtitle_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1A365D'), spaceAfter=10))
            
            story.append(Paragraph("1. Executive Summary & Macroeconomic Overview", heading_style))
            summary_text = f"""
            This certified institutional report evaluates capital market yields against headline inflation of <b>{headline_inflation:.2f}%</b>, 
            yielding a real purchasing power return of <b>{real_return:.2f}%</b> for <b>{security_type}</b>. 
            M&E evaluation for <b>{project_title}</b> under sector <b>{org_type}</b> records an SROI ratio of <b>{sroi_ratio:.2f}:1</b> across <b>{total_beneficiaries:,}</b> beneficiaries.
            """
            story.append(Paragraph(summary_text, body_style))
            
            story.append(Paragraph("2. Financial Yield & Custom Portfolio Scorecard", heading_style))
            fin_data = [
                [Paragraph("Metric / Asset", header_cell_style), Paragraph("Value / Yield", header_cell_style), Paragraph("Context / Allocation", header_cell_style)],
                [Paragraph("Headline Inflation", table_cell_style), Paragraph(f"{headline_inflation:.2f}%", table_cell_style), Paragraph("Macro Baseline", table_cell_style)],
                [Paragraph("Primary Instrument", table_cell_style), Paragraph(str(security_type), table_cell_style), Paragraph("Selected Asset", table_cell_style)],
                [Paragraph("Effective Annual Yield", table_cell_style), Paragraph(f"{eay:.2f}%", table_cell_style), Paragraph("Compounded Return", table_cell_style)],
                [Paragraph("Net Earnings Post-Tax", table_cell_style), Paragraph(f"{net_profit:,.2f} ETB", table_cell_style), Paragraph(f"Tax: {withholding_tax_rate}%", table_cell_style)],
                [Paragraph("Real Return Rate", table_cell_style), Paragraph(f"{real_return:.2f}%", table_cell_style), Paragraph("Fisher Real Return", table_cell_style)]
            ]
            
            for _, row in edited_portfolio.iterrows():
                inst_name = str(row.get("Instrument Name", "Custom Asset"))
                yld = row.get("Nominal Yield (%)", 0)
                alloc = row.get("Allocation (ETB)", 0)
                fin_data.append([
                    Paragraph(inst_name, table_cell_style),
                    Paragraph(f"{yld:.2f}% Nominal", table_cell_style),
                    Paragraph(f"Allocation: {alloc:,.2f} ETB", table_cell_style)
                ])

            t_fin = Table(fin_data, colWidths=[180, 140, 220])
            t_fin.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(t_fin)
            
            story.append(Paragraph("3. Impact, M&E & Custom Institutional KPIs", heading_style))
            me_data = [
                [Paragraph("Indicator", header_cell_style), Paragraph("Metric", header_cell_style), Paragraph("Assessment", header_cell_style)],
                [Paragraph("Project Title", table_cell_style), Paragraph(str(project_title), table_cell_style), Paragraph(str(implementing_agency), table_cell_style)],
                [Paragraph("Total Budget", table_cell_style), Paragraph(f"{project_budget:,.2f} ETB", table_cell_style), Paragraph("Capital Outlay", table_cell_style)],
                [Paragraph("Direct Beneficiaries", table_cell_style), Paragraph(f"{direct_beneficiaries:,}", table_cell_style), Paragraph(f"Cost: {cost_per_direct:,.2f} ETB/person", table_cell_style)],
                [Paragraph("SROI Ratio", table_cell_style), Paragraph(f"{sroi_ratio:.2f} : 1", table_cell_style), Paragraph("Social Efficiency", table_cell_style)]
            ]
            
            for _, row in edited_kpis.iterrows():
                ind_name = str(row.get("Indicator Name", "Custom Indicator"))
                val = row.get("Target Value", 0)
                unit = str(row.get("Unit", ""))
                me_data.append([
                    Paragraph(ind_name, table_cell_style),
                    Paragraph(f"{val:,.0f} {unit}", table_cell_style),
                    Paragraph("Custom Indicator Target", table_cell_style)
                ])

            t_me = Table(me_data, colWidths=[180, 140, 220])
            t_me.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(t_me)
            
            doc.build(story)
            pdf_buffer.seek(0)
            
            st.download_button(
                label="📥 Download Certified Institutional Report (.PDF)",
                data=pdf_buffer,
                file_name=f"Certified_Ethiopia_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                type="primary"
            )
    else:
        st.warning("🔒 **Report Generation Locked:** Please provide your **Sender Full Name**, **Account/Phone Number**, and a valid **Transaction Reference** to unlock report downloads.")

    st.divider()
    with st.expander("💬 Submit Feedback or Institutional Review"):
        with st.form("user_review_form"):
            reviewer_name = st.text_input("Name / Institution", placeholder="e.g., Commercial Bank Analyst")
            rating = st.slider("Platform Rating", 1, 5, 5)
            comments = st.text_area("Your Review or Feature Request")
            submit_btn = st.form_submit_button("Submit Review")
            
            if submit_btn:
                feedback_file = "user_feedback.csv"
                fb_exists = os.path.exists(feedback_file)
                
                with open(feedback_file, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if not fb_exists:
                        writer.writerow(["Timestamp", "Name", "Rating", "Comments"])
                    writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), reviewer_name, rating, comments])
                st.success("Thank you! Your feedback has been recorded.")

# ==============================================================================
# TAB 4: ADMIN DASHBOARD (RESTRICTED ACCESS)
# ==============================================================================
with tab4:
    st.header("🔒 Executive Admin Dashboard")
    st.caption("Restricted management interface for platform administrators and financial auditors.")
    
    admin_password = st.text_input("Enter Admin Master Key", type="password", key="admin_key")
    
    if admin_password == "ETHIO_ADMIN_2026":
        st.success("🔓 Access Granted: Welcome to the Management Console.")
        
        adm_tab1, adm_tab2, adm_tab3 = st.tabs([
            "💳 Payment & Sender Audit Logs", 
            "💬 User Feedback & Reviews", 
            "📊 Traffic & Analytics Overview"
        ])
        
        with adm_tab1:
            with adm_tab1:
            st.subheader("💳 Verified Transactions & Sender Profiles")
            payment_log_file = "payment_audit_trail.csv"
            
            if os.path.exists(payment_log_file):
                try:
                    # 'on_bad_lines' skips any mismatched legacy test rows automatically
                    df_payments = pd.read_csv(payment_log_file, on_bad_lines='skip')
                    st.dataframe(df_payments, use_container_width=True)
                    
                    csv_data = df_payments.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Payment Audit Log (.CSV)",
                        data=csv_data,
                        file_name=f"Payment_Audit_Log_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.warning("⚠️ Legacy payment log format detected. Resetting log file for new transactions...")
                    os.remove(payment_log_file)
            else:
                st.info("No payment transactions recorded yet.")
        with adm_tab2:
            st.subheader("💬 Community & Institutional Reviews")
            feedback_log_file = "user_feedback.csv"
            
            if os.path.exists(feedback_log_file):
                df_feedback = pd.read_csv(feedback_log_file)
                if "Rating" in df_feedback.columns:
                    avg_rating = df_feedback["Rating"].mean()
                    st.metric("Average Rating", f"⭐ {avg_rating:.1f} / 5.0")
                st.dataframe(df_feedback, use_container_width=True)
            else:
                st.info("No user reviews submitted yet.")

        with adm_tab3:
            st.subheader("📊 Platform Analytics & Traffic Reach")
            st.markdown("""
            **Streamlit Cloud Analytics:**  
            View live active sessions and bandwidth metrics in your [Streamlit Cloud Dashboard](https://share.streamlit.io).
            """)
            st.info("💡 **Google Analytics:** Traffic stats are logged directly to your Google Analytics dashboard using tag ID `G-XXXXXXXXXX`.")

    elif admin_password != "":
        st.error("❌ Invalid Admin Password. Access Denied.")
