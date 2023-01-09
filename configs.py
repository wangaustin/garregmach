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
- Email Handle (e.g. for austin.w.wang@vanderbilt.edu, the email handle would be "vanderbilt.edu")
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
    course and find materials already shared by others.
    \nThe goal of the GMP Library is for students who are good at finding the locations 
    of digital resources to help those who are not. This way, students will hopefully 
    reduce the amount of money needed to spend on physical copies of the academic resources 
    simply because they could not find them online.
    \n#### Example
    \nSuppose Tintin knows URL link of where to find the PDF for *Critique of Pure Reason*, 
    which is a book requested by a Philosophy course. 
    \nTintin can upload the link as follows for everyone else to see: 
    \n> **Library ➡️ Add to Database ➡️ Add Material**
    \nTintin is now a hero for sharing!
    \n#### Isn't This LibGen? What's So Different about GMP Library?
    \nLibGen is absolutely awesome! However, it can get a bit difficult to find what you 
    need there for a particular course.
    \nThe GMP Library asks people to add links to academic resources in association with a 
    particular course. This mandatory association is what sets it apart from other resource 
    sharing websites such as libgen, as it allows the system to easily filter queries.
    \nSo, if I only want to see the resources for the Modern Philosophy course at
    Vanderbilt University taught my Dr. Wuerth, for instance, the system can efficiently 
    query that. The association also adds another layer of filter as it has presumably been 
    deemed related to this course by the original uploader. 
    \n#### Ready to Search or Contribute?
    \nHead to 📚 [Library](/Library) now!
    """