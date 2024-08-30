from visualization import Visualization
import pandas as pd
import streamlit as st


def load_file(file):
    file_path = file.name
    if file_path.endswith(".csv"):
        df = pd.read_csv(file, encoding='utf-8', encoding_errors='ignore')
    elif file_path.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)
    elif file_path.endswith(".json"):
        df = pd.read_json(file)
    else:
        st.error("Unsupported file type")
        return None

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = pd.to_datetime(df[col]).dt.strftime("%d/%m/%Y")

    return df


def main():
    st.title("Data Analytics Dashboard")
    path = st.file_uploader("Upload file", type=["csv", "json", "xlsx", "xls"])
    if path is not None:
        df = load_file(path)
        if df is not None:
            st.write("File uploaded Successfully")
            st.write(df.head())

            vis = Visualization()
            chart_type = st.selectbox("select chart:", ["scatter", "line", "bar", "histogram", "area", "pie", "treemap"])
            x_column = st.selectbox("Choose X-axis: ", df.columns)
            y_column = st.selectbox("Choose Y-axis: ", [""] + list(df.columns))

            add_col = []

            if chart_type in ["area chart", "line chart"]:
                if st.checkbox("Add Additional values for y-axis"):
                    num_col = [col for col in df.columns if col not in [x_column, y_column]
                               and pd.api.types.is_numeric_dtype(df[col])]
                    add_col = st.multiselect("Select other columns:", options=num_col)

         # add_col = []
         #    if chart_type in ["area chart", "line chart"]:
         #        num_col = [col for col in df.columns if col not in [x_column, y_column]
         #                   and pd.api.types.is_numeric_dtype(df[col])]
         #        add_col = st.multiselect("Select other columns ", options=num_col)

            vis.visualize(df, chart_type, x_column, y_column or None, add_col=add_col)
        else:
            st.error("Failed to read file")
    else:
        st.info("Please upload a file to start")


if __name__ == "__main__":
    main()
