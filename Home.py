import streamlit as st

# todo: set configs
st.set_page_config(
    page_title="Garreg Mach"
    # initial_sidebar_state="collapsed" # TODO: change to collapsed for deployment
)

# hide "made with streamlit" and upper right hamburger
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.header("Welcome to Garreg Mach Project!")
user_logged_in = "You are logged in as " + str(st.experimental_user.email) + "."
st.caption(user_logged_in)

# st.info("[Quick Start](/Library)", icon="💡")
st.info("Click the upper left '>' to visit your desired pages!", icon="🤩")