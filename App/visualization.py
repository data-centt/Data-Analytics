import matplotlib.pyplot as plt
import seaborn as sns
from error_handler import ColumnError, ChartError, ErrorHandler
import streamlit as st


class Visualization:
    def __init__(self):
        self.error_handler = ErrorHandler()

    def bar_chart(self, df, x_column, y_column=None):
        try:
            self.error_handler.handle_column(df, x_column)
            if y_column:
                self.error_handler.handle_column(df, y_column)
            plt.figure(figsize=(10, 6))
            if y_column:
                sns.barplot(data=df, x=x_column, y=y_column)
                plt.title(f"Bar chart of {x_column} against {y_column}")
            else:
                sns.countplot(data=df, x=x_column)
                plt.title(f" Chart of {x_column}")
            st.pyplot(plt)
        except ColumnError as e:
            st.error(str(e))

    def line_chart(self, df, x_column, y_column):
        try:
            self.error_handler.handle_column(df, x_column)
            self.error_handler.handle_column(df, y_column)
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=df, x=x_column, y=y_column)
            plt.title(f"Line Chart of {x_column} against {y_column}")
            st.pyplot(plt)
        except ColumnError as e:
            st.error(str(e))

    def histogram(self, df, column):
        try:
            self.error_handler.handle_column(df, column)
            plt.figure(figsize=(10, 6))
            bins = st.number_input("input bins", min_value=2, max_value=500, step=1)
            sns.histplot(data=df, x=column, bins=bins)
            plt.title(f"Histogram of {column}")
            st.pyplot(plt)
        except ColumnError as e:
            st.error(str(e))

    def scatterplot(self, df, x_column, y_column):
        try:
            self.error_handler.handle_column(df, x_column)
            self.error_handler.handle_column(df, y_column)
            sns.scatterplot(df, x=x_column, y=y_column)
            plt.title(f"Scatter plot of {x_column} against {y_column}")
            st.pyplot(plt)
        except ColumnError as e:
            st.error(str(e))

    def visualize(self, df, chart_type, x_column, y_column=None):
        chart_types = ["bar", "histogram", "line", "scatter"]
        try:
            self.error_handler.chart_error(chart_type, chart_types)
            if chart_type == "bar":
                self.bar_chart(df, x_column, y_column)
            elif chart_type == "histogram":
                self.histogram(df, x_column)
            elif chart_type == "line":
                self.line_chart(df, x_column, y_column)
            elif chart_type == "scatter":
                self.scatterplot(df, x_column, y_column)
        except ChartError as e:
            st.error(str(e))
