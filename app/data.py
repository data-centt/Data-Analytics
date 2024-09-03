import streamlit as st
import io
from error_handler import load_file

st.markdown(
    """
    <style>
    /* General Styling */
    body {
        font-family: 'Open Sans', sans-serif;
        background-color: #f4f7fa;
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


def main():
    st.markdown('<p class="main-title">Data Overview</p>', unsafe_allow_html=True)

    reset = st.sidebar.button("Reset Data")

    if reset:
        st.session_state['file_uploaded'] = False
        st.session_state['df'] = None

    if 'df' not in st.session_state:
        st.session_state['df'] = None

    if 'file_uploaded' not in st.session_state:
        st.session_state['file_uploaded'] = False

    if not st.session_state['file_uploaded']:
        path = st.file_uploader("Upload file", type=["csv", "json", "xlsx", "xls"])
        if path:
            with st.spinner('Loading data...'):
                st.session_state['df'] = load_file(path)
                st.session_state['file_uploaded'] = True

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

    else:
        st.info("Please upload a file to start")


if __name__ == "__main__":
    main()
