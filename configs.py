import streamlit as st
import pymongo
from pymongo import MongoClient

_LIBRARY_TAB_NAMES = [
    "🔍 Search",
    "🆕 Recently Added",
    "➕ Add to Database",
    "🧸 More"
]

_LIBRARY_COURSE_LEVEL = {
    "Undergraduate",
    "Masters",
    "PhD"
}

_LIBRARY_MATERIAL_TYPE_LIST = ["PDF", "Website", "Slides", "Other"]

_LIBRARY_MATERIAL_STATUS = [
    "Professor Requested / Approved",
    "Supplementary"
]

_LIBRARY_ADD_SCHOOL_INFO = """
Adding a school requires a moderator!  
  
Please email garregmachproject@gmail.com with the following information:  
- School Name
- Email Handle (e.g. vanderbilt.edu, which comes from austin.w.wang@vanderbilt.edu)
- Logo URL (or a link to where to find the logo)
- Website URL (e.g. www.vanderbilt.edu)
"""


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

_MAIN_GMP_PROJECT_INTRO = """
An open-source project with the goal of reducing costs associated with higher education, 
one step at a time.
"""


_MAIN_LIBRARY_INTRO = """
    #### Intro
    \nThe GMP Library is a platform to share where you can find materials for a specific 
    course and find materials already shared by your others.  
    \nThe purpose of this platform is to allow those of us who are good at finding
    where digital resources are located at to help others who are not.\
    \n#### Example
    \nSuppose Tintin knows URL link of where to find the PDF for *Critique of Pure Reason*, 
    which is a book requested by a Philosophy course. 
    \nTintin can upload the link as follows for everyone else to see: 
    \n> **Library ➡️ Add to Database ➡️ Add Material**
    \nTintin is now a hero for sharing!
    \n#### Ready to Search or Contribute?
    \nHead to 📚 [Library](/Library) now!
    """