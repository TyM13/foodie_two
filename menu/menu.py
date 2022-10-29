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

    results = dbhelper.run_statment('CALL get_menu(?)', [request.args.get('restaurant_id')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)




def post():
    invalid = check_endpoint_info(request.headers, ['token'])
    invalid_info = check_endpoint_info(request.json, ['description','image_url','name','price'])
    if(invalid != None or invalid_info != None):
        return make_response(json.dumps(invalid, invalid_info, default=str), 400)

    results = dbhelper.run_statment('CALL post_menu(?,?,?,?,?)',
    [request.json['description'], request.json['image_url'], request.json['name'], request.json['price'], request.headers['token']])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)