import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="DataAnalyst AI", page_icon="✨", layout="wide")

# ✅ Google Search Console verification (PASTE ONCE, AT TOP)
st.markdown(
    """
    <meta name="google-site-verification" content="Yr6DCmnKvnLK57ejhzk4-qj6HX8CwTKG26DxQTg4heQ" />
    """,
    unsafe_allow_html=True
)

# -------------------- THEME: NEON + GLASS + ANIMATIONS --------------------
st.markdown("""
<style>
/* Remove Streamlit default padding line */
[data-testid="stToolbar"] {visibility: hidden; height: 0px;}
[data-testid="stDecoration"] {visibility: hidden; height: 0px;}

/* Animated background (neon blobs) */
html, body, [data-testid="stAppViewContainer"] {
  background: #070A12;
}
.bg-wrap{
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
}
.blob{
  position:absolute;
  width: 520px;
  height: 520px;
  filter: blur(50px);
  opacity: 0.55;
  border-radius: 999px;
  animation: drift 12s ease-in-out infinite;
}
.blob.b1{ left:-120px; top:-140px; background: radial-gradient(circle, rgba(99,102,241,0.95), rgba(99,102,241,0));}
.blob.b2{ right:-160px; top:50px; background: radial-gradient(circle, rgba(16,185,129,0.95), rgba(16,185,129,0)); animation-duration: 14s;}
.blob.b3{ left:20%; bottom:-220px; background: radial-gradient(circle, rgba(244,63,94,0.85), rgba(244,63,94,0)); animation-duration: 16s;}
@keyframes drift{
  0%{ transform: translate(0px,0px) scale(1); }
  50%{ transform: translate(40px,30px) scale(1.07); }
  100%{ transform: translate(0px,0px) scale(1); }
}

/* Layout */
.block-container {max-width: 1280px; padding-top: 1.2rem; padding-bottom: 2rem;}
hr {opacity:0.15;}

/* Glassmorphism components */
.glass{
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow: 0 10px 35px rgba(0,0,0,0.35);
  backdrop-filter: blur(12px);
  border-radius: 18px;
  padding: 16px;
}
.glass-soft{
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.09);
  box-shadow: 0 8px 28px rgba(0,0,0,0.30);
  backdrop-filter: blur(12px);
  border-radius: 18px;
  padding: 16px;
}
.muted{opacity:0.78;}
.small{font-size:13px; opacity:0.80;}
.badge{
  display:inline-block;
  padding: 6px 10px;
  margin: 6px 8px 0 0;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.15);
  background: rgba(255,255,255,0.07);
  font-size: 12px;
}

/* Neon brand bar */
.nav{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(12px);
  box-shadow: 0 0 0 1px rgba(99,102,241,0.10), 0 12px 35px rgba(0,0,0,0.35);
}
.brand{
  display:flex; align-items:center; gap:12px;
}
.brand-title{
  font-weight: 950;
  font-size: 18px;
  letter-spacing: 0.4px;
}
.brand-sub{
  font-size: 12px;
  opacity:0.78;
  margin-top:-2px;
}

/* Animated Neon Logo (orbit + pulse) */
.logo-wrap{
  position: relative;
  width: 46px; height: 46px;
}
.logo-core{
  width: 46px; height: 46px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(99,102,241,1), rgba(16,185,129,1));
  box-shadow: 0 0 30px rgba(99,102,241,0.45), 0 0 40px rgba(16,185,129,0.20);
  display:flex;
  align-items:center;
  justify-content:center;
  font-weight: 950;
}
.logo-core span{
  color: rgba(255,255,255,0.95);
  text-shadow: 0 0 12px rgba(255,255,255,0.35);
}
.logo-pulse{
  position:absolute;
  inset:-12px;
  border-radius: 22px;
  border: 2px solid rgba(99,102,241,0.35);
  animation: pulse 1.7s ease-out infinite;
}
@keyframes pulse{
  0%{transform: scale(0.86); opacity: 0.38;}
  70%{transform: scale(1.12); opacity: 0.06;}
  100%{transform: scale(1.22); opacity: 0;}
}
.logo-orbit{
  position:absolute;
  inset:-16px;
  border-radius: 26px;
  border: 1px solid rgba(16,185,129,0.16);
}
.logo-orbit:before{
  content:"";
  position:absolute;
  width: 10px; height: 10px;
  border-radius: 999px;
  background: rgba(16,185,129,1);
  box-shadow: 0 0 16px rgba(16,185,129,0.7);
  top: 50%; left: 50%;
  transform: translate(-50%,-50%) rotate(0deg) translateX(22px);
  animation: orbit 2.5s linear infinite;
}
@keyframes orbit{
  0%{ transform: translate(-50%,-50%) rotate(0deg) translateX(22px); }
  100%{ transform: translate(-50%,-50%) rotate(360deg) translateX(22px); }
}

/* Hero */
.hero{
  margin-top: 14px;
  border-radius: 24px;
  border: 1px solid rgba(255,255,255,0.10);
  background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(16,185,129,0.10));
  padding: 24px;
  position: relative;
  overflow: hidden;
}
.hero:before{
  content:"";
  position:absolute;
  width: 520px; height: 520px;
  background: radial-gradient(circle, rgba(255,255,255,0.18), rgba(255,255,255,0));
  top:-260px; right:-260px;
  animation: floaty 6s ease-in-out infinite;
}
@keyframes floaty{
  0%{ transform: translate(0px,0px); }
  50%{ transform: translate(-18px, 20px); }
  100%{ transform: translate(0px,0px); }
}
.hero-title{ font-size: 46px; font-weight: 980; line-height: 1.02;}
.hero-desc{ opacity:0.82; font-size: 15px; margin-top: 10px; max-width: 820px;}
.hero-chips{ display:flex; gap:10px; flex-wrap:wrap; margin-top: 14px;}
.chip{
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.06);
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 12px;
  opacity: 0.86;
}

/* KPI */
.kpi{ font-size: 28px; font-weight: 980; }
.kpi-label{ font-size: 12px; opacity: 0.78; }

/* Streamlit widget tweaks */
div[data-testid="stFileUploader"] section {background: rgba(255,255,255,0.02)!important; border-radius: 14px;}
div[data-testid="stTextInput"] input {background: rgba(255,255,255,0.06)!important;}
div[data-testid="stTextArea"] textarea {background: rgba(255,255,255,0.06)!important;}
</style>

<div class="bg-wrap">
  <div class="blob b1"></div>
  <div class="blob b2"></div>
  <div class="blob b3"></div>
</div>
""", unsafe_allow_html=True)

# -------------------- HELPERS --------------------
def safe_read(uploaded):
    name = uploaded.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded)
    if name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(uploaded)
    raise ValueError("Upload CSV or Excel only")

def numeric_cols(df):
    return list(df.select_dtypes(include=[np.number]).columns)

def categorical_cols(df):
    return list(df.select_dtypes(include=["object", "category", "bool"]).columns)

def normalize_dt(df, col):
    try:
        return pd.to_datetime(df[col], errors="coerce")
    except Exception:
        return pd.Series([pd.NaT] * len(df))

def ai_insights(df):
    out = []
    out.append(f"Dataset contains **{df.shape[0]} rows** and **{df.shape[1]} columns**.")
    missing = int(df.isna().sum().sum())
    if missing:
        out.append(f"Found **{missing} missing values** — fill (median/mode) or drop based on context.")
    else:
        out.append("No missing values detected — data quality looks good.")

    num = numeric_cols(df)
    if len(num) >= 2:
        corr = df[num].corr(numeric_only=True)
        best = None
        for i in corr.columns:
            for j in corr.columns:
                if i == j:
                    continue
                v = corr.loc[i, j]
                if pd.isna(v):
                    continue
                score = abs(v)
                if best is None or score > best[0]:
                    best = (score, i, j, v)
        if best:
            if best[0] >= 0.70:
                out.append(f"Strong relationship: **{best[1]} ↔ {best[2]}** (corr ≈ {best[3]:.2f}).")
            else:
                out.append(f"Top correlation: **{best[1]} ↔ {best[2]}** (corr ≈ {best[3]:.2f}).")
    out.append("Next steps: validate units, handle missing values, check outliers, and build KPI charts.")
    return out

def anomaly_iforest(df, col, contamination=0.03):
    d = df[[col]].dropna().copy()
    if len(d) < 20:
        return None, "Need at least ~20 numeric values."
    model = IsolationForest(
        n_estimators=250,
        contamination=min(max(contamination, 0.01), 0.2),
        random_state=42
    )
    model.fit(d)
    pred = model.predict(d)
    out = d.copy()
    out["anomaly"] = (pred == -1)
    return out, None

def forecast_simple(df, date_col, target_col, horizon=14, freq="D"):
    d = df.copy()
    d[date_col] = normalize_dt(d, date_col)
    d = d.dropna(subset=[date_col, target_col])
    if len(d) < 30:
        return None, "Need at least ~30 rows after cleaning."
    d = d.sort_values(date_col)
    agg = d.groupby(pd.Grouper(key=date_col, freq=freq))[target_col].mean().reset_index()
    agg = agg.dropna()
    if len(agg) < 15:
        return None, "Not enough time points after aggregation."

    X = np.arange(len(agg)).reshape(-1, 1)
    y = agg[target_col].values
    lr = LinearRegression()
    lr.fit(X, y)

    future_X = np.arange(len(agg), len(agg) + horizon).reshape(-1, 1)
    future_y = lr.predict(future_X)

    last = agg[date_col].iloc[-1]
    future_dates = pd.date_range(start=last, periods=horizon + 1, freq=freq)[1:]
    fut = pd.DataFrame({date_col: future_dates, target_col: future_y})
    return (agg, fut), None

def nl_query(df, q):
    qn = q.strip().lower()

    m = re.search(r"top\s+(\d+)\s+rows", qn)
    if m:
        return ("table", df.head(int(m.group(1))))

    m = re.search(r"(average|mean)\s+of\s+(.+)$", qn)
    if m:
        col = m.group(2).strip()
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            return ("text", f"Average of {col} = {df[col].mean():.4f}")
        return ("text", f"Column must exist and be numeric: {col}")

    m = re.search(r"sum\s+of\s+(.+)$", qn)
    if m:
        col = m.group(1).strip()
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            return ("text", f"Sum of {col} = {df[col].sum():.4f}")
        return ("text", f"Column must exist and be numeric: {col}")

    m = re.search(r"count\s+by\s+(.+)$", qn)
    if m:
        col = m.group(1).strip()
        if col in df.columns:
            out = df[col].astype(str).value_counts().reset_index()
            out.columns = [col, "count"]
            return ("table", out.head(30))
        return ("text", f"Column not found: {col}")

    m = re.search(r"correlation\s+between\s+(.+)\s+and\s+(.+)$", qn)
    if m:
        c1, c2 = m.group(1).strip(), m.group(2).strip()
        if c1 in df.columns and c2 in df.columns:
            if pd.api.types.is_numeric_dtype(df[c1]) and pd.api.types.is_numeric_dtype(df[c2]):
                val = df[[c1, c2]].corr(numeric_only=True).iloc[0, 1]
                return ("text", f"Correlation({c1}, {c2}) = {val:.4f}")
            return ("text", "Both columns must be numeric.")
        return ("text", "Column names not found.")

    return ("text", "Try: 'average of Sales', 'count by Region', 'top 10 rows', 'correlation between A and B'.")

# -------------------- STATE --------------------
if "df" not in st.session_state:
    st.session_state.df = None

# -------------------- NAVBAR (with logo image + neon icon) --------------------
left_logo, right_nav = st.columns([2, 1])
with left_logo:
    try:
        st.image("assets/logo.png", width=80)
    except Exception:
        pass

st.markdown("""
<div class="nav">
  <div class="brand">
    <div class="logo-wrap">
      <div class="logo-pulse"></div>
      <div class="logo-orbit"></div>
      <div class="logo-core"><span>DA</span></div>
    </div>
    <div>
      <div class="brand-title">DataAnalyst AI</div>
      <div class="brand-sub">Neon Glow • Glassmorphism • Interactive AI Analytics</div>
    </div>
  </div>
  <div class="small muted">Upload → Dashboard → Insights → Anomalies → Forecast → Ask Data</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Menu",
    ["🏠 Home", "📥 Upload", "📈 Dashboard", "🧠 Insights", "🚨 Anomalies", "🔮 Forecast", "💬 Ask Data"]
)

# -------------------- HOME --------------------
if page == "🏠 Home":
    st.markdown("""
    <div class="hero">
      <div class="hero-title">Neon + Glass AI<br>Data Analysis Dashboard</div>
      <div class="hero-desc">
        Upload your dataset and instantly get: profiling, interactive visual dashboards,
        human-style insights, anomaly detection, forecasting, and natural-language Q&A.
      </div>
      <div class="hero-chips">
        <div class="chip">⚡ Auto Profiling</div>
        <div class="chip">📊 Plotly Interactive Charts</div>
        <div class="chip">🧠 Insights (stats-based)</div>
        <div class="chip">🚨 Outlier Detection</div>
        <div class="chip">🔮 Forecasting</div>
        <div class="chip">💬 Ask Data</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------- UPLOAD --------------------
elif page == "📥 Upload":
    st.markdown("### 📥 Upload your dataset")
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded:
        try:
            df = safe_read(uploaded).copy()
            df.columns = [str(c).strip() for c in df.columns]
            df = df.drop_duplicates()
            st.session_state.df = df
            st.success("✅ Dataset loaded successfully!")
        except Exception as e:
            st.error(f"Upload error: {e}")

    df = st.session_state.df
    if df is not None:
        st.markdown("### Preview")
        st.dataframe(df.head(60), use_container_width=True)

# -------------------- DASHBOARD --------------------
elif page == "📈 Dashboard":
    df = st.session_state.df
    if df is None:
        st.warning("Upload dataset first in **Upload**.")
    else:
        st.markdown("### 📈 Interactive Dashboard")
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        cats = categorical_cols(df)
        fcol = st.selectbox("Filter column (optional)", ["(none)"] + cats)
        view = df.copy()
        if fcol != "(none)":
            values = sorted(view[fcol].astype(str).dropna().unique().tolist())[:600]
            chosen = st.multiselect("Select values", values)
            if chosen:
                view = view[view[fcol].astype(str).isin(chosen)]
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### Chart Builder")
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        chart = st.selectbox("Chart type", ["Bar", "Line", "Scatter", "Histogram", "Box"])
        cols = view.columns.tolist()
        x = st.selectbox("X axis", cols)
        y = st.selectbox("Y axis (numeric optional)", ["(none)"] + numeric_cols(view))

        fig = None
        try:
            if chart == "Bar":
                if y == "(none)":
                    tmp = view[x].astype(str).value_counts().head(30).reset_index()
                    tmp.columns = [x, "count"]
                    fig = px.bar(tmp, x=x, y="count")
                else:
                    fig = px.bar(view, x=x, y=y)
            elif chart == "Line":
                if y != "(none)":
                    fig = px.line(view, x=x, y=y)
            elif chart == "Scatter":
                if y != "(none)":
                    fig = px.scatter(view, x=x, y=y)
            elif chart == "Histogram":
                fig = px.histogram(view, x=x)
            elif chart == "Box":
                if y != "(none)":
                    fig = px.box(view, x=x, y=y)

            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Chart error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------- INSIGHTS --------------------
elif page == "🧠 Insights":
    df = st.session_state.df
    if df is None:
        st.warning("Upload dataset first in **Upload**.")
    else:
        st.markdown("### 🧠 AI Insights (Human-style)")
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        for line in ai_insights(df):
            st.write("• " + line)
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------- ANOMALIES --------------------
elif page == "🚨 Anomalies":
    df = st.session_state.df
    if df is None:
        st.warning("Upload dataset first in **Upload**.")
    else:
        num = numeric_cols(df)
        if not num:
            st.info("No numeric columns.")
        else:
            st.markdown("### 🚨 Anomaly Detection (Neon)")
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            col = st.selectbox("Numeric column", num)
            contam = st.slider("Sensitivity", 0.01, 0.15, 0.03, 0.01)
            st.markdown("</div>", unsafe_allow_html=True)

            out, err = anomaly_iforest(df, col, contam)
            if err:
                st.warning(err)
            else:
                an = out[out["anomaly"] == True]
                st.write(f"Detected **{len(an)} anomalies** in **{col}**.")
                st.dataframe(an.head(50), use_container_width=True)

# -------------------- FORECAST --------------------
elif page == "🔮 Forecast":
    df = st.session_state.df
    if df is None:
        st.warning("Upload dataset first in **Upload**.")
    else:
        st.markdown("### 🔮 Forecast (Predictive Analysis)")
        date_candidates = []
        for c in df.columns:
            sample = df[c].dropna().head(50)
            if len(sample) > 0:
                parsed = pd.to_datetime(sample, errors="coerce")
                if parsed.notna().mean() > 0.7:
                    date_candidates.append(c)

        num = numeric_cols(df)
        if not date_candidates or not num:
            st.info("Need a date-like column and numeric column.")
        else:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            dcol = st.selectbox("Date column", date_candidates)
            tcol = st.selectbox("Target numeric column", num)
            freq = st.selectbox("Frequency", ["D", "W", "M"])
            horizon = st.slider("Forecast horizon", 7, 90, 14, 1)
            st.markdown("</div>", unsafe_allow_html=True)

            result, err = forecast_simple(df, dcol, tcol, horizon=horizon, freq=freq)
            if err:
                st.warning(err)
            else:
                hist, fut = result
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hist[dcol], y=hist[tcol], mode="lines+markers", name="History"))
                fig.add_trace(go.Scatter(x=fut[dcol], y=fut[tcol], mode="lines+markers", name="Forecast"))
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(fut.head(50), use_container_width=True)

# -------------------- ASK DATA --------------------
else:
    df = st.session_state.df
    if df is None:
        st.warning("Upload dataset first in **Upload**.")
    else:
        st.markdown("### 💬 Ask Data (Natural Language)")
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.write("Examples: `average of Sales`, `count by Region`, `top 10 rows`, `correlation between A and B`")
        st.markdown("</div>", unsafe_allow_html=True)

        q = st.text_input("Type your question")
        if q.strip():
            kind, out = nl_query(df, q)
            if kind == "table":
                st.dataframe(out, use_container_width=True)
            else:
                st.write(out)
