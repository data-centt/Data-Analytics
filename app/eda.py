import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def navigate_to(page_name):
    st.session_state["current_page"] = page_name


def apply_custom_css():
    st.markdown(
        """
        <style>
        body {
                background-color: inherit;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                text-align: left;
            }
        .main-container {
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }

         .home-title {
                font-size: 40px;
                color: #2E86C1; 
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 20px;
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                text-align: center;
            }

        .sub-title {
            font-size: 26px;
            color: #4B0082;
            margin-top: 30px;
            font-weight: bold;
            text-align: center;
            text-transform: uppercase;
        }
        
        .desc {
            font-size: 18px;
            color: #696969;
            text-align: center;
            margin-bottom: 20px;
            line-height: 1.5;
            letter-spacing: 0.5px;
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
        .plot-container {
            padding: 20px;
            margin-top: 20px;
            border: 1px solid #ddd;
            border-radius: 12px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: transform 0.2s ease-in-out;
        }

        .plot-container:hover {
            transform: scale(1.02);
        }

        .stCheckbox, .stSelectbox {
            margin-top: 15px;
            margin-bottom: 15px;
        }

        @media (max-width: 768px) {
            .main-title {
                font-size: 28px;
            }
            .sub-title {
                font-size: 22px;
            }
            .plot-container {
                padding: 15px;
                margin-top: 15px;
            }
        }
        </style>
        """, unsafe_allow_html=True
    )


def main():
    apply_custom_css()
    st.markdown(
        '<div class="logo-container"><img src="https://raw.githubusercontent.com/data-centt/Data-Analytics/main/media/data-cent1.png" alt="Logo"></div>',
        unsafe_allow_html=True)
    st.markdown('<h1 class="home-title">Exploratory Data Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="desc">Explore your data and make quick statistical analysis with matplotlib and seaborn to better understand before further analysis or building machine learning models.</p>', unsafe_allow_html=True)

    if 'df' in st.session_state and st.session_state['df'] is not None:
        df = st.session_state['df']

        if df is not None:
            if st.checkbox("PairPlots", key="pairplot"):
                st.markdown(f'<h2 class="sub-title">PairPlots</h2>', unsafe_allow_html=True)
                with st.container():
                    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                    fig = sns.pairplot(df)
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)

            if st.checkbox("Boxplot", key="boxplot"):
                st.markdown(f'<h2 class="sub-title">Boxplot</h2>', unsafe_allow_html=True)
                st.write("X-axis only contains numeric columns, same as y.")
                with st.container():
                    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.boxplot(
                        data=df,
                        x=st.selectbox("x-axis", df.columns, key="box_x-axis"),
                        y=st.selectbox(
                            "y-axis",
                            [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])],
                            key="box_y-axis"
                        ),
                        ax=ax
                    )
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                    plt.tight_layout()
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)

            if st.checkbox("Histogram", key="histogram"):
                st.markdown(f'<h2 class="sub-title">Histogram</h2>', unsafe_allow_html=True)
                with st.container():
                    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.histplot(
                        data=df,
                        x=st.selectbox("x-axis:", df.columns, key="hist_x-axis"),
                        bins=st.slider("choose bins:", 1, 1000),
                        kde=True,
                        ax=ax
                    )
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)

            if st.checkbox("Scatter Plot", key="scatter"):
                st.markdown(f'<h2 class="sub-title">Scatter Plot</h2>', unsafe_allow_html=True)
                with st.container():
                    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.scatterplot(
                        data=df,
                        x=st.selectbox("X-axis", [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])], key="scatter_x-axis"),
                        y=st.selectbox("y-axis", [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])], key="scatter_y-axis"),
                        ax=ax
                    )
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)

            if st.checkbox("Count Plot", key="count"):
                st.markdown(f'<h2 class="sub-title">Count Plot</h2>', unsafe_allow_html=True)
                with st.container():
                    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(10, 5))
                    sns.countplot(data=df, x=st.selectbox("axis", df.columns, key="axis"), ax=ax)
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                    plt.tight_layout()
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)

            if st.checkbox("Violin Plot", key="violin"):
                st.markdown(f'<h2 class="sub-title">Violin Plot</h2>', unsafe_allow_html=True)
                with st.container():
                    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(10, 5))
                    sns.violinplot(
                        data=df,
                        x=st.selectbox("X-axis", df.columns, key="violin-x-axis"),
                        y=st.selectbox("y-axis", [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])], key="violin_y-axis"),
                        ax=ax
                    )
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                    plt.tight_layout()
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)

            if st.checkbox("Bar Chart", key="bar"):
                st.markdown(f'<h2 class="sub-title">Bar Chart</h2>', unsafe_allow_html=True)
                with st.container():
                    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(10, 5))
                    sns.barplot(
                        data=df,
                        x=st.selectbox("Labels", df.columns, key="bar_x-axis"),
                        y=st.selectbox("values", [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])], key="bar_y-axis"),
                        ax=ax,
                        ci=None
                    )
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                    plt.tight_layout()
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)

            if st.checkbox("Line Chart", key="line"):
                st.markdown(f'<h2 class="sub-title">Line Chart</h2>', unsafe_allow_html=True)
                with st.container():
                    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(10, 5))
                    sns.lineplot(
                        data=df,
                        x=st.selectbox("Labels", df.columns, key="line_x-axis"),
                        y=st.selectbox("values", [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])], key="line_y-axis"),
                        ax=ax,
                        ci=None
                    )
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                    plt.tight_layout()
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("No dataset available! Please click on the button below to upload a dataset.")
    st.button("Go to Data Page", on_click=navigate_to, args=("Data",))


if __name__ == "__main__":
    main()
