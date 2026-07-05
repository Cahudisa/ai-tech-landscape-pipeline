import streamlit as st
import pandas as pd
import plotly.express as px

# ── Configuración general ────────────────────────────────────
st.set_page_config(
    page_title="AI Tech Landscape",
    page_icon="🤖",
    layout="wide"
)

# ── Cargar datos ─────────────────────────────────────────────
@st.cache_data
def load_data():
    gold = "data/gold/"
    return {
        "precio_anual"  : pd.read_parquet(f"{gold}gold_bigtech_precio_anual.parquet"),
        "performance"   : pd.read_parquet(f"{gold}gold_bigtech_performance.parquet"),
        "gpu"           : pd.read_parquet(f"{gold}gold_gpu_race.parquet"),
        "top_revenue"   : pd.read_parquet(f"{gold}gold_ai_top_revenue.parquet"),
        "culture"       : pd.read_parquet(f"{gold}gold_ai_culture_vs_money.parquet"),
    }

data = load_data()

# ── Sidebar navegación ───────────────────────────────────────
st.sidebar.title("🤖 AI Tech Landscape")
st.sidebar.markdown("Who\'s winning the race?")
page = st.sidebar.radio("Navigate", [
    "Big Tech Overview",
    "Performance Analysis",
    "GPU Race",
    "AI Companies",
    "Culture vs Money"
])

# ════════════════════════════════════════════════════════════
# PÁGINA 1 — Big Tech Overview
# ════════════════════════════════════════════════════════════
if page == "Big Tech Overview":
    st.title("📈 Big Tech Overview")
    st.markdown("Stock price evolution and annual returns for 14 major tech companies.")

    df = data["precio_anual"]

    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        companies = st.multiselect("Select Companies", sorted(df["ticker"].unique()), default=["NVDA", "MSFT", "GOOGL", "AAPL"])
    with col2:
        year_range = st.slider("Select Year Range", int(df["year"].min()), int(df["year"].max()), (2015, 2023))

    df_filtered = df[df["ticker"].isin(companies) & df["year"].between(*year_range)]

    # KPIs
    k1, k2, k3 = st.columns(3)
    k1.metric("Companies Selected", len(companies))
    k2.metric("Year Range", f"{year_range[0]} – {year_range[1]}")
    k3.metric("Avg Close Price (USD)", f"${df_filtered['avg_close_price'].mean():.2f}")

    st.markdown("---")

    # Gráfico de líneas
    fig1 = px.line(df_filtered, x="year", y="avg_close_price", color="ticker",
                   title="Stock Price Evolution by Company",
                   labels={"year": "Year", "avg_close_price": "Avg Close Price (USD)", "ticker": "Company"})
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico de barras
    fig2 = px.bar(df_filtered, x="pct_change_yoy", y="ticker", color="ticker",
                  orientation="h",
                  title="Annual Price Change (%) by Company",
                  labels={"pct_change_yoy": "Avg Annual Change (%)", "ticker": "Company"})
    st.plotly_chart(fig2, use_container_width=True)

# ════════════════════════════════════════════════════════════
# PÁGINA 2 — Performance Analysis
# ════════════════════════════════════════════════════════════
elif page == "Performance Analysis":
    st.title("🏆 Performance Analysis")
    st.markdown("Best and worst single year return for each company.")

    df = data["performance"]

    k1, k2 = st.columns(2)
    k1.metric("Best Single Year Return (%)", f"{df['mejor_retorno_pct'].max():.2f}%")
    k2.metric("Worst Single Year Drop (%)", f"{df['peor_retorno_pct'].min():.2f}%")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(df.sort_values("mejor_retorno_pct", ascending=True),
                      x="mejor_retorno_pct", y="ticker", orientation="h",
                      title="Best Year Return (%) by Company",
                      labels={"mejor_retorno_pct": "Return (%)", "ticker": "Company"},
                      color="mejor_retorno_pct", color_continuous_scale="Greens")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(df.sort_values("peor_retorno_pct", ascending=True),
                      x="peor_retorno_pct", y="ticker", orientation="h",
                      title="Worst Year Return (%) by Company",
                      labels={"peor_retorno_pct": "Return (%)", "ticker": "Company"},
                      color="peor_retorno_pct", color_continuous_scale="Reds_r")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Full Performance Table")
    st.dataframe(df[["ticker", "mejor_anio", "mejor_retorno_pct", "peor_anio", "peor_retorno_pct"]]
                 .rename(columns={
                     "ticker": "Company",
                     "mejor_anio": "Best Year",
                     "mejor_retorno_pct": "Best Return (%)",
                     "peor_anio": "Worst Year",
                     "peor_retorno_pct": "Worst Drop (%)"
                 }), use_container_width=True)

# ════════════════════════════════════════════════════════════
# PÁGINA 3 — GPU Race
# ════════════════════════════════════════════════════════════
elif page == "GPU Race":
    st.title("🖥️ GPU Race: Who\'s Winning?")
    st.markdown("NVIDIA vs AMD vs INTEL — historical stock price evolution.")

    df = data["gpu"]

    year_range = st.slider("Select Year Range", int(df["year"].min()), int(df["year"].max()), (2010, 2024))
    df_filtered = df[df["year"].between(*year_range)]

    nvidia_peak = df[df["empresa"] == "NVIDIA"]["avg_close_price"].max()
    st.metric("NVIDIA Peak Price (USD)", f"${nvidia_peak:.2f}")

    st.markdown("---")

    fig1 = px.line(df_filtered, x="year", y="avg_close_price", color="empresa",
                   title="GPU Companies: Stock Price Evolution",
                   labels={"year": "Year", "avg_close_price": "Avg Close Price (USD)", "empresa": "Company"})
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(df_filtered.groupby("empresa")["pct_change_yoy"].mean().reset_index()
                  .sort_values("pct_change_yoy", ascending=True),
                  x="pct_change_yoy", y="empresa", orientation="h",
                  title="Annual Price Change (%) by GPU Company",
                  labels={"pct_change_yoy": "Avg Annual Change (%)", "empresa": "Company"},
                  color="empresa")
    st.plotly_chart(fig2, use_container_width=True)

# ════════════════════════════════════════════════════════════
# PÁGINA 4 — AI Companies
# ════════════════════════════════════════════════════════════
elif page == "AI Companies":
    st.title("🏢 Top AI Companies by Revenue")
    st.markdown("The biggest players in the AI industry by annual revenue.")

    df = data["top_revenue"]

    st.metric("Highest Revenue (USD Billions)", f"${df['revenue_usd_billions'].max():.2f}B")

    st.markdown("---")

    fig1 = px.bar(df.sort_values("revenue_usd_billions", ascending=True),
                  x="revenue_usd_billions", y="company_name", orientation="h",
                  title="Top 10 AI Companies by Revenue (USD Billions)",
                  labels={"revenue_usd_billions": "Revenue (USD Billions)", "company_name": "Company"},
                  color="revenue_usd_billions", color_continuous_scale="Blues")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Company Details")
    st.dataframe(df[["company_name", "revenue_usd_billions", "founded", "headquarters"]]
                 .rename(columns={
                     "company_name": "Company",
                     "revenue_usd_billions": "Revenue (USD B)",
                     "founded": "Founded",
                     "headquarters": "Headquarters"
                 }), use_container_width=True)

# ════════════════════════════════════════════════════════════
# PÁGINA 5 — Culture vs Money
# ════════════════════════════════════════════════════════════
elif page == "Culture vs Money":
    st.title("💼 Culture vs Money")
    st.markdown("Do the highest-earning AI companies treat their employees the best?")

    df = data["culture"]

    k1, k2 = st.columns(2)
    k1.metric("Highest Glassdoor Score", f"{df['glassdoor_score'].max():.2f} / 5")
    k2.metric("Companies Analyzed", len(df))

    st.markdown("---")

    fig1 = px.scatter(df, x="revenue_usd_billions", y="glassdoor_score",
                      color="company_name", hover_name="company_name",
                      title="Revenue vs Employee Satisfaction",
                      labels={
                          "revenue_usd_billions": "Revenue (USD Billions)",
                          "glassdoor_score": "Glassdoor Score (0-5)",
                          "company_name": "Company"
                      })
    st.plotly_chart(fig1, use_container_width=True)

    top15 = df.nlargest(15, "glassdoor_score")
    fig2 = px.bar(top15.sort_values("glassdoor_score", ascending=True),
                  x="glassdoor_score", y="company_name", orientation="h",
                  title="Top 15 Companies by Employee Satisfaction",
                  labels={"glassdoor_score": "Glassdoor Score", "company_name": "Company"},
                  color="glassdoor_score", color_continuous_scale="Greens")
    st.plotly_chart(fig2, use_container_width=True)
