from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4




# POTENTIAL ERROR?

def post():
    invalid = check_endpoint_info(request.json, ['email','password'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)    

    token = uuid4().hex
    results = dbhelper.run_statment('CALL client_login(?,?,?)',
    [request.json.get('email'), request.json.get('password'), token])
    
    if(type(results) == list and results[0][0] == 1):
        return make_response(json.dumps(results, default=str), 200)
    elif(type(results) == list and results[0][0] == 0):
        return make_response(json.dumps("Bad login attempt"), 400)
    else:
        return make_response(json.dumps("Sorry there has been an error"), 500) 