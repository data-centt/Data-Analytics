import pandas as pd
import streamlit as st
import io
import requests
from error_handler import load_file
from theme import page_header
from nav import goto


def main():
    page_header(
        "Data Overview",
        "Upload your own dataset or pick a sample to explore. Your data stays "
        "loaded as you move between the Dashboard and EDA pages.",
    )

    if 'radio_option' not in st.session_state:
        st.session_state['radio_option'] = "Upload data"

    option = st.radio("Select data source", ("Upload data", "Use sample data"),
                      index=("Upload data", "Use sample data").index(st.session_state['radio_option']),
                      horizontal=True)

    if option != st.session_state['radio_option']:
        st.session_state['radio_option'] = option

    path1 = "https://raw.githubusercontent.com/data-centt/Data-Analytics/main/sample%20data/fire.json"
    path2 = "https://raw.githubusercontent.com/data-centt/Data-Analytics/main/sample%20data/test.xlsx"

    if 'df' not in st.session_state:
        st.session_state['df'] = None

    if option == "Upload data":
        if 'file_uploaded' not in st.session_state:
            st.session_state['file_uploaded'] = False
        if 'uploader_key' not in st.session_state:
            st.session_state['uploader_key'] = 0

        if not st.session_state['file_uploaded']:
            path = st.file_uploader(
                "Upload file",
                type=["csv", "json", "xlsx", "xls"],
                key=f"uploader_{st.session_state['uploader_key']}"
            )
            if path:
                with st.spinner('Loading data...'):
                    st.session_state['df'] = load_file(path)
                    st.session_state['file_uploaded'] = True

        if st.session_state['file_uploaded']:
            if st.button("Reset"):
                st.session_state['file_uploaded'] = False
                st.session_state['df'] = None
                # New key => a fresh, empty uploader so the old file isn't reloaded.
                st.session_state['uploader_key'] += 1

    elif option == "Use sample data":
        if 'data_option' not in st.session_state:
            st.session_state['data_option'] = "Pick data"
        if 'data_loaded' not in st.session_state:
            st.session_state['data_loaded'] = False

        options = ["Pick data", "Fire data", "Employee data"]
        data_option = st.selectbox("Choose data", options, index=options.index(st.session_state['data_option']))

        if data_option != st.session_state["data_option"]:
            st.session_state["data_option"] = data_option
            st.session_state["df"] = None
            st.session_state['data_loaded'] = False

        if data_option != "Pick data" and not st.session_state['data_loaded']:
            url = path1 if data_option == "Fire data" else path2
            try:
                with st.spinner('Loading sample data...'):
                    response = requests.get(url, timeout=15)
                    response.raise_for_status()
                    if data_option == "Fire data":
                        sample = pd.read_json(io.StringIO(response.text))
                    else:
                        sample = pd.read_excel(io.BytesIO(response.content))
                for col in sample:
                    if pd.api.types.is_datetime64_any_dtype(sample[col]):
                        sample[col] = sample[col].dt.date
                st.session_state['df'] = sample
                st.session_state['data_loaded'] = True
            except requests.exceptions.RequestException as e:
                st.error(f"Could not download the sample data. Please try again. ({e})")

        if data_option == "Pick data":
            st.info("Select a sample dataset from the drop-down menu above.")

    if st.session_state['df'] is not None:
        df = st.session_state['df']
        st.success("Data loaded successfully! 🎉")

        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", f"{df.shape[0]:,}")
        c2.metric("Columns", f"{df.shape[1]:,}")
        c3.metric("Numeric columns", f"{df.select_dtypes(include='number').shape[1]:,}")

        tab1, tab2, tab3 = st.tabs(["Preview", "Column Information", "Descriptive Analysis"])

        with tab1:
            st.dataframe(df.head(50), use_container_width=True)

        with tab2:
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.code(buffer.getvalue())

        with tab3:
            st.caption("Statistics for numeric columns only; other columns are omitted.")
            st.dataframe(df.describe(), use_container_width=True)

        st.divider()
        nav1, nav2 = st.columns(2)
        with nav1:
            if st.button("Go to Dashboard →", use_container_width=True):
                goto("Dashboard")
        with nav2:
            if st.button("Go to EDA →", use_container_width=True):
                goto("EDA")

    else:
        st.info("Please upload or select a dataset to get started.")


if __name__ == "__main__":
    main()
