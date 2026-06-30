import streamlit as st

from theme import apply_theme, page_header, LOGO_PATH
from nav import goto
from data import main as data_main
from dashboard import main as dashboard_main
from eda import main as eda_main

st.set_page_config(
    page_title="Data-Cent",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
st.logo(LOGO_PATH)


def home_page():
    left, mid, right = st.columns([2, 1, 2])
    with mid:
        st.image(LOGO_PATH, width=170)

    st.markdown("<h1 style='text-align:center'>Data-Cent Data Analytics</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; font-size:1.15rem; opacity:0.7'>"
        "Upload, explore, and visualise your data — right in the browser, no setup required."
        "</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("#### 📤 Data")
            st.write(
                "Upload a CSV, Excel or JSON file (or pick a sample), then see a "
                "preview, column info and descriptive statistics at a glance."
            )
            if st.button("Open Data", key="cta_data", use_container_width=True):
                goto("Data")

    with col2:
        with st.container(border=True):
            st.markdown("#### 📊 Dashboard")
            st.write(
                "Build interactive Plotly visuals — bar, line, area, scatter, "
                "histogram, pie and treemap — and tell your data story."
            )
            if st.button("Open Dashboard", key="cta_dash", use_container_width=True):
                goto("Dashboard")

    with col3:
        with st.container(border=True):
            st.markdown("#### 🔍 EDA")
            st.write(
                "Run quick exploratory analysis with ready-made Seaborn charts to "
                "understand your data before modelling."
            )
            if st.button("Open EDA", key="cta_eda", use_container_width=True):
                goto("EDA")

    st.divider()
    st.caption(
        "Built with Streamlit · "
        "[GitHub](https://github.com/data-centt/Data-Analytics) · "
        "[LinkedIn](https://www.linkedin.com/in/daniel15568)"
    )


PAGES = {
    "Home": st.Page(home_page, title="Home", icon=":material/home:", default=True),
    "Data": st.Page(data_main, title="Data", icon=":material/cloud_upload:", url_path="data"),
    "Dashboard": st.Page(dashboard_main, title="Dashboard", icon=":material/dashboard:", url_path="dashboard"),
    "EDA": st.Page(eda_main, title="EDA", icon=":material/insights:", url_path="eda"),
}
st.session_state["_pages"] = PAGES

pg = st.navigation(list(PAGES.values()))
pg.run()
