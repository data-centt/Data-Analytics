import pandas as pd
import streamlit as st
import io
import requests
from error_handler import load_file


def apply_css():
    st.markdown(
        """
        <style>
        body {
            background-color: inherit;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            text-align: center;
        }
        .main-title {
            font-size: 40px;
            color: #2E86C1;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            font-family: Times New Roman;
        }
        .sub-header {
            font-size: 28px;
            color: #117A65;
            margin-top: 20px;
            margin-bottom: 10px;
            border-bottom: 2px solid #d1d8de;
            padding-bottom: 5px;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }

        .logo-container img {
            width: 200px; 
            max-width: 100%;
            height: auto;
        }
        .home-description {
            font-size: 18px;
            color: var(--text-color-light); 
            margin-top: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .info-message {
            background-color: #f9ebea;
            border-left: 6px solid #D5DBDB;
            padding: 10px;
            border-radius: 8px;
            color: #5D6D7E;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            background-color: #2E86C1;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #1F618D;
        }
        .stTabs [role="tablist"] .stMarkdown {
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def navigate_to(page_name):
    st.session_state["current_page"] = page_name


def main():
    apply_css()
    st.markdown(
        '<div class="logo-container"><img src="https://raw.githubusercontent.com/data-centt/Data-Analytics/main/media/data-cent1.png" alt="Logo"></div>',
        unsafe_allow_html=True)

    st.markdown('<p class="main-title">Data Overview</p>', unsafe_allow_html=True)

    st.markdown("""
        <p class="home-description">
        This is where you upload your data, you have two options of data to test the app, choose a data and click ok for it to work,
        After upload, simply press the 'X' to remove the upload window and continue. \n You can see the brief statistical details of your data, after getting the details, you can click the EDA button for Exploratory data analysis or the dashboard to enjoy the full experience of plotly express library.
        \n Done with current data? simply double-click the reset button to upload/use another data.
        </p>
    """, unsafe_allow_html=True)

    if 'radio_option' not in st.session_state:
        st.session_state['radio_option'] = "Upload data"

    option = st.radio("Select Data:", ("Upload data", "Use sample data"),
                      index=("Upload data", "Use sample data").index(st.session_state['radio_option']))

    if option != st.session_state['radio_option']:
        st.session_state['radio_option'] = option

    path1 = "https://raw.githubusercontent.com/data-centt/Data-Analytics/main/sample%20data/fire.json"
    path2 = "https://raw.githubusercontent.com/data-centt/Data-Analytics/main/sample%20data/test.xlsx"

    if 'df' not in st.session_state:
        st.session_state['df'] = None

    if option == "Upload data":
        if 'file_uploaded' not in st.session_state:
            st.session_state['file_uploaded'] = False

        if not st.session_state['file_uploaded']:
            path = st.file_uploader("Upload file", type=["csv", "json", "xlsx", "xls"])
            if path:
                with st.spinner('Loading data...'):
                    st.session_state['df'] = load_file(path)
                    st.session_state['file_uploaded'] = True

        if st.session_state['file_uploaded']:
            if st.button("Reset"):
                st.session_state['file_uploaded'] = False
                st.session_state['df'] = None

    elif option == "Use sample data":
        if 'data_option' not in st.session_state:
            st.session_state['data_option'] = "Pick data"
        if 'data_loaded' not in st.session_state:
            st.session_state['data_loaded'] = False

        options = ["Pick data", "Fire data", "Employee data"]
        data_option = st.selectbox("Choose data: ", options, index=options.index(st.session_state['data_option']))

        if data_option != st.session_state["data_option"]:
            st.session_state["data_option"] = data_option
            st.session_state["df"] = None
            st.session_state['data_loaded'] = False

        if data_option != "Pick data" and not st.session_state['data_loaded']:
            if data_option == "Fire data":
                response = requests.get(path1)
                if response.status_code == 200:
                    fire_data = pd.read_json(io.StringIO(response.text))
                    for col in fire_data:
                        if pd.api.types.is_datetime64_any_dtype(fire_data[col]):
                            fire_data[col] = fire_data[col].dt.date
                    st.session_state['df'] = fire_data
                    st.session_state['data_loaded'] = True

            elif data_option == "Employee data":
                response = requests.get(path2)
                if response.status_code == 200:
                    emp = pd.read_excel(io.BytesIO(response.content))
                    for col in emp:
                        if pd.api.types.is_datetime64_any_dtype(emp[col]):
                            emp[col] = emp[col].dt.date
                    st.session_state['df'] = emp
                    st.session_state['data_loaded'] = True

        if data_option == "Pick data":
            st.write("Select a sample data from the drop-down menu")

    if st.session_state['df'] is not None:
        df = st.session_state['df']
        st.success("File uploaded successfully! 🎉 ✅")

        tab1, tab2, tab3, tab4 = st.tabs(["Data Preview", "Data Information", "Column and Row Count", "Descriptive Analysis"])

        with tab1:
            st.markdown('<p class="sub-header">Data Preview</p>', unsafe_allow_html=True)
            st.write(df.head())

        with tab2:
            st.markdown('<p class="sub-header">Data Information</p>', unsafe_allow_html=True)
            buffer = io.StringIO()
            df.info(buf=buffer)
            s = buffer.getvalue()
            st.markdown(f"```{s}```")

        with tab3:
            st.markdown('<p class="sub-header">Column and Row Count</p>', unsafe_allow_html=True)
            st.write(f"Rows: {df.shape[0]}")
            st.write(f"Columns: {df.shape[1]}")

        with tab4:
            st.markdown('<p class="sub-header">Descriptive Analysis</p>', unsafe_allow_html=True)
            st.markdown('<div class="info-message">This gives the statistical value of the numerical columns in the dataframe, please note that other columns are omitted.</div>', unsafe_allow_html=True)
            st.write(df.describe())

    else:
        st.info("Please upload a file to start")

    st.button("Go to Dashboard", on_click=navigate_to, args=("Dashboard",), key='dashboard')
    st.button("Go to EDA Page", on_click=navigate_to, args=("EDA",))


if __name__ == "__main__":
    main()
