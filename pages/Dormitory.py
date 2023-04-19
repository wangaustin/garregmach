import streamlit as st
from datetime import date, datetime
import pymongo
from pymongo import MongoClient
import configs
import pandas as pd

# import helper functions ../helpers.py
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers


st.markdown(configs.hide_streamlit_style, unsafe_allow_html=True)

st.title("🏠 Dormitory")

client = configs.init_connection()

DATABASE = client.GarregMachDB
COLLECTION_COURSE = DATABASE.Course
COLLECTION_DEPARTMENT = DATABASE.Department
COLLECTION_SCHOOL = DATABASE.School
COLLECTION_PROFESSOR = DATABASE.Professor
COLLECTION_MATERIAL = DATABASE.Material
COLLECTION_DORMITORY = DATABASE.Dormitory
COLLECTION_DORMITORY_REVIEWS = DATABASE.DormitoryReviews

# UI layout
tab1, tab2, tab3 = st.tabs(configs._DORMITORY_TAB_NAMES)

with tab1:
    st.header("Search Reviews")

    subtab1, subtab2 = st.tabs(['Search by School', 'Search by Dorm'])

    ####################
    # SEARCH BY SCHOOL #
    ####################
    with subtab1:
        # ------ SCHOOL
        # -----------------------------
        ret_school_list = helpers.find_all_schools()
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
            key='search_dorm_reviews_by_school'
        )
        school_obj_id = ret_school_list[school][0]

        if st.button('Search by School', key='search_dorm_reviews_by_school_button'):
            pipeline = [
                {"$match": {"school": school_obj_id}},
                {"$group": {"_id": None, "avg_star": {"$avg": "$review_star"}}},
            ]
            dorm_review_search_cursor = COLLECTION_DORMITORY_REVIEWS.aggregate(pipeline)
            avg_star = next(dorm_review_search_cursor, {}).get("avg_star")

            

            st.subheader('Result(s)')
            st.caption('School Average Star')
            st.write(avg_star)
            st.caption('School Dorms Ratings')
            helpers.show_dorms_ratings_for_school(school_obj_id)
            st.caption('Review Details')
            for doc in COLLECTION_DORMITORY_REVIEWS.find({'school':school_obj_id}):
                helpers.format_review_doc(doc)

    with subtab2:
        # ------ SCHOOL
        # -----------------------------
        ret_school_list = helpers.find_all_schools()
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

        # ------ DORM
        # -----------------------------
        school_obj_id = ret_school_list[school][0]
        ret_dorm_list = helpers.find_all_dorms_for_school(school_obj_id)
        if len(ret_dorm_list) == 0:
            st.error("No dorm has been added for this school! Please contact support.", icon="🚨")
            st.stop()
        # compile department list for display
        dorm_list_for_display = []
        for dorm in ret_dorm_list:
            dorm_list_for_display.append(dorm[1])
        
        # build dropdown list
        dorm = st.selectbox(
            "Dorm",
            range(len(dorm_list_for_display)),
            format_func=lambda x: dorm_list_for_display[x],
            key='search_dorm_reviews_by_dorm'
        )

        dorm_obj_id = ret_dorm_list[dorm][0]

        if st.button('Search Dorm', key='search_dorm_reviews_by_dorm_button'):
            st.subheader('Result(s)')

            pipeline = [
                {"$match": {"school": school_obj_id, "dorm": dorm_obj_id}},
                {"$group": {"_id": None, "avg_star": {"$avg": "$review_star"}}},
            ]
            dorm_review_search_cursor = COLLECTION_DORMITORY_REVIEWS.aggregate(pipeline)

            avg_star = next(dorm_review_search_cursor, {}).get("avg_star")

            st.caption('Average Star')
            st.write(avg_star)

            for doc in COLLECTION_DORMITORY_REVIEWS.find({'school': school_obj_id, 'dorm': dorm_obj_id}):
                helpers.format_review_doc(doc)



    

with tab2:
    st.header("Add to Database")
    with st.form('new_dorm_review'):
        
        ret_school_list = helpers.find_all_schools()

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

        # ------ DORM
        # -----------------------------
        school_obj_id = ret_school_list[school][0]
        ret_dorm_list = helpers.find_all_dorms_for_school(school_obj_id)
        if len(ret_dorm_list) == 0:
            st.error("No dorm has been added for this school! Please contact support.", icon="🚨")
            st.stop()
        # compile department list for display
        dorm_list_for_display = []
        for dorm in ret_dorm_list:
            dorm_list_for_display.append(dorm[1])
        
        # build dropdown list
        dorm = st.selectbox(
            "Dorm",
            range(len(dorm_list_for_display)),
            format_func=lambda x: dorm_list_for_display[x]
        )
        dorm_obj_id = ret_dorm_list[dorm][0]

        review_star = st.slider("Review (1-5)", min_value=1, max_value=5, value=3)
        review_comment = st.text_area("Review Comment")
        uploader_alias = st.text_input(
            "Uploader Alias (Optional)",
            placeholder=configs._PLACEHOLDER_UPLOADER_ALIAS
        )

        #TODO: data validation before insertion

        submitted = st.form_submit_button("Submit")
        if submitted:
            school_id_to_add = ret_school_list[school][0]
            utc_now = datetime.utcnow().isoformat()
            COLLECTION_DORMITORY_REVIEWS.insert_one(
                {
                    'school': school_id_to_add,
                    #TODO: use data from DB instead of hard-coded list
                    'dorm': dorm_obj_id,
                    'review_star': review_star,
                    'review_comment': review_comment,
                    'uploader_alias': uploader_alias,
                    'submitted_time': utc_now
                }
            )
            st.success("Successfully added a new review!", icon='✅')

with tab3:
    st.header("Recently Added")

    # get dataframe
    dorm_review_cursor = COLLECTION_DORMITORY_REVIEWS.find().sort("submitted_time", 1)

    for doc in dorm_review_cursor:
        helpers.format_review_doc(doc)