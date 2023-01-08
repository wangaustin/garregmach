import streamlit as st
import pandas as pd
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
    page_title="Library"
    # initial_sidebar_state="collapsed" # TODO: change to collapsed for deployment
)

st.markdown(configs.hide_streamlit_style, unsafe_allow_html=True)

configs.setup_library_header()

st.title("📚 Library")

client = configs.init_connection()

DATABASE = client.LibraryDB
COLLECTION_COURSE = DATABASE.Course
COLLECTION_DEPARTMENT = DATABASE.Department
COLLECTION_SCHOOL = DATABASE.School
COLLECTION_PROFESSOR = DATABASE.Professor
COLLECTION_MATERIAL = DATABASE.Material

# @st.cache(ttl=10)
def find_school_of_deparment():
    obj_id_school = COLLECTION_DEPARTMENT.find_one()['school']
    school_of_department = COLLECTION_SCHOOL.find_one({'_id' : obj_id_school})['name']
    return school_of_department

# """
# @param: None
# @return: a list of all school names
# """
# @st.cache(ttl=10)
def find_all_schools():
    school_list = []
    for doc in COLLECTION_SCHOOL.find():
        school_list.append([doc['_id'], doc['name']])
    return school_list

# """
# @param: ObjectId of the school in question
# @return: a list of all departments for this school
# """
# @st.cache(ttl=10)
def find_all_departments_for_school(school):
    department_list = []
    for doc in COLLECTION_DEPARTMENT.find({'school' : school}):
        department_list.append([doc['_id'], doc['name'], doc['abbreviation']])

    return department_list

# """
# @param: ObjectId of the department in question
# @return: a list of all professors for this department (related to a school)
# """
# @st.cache(ttl=10)
def find_all_professors_for_department(department):
    professor_list = []
    for doc in COLLECTION_PROFESSOR.find({'department' : department}):
        professor_info = [doc['_id'], doc['first_name'], doc['last_name']]
        professor_list.append(professor_info)

    return professor_list

# """
# @param: department - ObjecId of department in question
# @param: professor - ObjectId of professor in question
# @return: list of courses taught my this professor at this department
# """
# @st.cache(ttl=60)
def find_all_courses(department, professor):
    course_list = []
    for doc in COLLECTION_COURSE.find({'department': department, 'professor': professor}):
        course_info = [doc['_id'], doc['course_id'], doc['name']]
        course_list.append(course_info)
    
    return course_list


# UI layout
tab1, tab2, tab3, tab4 = st.tabs(configs._LIBRARY_TAB_NAMES)

# TODO: switch order of 'recently added' and 'add to database'
with tab2:
    st.header("Recently Added")
    # for doc in COLLECTION_MATERIAL.find().limit(10):
    #     st.write(doc)

    for doc in COLLECTION_MATERIAL.find().limit(10):
    # build exapnder name from course id
        helpers.format_material_doc(
            doc,
            COLLECTION_COURSE,
            COLLECTION_DEPARTMENT,
            COLLECTION_SCHOOL,
            COLLECTION_PROFESSOR
        )



with tab3:
    st.header("Add")

    # -----------------------------
    # ------ SCHOOL
    # -----------------------------
    ret_school_list = find_all_schools()
    if len(ret_school_list) == 0:
        st.error(
            "No school has been added to this database! Please contact support.",
            icon="🚨"
        )
        st.stop()
    # compile school list for display
    school_list_for_display = []
    for school in ret_school_list:
        school_list_for_display.append(school[1])
    # build dropdown list
    school = st.selectbox(
        "School",
        range(len(school_list_for_display)),
        format_func=lambda x: school_list_for_display[x]
    )

    # -----------------------------
    # ------ DEPARTMENT
    # -----------------------------
    school_obj_id = ret_school_list[school][0]
    ret_department_list = find_all_departments_for_school(school_obj_id)
    if len(ret_department_list) == 0:
        st.error("No deparment has been added for this school! Please contact support.", icon="🚨")
        st.stop()
    # compile department list for siplay
    department_list_for_display = []
    for department in ret_department_list:
        department_list_for_display.append(department[1])
    
    # build dropdown list
    department = st.selectbox(
        "Department",
        range(len(department_list_for_display)),
        format_func=lambda x: department_list_for_display[x]
    )

    # -----------------------------
    # ------ PROFESSOR
    # -----------------------------
    department_obj_id = ret_department_list[department][0]
    ret_professor_list = find_all_professors_for_department(department_obj_id)
    # compile professor list for display
    professor_list_for_display = []
    for professor in ret_professor_list:
        professor_full_name = professor[1] + ' ' + professor[2]
        professor_list_for_display.append(professor_full_name)
    # build dropdown list
    professor = st.selectbox(
        "Professor",
        range(len(professor_list_for_display)),
        format_func=lambda x: professor_list_for_display[x]
    )

    # -----------------------------
    # ------ COURSE
    # -----------------------------
    professor_obj_id = ret_professor_list[professor][0]
    ret_course_list = find_all_courses(department_obj_id, professor_obj_id)
    department_abbreviation = ret_department_list[department][2]
    course_list_for_display = []
    for course in ret_course_list:
        course_full_name = department_abbreviation + ' ' + course[1]
        course_full_name += ' (' + course[2] + ')'
        course_list_for_display.append(course_full_name)

    course_id = st.selectbox(
        "Course ID",
        range(len(course_list_for_display)),
        format_func=lambda x: course_list_for_display[x]
    )

    material_type = st.selectbox(
        "Material Type",
        configs._LIBRARY_MATERIAL_TYPE_LIST
    )

    # -----------------------------
    # ------ MATERIAL STATUS
    # -----------------------------
    material_status = st.selectbox(
        "Material Status",
        configs._LIBRARY_MATERIAL_STATUS
    )

    # -----------------------------
    # ------ MATERIAL URL
    # -----------------------------
    material_url = st.text_input(
        "Material URL",
        placeholder="https://www.austinwang.co"
    )

    # -----------------------------
    # ------ MATERIAL DESCRIPTION
    # -----------------------------
    material_title = st.text_input(
        "Material Title",
        placeholder="To Save a Mockingbird"
    )

    # -----------------------------
    # ------ MATERIAL DESCRIPTION
    # -----------------------------
    material_description = st.text_input(
        "Material Description",
        placeholder="This is the PDF of the requested textbook."
    )

    # -----------------------------
    # ------ UPLOADER ALIAS
    # -----------------------------
    uploader_alias = st.text_input(
        "Uploader Alias (Optional)",
        placeholder="anonymous"
    )



    if st.button("Submit"):
        def check_data_validity():
            # TODO: add validity logic, currently it's just dummy
            return False

        ret_message = helpers.check_pending_add_validity(
            school, department, professor, course_id,
            material_type, material_status, material_url,
            material_title, material_description, uploader_alias)
        
        # use ObjectIds
        def add_material(
            course_id, material_type, material_status,
            material_url, material_title, material_description, uploader_alias):
            COLLECTION_MATERIAL.insert_one({
                'course_id': course_id,
                'material_type': material_type,
                'material_status': material_status,
                'material_url': material_url,
                'material_title': material_title,
                'material_description': material_description,
                'uploader_alias': uploader_alias,
                'upvote': int(0),
                'downvote': int(0),
                'datetime_added': datetime.utcnow()
            })


        if ret_message[0]:
            course_id_to_add = ret_course_list[course_id][0]
            add_material(
                course_id_to_add, material_type, material_status, material_url,
                material_title, material_description, uploader_alias)
            st.success("Submitted!", icon='✅')
        else:
            st.error(ret_message[1], icon='🚨')

with tab1:
    st.header("Search")

    subtab1, subtab2 = st.tabs(['Precise Search', 'By Professor'])

    with subtab2:
        st.write("What should this structure be?")
            



with tab4:
    st.header("More")

