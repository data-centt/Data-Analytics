import streamlit as st
from visualisation import Visualization
import pandas as pd


def navigate_to(page_name):
    st.session_state["current_page"] = page_name


def apply_advanced_css():
    st.markdown("""
        <style>
            body {
                background-color: inherit;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                text-align: center;
            }
            

            .css-18e3th9 {
                padding-top: 1rem;  
                padding-bottom: 1rem;  
                padding-left: 1rem;  
                padding-right: 1rem;  
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

            .home-description {
                font-size: 18px;
                color: var(--text-color-light); 
                margin-top: 10px;
                margin-bottom: 20px;
                text-align: center;
            }

            .sub-title {
                font-size: 24px;
                color: #2E86C1; 
                font-weight: bold;
                margin-bottom: 10px;
                text-align: center;
            }

            .sub-description {
                font-size: 16px;
                margin-bottom: 15px;
                color: var(--text-color-light); 
                text-align: center;
            }

            .visualization-container {
                padding: 20px;
                margin-top: 20px;
                border: 1px solid #ddd;
                border-radius: 12px;
                background-color: var(--container-bg-color);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                color: var(--container-text-color);
            }

            .visualization-container:hover {
                transform: scale(1.02);
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
            }

            .link-button {
                display: inline-block;
                font-size: 16px;
                color: #29649e; 
                font-weight: bold;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
                margin: 10px 5px;
                background-color: #007BFF; 
                transition: background-color 0.3s ease;
                text-align: center;
            }

            .link-button:hover {
                background-color: #0056b3; 
            }

            .sub-button {
                background-color: #28a745; 
                display: block;
                margin: auto;
                color: #FFFFFF; /* White text */
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                text-align: center;
            }

            .sub-button:hover {
                background-color: #218838; 
            }

            .logo-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 20px;
            }

            .logo-container img {
                width: 150px; 
                max-width: 100%;
                height: auto;
            }

            @media (max-width: 768px) {
                .sub-title {
                    font-size: 20px;
                }
                .visualization-container {
                    padding: 15px;
                }
            }
        </style>
    """, unsafe_allow_html=True)


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
    section_key = f'section_{section_num}'
    st.session_state[section_key]['inputs_confirmed'] = True


def reset_visualization(section_num):
    section_key = f'section_{section_num}'
    st.session_state[section_key]['inputs_confirmed'] = False


def render_dashboard_section(section_num):
    initialize_session_state(section_num)
    section_key = f'section_{section_num}'
    section_state = st.session_state[section_key]
    vis = Visualization()

    st.markdown(f"<div class='sub-title'>Visualization {section_num}</div>", unsafe_allow_html=True)

    if not section_state['inputs_confirmed']:
        chart_type = st.selectbox(
            f"Select chart for Visualization {section_num}:",
            ["scatter plot", "line chart", "bar chart", "histogram", "area chart", "pie chart", "treemap"],
            key=f'chart_type_{section_num}'
        )

        x_label = "X-axis"
        y_label = "Y-axis"

        if chart_type in ["pie chart", "treemap"]:
            x_label = "Labels"
            y_label = "Values"

        if chart_type == "scatter plot":
            x_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
            y_columns = x_columns
        elif chart_type in ["treemap", "bar chart", "line chart", "area chart"]:
            x_columns = [col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])]
            y_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
        elif chart_type == "histogram":
            x_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
            y_columns = []
        elif chart_type in ["treemap", "pie chart"]:
            y_columns = [col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])]
            x_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
        else:
            x_columns = df.columns
            y_columns = df.columns

        x_column = st.selectbox(f"Choose {x_label} for Visualization {section_num}:", x_columns, key=f'x_column_{section_num}')
        y_column = st.selectbox(f"Choose {y_label} for Visualization {section_num}:", [""] + list(y_columns), key=f'y_column_{section_num}') if chart_type not in ["histogram"] else None

        additional_selected_col = []
        if chart_type in ["area chart", "line chart"] and st.checkbox(f"Add Additional values for Y-axis in Visualization {section_num}", key=f'add_values_{section_num}'):
            num_col = [col for col in df.columns if col not in [x_column, y_column] and pd.api.types.is_numeric_dtype(df[col])]
            additional_selected_col = st.multiselect(f"Select other columns for Visualization {section_num}:", options=num_col, key=f'additional_cols_{section_num}')

        section_state['chart_config'] = {
            'chart_type': chart_type,
            'x_column': x_column,
            'y_column': y_column if y_column else None,
            'additional_selected_col': additional_selected_col
        }

        st.button(f"Confirm Selections for Visualization {section_num}", on_click=confirm_selections, args=(section_num,), key=f'confirm_{section_num}')
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

        st.checkbox(f"Reset", on_change=reset_visualization, args=(section_num,), key=f'reset_{section_num}')


def main():
    apply_advanced_css()
    st.markdown('<div class="logo-container"><img src="https://raw.githubusercontent.com/data-centt/Data-Analytics/main/media/data-cent1.png" alt="Logo"></div>', unsafe_allow_html=True)
    st.markdown('<div class="home-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown("""
        <p class="home-description">
        Welcome to the Dashboard Area! 🎉 This section allows you to choose from four different types of visuals for your data analysis. 📊

You can use a combination of these visuals to tell your data story effectively, whether it's four separate visuals or the same visual for different data partnerships. 🔄

The available visuals are standard storytelling options on MS PowerBI, including:  Pie Chart 🧩,    Treemap 🌳
 , Bar Chart 📈, and more.

**How to Use:**

1) _Select your visual from the options provided._
\n 2) _Click "Confirm Selection" to apply your choice._
\n 3) _If you want to start over, check the "Reset" box to clear your selection._
\n 4) _Use the navigation page to return to the home screen._

Stay tuned—more visuals coming soon! 🚀 📊
        </p>
    """, unsafe_allow_html=True)

    if 'df' in st.session_state and st.session_state['df'] is not None:
        global df
        df = st.session_state['df']

        for i in range(1, 5):
            render_dashboard_section(i)

    else:
        st.warning("No dataset available! Please click on the button below to upload a dataset.")
    st.button("Go to Data Page", on_click=navigate_to, args=("Data",))


if __name__ == "__main__":
    main()

