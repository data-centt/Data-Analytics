import os.path
import pandas as pd

class FileError(Exception):
    pass


class ColumnError(Exception):
    pass


class ChartError(Exception):
    pass


class ErrorHandler:
    def __init__(self):
        pass

    def handle_file_error(self, file_name):
        if not file_name:
            raise FileError("No file found")
        elif not os.path.exists(file_name):
            raise FileError("File does not exist")
        elif not file_name.endswith((".csv", ".xlsx", ".xls", ".json")):
            raise FileError("Wrong File, please upload a supported format, csv, excel or json")

    def chart_error(self, chart_type, available_charts, df=None, x_col=None, y_col=None):
        if chart_type not in available_charts:
            raise ChartError(f"{chart_type} not supported, please choose from: {', '.join(available_charts)}")
        if df is not None:
            if chart_type in ["scatter"]:
                if x_col and not pd.api.types.is_numeric_dtype(df[x_col]):
                    raise ColumnError(f"{x_col} is not compatible")
                if y_col and not pd.api.types.is_numeric_dtype(df[y_col]):
                    raise ColumnError(f"{y_col} is not compatible with this chart")
            elif chart_type in ["bar", "box", "histogram", "area"]:
                if y_col and not pd.api.types.is_numeric_dtype(df[y_col]):
                    raise ColumnError(f"{y_col} is not compatible with this chart")
            elif chart_type in ["treemap", "pie"]:
                if x_col and not pd.api.types.is_numeric_dtype(df[x_col]):
                    raise ColumnError(f"{x_col} is not compatible with this chart")


    def handle_column(self, df, column_name):
        if df is None or not hasattr(df, 'columns'):
            raise ColumnError("Could not show columns in the uploaded dataframe")
        if column_name not in df.columns:
            raise ColumnError("Choose column to get visualisation")

