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
    page_title = "Garreg Mach · Library",
    page_icon = "📚"
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
        helpers.format_material_doc(
            doc,
            COLLECTION_COURSE,
            COLLECTION_DEPARTMENT,
            COLLECTION_SCHOOL,
            COLLECTION_PROFESSOR,
            "add"
        )



with tab3:
    st.header("Add to Database")

    add_subtab1, add_subtab2, add_subtab3, add_subtab4 = st.tabs([
        "Add Material", "Add Department", "Add Course", "Add Professor"
    ])

    with add_subtab1:
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

        # ------ MATERIAL TYPE
        # -----------------------------
        material_type = st.selectbox(
            "Material Type",
            configs._LIBRARY_MATERIAL_TYPE_LIST
        )

        # ------ MATERIAL STATUS
        # -----------------------------
        material_status = st.selectbox(
            "Material Status",
            configs._LIBRARY_MATERIAL_STATUS
        )

        # ------ MATERIAL URL
        # -----------------------------
        material_url = st.text_input(
            "Material URL",
            placeholder="https://www.austinwang.co"
        )

        # ------ MATERIAL DESCRIPTION
        # -----------------------------
        material_title = st.text_input(
            "Material Title",
            placeholder="To Save a Mockingbird"
        )

        # ------ MATERIAL DESCRIPTION
        # -----------------------------
        material_description = st.text_input(
            "Material Description",
            placeholder="This is the PDF of the requested textbook."
        )

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
                st.success("Successfully added to database. Refresh to see it!", icon='✅')
            else:
                st.error(ret_message[1], icon='🚨')
    
    with add_subtab2:
        # ----- SCHOOL -----
        school = st.selectbox(
            "School",
            range(len(school_list_for_display)),
            format_func=lambda x: school_list_for_display[x],
            key="school_selectbox_add_department"
        )
        name = st.text_input(
            "Department Name",
            key="name_text_input_add_department"
        )
        website_url = st.text_input(
            "Department Website URL",
            key="website_url_text_input_add_department"
        )
        abbreviation = st.text_input(
            "Department Abbreviation",
            placeholder="PHIL",
            key="abbreviation_text_input_add_deparment"
        )
        abbreviation = abbreviation.upper()

        school_obj_id = ret_school_list[school][0]

        if st.button("Add Department", key="submit_button_add_department"):
            existing_department = COLLECTION_DEPARTMENT.find_one({
                'school': school_obj_id,
                'name': { "$regex" : name , "$options" : "i"},
                'abbreviation': abbreviation
            })
            # department pending add already exists
            if existing_department is not None:
                st.error("This department already exists for this school. Please refresh page and try again.", icon="🚨")
                st.stop()
            else:
                # TODO: add helper function to build error message
                COLLECTION_DEPARTMENT.insert_one({
                    'name': name.title(),
                    'school': school_obj_id,
                    'website_url': website_url,
                    'abbreviation': abbreviation
                })
                st.success("Successfully added department. Refresh to see it!", icon="✅")
    
    with add_subtab4:
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
            format_func=lambda x: school_list_for_display[x],
            key="school_selectbox_add_professor"
        )

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
            format_func=lambda x: department_list_for_display[x],
            key="department_selectbox_add_professor"
        )

        first_name = st.text_input(
            "First Name",
            key="first_name_text_input_add_professor"
        )
        last_name = st.text_input(
            "Last Name",
            key="last_name_text_input_add_professor"
        )

        department_obj_id = ret_department_list[department][0]

        # TODO: add helper function for validation and error messaging
        if st.button("Add Professor", key="submit_button_add_professor"):
            existing_professor = COLLECTION_PROFESSOR.find_one({
                'department': department_obj_id,
                'first_name': first_name.title(),
                'last_name': last_name.title()
            })

            if existing_professor is not None:
                st.error(
                    "This professor already exists in this department. Please refresh and try again.",
                    icon='🚨')
                st.stop()
            else:
                COLLECTION_PROFESSOR.insert_one({
                    'first_name': first_name.title(),
                    'last_name': last_name.title(),
                    'department': department_obj_id,
                    'courses': []
                })
                st.success("Successfully added professor to database. Refresh to see it!", icon='✅')


with tab1:
    st.header("Search")

    subtab1, subtab2 = st.tabs(['By Course', 'By Uploader Alias'])

    with subtab1:
        # ----- SCHOOL -----
        school = st.selectbox(
            "School",
            range(len(school_list_for_display)),
            format_func=lambda x: school_list_for_display[x],
            key="school_selectbox_search"
        )
        # ----- DEPARTMENT -----
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
            format_func=lambda x: department_list_for_display[x],
            key="department_selectbox_search"
        )
        # ----- PROFESSOR -----
        department_obj_id = ret_department_list[department][0]
        ret_professor_list = find_all_professors_for_department(department_obj_id)
        if len(ret_professor_list) == 0:
            st.error("No professor has been added for this department! Please refresh page and add at least one professor first.", icon="🚨")
            st.stop()
        # compile professor list for display
        professor_list_for_display = []
        for professor in ret_professor_list:
            professor_full_name = professor[1] + ' ' + professor[2]
            professor_list_for_display.append(professor_full_name)
        # build dropdown list
        professor = st.selectbox(
            "Professor",
            range(len(professor_list_for_display)),
            format_func=lambda x: professor_list_for_display[x],
            key="professor_selectbox_search"
        )
        # ----- COURSE -----
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
            format_func=lambda x: course_list_for_display[x],
            key="course_selectbox_search"
        )

        material_type_list = st.multiselect(
            "Material Type",
            configs._LIBRARY_MATERIAL_TYPE_LIST
        )

        material_status_list = st.multiselect(
            "Material Status",
            configs._LIBRARY_MATERIAL_STATUS
        )

        material_title = st.text_input(
            "Material Title",
            placeholder="To Save a Mockingbird",
            key="material_title_text_input_search"
        )

        if st.button("Find Materials"):
            if course_id is None:
                st.error("Must select a course!", icon="🚨")
                st.stop()
            st.subheader("Search Results")
            course_obj_id = ret_course_list[course_id][0]

            # build AND query logic
            and_query_logic = []

            # material status not selected
            if len(material_type_list) > 0:
                and_query_logic.append(
                    {'material_type':{
                        "$in": material_type_list
                    }}     
                )

            if len(material_status_list) > 0:
                and_query_logic.append(
                    {'material_status':{
                        "$in": material_status_list
                    }}
                )
            if len(material_title) > 0:
                and_query_logic.append(
                    {'material_title':{
                        "$regex": material_title,
                        "$options": "$i"
                    }}
                )

            and_query_logic.append({'course_id': course_obj_id})
            ret_materials_cursor = COLLECTION_MATERIAL.find(
                    {"$and":
                        and_query_logic
                    }
                )
            cursor_length = len(list(ret_materials_cursor.clone()))

            if cursor_length > 0:
                info_msg = "Found " + str(cursor_length) + " result(s)!"
                st.info(info_msg, icon="📬")
                for doc in ret_materials_cursor:
                    new_doc = COLLECTION_MATERIAL.find_one({'_id': doc['_id']})
                    helpers.format_material_doc(
                        new_doc,
                        COLLECTION_COURSE,
                        COLLECTION_DEPARTMENT,
                        COLLECTION_SCHOOL,
                        COLLECTION_PROFESSOR,
                        "search"
                    )
            else:
                st.error("No materials found.", icon="📭")

    with subtab2:
        uploader_alias = st.text_input(
            "Uploader Alias",
            placeholder="tintinisagoodboi",
            key="uploader_alias_text_input_search"
        )
        if st.button("Find Materials", key="search_by_uploader_alias_button"):
            st.subheader("Search Results")
            ret_materials_cursor = COLLECTION_MATERIAL.find({'uploader_alias': uploader_alias})
            for doc in ret_materials_cursor:
                helpers.format_material_doc(
                    doc,
                    COLLECTION_COURSE,
                    COLLECTION_DEPARTMENT,
                    COLLECTION_SCHOOL,
                    COLLECTION_PROFESSOR,
                    "search"
                )

            



with tab4:
    st.header("More")

