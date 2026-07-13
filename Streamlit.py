import streamlit as st
import requests

st.set_page_config(page_title="FinGuard AI - Tech Girl Dashboard", page_icon="🏦", layout="wide")

# Styling Header Theme
st.markdown("<h1 style='color: #0b6623;'>🏦 FinGuard AI - Risk Assessment Framework</h1>", unsafe_allow_html=True)
st.markdown("### Powered by LangSmith Observability Platform | Track: Default Prediction Model")
st.write("---")

# Layout Split
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Document Ingestion Pipeline")
    company = st.text_input("MSME Company Name", value="Balaji Manufacturing Ltd")
    webhook = st.text_input("Target Webhook URL Endpoint", value="https://api.idbi.com/v1/credit-listener")
    
    raw_text = st.text_area(
        "Ingested Financial Text / Unstructured Ledgers", 
        value="Annual Net Operating Income: 175000.\nTotal Debt Obligations: 100000.\nNote: Check for balance sheet math adjustments.",
        height=250
    )
    
    # Injecting a test anomaly control to showcase Reverse Prompt Engineering
    inject_error = st.checkbox("Simulate Balance Sheet Math Mismatch (Trigger Mistake Audit Engine)")
    if inject_error:
        raw_text += "\n[ALERT SYSTEM]: Internal balance mismatch found in liabilities column calculation."

    run_btn = st.button("Execute Credit Audit Pipeline", type="primary")

with col2:
    st.subheader("🔍 Real-Time Analysis & System Tracing Metrics")
    
    if run_btn:
        with st.spinner("Executing RTF/TCI Prompt Chains and Auditing Backward Lineage..."):
            payload = {
                "company_name": company,
                "raw_financial_text": raw_text,
                "webhook_url": webhook
            }
            
            try:
                # Call local FastAPI App backend
                response = requests.post("http://localhost:8000/api/v1/analyze-credit", json=payload)
                
                if response.status_code == 200:
                    res_data = response.json()
                    
                    # Display metrics summary block
                    m_col1, m_col2, m_col3 = st.columns(3)
                    m_col1.metric("Baseline DSCR", f"{res_data['baseline_dscr']}x")
                    m_col2.metric("Stressed DSCR (+200bps)", f"{res_data['stressed_dscr']}x")
                    m_col3.metric("Cash Runway Status", f"{res_data['cash_runway_months']} Months")
                    
                    st.success(f"Risk Evaluation Result: **{res_data['default_risk_tier']}**")
                    
                    st.write("#### 🛡️ Generated Audit Justification:")
                    st.info(res_data['audit_justification'])
                    
                    st.write("#### 🚨 Mistake Finding Engine Log:")
                    if res_data['anomalies_found']:
                        for anomaly in res_data['anomalies_found']:
                            st.error(anomaly)
                    else:
                        st.success("Zero financial anomalies or mathematical extrapolation loops detected during RPE check.")
                        
                    st.toast("Telemetry data successfully broadcast to core banking webhook system.")
                    
                else:
                    st.error("Error communicating with backend application services.")
            except Exception as e:
                st.error(f"Failed to connect to backend engine instance: {str(e)}")
