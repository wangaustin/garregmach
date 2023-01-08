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
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# construct sidebar
with st.sidebar:
    st.header("Garreg Mach")
    # doesn't seem like we can use a container here
    st.subheader("ℹ️ About")
    st.write("The Garreg Mach Project is being actively developed by Austin Wang")


st.header("Welcome to Garreg Mach Project!")

# st.info("[Quick Start](/Library)", icon="💡")
st.info("Click the upper left '>' to visit your desired pages!", icon="🤩")