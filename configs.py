import streamlit as st
import pymongo
from pymongo import MongoClient

_LIBRARY_TAB_NAMES = [
    "🔍 Search",
    "🆕 Recently Added",
    "➕ Add to Database",
    "🧸 More"
]

_LIBRARY_MATERIAL_TYPE_LIST = ["PDF", "Website", "Slides", "Other"]

_LIBRARY_MATERIAL_STATUS = [
    "Professor Requested / Approved",
    "Supplementary"
]


# hide "made with streamlit" and upper right hamburger
hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stApp [data-testid="stToolbar"] {display: none;}
            .styles_stateContainer__29Rp6 [data-testid="manage-app-button"] {display: none;}
            .styles_stateContainer__29Rp6 .viewerBadge_container__1QSob {display: none;}
            </style>
            """

# get mongodb connection
@st.experimental_singleton(suppress_st_warning=True)
def init_connection():
    return pymongo.MongoClient(st.secrets['db_connection_url'])

def setup_library_header():
    if st.button('↺ Refresh'):
        st.experimental_rerun