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
tab1, tab2 = st.tabs(configs._DORMITORY_TAB_NAMES)

st.subheader("This is a test for Nikhil's branch.")

with tab1:
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

        # TODO: use data from DB
        # compile dorm list for this school

        dorm = st.selectbox(
            "Dorm",
            configs._DORMITORY_VANDERBILT_DORMS
        )

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
                    'dorm': dorm,
                    'review_star': review_star,
                    'review_comment': review_comment,
                    'uploader_alias': uploader_alias,
                    'submitted_time': utc_now
                }
            )

with tab2:
    st.header("Recently Added")

    # get dataframe
    dorm_review_cursor = COLLECTION_DORMITORY_REVIEWS.find().sort("submitted_time", 1)
    dorm_review_df = pd.DataFrame(list(dorm_review_cursor.clone()))

    cols = dorm_review_df.columns.tolist()

    dorm_review_df = dorm_review_df.drop('_id',axis=1)
    
    # # move 'codename' to the front of the df
    # cols = cols[-2:] + cols[:-2]
    # dorm_review_df = dorm_review_df[cols]

    i = 0
    for doc in dorm_review_cursor:
        # dorm_review_df.at[i, '_id'] = str(dorm_review_df.at[i, '_id'])
        dorm_review_df.at[i, 'school'] = COLLECTION_SCHOOL.find_one({'_id': dorm_review_df.at[i, 'school']})['name']
        i += 1

    st.dataframe(dorm_review_df, use_container_width=True)