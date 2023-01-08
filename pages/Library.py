import streamlit as st
import pandas as pd
from datetime import date, datetime
import pymongo
from pymongo import MongoClient
import configs

# set configs
st.set_page_config(
    page_title="Library"
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

st.title("📚 Library")

# get mongodb connection
@st.experimental_singleton(suppress_st_warning=True)
def init_connection():
    return pymongo.MongoClient(st.secrets['db_connection_url'])
client = init_connection()

DATABASE = client.LibraryDB
COLLECTION_COURSE = DATABASE.Course

st.write(COLLECTION_COURSE.find_one())


# define initial schema for everything as dummies
dummy_course = {
    "course_id": 1, # obj_id
    "department": 88, # obj_id, not number
    "professor": 9, # obj_id
    "level": "Undergraduate"
}

dummy_department = {
    "name": "Philosophy",
    "department_head": 9,
    "url": "https://www.google.com"
}

dummy_professor = {
    "first_name": "John",
    "last_name": "Doe",
    "department": 88, # obj_id
    "courses": ["course 1", "course 2", "course 3"]
}

dummy_school = {
    "name" : "Vanderbilt",
    "email_handle": "vanderbilt.edu", # what comes after @
    "url": "https://www.google.com"
}

# is this necessary?
dummy_material_type = {
    "format": "PDF",
    "priority": 0
}

# is this necessary?
dummy_material_status = {
    "status": "Professor Requested/Approved" # or sth. like supplementary
}


# UI layout
tab1, tab2, tab3, tab4 = st.tabs(configs._LIBRARY_TAB_NAMES)

# TODO: switch order of 'recently added' and 'add to database'
with tab2:
    st.header("Recently Added")
    # TODO: show 10

with tab1:
    st.header("Add to Database")

    # not using a form here because that would not allow for dynamic
    # conditional field update

    # TODO: change to actual db data for all
    dummy_school_list = ["Vanderbilt", "TSU", "Belmont"]
    school = st.selectbox(
        "School",
        dummy_school_list
    )

    dummy_department_list = ["Philosophy", "Computer Science", "Physics"]
    department = st.selectbox(
        "Department",
        dummy_department_list
    )

    dummy_professor_list = ["John Doe", "Jane Doe", "Santa Claus"]
    professor = st.selectbox(
        "Professor",
        dummy_professor_list
    )

    dummy_course_list = ["4201", "1002", "3008"]
    course_id = st.selectbox(
        "Course ID",
        dummy_course_list
    )

    material_type = st.selectbox(
        "Material Type",
        configs._MATERIAL_TYPE_LIST
    )

    material_url = st.text_input(
        "Material URL",
        placeholder="https://www.austinwang.co"
    )

    material_description = st.text_input(
        "Material Description",
        placeholder="This is the PDF of the requested textbook."
    )

    uploader_alias = st.text_input(
        "Uploader Alias (Optional)",
        placeholder="anonymous"
    )

    # def pretty_get_pending_add():
    #     text = "School: " + school
    #     text += "\nDepartment: " + department
    #     text += "\nProfessor: " + professor
    #     text += "\nCourse ID: " + course_id
    #     text += "\nMaterial Type: " + material_type
    #     text += "\tMaterial URL: " + str(material_url)
    #     text += "\nMaterial Description: " + material_description
    #     text += "\nUploader Alias: " + uploader_alias
    #     return text

    if st.button("Check Inputted Data"):
        st.write("Checking validity...")
        # st.write(pretty_get_pending_add())


    if st.button("Submit"):
        def check_data_validity():
            # TODO: add validity logic, currently it's just dummy
            return True

        if check_data_validity():
            st.success("Submitted!", icon="✅")
        else:
            st.error("ERROR! Please check data first.")

with tab3:
    st.header("Search")

with tab4:
    st.header("More")

