from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4

def get():
    invalid = check_endpoint_info(request.args, ['restaurant_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

    results = dbhelper.run_statment('CALL get_restaurant(?)', [request.args.get('restaurant_id')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)


def post():
    invalid = check_endpoint_info(request.json, ['email','name','address','phone_number','bio','city','profile_url','banner_url','password'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)


    token = uuid4().hex
    results = dbhelper.run_statment('CALL post_restaurant(?,?,?,?,?,?,?,?,?,?)',
    [request.json.get('email'), request.json.get('name'), request.json.get('address'), request.json.get('phone_number'),
    request.json.get('bio'), request.json.get('city'), request.json.get('profile_url'), request.json.get('banner_url'), request.json.get('password'), token])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)