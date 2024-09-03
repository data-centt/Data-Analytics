import streamlit as st
from eda import main as eda_main
from data import main as data_main
from dashboard import main as dashboard_main


def navigate_to(page_name):
    st.session_state["current_page"] = page_name


if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    navigate_to("Home")
if st.sidebar.button("Data"):
    navigate_to("Data")
if st.sidebar.button("Dashboard"):
    navigate_to("Dashboard")
if st.sidebar.button("EDA"):
    navigate_to("EDA")

current_page = st.session_state['current_page']

if current_page == "Home":
    st.markdown(
        """
        <style>
        .container {
            max-width: 850px;
            margin: 0 auto;
            padding: 20px;
            border-radius: 10px;
            background-color: #f7f9fc;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .home-title {
            font-size: 36px;
            color: #097AFA;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .home-description {
            font-size: 18px;
            color: #34495E;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        .link-button {
            display: inline-block;
            font-size: 16px;
            color: #F1E4E8;
            font-weight: bold;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
            margin: 10px 5px;
            transition: background-color 0.3s ease;
        }
        .github-link {
            background-color: #333;
        }
        .github-link:hover {
            background-color: #555;
        }
        .linkedin-link {
            background-color: #C5CFDC;
        }
        .linkedin-link:hover {
            background-color: #005582;
        }
        .logo-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .logo-container img {
            width: 200px;
            max-width: 100%;
            height: auto;
        }
        .sub-container {
            background-color: #eaf2f8;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            text-align: left;
        }
        .sub-title {
            font-size: 24px;
            color: #097AFA;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .sub-description {
            font-size: 16px;
            color: #34495E;
            margin-bottom: 15px;
        }
        .sub-button {
            background-color: #3498db;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .sub-button:hover {
            background-color: #2980b9;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="logo-container"><img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*hf5w4xLfIfnr50ZYEUNOVw.jpeg" alt="Logo"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="container">
            <div class="home-title">Data Analytics!</div>
            <p class="home-description">
                
This project is made to deliver powerful data analysis and visualization tools, offering a comprehensive platform for in-depth data exploration 📊. With this project, you can delve into a diverse range of datasets, perform detailed Exploratory Data Analysis (EDA) 🔍, and interact with dynamic dashboards designed to uncover valuable insights 📈. Whether you're a data enthusiast, a seasoned professional, or simply curious about data trends, this project is tailored to make data exploration both accessible and engaging for everyone 🌟.

For any issues you encounter while performing analysis or navigating through the webpage, please refer to the GitHub repository linked below to create an issue 🛠️. Alternatively, feel free to reach out to me directly via LinkedIn for personalized assistance 💬. Your feedback is crucial for improving the project and ensuring a smooth user experience 🚀.
            </p>
            <div>
                <a class="link-button github-link" href="https://github.com/Daniel15568/Data-Analytics-Dashboard" target="_blank">
                    👉 Check out the GitHub Repository
                </a>
                <a class="link-button linkedin-link" href="https://www.linkedin.com/in/daniel15568" target="_blank">
                    👨‍💻 Connect with me on LinkedIn
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    with st.container():
        st.markdown(
            """
            <div class="sub-container">
                <div class="sub-title">Data</div>
                <p class="sub-description">
                    Upload and explore your datasets with ease! 📤 Whether you choose to upload your own data or utilize one of the provided sample datasets, you’ll have the tools to perform comprehensive analyses 🔍. Dive into detailed statistical summaries and gain a thorough understanding of your data with our intuitive interface 📊.

Quickly access essential statistical insights and uncover full information about your datasets to drive informed decisions and discoveries. 📈✨
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Go to Data Page"):
            navigate_to("Data")

    with st.container():
        st.markdown(
            """
            <div class="sub-container">
                <div class="sub-title">Exploratory Data Analysis ( EDA )</div>
                <p class="sub-description">
                   Dive into Exploratory Data Analysis (EDA) with our collection of pre-made charts, created using the powerful Matplotlib and Seaborn visualization libraries 🎨📊. Whether you're preparing to apply machine learning techniques or simply looking to uncover statistical insights, these ready-to-use visualizations are designed to provide a deeper statistical understanding of your data 🔍📈. Easily identify patterns, trends, and key insights with these intuitive and informative graphics, and enhance your analytical capabilities effortlessly.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Go to EDA Page"):
            navigate_to("EDA")

    with st.container():
        st.markdown(
            """
            <div class="sub-container">
                <div class="sub-title">Custom Dashboard</div>
                <p class="sub-description">
                    View interactive dashboards that offer valuable insights into key metrics and trends within your data 🌟📊. Customize your dashboard to match your specific analytical needs, whether for business or personal analysis 🔧📈.

Experience the power of interactive dashboards and data insights without the need to subscribe to or download any additional apps. Our dashboards, powered by the robust Plotly Express library, provide dynamic and visually engaging data visualizations 🚀📉. Enjoy open-source business analysis tools at no cost and gain comprehensive insights for free!
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Go to Dashboard Page"):
            navigate_to("Dashboard")


elif current_page == "Data":
    data_main()
elif current_page == "Dashboard":
    dashboard_main()
elif current_page == "EDA":
    eda_main()
