import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import csv
import requests
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

# ==============================================================================
# HELPER FUNCTIONS: SMS GATEWAY & CHAPA PAYMENT INTEGRATION
# ==============================================================================
def send_smsethiopia_alert(recipient_phone, message_text):
    """
    Triggers an instant SMS notification via SMSEthiopia HTTP API.
    """
    api_endpoint = "https://api.smsethiopia.com/v1/sms/send"
    api_key = st.secrets.get("SMSETHIOPIA_API_KEY", "YOUR_SMSETHIOPIA_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "msisdn": recipient_phone,
        "text": message_text
    }
    try:
        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        return {"sent": False, "description": str(e)}

def initialize_chapa_checkout(email, amount, currency, tx_ref, first_name, last_name, phone_number):
    """
    Initializes a checkout session using the Chapa Payment Gateway API.
    Supports local ETB (telebirr/CBE) and foreign USD credit card payments.
    """
    url = "https://api.chapa.co/v1/transaction/initialize"
    chapa_secret = st.secrets.get("CHAPA_SECRET_KEY", "CHASECK_TEST-xxxxxxxxxxxxxxxxxxxx")
    
    headers = {
        "Authorization": f"Bearer {chapa_secret}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": str(amount),
        "currency": currency,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "tx_ref": tx_ref,
        "callback_url": "https://share.streamlit.io",
        "customization": {
            "title": "EthioMarkets PDF License",
            "description": "Ethiopian Capital Market & Impact Analytics Briefing"
        }
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"status": "failed", "message": str(e)}

# ==============================================================================
# MAIN INTERFACE HEADER
# ==============================================================================
st.title("🇪🇹 Ethiopian Capital Market & Development M&E Analytics Engine")
st.markdown("""
**A Comprehensive Macroeconomic, Fixed Income Yield & Social Impact Evaluation Platform**  
*Designed for Commercial Banks, Institutional Investors, NGOs, Development Agencies, and Strategic Planning Sectors.*
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
    st.caption("Aligned with NGO, Development Agency & Strategic Sector Monitoring Frameworks.")
    
    col_m1, col_m2 = st.columns([1, 1])
    
    with col_m1:
        st.subheader("📋 Core Project Parameters")
        org_type = st.selectbox("Organization / Sector Focus", ["NGO / Non-Profit Development", "Private Enterprise / Commercial", "Impact Investor / VC", "Government / Public Sector"])
        project_title = st.text_input("Project Name / Initiative Title", "National Agricultural Productivity Enhancement Project")
        implementing_agency = st.text_input("Implementing Organization / Bureau", "Ministry of Agriculture / NGO Sector")
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
# TAB 3: EXECUTIVE REPORT GENERATOR & MULTI-CHANNEL PAYMENT GATEWAY
# ==============================================================================
with tab3:
    st.header("3. Executive PDF Report & Institutional Licensing Gateway")
    st.markdown("Unlock certified institutional reports by completing payment via **telebirr**, **International Remittance**, **CBE Bank Transfer**, or **USD Credit Cards**.")
    
    col_rep1, col_rep2 = st.columns([1, 1])
    
    with col_rep1:
        st.subheader("📝 Report Configuration")
        report_title = st.text_input("Document Title", "Ethiopian Capital Market & Impact Performance Evaluation Briefing")
        prepared_by = st.text_input("Prepared By (Author / Analyst)", "Economic Planning & Financial Analytics Division")
        exec_comments = st.text_area("Custom Executive Remarks", "Evaluates capital allocation efficiency and inflation adjustments for institutional review.")

    with col_rep2:
        st.subheader("💳 Secure Multi-Channel Payment & Verification")
        payment_gateway = st.selectbox(
            "Select Payment Channel", 
            ["1. telebirr / Remitly / Bank Transfer (Manual Verification)", "2. Automated Chapa Gateway (ETB / USD Cards)", "3. Enter Verified Access Key"]
        )
        
        is_authorized = False

        if payment_gateway == "1. telebirr / Remitly / Bank Transfer (Manual Verification)":
            st.info(
                "**Report Licensing Fee:** 500.00 ETB or $10.00 USD\n\n"
                "**📱 Option 1: Telebirr / Remitly / Sendwave**\n"
                "* **Account Name:** Belayhun Adefrese\n"
                "* **Phone Number:** `+251986884912`\n"
                "* **Accepted Services:** Telebirr, Sendwave, Remitly, WorldRemit\n\n"
                "**🏦 Option 2: Commercial Bank of Ethiopia (CBE)**\n"
                "* **Account Name:** Belayhun Adefrese Metaferia\n"
                "* **CBE Account:** `1000296269488`\n"
                "* **Bank Branch:** Lem Area Branch (Addis Ababa)"
            )
            
            sender_name = st.text_input("Sender Full Name (Account Holder)", placeholder="e.g., Belayhun Adefrese")
            sender_account = st.text_input("Sender Mobile / Account Number", placeholder="e.g., +251986884912 or CBE Account")
            tx_reference = st.text_input(
                "Transaction Reference / SMS Code / MTCN Code", 
                placeholder="e.g., TR98234101 (telebirr) or RMT123456 (Remitly MTCN)",
                help="Enter the exact receipt code from your transfer confirmation SMS or remittance email."
            )
            
            if st.button("📩 Submit Payment for Manual Verification", type="primary"):
                if len(sender_name.strip()) > 3 and len(sender_account.strip()) > 6 and len(tx_reference.strip()) > 5:
                    payment_log_file = "payment_audit_trail.csv"
                    file_exists = os.path.exists(payment_log_file)
                    
                    with open(payment_log_file, "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        if not file_exists:
                            writer.writerow(["Timestamp", "Payment Gateway", "Sender Full Name", "Sender Account/Phone", "Reference Code", "Report Title", "Status"])
                        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Manual Verification Request", sender_name, sender_account, tx_reference, report_title, "Pending Audit"])
                    
                    clean_client_phone = sender_account.replace("+", "").strip()
                    admin_phone = "251986884912"
                    
                    admin_message = f"VERIFY PAYMENT: 500 ETB claimed by {sender_name} ({clean_client_phone}). Ref: {tx_reference}."
                    send_smsethiopia_alert(admin_phone, admin_message)
                    
                    st.info("⏳ **Payment Claim Logged!** Our finance team is cross-checking your transaction reference against our bank/telebirr statements. Once verified, your report access key will be issued.")
                else:
                    st.error("❌ Please fill in all fields accurately with your genuine transfer receipt details.")

        elif payment_gateway == "2. Automated Chapa Gateway (ETB / USD Cards)":
            st.caption("Automated instant verification for local ETB mobile money and foreign USD Visa/Mastercard transactions.")
            ch_currency = st.radio("Select Billing Currency", ["ETB (500.00 ETB)", "USD ($10.00 USD)"])
            ch_amount = 500.0 if "ETB" in ch_currency else 10.0
            curr_code = "ETB" if "ETB" in ch_currency else "USD"
            
            ch_email = st.text_input("Customer Email Address", placeholder="user@institution.com")
            ch_phone = st.text_input("Mobile Phone Number", placeholder="251911XXXXXX")
            ch_name = st.text_input("Full Name", placeholder="Ato Kebede Tadesse")
            
            if st.button("🚀 Proceed to Chapa Payment Gateway", type="primary"):
                if ch_email and ch_phone and ch_name:
                    tx_ref = f"ETHIO-{curr_code}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    ch_res = initialize_chapa_checkout(
                        email=ch_email,
                        amount=ch_amount,
                        currency=curr_code,
                        tx_ref=tx_ref,
                        first_name=ch_name.split()[0],
                        last_name=ch_name.split()[-1] if len(ch_name.split()) > 1 else "User",
                        phone_number=ch_phone
                    )
                    
                    if ch_res.get("status") == "success":
                        checkout_url = ch_res["data"]["checkout_url"]
                        st.success("✅ Payment session created!")
                        st.markdown(f"[👉 Click Here to Open Secure Payment Checkout Page]({checkout_url})")
                    else:
                        st.error(f"Gateway Error: {ch_res.get('message', 'Initialization failed')}")
                else:
                    st.error("Please fill in your email, phone, and name to proceed.")

        else:
            access_key = st.text_input("Enter Approved Access Key", type="password")
            sender_name = "Licensed Institutional User"
            sender_account = "Authorized Key"
            
            is_authorized = (access_key == "ETHIOPIA2026")
            if not is_authorized and access_key != "":
                st.error("❌ Invalid or Unverified Access Key. Please complete payment verification first.")
            elif not is_authorized:
                st.warning("Hint for testing: Enter access key **ETHIOPIA2026**")

    st.divider()
    
    if is_authorized:
        st.success("✅ Access Key Authorized! You can now generate and download your certified PDF report.")
        
        if st.button("🚀 Generate Certified Executive PDF Report", type="primary"):
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=15, textColor=colors.HexColor('#1A365D'), spaceAfter=6)
            subtitle_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontSize=8.5, textColor=colors.HexColor('#4A5568'), spaceAfter=10)
            heading_style = ParagraphStyle('SectionHeading', fontSize=10.5, textColor=colors.HexColor('#1A365D'), spaceBefore=10, spaceAfter=4)
            body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8.5, textColor=colors.HexColor('#2D3748'), spaceAfter=4, leading=12)
            
            header_cell_style = ParagraphStyle('HeaderCell', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.whitesmoke, leading=11)
            table_cell_style = ParagraphStyle('TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor('#2D3748'), leading=11)
            
            story = []
            story.append(Paragraph("<b>ETHIOPIAN CAPITAL MARKET & DEVELOPMENT M&E ENGINE</b>", title_style))
            story.append(Paragraph(f"<b>Title:</b> {report_title} | <b>Sector:</b> {org_type} | <b>Licensed To:</b> {sender_name} | <b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}", subtitle_style))
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
        st.warning("🔒 **Report Downloads Protected:** Submit your transaction verification request or enter an active access key to unlock.")

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
            "💳 Pending & Verified Payments", 
            "💬 User Feedback & Reviews", 
            "📊 Traffic & Analytics Overview"
        ])
        
        with adm_tab1:
            st.subheader("💳 Verified Transactions & Pending Payment Claims")
            payment_log_file = "payment_audit_trail.csv"
            
            if os.path.exists(payment_log_file):
                try:
                    df_payments = pd.read_csv(payment_log_file, on_bad_lines='skip')
                    st.dataframe(df_payments, use_container_width=True)
                    
                    csv_data = df_payments.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Payment Audit Log (.CSV)",
                        data=csv_data,
                        file_name=f"Payment_Audit_Log_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                except Exception:
                    os.remove(payment_log_file)
                    st.rerun()
            else:
                st.info("No payment transactions recorded yet.")

        with adm_tab2:
            st.subheader("💬 Community & Institutional Reviews")
            feedback_log_file = "user_feedback.csv"
            
            if os.path.exists(feedback_log_file):
                try:
                    df_feedback = pd.read_csv(feedback_log_file, on_bad_lines='skip')
                    if "Rating" in df_feedback.columns:
                        avg_rating = df_feedback["Rating"].mean()
                        st.metric("Average Rating", f"⭐ {avg_rating:.1f} / 5.0")
                    st.dataframe(df_feedback, use_container_width=True)
                except Exception:
                    os.remove(feedback_log_file)
                    st.rerun()
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
