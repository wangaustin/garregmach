# """
# @param: all the fields in the add form
# @return: error message if applicable
# """
def check_pending_add_validity(
    school, department, professor, course_id,
    material_type, material_status, material_url,
    material_title, material_description, uploader_alias):

    is_valid = True
    ret_msg = '''
    ERROR! Not submitted due to the following reason(s): \n
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
    if len(material_title) == 0:
        is_valid = False
        ret_msg += '''\n- \"Material Title\" is empty'''
    if len(material_description) == 0:
        is_valid = False
        ret_msg += '''\n- \"Material Description\" is empty'''
    # if uploader_alias is None:
        # ret_msg += '''\n- Uploader Alias has not been entered'''
    return [is_valid, ret_msg]


# """
# @param: url - url link that opens when clicked
# @param: link_text - show link as this text
# @return: clickable text
# """
def make_clickable_link(url, link_text):
    text = "[" + link_text + "](" + url + ")"
    return text