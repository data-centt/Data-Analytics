"""Cross-page navigation helper.

The entry script (home.py) registers the st.Page objects in session state so any
page can jump to another with goto("Dashboard"), e.g. from a call-to-action
button. The sidebar still provides the primary navigation.
"""
import streamlit as st


def goto(name):
    pages = st.session_state.get("_pages", {})
    if name in pages:
        st.switch_page(pages[name])
