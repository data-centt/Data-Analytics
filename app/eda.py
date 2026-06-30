import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from theme import page_header
from nav import goto


def main():
    page_header(
        "Exploratory Data Analysis",
        "Quick statistical visuals with Matplotlib and Seaborn to understand your "
        "data before deeper analysis or modelling. Tick a chart to reveal it.",
    )

    if 'df' in st.session_state and st.session_state['df'] is not None:
        df = st.session_state['df']
        numeric_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]

        if st.checkbox("Pair Plot", key="pairplot"):
            with st.container(border=True):
                numeric_df = df.select_dtypes(include="number")
                if numeric_df.shape[1] < 2:
                    st.warning("Pair plots need at least two numeric columns.")
                else:
                    if numeric_df.shape[1] > 8:
                        st.info("Showing the first 8 numeric columns to keep the pair plot readable.")
                        numeric_df = numeric_df.iloc[:, :8]
                    with st.spinner("Building pair plot..."):
                        fig = sns.pairplot(numeric_df)
                    st.pyplot(fig)

        if st.checkbox("Box Plot", key="boxplot"):
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.boxplot(
                    data=df,
                    x=st.selectbox("X-axis", df.columns, key="box_x-axis"),
                    y=st.selectbox("Y-axis", numeric_columns, key="box_y-axis"),
                    ax=ax
                )
                ax.tick_params(axis='x', rotation=90)
                plt.tight_layout()
                st.pyplot(fig)

        if st.checkbox("Histogram", key="histogram"):
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.histplot(
                    data=df,
                    x=st.selectbox("X-axis", df.columns, key="hist_x-axis"),
                    bins=st.slider("Bins", 1, 1000, value=20),
                    kde=True,
                    ax=ax
                )
                st.pyplot(fig)

        if st.checkbox("Scatter Plot", key="scatter"):
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.scatterplot(
                    data=df,
                    x=st.selectbox("X-axis", numeric_columns, key="scatter_x-axis"),
                    y=st.selectbox("Y-axis", numeric_columns, key="scatter_y-axis"),
                    ax=ax
                )
                st.pyplot(fig)

        if st.checkbox("Count Plot", key="count"):
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.countplot(data=df, x=st.selectbox("Column", df.columns, key="axis"), ax=ax)
                ax.tick_params(axis='x', rotation=90)
                plt.tight_layout()
                st.pyplot(fig)

        if st.checkbox("Violin Plot", key="violin"):
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.violinplot(
                    data=df,
                    x=st.selectbox("X-axis", df.columns, key="violin-x-axis"),
                    y=st.selectbox("Y-axis", numeric_columns, key="violin_y-axis"),
                    ax=ax
                )
                ax.tick_params(axis='x', rotation=90)
                plt.tight_layout()
                st.pyplot(fig)

        if st.checkbox("Bar Chart", key="bar"):
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.barplot(
                    data=df,
                    x=st.selectbox("Labels", df.columns, key="bar_x-axis"),
                    y=st.selectbox("Values", numeric_columns, key="bar_y-axis"),
                    ax=ax,
                    errorbar=None
                )
                ax.tick_params(axis='x', rotation=90)
                plt.tight_layout()
                st.pyplot(fig)

        if st.checkbox("Line Chart", key="line"):
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.lineplot(
                    data=df,
                    x=st.selectbox("Labels", df.columns, key="line_x-axis"),
                    y=st.selectbox("Values", numeric_columns, key="line_y-axis"),
                    ax=ax,
                    errorbar=None
                )
                ax.tick_params(axis='x', rotation=90)
                plt.tight_layout()
                st.pyplot(fig)

    else:
        st.warning("No dataset available yet — load one on the Data page first.")
        st.button("Go to Data page →", on_click=goto, args=("Data",))


if __name__ == "__main__":
    main()
