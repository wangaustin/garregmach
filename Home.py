import streamlit as st
import configs

# todo: set configs
st.set_page_config(
    page_title="Garreg Mach · Home"
)

st.markdown(configs.hide_streamlit_style, unsafe_allow_html=True)

st.header("Welcome to Garreg Mach Project!")
st.caption(configs._MAIN_GMP_PROJECT_INTRO)

st.subheader("Current Platforms")

with st.expander("📚 Library", expanded=True):
    st.write(configs._MAIN_LIBRARY_INTRO)

st.subheader("🛣 Future Roadmap")
with st.expander("Coming Soon!"):
    st.write("Thanks for checking out GMP, please check back later for the project's roadmap!")

st.subheader("💬 Have a Suggestion?")
st.write("Create an issue at [GMP's Github repo](https://github.com/wangaustin/garregmach)!")
st.write("Alternatively, email your suggestion to [garregmachproject@gmail.com](mailto:garregmachproject@gmail.com).")