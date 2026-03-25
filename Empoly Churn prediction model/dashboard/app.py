import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API = "http://127.0.0.1:8000"

st.set_page_config(layout="wide", page_title="Churn Intelligence", page_icon="⚡")

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0c10 !important;
    color: #e8eaf0 !important;
    font-family: 'DM Mono', monospace !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }

/* ── Hero ── */
.hero { padding: 2.5rem 0 1.5rem; border-bottom: 1px solid #1e2330; margin-bottom: 2rem; }
.hero-tag { font-size: 0.65rem; letter-spacing: 0.25em; color: #4ade80; text-transform: uppercase; margin-bottom: 0.4rem; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 2.6rem; font-weight: 800; letter-spacing: -0.03em; color: #f0f2f8; line-height: 1; margin: 0; }
.hero-title span { color: #f87171; }
.hero-sub { font-size: 0.72rem; color: #4a5270; margin-top: 0.5rem; letter-spacing: 0.08em; }

/* ── KPI Cards ── */
.kpi-card { background: #0f1219; border: 1px solid #1e2330; border-radius: 12px; padding: 1.4rem 1.6rem; position: relative; overflow: hidden; transition: border-color 0.2s; }
.kpi-card:hover { border-color: #2d3550; }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; }
.kpi-card.green::before  { background: linear-gradient(90deg, #4ade80, transparent); }
.kpi-card.red::before    { background: linear-gradient(90deg, #f87171, transparent); }
.kpi-card.blue::before   { background: linear-gradient(90deg, #60a5fa, transparent); }
.kpi-card.amber::before  { background: linear-gradient(90deg, #fbbf24, transparent); }
.kpi-label { font-size: 0.6rem; letter-spacing: 0.2em; text-transform: uppercase; color: #4a5270; margin-bottom: 0.5rem; }
.kpi-value { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 700; color: #f0f2f8; line-height: 1; }
.kpi-badge { display: inline-block; font-size: 0.6rem; padding: 2px 8px; border-radius: 20px; margin-top: 0.5rem; letter-spacing: 0.1em; }
.badge-green  { background: #0d2b1a; color: #4ade80; }
.badge-red    { background: #2b0d0d; color: #f87171; }
.badge-blue   { background: #0d1a2b; color: #60a5fa; }
.badge-amber  { background: #2b1e0d; color: #fbbf24; }

/* ── Section Headers ── */
.section-header { display: flex; align-items: center; gap: 0.6rem; margin: 2rem 0 1rem; }
.section-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.section-title { font-family: 'Syne', sans-serif; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #8892b0; }
.section-line { flex: 1; height: 1px; background: #1e2330; }

/* ── Panel ── */
.panel-title { font-family: 'Syne', sans-serif; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #8892b0; margin-bottom: 1.2rem; padding-bottom: 0.8rem; border-bottom: 1px solid #1e2330; }

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: #0a0c10 !important;
    border: 1px solid #1e2330 !important;
    color: #e8eaf0 !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}
label { color: #4a5270 !important; font-size: 0.65rem !important; letter-spacing: 0.12em !important; text-transform: uppercase !important; }

/* ── Buttons ── */
[data-testid="stButton"] button {
    background: #f87171 !important;
    color: #0a0c10 !important;
    border: none !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
[data-testid="stButton"] button:hover { opacity: 0.85 !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #0f1219;
    border-radius: 10px 10px 0 0;
    border: 1px solid #1e2330;
    border-bottom: none;
    padding: 0.3rem 0.5rem 0;
    gap: 0.2rem;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    color: #4a5270 !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 0.5rem 1.2rem !important;
    border: none !important;
    background: transparent !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #f0f2f8 !important;
    background: #0a0c10 !important;
    border-top: 2px solid #f87171 !important;
}
[data-testid="stTabPanel"] {
    background: #0a0c10;
    border: 1px solid #1e2330;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 1.5rem;
}

/* ── Prediction banner ── */
.pred-banner { border-radius: 10px; padding: 1.2rem 1.6rem; margin-top: 1rem; display: flex; align-items: center; gap: 1rem; }
.pred-banner.churn    { background: #2b0d0d; border: 1px solid #f87171; }
.pred-banner.retained { background: #0d2b1a; border: 1px solid #4ade80; }
.pred-icon  { font-size: 2rem; }
.pred-label { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 800; }
.pred-sub   { font-size: 0.65rem; color: #8892b0; letter-spacing: 0.1em; margin-top: 0.2rem; }
.pred-prob  { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; margin-left: auto; }
.gauge-track { background: #1e2330; border-radius: 99px; height: 8px; margin-top: 0.6rem; overflow: hidden; }
.gauge-fill  { height: 100%; border-radius: 99px; }

/* ── Misc ── */
[data-testid="stDataFrame"] { border: 1px solid #1e2330 !important; border-radius: 8px !important; overflow: hidden; }
hr { border-color: #1e2330 !important; }
</style>
""", unsafe_allow_html=True)


# ── PLOTLY THEME ──────────────────────────────────────────────────────────────
CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color="#8892b0", size=11),
    xaxis=dict(gridcolor="#1e2330", linecolor="#1e2330", tickcolor="#1e2330"),
    yaxis=dict(gridcolor="#1e2330", linecolor="#1e2330", tickcolor="#1e2330"),
    margin=dict(l=10, r=10, t=30, b=10),
    colorway=["#f87171","#60a5fa","#4ade80","#fbbf24","#c084fc","#34d399"],
)
def apply_theme(fig):
    fig.update_layout(**CHART_THEME)
    return fig


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">⚡ Real-time Analytics</div>
  <h1 class="hero-title">Churn <span>Intelligence</span></h1>
  <p class="hero-sub">CUSTOMER RETENTION PLATFORM · LIVE DATA</p>
</div>
""", unsafe_allow_html=True)


# ── FETCH DATA ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def fetch_dashboard():
    return requests.get(f"{API}/dashboard").json()

@st.cache_data(ttl=30)
def fetch_customers():
    return requests.get(f"{API}/customers").json()

try:
    data      = fetch_dashboard()
    customers = fetch_customers()
    df        = pd.DataFrame(customers)
    api_ok    = True
except Exception:
    st.error("⚠️  Cannot reach API at " + API)
    api_ok = False
    df   = pd.DataFrame()
    data = {"total_customers": 0, "churn_percentage": 0, "avg_monthly_charges": 0}


# ── KPI CARDS ─────────────────────────────────────────────────────────────────
total     = data.get("total_customers", 0)
churn_pct = round(data.get("churn_percentage", 0), 2)
avg_chg   = round(data.get("avg_monthly_charges", 0), 2)
high_risk = int(len(df[df["probability"] > 0.7])) if not df.empty and "probability" in df.columns else 0

c1, c2, c3, c4 = st.columns(4)
for col, color, label, value, badge_text, badge_cls in [
    (c1, "green",  "TOTAL CUSTOMERS",    f"{total:,}",    "ACTIVE",          "badge-green"),
    (c2, "red",    "CHURN RATE",          f"{churn_pct}%", "NEEDS ATTENTION", "badge-red"),
    (c3, "blue",   "AVG MONTHLY CHARGE",  f"${avg_chg}",   "PER CUSTOMER",    "badge-blue"),
    (c4, "amber",  "HIGH RISK",           f"{high_risk}",  "PROB > 70%",      "badge-amber"),
]:
    with col:
        st.markdown(f"""
        <div class="kpi-card {color}">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <span class="kpi-badge {badge_cls}">{badge_text}</span>
        </div>""", unsafe_allow_html=True)


# ── CHARTS ROW 1 ──────────────────────────────────────────────────────────────
if not df.empty:
    st.markdown("""<div class="section-header">
      <div class="section-dot" style="background:#f87171"></div>
      <span class="section-title">Churn Overview</span>
      <div class="section-line"></div></div>""", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.4, 1], gap="medium")
    with col_l:
        if "prediction" in df.columns:
            counts = df["prediction"].value_counts().reset_index()
            counts.columns = ["Status","Count"]
            counts["Status"] = counts["Status"].map(
                lambda x: "Churned" if str(x) in ["1","Yes","yes","true","True"] else "Retained")
            fig = px.pie(counts, values="Count", names="Status", hole=0.65,
                         color="Status", color_discrete_map={"Churned":"#f87171","Retained":"#1e2b3f"})
            fig.update_traces(textposition="outside", textinfo="percent+label",
                              textfont=dict(family="DM Mono",size=11,color="#8892b0"),
                              marker=dict(line=dict(color="#0a0c10",width=3)))
            fig = apply_theme(fig)
            fig.update_layout(showlegend=False, height=280,
                              title="Churn Distribution",
                              title_font=dict(family="Syne",size=13,color="#8892b0"))
            ret = round(counts.loc[counts["Status"]=="Retained","Count"].sum()/counts["Count"].sum()*100,1) if len(counts) else 0
            fig.add_annotation(text=f"<b>{ret}%</b><br><span style='font-size:9px'>RETAINED</span>",
                               x=0.5,y=0.5,showarrow=False,
                               font=dict(family="Syne",size=14,color="#f0f2f8"),align="center")
            st.plotly_chart(fig, use_container_width=True)

    with col_r:
        if "probability" in df.columns:
            fig2 = px.histogram(df, x="probability", nbins=20,
                                title="Risk Score Distribution",
                                color_discrete_sequence=["#f87171"])
            fig2.update_traces(marker_line_color="#0a0c10",marker_line_width=1)
            fig2 = apply_theme(fig2)
            fig2.update_layout(title_font=dict(family="Syne",size=13,color="#8892b0"),
                               showlegend=False, height=280, bargap=0.05,
                               xaxis_title="Churn Probability", yaxis_title="Customers")
            st.plotly_chart(fig2, use_container_width=True)


# ── CHARTS ROW 2 ──────────────────────────────────────────────────────────────
if not df.empty:
    st.markdown("""<div class="section-header">
      <div class="section-dot" style="background:#60a5fa"></div>
      <span class="section-title">Financial Signals</span>
      <div class="section-line"></div></div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns([1.6, 1], gap="medium")
    with col_a:
        if "MonthlyCharges" in df.columns:
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(y=df["MonthlyCharges"].reset_index(drop=True), mode="lines",
                                      fill="tozeroy", line=dict(color="#60a5fa",width=1.5),
                                      fillcolor="rgba(96,165,250,0.07)"))
            fig3 = apply_theme(fig3)
            fig3.update_layout(title="Monthly Charges · All Customers",
                               title_font=dict(family="Syne",size=13,color="#8892b0"),
                               showlegend=False, height=240,
                               xaxis_title="Customer Index", yaxis_title="$ Charge")
            st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        if "MonthlyCharges" in df.columns:
            mn,av,md,mx = (df["MonthlyCharges"].min(), df["MonthlyCharges"].mean(),
                           df["MonthlyCharges"].median(), df["MonthlyCharges"].max())
            fm = go.Figure(go.Bar(x=["Min","Avg","Median","Max"], y=[mn,av,md,mx],
                                  marker_color=["#1e2b3f","#60a5fa","#4ade80","#f87171"],
                                  text=[f"${v:.0f}" for v in [mn,av,md,mx]],
                                  textposition="outside",
                                  textfont=dict(size=10,family="DM Mono",color="#8892b0")))
            fm = apply_theme(fm)
            fm.update_layout(height=240, showlegend=False, yaxis_showticklabels=False,
                             xaxis_tickfont=dict(size=9), margin=dict(l=0,r=0,t=10,b=0))
            st.plotly_chart(fm, use_container_width=True)


# ── HIGH RISK TABLE ────────────────────────────────────────────────────────────
if not df.empty and "probability" in df.columns:
    st.markdown("""<div class="section-header">
      <div class="section-dot" style="background:#fbbf24"></div>
      <span class="section-title">High Risk Customers · probability &gt; 70%</span>
      <div class="section-line"></div></div>""", unsafe_allow_html=True)

    hr_df = df[df["probability"] > 0.7].copy()
    if hr_df.empty:
        st.markdown('<p style="color:#4a5270;font-size:0.8rem">No high-risk customers found.</p>', unsafe_allow_html=True)
    else:
        def tier(p):
            if p >= 0.9: return "🔴 Critical"
            if p >= 0.8: return "🟠 High"
            return "🟡 Elevated"
        hr_df["Risk Tier"]   = hr_df["probability"].apply(tier)
        hr_df["probability"] = hr_df["probability"].apply(lambda x: f"{x:.1%}")
        st.dataframe(hr_df, use_container_width=True,
                     height=min(300, 36+len(hr_df)*35),
                     column_config={
                         "probability": st.column_config.TextColumn("Churn Prob"),
                         "Risk Tier":   st.column_config.TextColumn("Risk Tier"),
                         "MonthlyCharges": st.column_config.NumberColumn("Monthly $", format="$%.2f"),
                     })


# ══════════════════════════════════════════════════════════════════════════════
# ── CUSTOMER MANAGEMENT TABS ──────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-header" style="margin-top:2.5rem">
  <div class="section-dot" style="background:#c084fc"></div>
  <span class="section-title">Customer Management</span>
  <div class="section-line"></div></div>""", unsafe_allow_html=True)

tab_search, tab_add, tab_update, tab_predict = st.tabs([
    "🔍  Search", "➕  Add Customer", "✏️  Update Customer", "⚡  Predict Churn"
])


# ── Shared form helper ────────────────────────────────────────────────────────
def customer_form(prefix, defaults=None):
    d = defaults or {}

    c1, c2, c3 = st.columns(3)
    with c1:
        gender     = st.selectbox("Gender",          ["Male","Female"],        key=f"{prefix}_gender",
                                  index=0 if d.get("gender","Male")=="Male" else 1)
        senior     = st.selectbox("Senior Citizen",  ["No","Yes"],             key=f"{prefix}_senior",
                                  index=int(d.get("SeniorCitizen",0)))
        partner    = st.selectbox("Partner",         ["Yes","No"],             key=f"{prefix}_partner",
                                  index=0 if d.get("Partner","Yes")=="Yes" else 1)
        dependents = st.selectbox("Dependents",      ["No","Yes"],             key=f"{prefix}_dep",
                                  index=0 if d.get("Dependents","No")=="No" else 1)
    with c2:
        tenure  = st.number_input("Tenure (months)",     min_value=0,   max_value=120,
                                   value=int(d.get("tenure",12)),    key=f"{prefix}_tenure")
        monthly = st.number_input("Monthly Charges ($)",  min_value=0.0,
                                   value=float(d.get("MonthlyCharges",65.0)), key=f"{prefix}_monthly", step=0.5)
        total   = st.number_input("Total Charges ($)",    min_value=0.0,
                                   value=float(d.get("TotalCharges",780.0)),  key=f"{prefix}_total",   step=1.0)
        phone   = st.selectbox("Phone Service", ["Yes","No"],                  key=f"{prefix}_phone",
                               index=0 if d.get("PhoneService","Yes")=="Yes" else 1)
    with c3:
        internet = st.selectbox("Internet Service", ["DSL","Fiber optic","No"], key=f"{prefix}_internet",
                                index=["DSL","Fiber optic","No"].index(d.get("InternetService","DSL")))
        contract = st.selectbox("Contract", ["Month-to-month","One year","Two year"], key=f"{prefix}_contract",
                                index=["Month-to-month","One year","Two year"].index(
                                    d.get("Contract","Month-to-month")))
        payment  = st.selectbox("Payment Method",
                                ["Electronic check","Mailed check",
                                 "Bank transfer (automatic)","Credit card (automatic)"],
                                key=f"{prefix}_payment",
                                index=["Electronic check","Mailed check",
                                       "Bank transfer (automatic)","Credit card (automatic)"].index(
                                    d.get("PaymentMethod","Electronic check")))
        paperless = st.selectbox("Paperless Billing", ["Yes","No"], key=f"{prefix}_paper",
                                 index=0 if d.get("PaperlessBilling","Yes")=="Yes" else 1)

    return {
        "gender": gender,
        "SeniorCitizen": 1 if senior=="Yes" else 0,
        "Partner": partner, "Dependents": dependents,
        "tenure": tenure, "MonthlyCharges": monthly, "TotalCharges": total,
        "PhoneService": phone, "InternetService": internet,
        "Contract": contract, "PaymentMethod": payment,
        "PaperlessBilling": paperless,
    }


# ── TAB 1 — SEARCH ────────────────────────────────────────────────────────────
with tab_search:
    ci_col, cb_col, _ = st.columns([1, 0.4, 2])
    with ci_col:
        customer_id = st.number_input("Customer ID", min_value=1, step=1,
                                      key="search_id", label_visibility="collapsed")
    with cb_col:
        do_search = st.button("Search →", key="btn_search")

    if do_search:
        with st.spinner("Fetching…"):
            try:   result = requests.get(f"{API}/customers/{customer_id}").json()
            except: result = {"error": "API unreachable"}

        if "error" in result:
            st.markdown('<p style="color:#f87171;font-size:0.8rem">⚠ Customer not found.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#4ade80;font-size:0.75rem;letter-spacing:0.1em">✓ RECORD FOUND</p>', unsafe_allow_html=True)
            prob = result.get("probability", 0)
            pred = result.get("prediction", "N/A")
            chg  = result.get("MonthlyCharges", 0)

            pc1, pc2, pc3 = st.columns(3)
            with pc1:
                st.markdown(f'<div class="kpi-card blue" style="padding:1rem"><div class="kpi-label">Monthly Charge</div><div class="kpi-value" style="font-size:1.4rem">${chg}</div></div>', unsafe_allow_html=True)
            with pc2:
                col = "red" if prob>0.7 else ("amber" if prob>0.4 else "green")
                st.markdown(f'<div class="kpi-card {col}" style="padding:1rem"><div class="kpi-label">Churn Probability</div><div class="kpi-value" style="font-size:1.4rem">{prob:.1%}</div></div>', unsafe_allow_html=True)
            with pc3:
                lbl = "Churner" if str(pred) in ["1","Yes","yes","true","True"] else "Retained"
                bc  = "red" if lbl=="Churner" else "green"
                st.markdown(f'<div class="kpi-card {bc}" style="padding:1rem"><div class="kpi-label">Prediction</div><div class="kpi-value" style="font-size:1.4rem">{lbl}</div></div>', unsafe_allow_html=True)

            if not df.empty and "MonthlyCharges" in df.columns:
                avg_c = df["MonthlyCharges"].mean()
                fc = go.Figure(go.Bar(
                    x=["This Customer","Avg Customer"], y=[chg, avg_c],
                    marker_color=["#f87171" if chg>avg_c else "#4ade80","#1e2b3f"],
                    text=[f"${chg:.2f}", f"${avg_c:.2f}"], textposition="outside",
                    textfont=dict(family="DM Mono",size=11,color="#8892b0")))
                fc = apply_theme(fc)
                fc.update_layout(title=f"Customer #{customer_id} · Charge vs Fleet Average",
                                 title_font=dict(family="Syne",size=12,color="#8892b0"),
                                 height=220, showlegend=False, yaxis_showticklabels=False,
                                 margin=dict(l=10,r=10,t=36,b=10))
                st.plotly_chart(fc, use_container_width=True)

            with st.expander("Raw JSON →"):
                st.json(result)


# ── TAB 2 — ADD CUSTOMER ──────────────────────────────────────────────────────
with tab_add:
    st.markdown('<div class="panel-title">➕ New Customer Details</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4a5270;font-size:0.72rem;margin-bottom:1.2rem">Fill in all fields and click Add Customer to create a new record.</p>', unsafe_allow_html=True)

    new_data = customer_form("add")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Add Customer →", key="btn_add"):
        with st.spinner("Saving…"):
            try:
                resp = requests.post(f"{API}/customers", json=new_data)
                if resp.status_code in (200, 201):
                    created = resp.json()
                    new_id  = created.get("id", created.get("customer_id", "—"))
                    st.markdown(f"""
                    <div style="background:#0d2b1a;border:1px solid #4ade80;border-radius:10px;
                                padding:1rem 1.4rem;margin-top:0.5rem">
                      <span style="color:#4ade80;font-family:'Syne',sans-serif;font-weight:700">
                        ✅ Customer added successfully!
                      </span><br>
                      <span style="color:#8892b0;font-size:0.72rem">New Customer ID: <b style="color:#f0f2f8">{new_id}</b></span>
                    </div>""", unsafe_allow_html=True)
                    with st.expander("View created record →"):
                        st.json(created)
                    st.cache_data.clear()
                else:
                    st.error(f"⚠ Error {resp.status_code}: {resp.text}")
            except Exception as e:
                st.error(f"⚠ API unreachable — {e}")


# ── TAB 3 — UPDATE CUSTOMER ───────────────────────────────────────────────────
with tab_update:
    st.markdown('<div class="panel-title">✏️ Update Existing Customer</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4a5270;font-size:0.72rem;margin-bottom:1rem">Enter the Customer ID, load the record, edit fields, then save.</p>', unsafe_allow_html=True)

    uid_col, ufetch_col, _ = st.columns([1, 0.5, 2])
    with uid_col:
        update_id = st.number_input("Customer ID to Update", min_value=1, step=1, key="update_id")
    with ufetch_col:
        st.markdown("<br>", unsafe_allow_html=True)
        fetch_btn = st.button("Load Record →", key="btn_fetch")

    if fetch_btn:
        with st.spinner("Loading…"):
            try:
                fetched = requests.get(f"{API}/customers/{update_id}").json()
                if "error" in fetched:
                    st.error("⚠ Customer not found.")
                    if "update_defaults" in st.session_state:
                        del st.session_state["update_defaults"]
                else:
                    st.session_state["update_defaults"]  = fetched
                    st.session_state["update_loaded_id"] = update_id
                    st.success(f"✓ Loaded customer #{update_id}")
            except:
                st.error("⚠ API unreachable.")

    if "update_defaults" in st.session_state:
        st.markdown('<hr style="border-color:#1e2330;margin:1rem 0">', unsafe_allow_html=True)
        upd_data = customer_form("upd", st.session_state["update_defaults"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save Changes →", key="btn_update"):
            uid = st.session_state["update_loaded_id"]
            with st.spinner("Updating…"):
                try:
                    resp = requests.put(f"{API}/customers/{uid}", json=upd_data)
                    if resp.status_code == 200:
                        st.markdown(f"""
                        <div style="background:#0d2b1a;border:1px solid #4ade80;border-radius:10px;
                                    padding:1rem 1.4rem;margin-top:0.5rem">
                          <span style="color:#4ade80;font-family:'Syne',sans-serif;font-weight:700">
                            ✅ Customer #{uid} updated!
                          </span>
                        </div>""", unsafe_allow_html=True)
                        with st.expander("View updated record →"):
                            st.json(resp.json())
                        st.cache_data.clear()
                        del st.session_state["update_defaults"]
                    else:
                        st.error(f"⚠ Error {resp.status_code}: {resp.text}")
                except Exception as e:
                    st.error(f"⚠ API unreachable — {e}")


# ── TAB 4 — PREDICT CHURN ─────────────────────────────────────────────────────
with tab_predict:
    st.markdown('<div class="panel-title">⚡ Real-time Churn Prediction</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4a5270;font-size:0.72rem;margin-bottom:1.2rem">Fill in customer details and get an instant ML prediction with risk factor breakdown.</p>', unsafe_allow_html=True)

    pred_data = customer_form("pred")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Run Prediction →", key="btn_predict"):
        with st.spinner("Running model…"):
            try:
                resp = requests.post(f"{API}/predict", json=pred_data)
                if resp.status_code == 200:
                    result   = resp.json()
                    prob     = float(result.get("probability", result.get("churn_probability", 0)))
                    pred_val = result.get("prediction", result.get("churn_prediction", 0))
                    is_churn = str(pred_val) in ["1","Yes","yes","true","True"] or prob >= 0.5

                    # ── Result banner ──
                    if is_churn:
                        st.markdown(f"""
                        <div class="pred-banner churn">
                          <div class="pred-icon">🔴</div>
                          <div>
                            <div class="pred-label" style="color:#f87171">LIKELY TO CHURN</div>
                            <div class="pred-sub">HIGH RETENTION RISK — IMMEDIATE ACTION RECOMMENDED</div>
                          </div>
                          <div class="pred-prob" style="color:#f87171">{prob:.1%}</div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="pred-banner retained">
                          <div class="pred-icon">🟢</div>
                          <div>
                            <div class="pred-label" style="color:#4ade80">LIKELY TO STAY</div>
                            <div class="pred-sub">LOW CHURN RISK — CUSTOMER IS STABLE</div>
                          </div>
                          <div class="pred-prob" style="color:#4ade80">{prob:.1%}</div>
                        </div>""", unsafe_allow_html=True)

                    # ── Gauge bar ──
                    fill = "linear-gradient(90deg,#f87171,#fbbf24)" if is_churn else "#4ade80"
                    st.markdown(f"""
                    <div style="margin-top:1rem">
                      <div style="display:flex;justify-content:space-between;
                                  font-size:0.6rem;color:#4a5270;margin-bottom:4px">
                        <span>0%  LOW RISK</span><span>HIGH RISK  100%</span>
                      </div>
                      <div class="gauge-track">
                        <div class="gauge-fill" style="width:{prob*100:.1f}%;background:{fill}"></div>
                      </div>
                    </div>""", unsafe_allow_html=True)

                    # ── Risk factor breakdown chart ──
                    st.markdown("<br>", unsafe_allow_html=True)
                    factors = {
                        "Contract Type":    1.0 if pred_data["Contract"]=="Month-to-month" else (0.4 if pred_data["Contract"]=="One year" else 0.1),
                        "Tenure":           max(0.0, round(1 - pred_data["tenure"]/72, 2)),
                        "Monthly Charges":  min(1.0, round(pred_data["MonthlyCharges"]/120, 2)),
                        "Internet Service": 0.85 if pred_data["InternetService"]=="Fiber optic" else (0.4 if pred_data["InternetService"]=="DSL" else 0.05),
                        "Payment Method":   0.75 if pred_data["PaymentMethod"]=="Electronic check" else 0.2,
                        "Paperless Billing":0.55 if pred_data["PaperlessBilling"]=="Yes" else 0.2,
                        "Senior Citizen":   0.6 if pred_data["SeniorCitizen"]==1 else 0.15,
                    }

                    bar_colors = ["#f87171" if v >= 0.6 else ("#fbbf24" if v >= 0.35 else "#4ade80")
                                  for v in factors.values()]

                    fig_risk = go.Figure(go.Bar(
                        x=list(factors.values()),
                        y=list(factors.keys()),
                        orientation="h",
                        marker_color=bar_colors,
                        text=[f"{v:.0%}" for v in factors.values()],
                        textposition="outside",
                        textfont=dict(size=10, family="DM Mono", color="#8892b0"),
                    ))
                    fig_risk = apply_theme(fig_risk)
                    fig_risk.update_layout(
                        title="Risk Factor Breakdown",
                        title_font=dict(family="Syne", size=13, color="#8892b0"),
                        height=280, showlegend=False,
                        xaxis=dict(range=[0,1.25], tickformat=".0%",
                                   gridcolor="#1e2330", linecolor="#1e2330"),
                        yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="#1e2330"),
                        margin=dict(l=10, r=60, t=40, b=10),
                    )
                    st.plotly_chart(fig_risk, use_container_width=True)

                    # ── Legend ──
                    st.markdown("""
                    <div style="display:flex;gap:1.5rem;font-size:0.62rem;color:#4a5270;margin-top:-0.5rem">
                      <span><span style="color:#f87171">■</span> High Risk ≥ 60%</span>
                      <span><span style="color:#fbbf24">■</span> Medium 35–59%</span>
                      <span><span style="color:#4ade80">■</span> Low &lt; 35%</span>
                    </div>""", unsafe_allow_html=True)

                    with st.expander("Full API Response →"):
                        st.json(result)

                else:
                    st.error(f"⚠ Prediction API error {resp.status_code}: {resp.text}")
            except Exception as e:
                st.error(f"⚠ API unreachable — {e}")
                st.info("Make sure your FastAPI backend has a `POST /predict` endpoint.")


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:3rem;padding-top:1.2rem;border-top:1px solid #1e2330;
            display:flex;justify-content:space-between;align-items:center;">
  <span style="font-size:0.6rem;letter-spacing:0.15em;color:#2d3550">CHURN INTELLIGENCE PLATFORM</span>
  <span style="font-size:0.6rem;color:#2d3550">LIVE · AUTO-REFRESH 30s</span>
</div>
""", unsafe_allow_html=True)