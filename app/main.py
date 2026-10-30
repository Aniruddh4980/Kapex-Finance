import streamlit as st
import pandas as pd
from prediction_helper import predict_risk

# ==================================================
# Page Configuration
# ==================================================
st.set_page_config(
    page_title="Kapex Finance | Credit Risk Engine",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# Modern Dark Glassmorphism & Bento Grid CSS
# ==================================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

        /* Global App Styling */
        .stApp {
            background: radial-gradient(circle at 15% 10%, #131c31 0%, #090d16 55%, #05070b 100%);
            color: #f8fafc;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1380px !important;
        }

        /* Top Navigation Banner */
        .top-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 1.25rem 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
        }

        .brand-box {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .brand-logo {
            width: 46px;
            height: 46px;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35);
        }

        .brand-title {
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }

        .brand-subtitle {
            font-size: 13px;
            color: #94a3b8;
            margin: 2px 0 0 0;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.25);
            color: #34d399;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.4px;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 10px #10b981;
        }

        /* Streamlit Container Borders Override for Glass Panels */
        div[data_and_notebooks-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(15, 23, 42, 0.55) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 20px !important;
            padding: 1.5rem 1.5rem 1.85rem 1.5rem !important;
            box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.4) !important;
        }

        /* Modernized Tabs */
        .stTabs [data_and_notebooks-baseweb="tab-list"] {
            gap: 12px;
            background-color: rgba(2, 6, 23, 0.6);
            padding: 6px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            margin-bottom: 1rem;
        }
        .stTabs [data_and_notebooks-baseweb="tab"] {
            height: 42px;
            padding: 0px 24px !important;
            border-radius: 10px;
            color: #94a3b8;
            font-weight: 600;
            font-size: 14px;
            border: none !important;
            background-color: transparent;
            transition: all 0.2s ease;
        }
        .stTabs [aria-selected="true"] {
            height: 45px !important;
            padding: 0px 12px !important;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%) !important;
            color: #ffffff !important;
            border: 1px solid rgba(99, 102, 241, 0.4) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }

        /* Input Labels */
        .stNumberInput label, .stSlider label, .stSelectbox label, .stRadio label {
            color: #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 13.5px !important;
        }

        /* Live Telemetry Strip */
        .telemetry-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 14px;
            margin-bottom: 8px;
        }

        .telemetry-card {
            background: rgba(2, 6, 23, 0.65);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 14px;
            padding: 14px 16px;
            transition: border-color 0.2s ease;
        }

        .telemetry-card:hover {
            border-color: rgba(99, 102, 241, 0.35);
        }

        .t-label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #64748b;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .t-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 20px;
            font-weight: 700;
            color: #f8fafc;
        }

        .t-sub {
            font-size: 11px;
            margin-top: 4px;
            font-weight: 600;
        }

        /* Primary CTA Button */
        div.stButton > button {
            width: 100%;
            height: 54px;
            background: linear-gradient(135deg, #3b82f6 0%, #6366f1 50%, #8b5cf6 100%);
            color: #ffffff;
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 0.3px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.5);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            margin-top: 10px;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.7);
            border-color: rgba(255, 255, 255, 0.3);
            color: #ffffff;
        }
        div.stButton > button:active {
            transform: translateY(0px);
        }

        /* Results Bento Cards */
        .bento-metric {
            background: rgba(2, 6, 23, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 16px;
            padding: 18px 20px;
            margin-top: 12px;
            margin-bottom: 23px;
        }

        .prob-bar-bg {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 999px;
            overflow: hidden;
            margin-top: 10px;
        }

        .empty-workbench {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 3.5rem 1.5rem;
            border: 1px dashed rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            background: rgba(2, 6, 23, 0.3);
            margin-top: 12px;
            margin-bottom: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# Top Navigation Bar
# ==================================================
st.markdown(
    """
    <div class="top-nav">
        <div class="brand-box">
            <div class="brand-logo">💳</div>
            <div>
                <div class="brand-title">KAPEX FINANCE</div>
                <div class="brand-subtitle">Autonomous Credit Underwriting & Default Telemetry</div>
            </div>
        </div>
        <div class="status-pill">
            <span class="pulse-dot"></span> RISK ENGINE READY
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# Main Split-Screen Workspace
# ==================================================
left_col, right_col = st.columns([1.35, 1], gap="large")

with left_col:
    with st.container(border=True):
        st.markdown("#### 🎛️ Applicant Configuration Studio")
        st.caption("Adjust parameters across the tabs below. Live financial ratios update automatically.")

        tab_profile, tab_credit, tab_collateral = st.tabs([
            "👤 Profile & Capital",
            "📈 Credit Velocity",
            "🏛️ Loan Structure"
        ])

        # --- TAB 1: Profile & Capital ---
        with tab_profile:
            c1, c2 = st.columns(2)
            with c1:
                age = st.slider("Applicant Age (Years)", min_value=18, max_value=100, value=32, step=1)
                income = st.number_input(
                    "Annual Gross Income (₹)",
                    min_value=0,
                    max_value=12000000,
                    value=1200000,
                    step=50000
                )
            with c2:
                loan_tenure_months = st.slider("Loan Tenure (Months)", min_value=6, max_value=360, value=60, step=6)
                loan_amount = st.number_input(
                    "Requested Loan Principal (₹)",
                    min_value=0,
                    max_value=50000000,
                    value=1500000,
                    step=50000
                )

        # --- TAB 2: Credit Velocity ---
        with tab_credit:
            c3, c4 = st.columns(2)
            with c3:
                credit_utilization_ratio = st.slider(
                    "Credit Utilization Ratio (%)",
                    min_value=0,
                    max_value=100,
                    value=35
                )
                delinquency_ratio = st.slider(
                    "Delinquency Ratio (%)",
                    min_value=0,
                    max_value=100,
                    value=5
                )
            with c4:
                avg_dpd_per_delinquency = st.number_input(
                    "Average DPD (Days Past Due)",
                    min_value=0,
                    max_value=100,
                    value=0,
                    step=1
                )
                number_of_open_accounts = st.number_input(
                    "Active Open Loan Accounts",
                    min_value=1,
                    max_value=100,
                    value=2,
                    step=1
                )

        # --- TAB 3: Loan Structure ---
        with tab_collateral:
            st.markdown("<div style='height: 6px'></div>", unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            with r1:
                residence_type = st.radio(
                    "Residence Ownership",
                    options=['Owned', 'Rented', 'Mortgage'],
                    horizontal=True
                )
                loan_type = st.radio(
                    "Collateral Structure",
                    options=['Secured', 'Unsecured'],
                    horizontal=True
                )
            with r2:
                loan_purpose = st.selectbox(
                    "Primary Loan Purpose",
                    options=['Home', 'Auto', 'Education', 'Personal']
                )

        # --- Real-Time Pre-Flight Telemetry Bar ---
        loan_to_income = loan_amount / income if income > 0 else 0.0
        est_monthly_obligation = (loan_amount / loan_tenure_months) if loan_tenure_months > 0 else 0.0

        if loan_to_income <= 2.0:
            lti_status, lti_color = "Optimal Leverage", "#10b981"
        elif loan_to_income <= 4.0:
            lti_status, lti_color = "Moderate Leverage", "#f59e0b"
        else:
            lti_status, lti_color = "High Leverage Alert", "#ef4444"

        if credit_utilization_ratio <= 30:
            util_status, util_color = "Healthy Buffer", "#10b981"
        elif credit_utilization_ratio <= 65:
            util_status, util_color = "Elevated Usage", "#f59e0b"
        else:
            util_status, util_color = "Maxed Capacity", "#ef4444"

        st.markdown(
            f"""
            <div class="telemetry-grid">
                <div class="telemetry-card">
                    <div class="t-label">Loan-to-Income (LTI)</div>
                    <div class="t-value">{loan_to_income:.2f}x</div>
                    <div class="t-sub" style="color: {lti_color};">● {lti_status}</div>
                </div>
                <div class="telemetry-card">
                    <div class="t-label">Principal / Month</div>
                    <div class="t-value">₹{est_monthly_obligation:,.0f}</div>
                    <div class="t-sub" style="color: #94a3b8;">Over {loan_tenure_months} months</div>
                </div>
                <div class="telemetry-card">
                    <div class="t-label">Revolving Utilization</div>
                    <div class="t-value">{credit_utilization_ratio}%</div>
                    <div class="t-sub" style="color: {util_color};">● {util_status}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        evaluate_btn = st.button("⚠️ Calculate Risk")

# ==================================================
# Right Column: Decision Engine & SVG Gauge
# ==================================================
with right_col:
    with st.container(border=True):
        st.markdown("#### 🛡️ Risk Intelligence Telemetry")
        st.caption("Real-time default probability, credit score gauge, and underwriting rating.")

        if evaluate_btn:
            try:
                probability, credit_score, rating = predict_risk(
                    age,
                    income,
                    loan_amount,
                    loan_tenure_months,
                    avg_dpd_per_delinquency,
                    delinquency_ratio,
                    credit_utilization_ratio,
                    number_of_open_accounts,
                    residence_type,
                    loan_purpose,
                    loan_type
                )

                rating_clean = str(rating).strip().lower()
                palette = {
                    "poor": {"color": "#ef4444", "bg": "rgba(239, 68, 68, 0.12)", "decision": "HIGH RISK — MANUAL REVIEW"},
                    "average": {"color": "#f59e0b", "bg": "rgba(245, 158, 11, 0.12)", "decision": "MODERATE RISK — CONDITIONAL"},
                    "good": {"color": "#3b82f6", "bg": "rgba(59, 130, 246, 0.12)", "decision": "LOW RISK — STANDARD APPROVAL"},
                    "excellent": {"color": "#10b981", "bg": "rgba(16, 185, 129, 0.12)", "decision": "PRIME TIER — AUTO APPROVE"}
                }
                theme = palette.get(rating_clean, {"color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.12)", "decision": "ASSESSMENT COMPLETE"})

                # Normalize Credit Score (300 - 900 scale) for SVG Semi-Circle Gauge
                norm_score = max(0.0, min(1.0, (float(credit_score) - 300.0) / 600.0))
                arc_length = 251.2  # Circumference of semi-circle with r=80
                dash_offset = arc_length * (1.0 - norm_score)
                prob_pct = min(100.0, max(0.0, float(probability) * 100.0))

                st.markdown(
                    f"""
                    <!-- Decision Badge -->
                    <div style="
                        background: {theme['bg']};
                        border: 1px solid {theme['color']}55;
                        color: {theme['color']};
                        padding: 10px 16px;
                        border-radius: 12px;
                        font-size: 12px;
                        font-weight: 800;
                        letter-spacing: 0.8px;
                        text-align: center;
                        margin-top: 8px;
                    ">
                        {theme['decision']}
                    </div>

                    <!-- Custom SVG Credit Score Speedometer -->
                    <div style="display: flex; flex-direction: column; align-items: center; margin: 18px 0 8px 0;">
                        <svg viewBox="0 0 200 115" width="240" height="140">
                            <defs>
                                <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" stop-color="#ef4444" />
                                    <stop offset="50%" stop-color="#f59e0b" />
                                    <stop offset="100%" stop-color="#10b981" />
                                </linearGradient>
                            </defs>
                            <!-- Background Track -->
                            <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="16" stroke-linecap="round"/>
                            <!-- Animated Value Arc -->
                            <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="url(#scoreGrad)" stroke-width="16" stroke-linecap="round"
                                  stroke-dasharray="{arc_length}" stroke-dashoffset="{dash_offset}"/>
                            <!-- Score Readout -->
                            <text x="100" y="82" text-anchor="middle" fill="#ffffff" font-size="34" font-weight="800" font-family="JetBrains Mono, monospace">{credit_score}</text>
                            <text x="100" y="102" text-anchor="middle" fill="#64748b" font-size="10" font-weight="700" letter-spacing="1.2">CREDIT SCORE (300-900)</text>
                        </svg>
                    </div>

                    <!-- Rating & Default Probability Bento Cards -->
                    <div class="bento-metric">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span class="t-label">Assigned Risk Rating</span>
                            <span style="font-size: 22px; font-weight: 800; color: {theme['color']};">{str(rating).upper()}</span>
                        </div>
                    </div>

                    <div class="bento-metric">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <span class="t-label">Default Probability</span>
                            <span class="t-value" style="color: {theme['color']};">{probability:.2%}</span>
                        </div>
                        <div class="prob-bar-bg">
                            <div style="width: {prob_pct:.1f}%; height: 100%; background: {theme['color']}; border-radius: 999px;"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b; margin-top: 6px;">
                            <span>0% (Safe)</span>
                            <span>100% (Default)</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error("Unable to execute prediction pipeline.")
                st.exception(e)
        else:
            # Idle Workbench State (Before Clicking Evaluate)
            st.markdown(
                """
                <div class="empty-workbench">
                    <div style="font-size: 42px; margin-bottom: 12px; opacity: 0.8;">🛰️</div>
                    <div style="font-size: 16px; font-weight: 700; color: #e2e8f0; margin-bottom: 6px;">
                        Awaiting Applicant Telemetry
                    </div>
                    <div style="font-size: 13px; color: #64748b; max-width: 280px; line-height: 1.5;">
                        Configure the applicant's capital profile and credit velocity on the left, then trigger the underwriting model to generate the live score gauge.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )