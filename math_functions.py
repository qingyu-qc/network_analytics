def compare(query, subject):
    if query < subject:
       return query, subject
    return subject, query
 
def jaccard(query_set, subject_set):
    intersection = 0.0
    q_len, s_len = len(query_set), len(subject_set)
    assert(type(query_set) == set)
    assert(type(subject_set) == set)
    for ele in query_set:
        if ele in subject_set:
           intersection += 1
    jaccard_sim = intersection / (q_len+s_len-intersection)
    return jaccard_sim