import os.path


class FileError(Exception):
    pass


class ColumnError(Exception):
    pass


class ChartError(Exception):
    pass


class ErrorHandler:
    def handle_file_error(self, file_name):
        if not file_name:
            raise FileError("No file found")
        elif not os.path.exists(file_name):
            raise FileError("File does not exist")
        elif not file_name.endswith((".csv", ".xlsx", ".xls", ".json")):
            raise FileError("Wrong File, please upload a supported format, csv, excel or json")

    def chart_error(self, chart_type, available_charts):
        if chart_type not in available_charts:
            raise ChartError(f"{chart_type} not supported, please choose from: {', '.join(available_charts)}")

    def handle_column(self, df, column_name):
        if df is None or not hasattr(df, 'columns'):
            raise ColumnError("Could not show columns in the uploaded dataframe")
        if column_name not in df.columns:
            raise ColumnError("Column not available")


error_handler = ErrorHandler()
error_handler.handle_file_error("Budget.xlsx")
