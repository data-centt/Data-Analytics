from plotly import express as px
from error_handler import ColumnError, ChartError, ErrorHandler
import plotly.graph_objects as go
import streamlit as st
import pandas as pd


class Visualization:
    def __init__(self):
        self.error_handler = ErrorHandler()
        self.colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'grey']
        self.color_index = 0

    def get_next_color(self):
        color = self.colors[self.color_index % len(self.colors)]
        self.color_index += 1
        return color

    def bar_chart(self, df, x_column, y_column=None):
        try:
            self.error_handler.handle_column(df, x_column)
            if y_column:
                self.error_handler.handle_column(df, y_column)
            if y_column:
                fig = px.bar(data_frame=df, x=x_column, y=y_column, title=f"Bar chart of {x_column} against {y_column}")
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
            else:
                fig = px.bar(data_frame=df, x=x_column, title=f"Bar Chart of {x_column}")
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
            fig.update_layout(
                title=dict(
                    font=dict(size=14),
                    x=0.5
                ),
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis=dict(tickangle=45),
                yaxis=dict(showgrid=False),
                height=300
            )

            st.plotly_chart(fig)
        except ColumnError as e:
            st.error(str(e))

    def line_chart(self, df, x_column, y_column, add_col=None):
        try:
            self.error_handler.handle_column(df, x_column)
            self.error_handler.handle_column(df, y_column)

            df_agg = df.groupby(x_column, as_index=False)[y_column].sum()
            df_agg = df_agg.sort_values(by=x_column)

            fig = px.line(
                data_frame=df_agg,
                x=x_column,
                y=y_column,
                title=f"Line Chart of {x_column} against {y_column}"
            )

            if add_col:
                for col in add_col:
                    if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                        df_add = df.groupby(x_column, as_index=False)[col].sum()
                        df_add = df_add.sort_values(by=x_column)

                        fig.add_trace(
                            go.Scatter(
                                x=df_add[x_column],
                                y=df_add[col],
                                mode="lines",
                                name=f"{col}",
                                line=dict(color=self.get_next_color())
                            )
                        )

            fig.update_layout(
                title={
                    'text': f"Line Chart of {x_column} against {y_column}",
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {
                        'size': 15
                    }
                },
                xaxis_title=f"{x_column}",
                yaxis_title=f"{y_column}",
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(204, 204, 204)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                ),
                yaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(0, 0, 224)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='New Times Roman',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                ),
                autosize=True,
                margin=dict(
                    autoexpand=True,
                    l=100,
                    r=20,
                    t=110,
                ),
                showlegend=True,
                plot_bgcolor='white'
            )
            fig.update_traces(mode='lines', marker=dict(size=5, line=dict(width=1)))

            st.plotly_chart(fig)
        except ColumnError as e:
            st.error(str(e))

    def histogram(self, df, column):
        try:
            self.error_handler.handle_column(df, column)
            bins = st.slider("input bins", min_value=50, max_value=200, step=10)
            fig = px.histogram(data_frame=df, x=column, nbins=bins, title=f"Histogram of {column}")
            fig.update_layout(
                title={
                    'text': f"Histogram of {column}",
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {
                        'size': 20
                    }
                },
                xaxis_title=f"{column}",
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(204, 204, 204)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                ),
                yaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(0, 0, 224)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='New Times Roman',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                ),
                autosize=True,
                margin=dict(
                    autoexpand=True,
                    l=100,
                    r=20,
                    t=110,
                ),
                showlegend=False,
                plot_bgcolor='white'
            )
            fig.update_traces(marker=dict(line=dict(width=1, color='black')))

            st.plotly_chart(fig)

        except ColumnError as e:
            st.error(str(e))

    def scatterplot(self, df, x_column, y_column):
        try:
            self.error_handler.handle_column(df, x_column)
            self.error_handler.handle_column(df, y_column)
            fig = px.scatter(data_frame=df, x=x_column, y=y_column, title=f"Scatter Plot of {x_column} and {y_column}")
            fig.update_layout(
                title={
                    'text': f"Scatter Plot of {x_column} and {y_column}",
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {
                        'size': 20
                    }
                },
                xaxis_title=f"{x_column}",
                yaxis_title=f"{y_column}",
                xaxis=dict(
                    showline=False,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(204, 204, 204)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                ),
                yaxis=dict(
                    showline=False,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(0, 0, 224)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='New Times Roman',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                ),
                autosize=True,
                margin=dict(
                    autoexpand=True,
                    l=100,
                    r=20,
                    t=110,
                ),
                showlegend=False,
                plot_bgcolor='white'
            )

            st.plotly_chart(fig)

        except ColumnError as e:
            st.error(str(e))

    def treemap(self, df, labels, values):
        try:
            self.error_handler.handle_column(df, labels)
            self.error_handler.handle_column(df, values)
            fig = px.treemap(data_frame=df, path=[labels], values=values)

            fig.update_layout(
                title={
                    'text': f"Treemap of {labels}",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {
                        'size': 20
                    }
                },
                autosize=True,
                margin=dict(
                    autoexpand=True,
                    l=50,
                    r=50,
                    t=70,
                ),
                plot_bgcolor='white'
            )
            fig.update_traces(marker=dict(line=dict(width=2, color='rgba(0, 0, 0, 0.2)')))
            st.plotly_chart(fig)
        except ColumnError as e:
            st.error(str(e))

    def pie_chart(self, df, values, names):
        try:
            self.error_handler.handle_column(df, values)
            self.error_handler.handle_column(df, names)
            df_agg = df.groupby(names, as_index=False)[values].sum()
            fig = px.pie(data_frame=df_agg, names=names, values=values)
            fig.update_layout(
                title={
                    'text': f"Pie Chart of {values} by {names}",
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {
                        'size': 20
                    }
                },
                showlegend=True
            )
            st.plotly_chart(fig)
        except ChartError as e:
            st.error(str(e))

    def area(self, df, x_col, y_col, add_col=None):
        try:
            self.error_handler.handle_column(df, x_col)
            self.error_handler.handle_column(df, y_col)
            df_agg = df.groupby(x_col, as_index=False)[y_col].sum()

            fig = px.area(data_frame=df_agg, x=x_col, y=y_col, title=f"Area chart of {x_col} and {y_col}")

            if add_col:
                for col in add_col:
                    if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                        df_add = df.groupby(x_col, as_index=False)[col].sum()
                        fig.add_trace(
                            go.Scatter(
                                x=df_add[x_col],
                                y=df_add[col],
                                mode='lines',
                                fill='tonexty',
                                name=col
                            )
                        )
                    else:
                        st.warning(f"{col} not compatible")
            fig.update_layout(
                title={
                    'text': f"Line Chart of {x_col} against {y_col}",
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {
                        'size': 20
                    }
                },
                xaxis_title=f"{x_col}",
                yaxis_title=f"{y_col}",
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(204, 204, 204)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                ),
                yaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=False,
                    linecolor='rgb(0, 0, 224)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='New Times Roman',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                ),
                autosize=True,
                margin=dict(
                    autoexpand=True,
                    l=100,
                    r=20,
                    t=110,
                ),
                showlegend=True,
                plot_bgcolor='white'
            )
            st.plotly_chart(fig)
        except ChartError as e:
            st.error(str(e))

    def visualize(self, df, chart_type, x_column, y_column=None, add_col=None):
        chart_types = ["scatter plot", "line chart", "bar chart", "histogram", "area chart", "pie chart", "treemap"]
        try:
            self.error_handler.chart_error(chart_type, chart_types)
            if chart_type == "bar chart":
                self.bar_chart(df, x_column, y_column)
            elif chart_type == "histogram":
                self.histogram(df, x_column)
            elif chart_type == "line chart":
                self.line_chart(df, x_column, y_column, add_col=add_col)
            elif chart_type == "scatter plot":
                self.scatterplot(df, x_column, y_column)
            elif chart_type == "pie chart":
                if not x_column and not y_column:
                    raise ChartError("Please input both columns")
                self.pie_chart(df, values=x_column, names=y_column)
            elif chart_type == "area chart":
                self.area(df, x_column, y_column, add_col=add_col)
            elif chart_type == "treemap":
                self.treemap(df, x_column, y_column)

        except (ChartError, ColumnError) as e:
            st.error(str(e))
