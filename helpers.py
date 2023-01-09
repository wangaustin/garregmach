import streamlit as st
# """
# @param: all the fields in the add form
# @return: error message if applicable
# """
def check_material_pending_add_validity(
    school, department, professor, course_id,
    material_type, material_status, material_url,
    material_title, material_description, uploader_alias):

    is_valid = True
    ret_msg = '''
    ERROR! Material was not added due to the following reason(s): \n
    '''
    if school is None:
        is_valid = False
        ret_msg += '''\n- \"School\" is not selected'''
    if department is None:
        is_valid = False
        ret_msg += '''\n- \"Department\" is not selected'''
    if professor is None:
        is_valid = False
        ret_msg += '''\n- \"Professor\" is not selected'''
    if course_id is None:
        is_valid = False
        ret_msg += '''\n- \"Course ID\" is not selected'''
    if material_type is None:
        is_valid = False
        ret_msg += '''\n- \"Material Type\" is not selected'''
    if material_status is None:
        is_valid = False
        ret_msg += '''\n- \"Material Status\" is not selected'''
    if len(material_url) == 0:
        is_valid = False
        ret_msg += '''\n- \"Material URL\" is empty'''
    if not material_url.startswith("http"):
        is_valid = False
        ret_msg += '''\n- \"Material URL\" does not start with http'''
    if len(material_title) == 0:
        is_valid = False
        ret_msg += '''\n- \"Material Title\" is empty'''
    if len(material_description) == 0:
        is_valid = False
        ret_msg += '''\n- \"Material Description\" is empty'''
    # if uploader_alias is None:
        # ret_msg += '''\n- Uploader Alias has not been entered'''
    return [is_valid, ret_msg]

def check_department_pending_add_validity(
    school, name, website_url, abbreviation):
    is_valid = True

    ret_msg = '''
    ERROR! Department was not added due to the following reason(s): \n
    '''
    if school is None:
        is_valid = False
        ret_msg += '''\n- \"School\" is not selected'''
    if len(name) == 0:
        is_valid = False
        ret_msg += '''\n- \"Name\" is empty'''
    if len(website_url) == 0:
        is_valid = False
        ret_msg += '''\n- \"Website URL\" is empty'''
    if not website_url.startswith("http"):
        is_valid = False
        ret_msg += '''\n- \"Website URL\" does not start with http'''
    if len(abbreviation) == 0:
        is_valid = False
        ret_msg += '''\n- \"Abbreviation\" is empty'''

    return [is_valid, ret_msg]

def format_material_doc(
    doc,
    COLLECTION_COURSE,
    COLLECTION_DEPARTMENT,
    COLLECTION_SCHOOL,
    COLLECTION_PROFESSOR,
    key_extension
    ):
    course_doc = COLLECTION_COURSE.find_one({'_id': doc['course_id']})
    expander_name = doc['material_title'] + ' (' +doc['material_type'] + ')'

    with st.expander(expander_name):
        st.subheader(doc['material_title'])
        department_doc = COLLECTION_DEPARTMENT.find_one({
            '_id': course_doc['department']
        })
        school_doc = COLLECTION_SCHOOL.find_one({
            '_id': department_doc['school']
        })
        st.caption('School')
        st.write(school_doc['name'])
        st.caption('Department')
        st.write(department_doc['name'])
        course_name = department_doc['abbreviation'] + ' ' + course_doc['course_id'] + " (" + course_doc['name'] + ')'
        st.caption("Professor")
        professor_doc = COLLECTION_PROFESSOR.find_one({
            '_id': course_doc['professor']
        })
        st.write(professor_doc['first_name'], ' ', professor_doc['last_name'])
        st.caption('Course Name')
        st.write(course_name)
        st.caption('Material Status')
        st.write(doc['material_status'])
        st.caption('Uploader Alias')
        st.write(doc['uploader_alias'])
        st.caption('Datetime Added (UTC)')
        st.write(doc['datetime_added'])
        st.caption('Material URL')
        st.write(make_clickable_link(doc['material_url'], doc['material_type']))

        col_left, col_right = st.columns(2, gap="small")
        upvote_button_key_name = 'upvote-' + str(doc['_id']) + '-' + key_extension
        downvote_button_key_name = 'downvote-' + str(doc['_id']) + '-' + key_extension
        upvote_button_text = "👍 Upvote" + ' (' + str(doc['upvote']) + ')'
        downvote_button_text = "👎 Downvote" + ' (' + str(doc['downvote']) + ')'
        if col_left.button(
            upvote_button_text,
            help="Social feature is currently pending implementation!",
            key=upvote_button_key_name):
                st.write("Pending implementation...")
        if col_right.button(
            downvote_button_text,
            help="Social feature is currently pending implementation!",
            key=downvote_button_key_name):
                st.write('Social feature is currently pending implementation!')


# """
# @param: url - url link that opens when clicked
# @param: link_text - show link as this text
# @return: clickable text
# """
def make_clickable_link(url, link_text):
    text = "[" + link_text + "](" + url + ")"
    return text