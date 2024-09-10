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
    global response
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
    st.button("Go to EDA Page", on_click=navigate_to, args=("EDA",))
    st.button("Go to Dashboard", on_click=navigate_to, args=("Dashboard",), key='dashboard')
    
    option = st.radio("Select Data:", ("I have my data", "Test with sample data"))
    
    path1 = "https://raw.githubusercontent.com/data-centt/Data-Analytics/main/sample%20data/fire.json"
    path2 = "https://raw.githubusercontent.com/data-centt/Data-Analytics/main/sample%20data/test.xlsx"

    if 'df' not in st.session_state:
        st.session_state['df'] = None

    if "data_source" not in st.session_state:
        st.session_state["data_source"] = "Upload your own data"

    if st.session_state["data_source"] != option:
        st.session_state["data_source"] = option
        st.session_state["df"] = None

    if option == "I have my data":
        if 'file_uploaded' not in st.session_state:
            st.session_state['file_uploaded'] = False

        if not st.session_state['file_uploaded']:
            path = st.file_uploader("Upload file", type=["csv", "json", "xlsx", "xls"])
            if path:
                with st.spinner('Loading data...'):
                    st.session_state['df'] = load_file(path)
                    st.session_state['file_uploaded'] = True

    elif option == "Test with sample data":
        if "data_option" not in st.session_state:
            st.session_state["data_option"] = "Pick data"

        options = ["Pick data", "Fire data", "Employee data"]
        current_option = st.session_state.get("data_option", "Pick data")

        if current_option not in options:
            current_option = "Pick data"

        data_option = st.selectbox("Choose data: ", options,
                                   index=options.index(current_option))

        if st.session_state["data_option"] != data_option:
            st.session_state["data_option"] = data_option
            st.session_state["df"] = None

        if st.session_state['df'] is None:
            if data_option == "Fire data":
                response = requests.get(path1)
                if response.status_code == 200:
                    st.session_state['df'] = pd.read_json(io.StringIO(response.text))
            elif data_option == "Employee data":
                response = requests.get(path2)
                if response.status_code == 200:
                    st.session_state['df'] = pd.read_excel(io.BytesIO(response.content))
            elif data_option == "Pick data":
                st.write("Select a sample data from the drop-down menu")
            else:
                st.error("Seems like there are no sample data, please upload yours or reach out to me on linkedIn.")

    if st.session_state['df'] is not None:
        df = st.session_state['df']

        if df is not None:
            st.success("File uploaded successfully! 🎉🙌 ✅👍📶")

            tab1, tab2, tab3, tab4 = st.tabs(["Data Preview", "Data Information", "Column and Row Count",
                                              "Descriptive Analysis"])

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
                st.markdown(
                    '<div class="info-message">This gives the statistical value of the numerical columns in the '
                    'dataframe, please note that other columns are omitted.</div>',
                    unsafe_allow_html=True)
                st.write(df.describe())

            reset = st.button("Reset Uploaded Data")

            if reset:
                st.session_state['file_uploaded'] = False
                st.session_state['df'] = None

    else:
        st.info("Please upload a file to start")
    st.button("Home Page", on_click=navigate_to, args=("Home",))


if __name__ == "__main__":
    main()
