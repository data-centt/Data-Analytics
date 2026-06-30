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
            df[col] = df[col].dt.date

    return df


class ColumnError(Exception):
    pass


class ChartError(Exception):
    pass


class ErrorHandler:
    def chart_error(self, chart_type, available_charts):
        if chart_type not in available_charts:
            raise ChartError(f"{chart_type} not supported, please choose from: {', '.join(available_charts)}")

    def handle_column(self, df, column_name):
        if df is None or not hasattr(df, 'columns'):
            raise ColumnError("Could not show columns in the uploaded dataframe")
        if column_name not in df.columns:
            raise ColumnError("Choose column to get visualisation")
