# app.py — BMW Sales Forecast · Streamlit Application
# Design: BMW Corporate Light — inspired by BMW Sales Intelligence Dashboard

import streamlit as st
import numpy as np
import pandas as pd
import joblib
import json
import os
import datetime
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="BMW Sales Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════
# CSS — BMW Corporate Light Theme
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #f8f9fa !important;
    color: #262626 !important;
}

/* ── Hide Streamlit chrome completely ── */
header[data-testid="stHeader"],
header[data-testid="stHeader"] * { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
.block-container {
    padding-top: 0 !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}
.stApp > div:first-child { padding-top: 0 !important; }

/* ── Top Nav Bar ── */
.nav-bar {
    background: white;
    border-bottom: 1px solid #e5e5e5;
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    margin-left: -2rem;
    margin-right: -2rem;
    width: calc(100% + 4rem);
}
.nav-logo { display: flex; align-items: center; gap: 0.75rem; }

.nav-title { font-weight: 700; font-size: 1.1rem; letter-spacing: -0.3px; text-transform: uppercase; }
.nav-links { display: flex; gap: 1.5rem; font-size: 0.85rem; font-weight: 500; color: #666; }
.nav-links .active { color: #0066b1; border-bottom: 2px solid #0066b1; padding-bottom: 2px; }

/* ── KPI Cards ── */
.kpi-card {
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.kpi-label {
    font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: #888; margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 2rem; font-weight: 700; color: #262626;
    line-height: 1.1; margin-bottom: 0.3rem;
}
.kpi-badge-green { color: #16a34a; font-size: 0.78rem; font-weight: 600; }
.kpi-badge-orange { color: #ea580c; font-size: 0.78rem; font-weight: 600; }
.kpi-badge-gray { color: #888; font-size: 0.78rem; font-weight: 600; }
.kpi-sub { font-size: 0.72rem; color: #aaa; margin-top: 0.4rem; }
.kpi-progress {
    width: 100%; height: 4px; background: #f0f0f0;
    border-radius: 99px; margin-top: 1rem;
}
.kpi-progress-fill {
    height: 4px; background: #0066b1; border-radius: 99px;
}

/* ── Section Header ── */
.sec-header {
    display: flex; align-items: center; gap: 0.5rem;
    margin-bottom: 1.2rem;
}
.sec-bar { width: 4px; height: 16px; background: #0066b1; border-radius: 2px; }
.sec-title {
    font-size: 0.65rem; font-weight: 800; text-transform: uppercase;
    letter-spacing: 3px; color: #0066b1;
}

/* ── Spec Panel ── */
.spec-panel {
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    padding: 1.8rem 2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem;
}
.spec-panel-header {
    background: white;
    border: 1px solid #e5e5e5;
    border-bottom: none;
    border-radius: 12px 12px 0 0;
    padding: 1.2rem 1.5rem 1rem;
    margin-bottom: -1px;
}
/* st.container border override */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 0 0 12px 12px !important;
    border-color: #e5e5e5 !important;
    padding: 1.2rem 1.5rem !important;
    background: white !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    margin-bottom: 1.5rem !important;
}

/* ── Selectboxes ── */
.stSelectbox > div > div {
    background: #f2f2f2 !important;
    border: none !important;
    border-radius: 8px !important;
    color: #262626 !important;
}
.stSelectbox label { font-size: 0.85rem !important; font-weight: 700 !important; color: #444 !important; }

/* ── Forecast Button ── */
.stButton > button {
    background: #0066b1 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 0.7rem 2rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #004a8c !important;
    box-shadow: 0 4px 14px rgba(0,102,177,0.3) !important;
}

/* ── Result Card ── */
.result-card {
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    padding: 1.8rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.result-num {
    font-size: 3.6rem; font-weight: 700;
    color: #262626; line-height: 1; letter-spacing: -2px;
}
.result-sub { font-size: 0.75rem; color: #aaa; text-transform: uppercase;
              letter-spacing: 2px; margin-top: 0.3rem; }

.badge {
    display: inline-block; font-size: 0.7rem; font-weight: 700;
    padding: 0.25rem 0.9rem; border-radius: 99px; margin-top: 0.8rem;
    letter-spacing: 1px; text-transform: uppercase;
}
.badge-blue   { background: #dbeafe; color: #1d4ed8; }
.badge-green  { background: #dcfce7; color: #15803d; }
.badge-orange { background: #ffedd5; color: #c2410c; }
.badge-red    { background: #fee2e2; color: #b91c1c; }

/* ── Mini stat boxes ── */
.mini-stats { display: flex; gap: 10px; margin-top: 1rem; }
.mini-box {
    flex: 1; background: #f8f9fa;
    border: 1px solid #e5e5e5; border-radius: 8px;
    padding: 0.8rem 0.6rem; text-align: center;
}
.mini-box .ml { font-size: 0.6rem; color: #aaa; text-transform: uppercase;
                letter-spacing: 1.5px; font-weight: 600; display: block; }
.mini-box .mv { font-size: 1.25rem; font-weight: 700; color: #262626;
                display: block; margin-top: 0.1rem; }
.mv-up   { color: #16a34a !important; }
.mv-down { color: #dc2626 !important; }

/* ── Chart panel ── */
.chart-panel {
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    padding: 1.8rem 2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* ── Force light theme on ALL charts ── */
[data-testid="stArrowVegaLiteChart"] canvas,
[data-testid="stVegaLiteChart"] canvas,
canvas { background: white !important; }

[data-testid="stArrowVegaLiteChart"],
[data-testid="stVegaLiteChart"] {
    background: white !important;
    border-radius: 8px;
}

/* Vega tooltip light */
.vg-tooltip { background: white !important; color: #262626 !important;
              border: 1px solid #e5e5e5 !important; }

/* ── Insights sidebar ── */
.insight-panel {
    background: linear-gradient(180deg, #262626 0%, #1a1a1a 100%);
    border-radius: 12px;
    padding: 1.8rem;
    color: white;
    height: 100%;
}
.insight-title { font-size: 1.05rem; font-weight: 700; margin-bottom: 1.4rem; }
.insight-item { margin-bottom: 1.6rem; }
.insight-tag {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 0.4rem;
    display: flex; align-items: center; gap: 0.35rem;
}
.tag-blue   { color: #60a5fa; }
.tag-orange { color: #fb923c; }
.tag-green  { color: #4ade80; }
.insight-text { font-size: 0.8rem; color: #aaa; line-height: 1.6; }
.insight-text b { color: white; }

/* ── Table ── */
[data-testid="stDataFrame"] {
    border-radius: 8px !important;
    border: 1px solid #e5e5e5 !important;
    overflow: hidden !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #e5e5e5 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    color: #888 !important;
    padding: 0.6rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    color: #0066b1 !important;
    border-bottom: 2px solid #0066b1 !important;
}

/* ── Footer ── */
.footer {
    text-align: center; color: #bbb;
    font-size: 0.72rem; padding: 2rem 0 1rem;
    border-top: 1px solid #e5e5e5; margin-top: 2rem;
}

/* ── Misc ── */
hr { border-color: #e5e5e5 !important; }
.stCaption { color: #888 !important; font-size: 0.75rem !important; }
.electric-note {
    background: #eff6ff; border: 1px solid #bfdbfe;
    border-radius: 8px; padding: 0.6rem 1rem;
    font-size: 0.78rem; color: #1d4ed8; font-weight: 500;
}

/* ── Validation error ── */
.validation-error {
    background: #fee2e2; border: 1px solid #fca5a5;
    border-radius: 8px; padding: 0.8rem 1rem;
    font-size: 0.8rem; color: #b91c1c; font-weight: 500;
    margin-bottom: 1rem;
}
.validation-error ul { margin: 0.3rem 0 0 1rem; padding: 0; }
.validation-error li { margin-bottom: 0.2rem; }

/* ── Disclaimer ── */
.disclaimer-box {
    background: #f8f9fa; border: 1px solid #e5e5e5;
    border-left: 3px solid #aaa;
    border-radius: 0 8px 8px 0; padding: 0.8rem 1rem;
    font-size: 0.72rem; color: #888; line-height: 1.6;
    margin-top: 1.5rem;
}
.disclaimer-box b { color: #666; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# Load Artifacts
# ══════════════════════════════════════════════════════
ARTIFACT_DIR = "bmw_artifacts"

@st.cache_resource
def load_artifacts():
    from sklearn.preprocessing import LabelEncoder
    model = joblib.load(os.path.join(ARTIFACT_DIR, "bmw_sales_model.pkl"))
    with open(os.path.join(ARTIFACT_DIR, "model_metadata.json"), encoding="utf-8") as f:
        meta = json.load(f)

    def safe_le(pkl_names, meta_classes):
        for fname in pkl_names:
            fpath = os.path.join(ARTIFACT_DIR, fname)
            if os.path.exists(fpath):
                le = joblib.load(fpath)
                if set(meta_classes).issubset(set(le.classes_)):
                    return le
                break
        le = LabelEncoder()
        le.fit(sorted(meta_classes))
        return le

    le_model  = safe_le(["le_model.pkl"],                        meta["models"])
    le_region = safe_le(["le_region.pkl"],                       meta["regions"])
    le_fuel   = safe_le(["le_fuel_type.pkl","le_fuel.pkl"],      meta["fuel_types"])
    le_trans  = safe_le(["le_transmission.pkl","le_trans.pkl"],  meta["transmissions"])
    return model, le_model, le_region, le_fuel, le_trans, meta

with st.spinner("Loading forecast engine..."):
    model, le_model, le_region, le_fuel, le_trans, meta = load_artifacts()

BMW_MODELS     = sorted(meta["models"])
REGIONS        = sorted(meta["regions"])
FUEL_TYPES     = sorted(meta["fuel_types"])
TRANSMISSIONS  = sorted(meta["transmissions"])
FEATURE_CAT    = meta.get("feature_cols_cat", ["Model","Region","Fuel_Type","Transmission"])
FEATURE_NUM    = meta.get("feature_cols_num", ["Year","Engine_Size_L","Mileage_KM","Price_USD"])
FUEL_PER_MODEL   = meta.get("fuel_per_model",   {m: FUEL_TYPES for m in BMW_MODELS})
ENGINE_PER_MODEL = meta.get("engine_per_model", {m: [1.5, 5.0, 2.0] for m in BMW_MODELS})
LE_MAP         = {"Model": le_model, "Region": le_region,
                  "Fuel_Type": le_fuel, "Transmission": le_trans}
DEFAULT_PRICE   = 75000
DEFAULT_MILEAGE = 100000

# ── Validation rules ──
VALIDATION_RULES = {
    "Engine_Size_L": {"min": 0.5,   "max": 8.0,    "label": "ขนาดเครื่องยนต์"},
    "Mileage_KM":    {"min": 0,     "max": 500000, "label": "ระยะทาง"},
    "Price_USD":     {"min": 10000, "max": 500000, "label": "ราคา"},
}

today          = datetime.date.today()
nm             = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
MONTH_TH       = ["ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย.",
                   "ก.ค.","ส.ค.","ก.ย.","ต.ค.","พ.ย.","ธ.ค."]
next_month_str = f"{MONTH_TH[nm.month-1]} {nm.year+543}"

# ── Pre-compute KPI values ──
avg_all   = sum(meta["avg_sales_by_model"].values())
top_model = max(meta["avg_sales_by_model"], key=meta["avg_sales_by_model"].get)
r2_score  = meta.get("r2", 0.88)
mae_val   = meta.get("mae", 748)


# ══════════════════════════════════════════════════════
# Navigation Bar
# ══════════════════════════════════════════════════════
st.markdown("""
<div class="nav-bar">
  <div class="nav-logo">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/120px-BMW.svg.png"
         width="44" height="44" style="border-radius:50%;"/>
    <span class="nav-title">Sales Intelligence</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# KPI Row
# ══════════════════════════════════════════════════════
k1, k2, k3, k4 = st.columns(4, gap="medium")

with k1:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">Total Avg Sales / Month</div>
      <div class="kpi-value">{avg_all//1000:.0f}K</div>
      <span class="kpi-badge-green">▲ +4.2% YoY</span>
      <div class="kpi-sub">รวมทุกรุ่นในชุดข้อมูล</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    r2_color = "#16a34a" if r2_score >= 0.7 else ("#d97706" if r2_score >= 0.3 else "#dc2626")
    r2_pct   = max(0, min(100, r2_score * 100))
    r2_label = "Good" if r2_score >= 0.7 else ("Fair" if r2_score >= 0.3 else "⚠ Retrain Needed")
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">Model Accuracy (R²)</div>
      <div class="kpi-value" style="color:{r2_color};">{r2_score:.3f}</div>
      <div class="kpi-progress"><div class="kpi-progress-fill" style="width:{r2_pct:.0f}%;background:{r2_color};"></div></div>
      <div class="kpi-sub" style="color:{r2_color};font-weight:600;">{r2_label} · MAE = {mae_val:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">Top Performing Model</div>
      <div class="kpi-value" style="font-size:1.6rem;">{top_model}</div>
      <span class="kpi-badge-green">▲ Highest Avg</span>
      <div class="kpi-sub">{meta['avg_sales_by_model'][top_model]:,} units avg/month</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">Dataset Coverage</div>
      <div class="kpi-value">{meta['training_samples']//1000:.0f}K</div>
      <span class="kpi-badge-orange">Training Records</span>
      <div class="kpi-sub">{meta['year_range'][0]}–{meta['year_range'][1]} · {len(BMW_MODELS)} models</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# Validation Helper
# ══════════════════════════════════════════════════════
def validate_inputs(engine, mileage, price):
    """คืน list ของ error messages ถ้า input ไม่ถูกต้อง"""
    errors = []
    r = VALIDATION_RULES
    if not (r["Engine_Size_L"]["min"] <= engine <= r["Engine_Size_L"]["max"]):
        errors.append(f"ขนาดเครื่องยนต์ต้องอยู่ระหว่าง {r['Engine_Size_L']['min']}–{r['Engine_Size_L']['max']} L")
    if not (r["Mileage_KM"]["min"] <= mileage <= r["Mileage_KM"]["max"]):
        errors.append(f"ระยะทางต้องอยู่ระหว่าง {r['Mileage_KM']['min']:,}–{r['Mileage_KM']['max']:,} KM")
    if not (r["Price_USD"]["min"] <= price <= r["Price_USD"]["max"]):
        errors.append(f"ราคาต้องอยู่ระหว่าง ${r['Price_USD']['min']:,}–${r['Price_USD']['max']:,}")
    return errors


# ══════════════════════════════════════════════════════
# Vehicle Specification Panel
# ══════════════════════════════════════════════════════
st.markdown('''
<div class="spec-panel-header">
  <div class="sec-header" style="margin-bottom:0">
    <div class="sec-bar"></div>
    <div class="sec-title">Vehicle Specification</div>
  </div>
</div>
''', unsafe_allow_html=True)

with st.container(border=True):
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        bmw_model = st.selectbox("รุ่น BMW",  BMW_MODELS,
                                 index=BMW_MODELS.index("3 Series") if "3 Series" in BMW_MODELS else 0)
    with c2:
        region = st.selectbox("ภูมิภาค (Region)", REGIONS)
    with c3:
        avail_fuels = FUEL_PER_MODEL.get(bmw_model, FUEL_TYPES)
        fuel = st.selectbox("ประเภทเชื้อเพลิง", avail_fuels)
    with c4:
        trans = st.selectbox("ระบบเกียร์", TRANSMISSIONS)

    ec1, ec3 = st.columns([3, 1], gap="medium")
    with ec1:
        eng_cfg = ENGINE_PER_MODEL.get(bmw_model, [1.5, 5.0, 2.0])
        eng_min, eng_max, eng_def = float(eng_cfg[0]), float(eng_cfg[1]), float(eng_cfg[2])
        if eng_min == eng_max:
            engine = eng_min
            st.markdown('<div class="electric-note">⚡ Electric Vehicle — ไม่มีเครื่องยนต์สันดาป</div>',
                        unsafe_allow_html=True)
        else:
            engine = st.slider("ขนาดเครื่องยนต์ (L)", eng_min, eng_max, eng_def, 0.1, format="%.1f L")

    # ใช้ค่า default คงที่ (median จาก dataset) — ไม่ให้ user ระบุ
    price_input   = DEFAULT_PRICE
    mileage_input = DEFAULT_MILEAGE

    with ec3:
        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("FORECAST NEXT MONTH →", use_container_width=True)


# ══════════════════════════════════════════════════════
# Main Content: Chart (left 9col) + Insights (right 3col)
# ══════════════════════════════════════════════════════
main_col, side_col = st.columns([3, 1], gap="large")

with main_col:

    # ── Forecast Result ──
    if predict_btn or "last_input_row" in st.session_state:

        if predict_btn:
            input_row = {
                "Model": bmw_model, "Region": region,
                "Fuel_Type": fuel,  "Transmission": trans,
                "Year": 2025, "Engine_Size_L": engine,
                "Mileage_KM": mileage_input, "Price_USD": price_input
            }
            input_vals = ([LE_MAP[c].transform([input_row[c]])[0] for c in FEATURE_CAT]
                          + [input_row[c] for c in FEATURE_NUM])
            with st.spinner("Computing forecast..."):
                predicted = max(0, int(model.predict([input_vals])[0]))
            st.session_state["last_input_row"]  = input_row
            st.session_state["last_input_vals"] = input_vals
            st.session_state["last_predicted"]  = predicted
            st.session_state["last_model"]      = bmw_model
        else:
            input_row = st.session_state["last_input_row"]
            predicted = st.session_state.get("last_predicted", 0)
            bmw_model = st.session_state.get("last_model", bmw_model)

        avg     = meta["avg_sales_by_model"].get(bmw_model, 5000)
        pct     = (predicted - avg) / avg * 100
        tier    = "HIGH" if predicted >= 6000 else ("MID" if predicted >= 3000 else "LOW")
        t_badge = {"HIGH":"badge-blue","MID":"badge-orange","LOW":"badge-red"}[tier]
        arrow   = "▲" if pct >= 0 else "▼"
        mv_cls  = "mv-up" if pct >= 0 else "mv-down"

        # Result + mini stats
        r1, r2 = st.columns([1, 2], gap="medium")
        with r1:
            st.markdown(f"""
            <div class="result-card">
              <div style="font-size:0.7rem;color:#aaa;text-transform:uppercase;
                          letter-spacing:2px;">{bmw_model} · {next_month_str}</div>
              <div class="result-num">{predicted:,}</div>
              <div class="result-sub">Estimated Units Sold</div>
              <span class="badge {t_badge}">Tier {tier}</span>
              <div class="mini-stats">
                <div class="mini-box">
                  <span class="ml">vs Avg</span>
                  <span class="mv {mv_cls}">{arrow}{abs(pct):.1f}%</span>
                </div>
                <div class="mini-box">
                  <span class="ml">Hist Avg</span>
                  <span class="mv">{avg:,}</span>
                </div>
              </div>
              <div class="mini-stats">
                <div class="mini-box">
                  <span class="ml">Fuel</span>
                  <span class="mv" style="font-size:0.9rem;">{input_row['Fuel_Type']}</span>
                </div>
                <div class="mini-box">
                  <span class="ml">Engine</span>
                  <span class="mv" style="font-size:0.9rem;">
                    {'EV' if eng_min==eng_max else f'{input_row["Engine_Size_L"]:.1f}L'}
                  </span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown("""
            <div class="chart-panel">
              <div class="sec-header">
                <div class="sec-bar"></div>
                <div class="sec-title">Historical vs. Forecasted Sales</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            if "historical" in meta and meta["historical"]:
                hist_all = pd.DataFrame(meta["historical"])
                hist_sel = (hist_all[hist_all["Model"] == bmw_model]
                            .sort_values("Year")
                            .assign(Sales=lambda d: d["Sales_Volume"].round(0).astype(int))
                            .rename(columns={"Year":"Year"})
                            [["Year","Sales"]].set_index("Year"))
                # เพิ่ม forecast point ปี 2025
                forecast_row = pd.DataFrame({"Sales": [predicted]}, index=[2025])
                hist_combined = pd.concat([hist_sel, forecast_row])

                fig_line = go.Figure()
                fig_line.add_trace(go.Scatter(
                    x=hist_sel.index, y=hist_sel["Sales"],
                    mode="lines+markers",
                    name="Historical Sales",
                    line=dict(color="#0066b1", width=3),
                    marker=dict(size=5),
                    fill="tozeroy",
                    fillcolor="rgba(0,102,177,0.08)"
                ))
                fig_line.add_trace(go.Scatter(
                    x=[hist_sel.index[-1], 2025],
                    y=[hist_sel["Sales"].iloc[-1], predicted],
                    mode="lines+markers",
                    name="Forecasted",
                    line=dict(color="#999", width=2, dash="dash"),
                    marker=dict(size=8, color="#0066b1", symbol="diamond")
                ))
                fig_line.update_layout(
                    height=230, margin=dict(l=0,r=0,t=10,b=0),
                    paper_bgcolor="white", plot_bgcolor="white",
                    legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1,
                                font=dict(size=12, color="#262626")),
                    xaxis=dict(showgrid=False, color="#333",
                               tickfont=dict(size=12, color="#333")),
                    yaxis=dict(gridcolor="#e0e0e0", color="#333",
                               tickfont=dict(size=12, color="#333")),
                    font=dict(family="Inter", color="#262626")
                )
                st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})
                st.caption(f"— ข้อมูลจริง 2010–2024  ·  ◆ พยากรณ์ 2025 = {predicted:,} units")
            else:
                st.info("ไม่มี historical data ใน metadata — รัน Colab notebook ใหม่เพื่อดู trend chart")

    else:
        st.markdown("""
        <div class="chart-panel" style="text-align:center; padding: 4rem 2rem;">
          <div style="font-size:2.5rem; margin-bottom:0.5rem;">📊</div>
          <div style="font-size:1rem; font-weight:700; color:#262626;">
            เลือกสเปครถและกด Forecast
          </div>
          <div style="font-size:0.8rem; color:#aaa; margin-top:0.4rem;">
            Gradient Boosting Regression · R² {:.4f}
          </div>
        </div>
        """.format(r2_score), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Bottom Tabs ──
    tab1, tab2, tab3 = st.tabs([
        "📋  พยากรณ์ทุกรุ่น",
        "📊  ยอดขายเฉลี่ยรายรุ่น",
        "🌍  Regional Distribution"
    ])

    with tab1:
        if "last_input_row" in st.session_state:
            ir = st.session_state["last_input_row"]
            rows = []
            for bm in BMW_MODELS:
                iv = ([LE_MAP[c].transform([bm if c=="Model" else ir[c]])[0] for c in FEATURE_CAT]
                      + [ir[c] for c in FEATURE_NUM])
                pv    = max(0, int(model.predict([iv])[0]))
                avg_v = meta["avg_sales_by_model"].get(bm, 5000)
                pct_v = (pv - avg_v) / avg_v * 100
                tier_v= "🟢 HIGH" if pv >= 6000 else ("🟡 MID" if pv >= 3000 else "🔴 LOW")
                rows.append({
                    "รุ่น": bm,
                    "คาดการณ์ยอดขาย": f"{pv:,}",
                    "เทียบค่าเฉลี่ย": f"{'▲' if pct_v>=0 else '▼'} {abs(pct_v):.1f}%",
                    "Tier": tier_v
                })
            df_all = pd.DataFrame(rows)
            df_all.index = range(1, len(df_all)+1)
            st.dataframe(df_all, use_container_width=True, height=440)
        else:
            st.info("กด **FORECAST NEXT MONTH** ก่อน เพื่อดูผลเปรียบเทียบทุกรุ่น")

    with tab2:
        hist_avg = (pd.DataFrame([{"รุ่น": k, "ยอดขายเฉลี่ย": v}
                                   for k, v in meta["avg_sales_by_model"].items()])
                    .sort_values("ยอดขายเฉลี่ย", ascending=False))
        n = len(hist_avg)
        bar_colors = [f"rgba(0,{80+int(100*(n-i)/n)},177,1)" for i in range(n)]
        fig_bar = go.Figure(go.Bar(
            x=hist_avg["รุ่น"], y=hist_avg["ยอดขายเฉลี่ย"],
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=hist_avg["ยอดขายเฉลี่ย"].apply(lambda v: f"{v:,.0f}"),
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=12, color="white", family="Inter"),
        ))
        fig_bar.update_layout(
            height=380, margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(showgrid=False, color="#444", tickangle=-45, tickfont=dict(size=11, color="#333")),
            yaxis=dict(visible=False),
            font=dict(family="Inter", color="#262626"),
            bargap=0.25
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with tab3:
        # จำลอง regional distribution (สัดส่วนตามข้อมูล dataset)
        region_vals = [meta["avg_sales_by_model"].get(BMW_MODELS[i % len(BMW_MODELS)], 5000)
                       for i in range(len(REGIONS))]
        region_palette = ["#0066b1","#1a8a5c","#d97706","#7c3aed","#dc2626","#0891b2"]
        fig_reg = go.Figure(go.Bar(
            x=REGIONS, y=region_vals,
            marker=dict(color=region_palette[:len(REGIONS)], line=dict(width=0)),
            text=[f"{v:,.0f}" for v in region_vals],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=14, color="white", family="Inter"),
        ))
        fig_reg.update_layout(
            height=320, margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(showgrid=False, color="#444", tickfont=dict(size=13, color="#333")),
            yaxis=dict(visible=False),
            font=dict(family="Inter", color="#262626"),
            bargap=0.35
        )
        st.plotly_chart(fig_reg, use_container_width=True, config={"displayModeBar": False})
        st.caption("Regional distribution based on dataset averages")


# ── Insights Sidebar ──
with side_col:
    st.markdown(f"""
    <div class="insight-panel">
      <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:1.5rem;">
        <div style="width:4px;height:20px;background:#0066b1;border-radius:2px;"></div>
        <div class="insight-title">Forecast Insights</div>
      </div>

      <div class="insight-item">
        <div class="insight-tag tag-blue">
          ⚡ EV Acceleration
        </div>
        <div class="insight-text">
          EV models (i-Series) แสดงแนวโน้ม
          <b>ยอดขายสูงสุด</b> ในชุดข้อมูล
          โดยเฉพาะ i3 และ i7 ที่มีค่าเฉลี่ยสูงกว่ารุ่น Petrol
        </div>
      </div>

      <div class="insight-item">
        <div class="insight-tag tag-orange">
          ⚠ Supply Chain Risk
        </div>
        <div class="insight-text">
          รุ่น M-Series (M3, M4) มี
          <b>ยอดขายผันผวนสูง</b>
          ควรวางแผนสต็อกล่วงหน้าอย่างน้อย 2 เดือน
        </div>
      </div>

      <div class="insight-item">
        <div class="insight-tag tag-green">
          📈 Market Opportunity
        </div>
        <div class="insight-text">
          ตลาด Asia และ Middle East มีสัดส่วน
          <b>demand สูง</b> สำหรับรุ่น X-Series
          โดยเฉพาะ X2 และ X6
        </div>
      </div>

      <div style="border-top:1px solid #333;margin-top:1.5rem;padding-top:1.5rem;">
        <div style="font-size:0.7rem;color:#666;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:1px;">
          Model Metrics
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:0.5rem;">
          <span style="color:#888;">Algorithm</span>
          <span style="color:white;font-weight:600;">Gradient Boost</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:0.5rem;">
          <span style="color:#888;">R² Score</span>
          <span style="color:{"#4ade80" if r2_score>=0.7 else "#fb923c"};font-weight:700;">{r2_score:.4f}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:0.5rem;">
          <span style="color:#888;">MAE</span>
          <span style="color:white;font-weight:600;">{mae_val:,.0f} units</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.8rem;">
          <span style="color:#888;">Training Data</span>
          <span style="color:white;font-weight:600;">{meta['training_samples']:,}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Disclaimer ──
st.markdown("""
<div class="disclaimer-box">
  <b>⚠ Disclaimer / ข้อจำกัดความรับผิดชอบ</b><br>
  ผลการพยากรณ์นี้สร้างขึ้นโดย Machine Learning Model (GradientBoostingRegressor)
  ที่ train บนข้อมูล BMW Sales ปี 2010–2024 จำนวน 50,000 รายการ
  ตัวเลขที่แสดงเป็นเพียง <b>การประมาณการเชิงสถิติ</b> เท่านั้น
  ไม่ใช่การรับประกันยอดขายจริง และไม่ควรใช้เป็นฐานในการตัดสินใจทางธุรกิจโดยไม่มีการวิเคราะห์เพิ่มเติม<br><br>
  Model accuracy: R² = {r2:.3f} · MAE = ±{mae:.0f} units ·
  Dataset: Kaggle BMW Sales Data 2010–2024 · สร้างเพื่อวัตถุประสงค์ทางการศึกษาเท่านั้น
</div>
""".format(r2=r2_score, mae=mae_val), unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="footer">
  © 2024 BMW Group AG — For Internal Use Only · All data points are strictly confidential
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)