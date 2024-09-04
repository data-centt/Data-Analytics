import streamlit as st
from visualisation import Visualization
import pandas as pd


def apply_advanced_css():
    st.markdown("""
        <style>
            .main-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }

            .main .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
                padding-left: 2rem;
                padding-right: 2rem;
                background-color: #f7f7f9;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transition: all 0.2s ease-in-out;
            }

            .css-18e3th9 {
                padding-top: 1rem;  
                padding-bottom: 1rem;  
                padding-left: 1rem;  
                padding-right: 1rem;  
            }

            .stMarkdown h2 {
                color: #4B0082;
                font-weight: bold;
                text-align: center;
                margin-top: 20px;
                margin-bottom: 20px;
                text-transform: uppercase;
            }

            .small-checkbox {
                display: inline-block;
                margin-right: 10px;
                margin-top: 10px;
            }


            .stSelectbox, .stButton {
                margin-top: 15px;
                margin-bottom: 15px;
            }


            .visualization-container {
                padding: 20px;
                margin-top: 20px;
                border: 1px solid #ddd;
                border-radius: 12px;
                background-color: #ffffff;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .visualization-container:hover {
                transform: scale(1.02);
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
            }

            @media (max-width: 768px) {
                .main .block-container {
                    padding: 1rem;
                }
                .stMarkdown h2 {
                    font-size: 20px;
                }
                .visualization-container {
                    padding: 15px;
                }
            }
        </style>
    """, unsafe_allow_html=True)


def render_dashboard_section(section_num):
    with st.container():
        st.subheader(f"Visualization {section_num}")

        section_key = f'section_{section_num}'
        if section_key not in st.session_state:
            st.session_state[section_key] = {
                'inputs_confirmed': False,
                'chart_config': {
                    'chart_type': None,
                    'x_column': None,
                    'y_column': None,
                    'additional_selected_col': []
                }
            }

        section_state = st.session_state[section_key]
        vis = Visualization()

        if not section_state['inputs_confirmed']:
            chart_type = st.selectbox(f"Select chart for Visualization {section_num}:",
                                      ["scatter plot", "line chart", "bar chart", "histogram",
                                       "area chart", "pie chart", "treemap"])

            x_label = "X-axis"
            y_label = "Y-axis"
            if chart_type in ["pie chart"]:
                x_label = "Values"
                y_label = "Labels"

            x_column = st.selectbox(f"Choose {x_label} for Visualization {section_num}:", df.columns)

            y_column = None
            if chart_type in ["scatter plot", "line chart", "bar chart", "area chart", "pie chart", "treemap"]:
                y_column = st.selectbox(f"Choose {y_label} for Visualization {section_num}:", [""] + list(df.columns))

            additional_selected_col = []
            if chart_type in ["area chart", "line chart"]:
                if st.checkbox(f"Add Additional values for Y-axis in Visualization {section_num}"):
                    num_col = [col for col in df.columns if col not in [x_column, y_column]
                               and pd.api.types.is_numeric_dtype(df[col])]
                    additional_selected_col = st.multiselect(f"Select other columns for Visualization {section_num}:",
                                                             options=num_col)

            section_state['chart_config'] = {
                'chart_type': chart_type,
                'x_column': x_column,
                'y_column': y_column if y_column else None,
                'additional_selected_col': additional_selected_col
            }

            if st.button(f"Confirm Selections for Visualization {section_num}"):
                section_state['inputs_confirmed'] = True
        else:
            config = section_state['chart_config']
            x_col = config['x_column']
            y_col = config['y_column']
            add_cols = config['additional_selected_col']

            if config['chart_type'] == "histogram":
                vis.histogram(df, x_col)
            elif config['chart_type'] == "treemap":
                vis.treemap(df, x_col, y_col if y_col else x_col)
            elif config['chart_type'] == "pie chart":
                vis.pie_chart(df, values=x_col, names=y_col if y_col else x_col)
            else:
                vis.visualize(df, config['chart_type'], x_col, y_col, add_col=add_cols)

            reset_input = st.checkbox(f"Reset Visualization {section_num}", key=f'reset_{section_num}', value=False,
                                      help="Check to reset visualization inputs.")
            if reset_input:
                section_state['inputs_confirmed'] = False


def main():

    apply_advanced_css()

    st.title("Multi-Visualization Dashboard")

    if 'df' in st.session_state and st.session_state['df'] is not None:
        global df
        df = st.session_state['df']

        for i in range(1, 5):
            render_dashboard_section(i)
    else:
        st.write("**Please upload a dataset on the main page**")


if __name__ == "__main__":
    main()
