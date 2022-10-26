from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4

#---------------------------------------------------------------------------------#
#client-info-get

def get():
    invalid = check_endpoint_info(request.args, ['client_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)


    results = dbhelper.run_statment('CALL get_client(?)',
    [request.args.get('client_id')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)


#---------------------------------------------------------------------------------#
#client-signup-post

def post():
    invalid = check_endpoint_info(request.json, ['email', 'first_name', 'last_name',
     'image_url', 'username', 'password'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

    token = uuid4().hex
    results = dbhelper.run_statment('CALL post_client(?,?,?,?,?,?,?)', [request.json.get('email'), request.json.get('first_name'), request.json.get('last_name'),
    request.json.get('image_url'), request.json.get('username'), request.json.get('password'), token])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)

#---------------------------------------------------------------------------------#

