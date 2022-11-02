from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4

def get():
# checks the sent data request.args and the expected data restaurant_id and stores it as the variable invalid
    invalid = check_endpoint_info(request.args, ['restaurant_id'])
# if the variable invalid is not none it will send back 400 error and a message (client error)
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

# runs the statment CALL get_restaurant and sends the restaurant_id that's input as an arguement and stores it as the variable results
    results = dbhelper.run_statment('CALL get_restaurant(?)', [request.args.get('restaurant_id')])
# if results is equal to a list it will display a 200 message (success), and print the results of the procedure as json 
# if it isn't it will display a 500 message (server error)
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)


def post():
#checks the sent data request.json and the expected data
# 'email','name','address','phone_number','bio','city','profile_url','banner_url','password' and stores it as the variable invalid
    invalid = check_endpoint_info(request.json, ['email','name','address','phone_number','bio','city','profile_url','banner_url','password'])
# if the variable invalid is not none it will send back 400 error and a message (client error)
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

# generates a random unique id and sets it as the variable token and salt
    token = uuid4().hex
    salt = uuid4().hex
# runs the statment CALL post_restaurant and sends the
#  'description','image_url','name','price' that's input as an arguement as well as the token/salt and stores it as the variable results
    results = dbhelper.run_statment('CALL post_restaurant(?,?,?,?,?,?,?,?,?,?,?)',
    [request.json.get('email'), request.json.get('name'), request.json.get('address'), request.json.get('phone_number'),
    request.json.get('bio'), request.json.get('city'), request.json.get('profile_url'), request.json.get('banner_url'), request.json.get('password'), token, salt])
# if results is equal to a list it will display a 200 message (success), and print the results of the procedure as json
# if it isn't it will display a 500 message (server error)
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)