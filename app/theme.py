"""Shared theming and small UI helpers for the Data-Cent app.

Keeping all presentation in one place means every page looks consistent and the
CSS lives in exactly one spot instead of being copy-pasted across modules.
"""
import os
import streamlit as st

# media/ lives one level up from app/
LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "media", "data-cent1.png")

_GLOBAL_CSS = """
<style>
/* Roomier, centred content column */
.block-container { padding-top: 2.5rem; padding-bottom: 4rem; max-width: 1120px; }

/* Headings: tighter, modern */
h1, h2, h3 { letter-spacing: -0.015em; font-weight: 700; }

/* Buttons: pill-ish, confident */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    padding: 0.45rem 1rem;
}

/* Give bordered containers a touch more breathing room */
[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 14px; }
</style>
"""


def apply_theme():
    """Inject the global stylesheet. Call once from the entry script."""
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)


def page_header(title, subtitle=None):
    """Standard page title + optional subtitle + divider."""
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()
