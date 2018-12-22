from flask import request

#####################################
# Before Requests
#####################################



#####################################
# After Requests
#####################################
def add_content_type_header(response):
    response.headers['Content-Type'] = "application/json"

    return response
