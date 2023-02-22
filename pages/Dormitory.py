import streamlit as st
from datetime import date, datetime
import pymongo
from pymongo import MongoClient
import configs

# import helper functions ../helpers.py
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers


# set configs
st.set_page_config(
    page_title = "Garreg Mach · Dormitory",
    page_icon = "🏠"
)

st.markdown(configs.hide_streamlit_style, unsafe_allow_html=True)

st.title("🏠 Dormitory")

client = configs.init_connection()