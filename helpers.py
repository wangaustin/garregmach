# returns a list with all school names
def find_all_schools():
    school_list = []
    for doc in COLLECTION_SCHOOL.find():
        school_list.append(doc['name'])
    return school_list