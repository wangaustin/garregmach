import streamlit as st
import configs

# todo: set configs
st.set_page_config(
    page_title="Garreg Mach ยท Home"
)

st.markdown(configs.hide_streamlit_style, unsafe_allow_html=True)

st.header("Welcome to Garreg Mach Project!")
st.caption(configs._MAIN_GMP_PROJECT_INTRO)

st.subheader("๐คฉ Current Platforms")

with st.expander("๐ Library", expanded=True):
    st.write(configs._MAIN_LIBRARY_INTRO)

st.subheader("๐ฃ Future Roadmap")
with st.expander("๐  Dormitory", expanded=False):
    st.write(configs._MAIN_DORMITORY_INTRO)
with st.expander("๐ Dining Hall", expanded=False):
    st.write(configs._MAIN_DINING_HALL_INTRO)



st.subheader("๐ฌ Have a Suggestion?")
st.write("Create an issue at [GMP's Github repo](https://github.com/wangaustin/garregmach)!")
st.write("Alternatively, email your suggestion to [garregmachproject@gmail.com](mailto:garregmachproject@gmail.com).")