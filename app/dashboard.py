import streamlit as st
import pandas as pd
from visualisation import Visualization
from theme import page_header
from nav import goto


def initialize_session_state(section_num):
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


def confirm_selections(section_num):
    st.session_state[f'section_{section_num}']['inputs_confirmed'] = True


def reset_visualization(section_num):
    st.session_state[f'section_{section_num}']['inputs_confirmed'] = False


def render_dashboard_section(section_num, df):
    initialize_session_state(section_num)
    section_key = f'section_{section_num}'
    section_state = st.session_state[section_key]
    vis = Visualization()

    with st.container(border=True):
        st.markdown(f"#### Visualization {section_num}")

        if not section_state['inputs_confirmed']:
            chart_type = st.selectbox(
                f"Select chart for Visualization {section_num}:",
                ["scatter plot", "line chart", "bar chart", "histogram", "area chart", "pie chart", "treemap"],
                key=f'chart_type_{section_num}'
            )

            x_label = "X-axis"
            y_label = "Y-axis"
            if chart_type in ["pie chart", "treemap"]:
                x_label = "Values"
                y_label = "Labels"

            numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
            categorical_cols = [col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])]

            if chart_type == "scatter plot":
                x_columns = numeric_cols
                y_columns = numeric_cols
            elif chart_type in ["bar chart", "line chart", "area chart"]:
                x_columns = categorical_cols
                y_columns = numeric_cols
            elif chart_type == "histogram":
                x_columns = numeric_cols
                y_columns = []
            elif chart_type in ["pie chart", "treemap"]:
                # X = Values (numeric), Y = Labels (categorical)
                x_columns = numeric_cols
                y_columns = categorical_cols
            else:
                x_columns = df.columns
                y_columns = df.columns

            x_column = st.selectbox(f"Choose {x_label} for Visualization {section_num}:", x_columns, key=f'x_column_{section_num}')

            # Y is optional only for a bar chart (it falls back to a count); every
            # other chart needs Y, so preselect a real column instead of a blank "".
            y_optional = chart_type == "bar chart"
            y_options = ([""] + list(y_columns)) if y_optional else list(y_columns)
            y_column = st.selectbox(f"Choose {y_label} for Visualization {section_num}:", y_options, key=f'y_column_{section_num}') if chart_type != "histogram" else None

            additional_selected_col = []
            if chart_type in ["area chart", "line chart"] and st.checkbox(f"Add additional Y-axis values", key=f'add_values_{section_num}'):
                num_col = [col for col in df.columns if col not in [x_column, y_column] and pd.api.types.is_numeric_dtype(df[col])]
                additional_selected_col = st.multiselect(f"Select other columns:", options=num_col, key=f'additional_cols_{section_num}')

            section_state['chart_config'] = {
                'chart_type': chart_type,
                'x_column': x_column,
                'y_column': y_column if y_column else None,
                'additional_selected_col': additional_selected_col
            }

            st.button("Confirm", on_click=confirm_selections, args=(section_num,), key=f'confirm_{section_num}')
        else:
            config = section_state['chart_config']
            x_col = config['x_column']
            y_col = config['y_column']
            add_cols = config['additional_selected_col']

            if config['chart_type'] == "histogram":
                vis.histogram(df, x_col)
            elif config['chart_type'] == "treemap":
                vis.treemap(df, labels=y_col, values=x_col)
            elif config['chart_type'] == "pie chart":
                vis.pie_chart(df, values=x_col, names=y_col)
            else:
                vis.visualize(df, config['chart_type'], x_col, y_col, add_col=add_cols)

            st.checkbox("Reset", on_change=reset_visualization, args=(section_num,), key=f'reset_{section_num}')


def main():
    page_header(
        "Dashboard",
        "Choose up to four interactive Plotly visuals. Pick a chart, select your "
        "columns and click Confirm. Check Reset on a card to start it over.",
    )

    if 'df' in st.session_state and st.session_state['df'] is not None:
        df = st.session_state['df']
        for i in range(1, 5):
            render_dashboard_section(i, df)
    else:
        st.warning("No dataset available yet — load one on the Data page first.")
        if st.button("Go to Data page →"):
            goto("Data")


if __name__ == "__main__":
    main()
