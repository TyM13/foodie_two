from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4



def get():
# runs the statment CALL get_restaurant,
    results = dbhelper.run_statment('CALL get_restaurants()')
# if results is equal to a list it will display a 200 message (success), and print the results of the procedure as json
#  and if it isn't it will display a 500 message (server error)
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)