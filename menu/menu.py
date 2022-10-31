from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json


def get():
# checks the sent data request.args and the expected data restaurant_id and stores it as the variable invalid
    invalid = check_endpoint_info(request.args, ['restaurant_id'])
# if the variable invalid is not none it will send back 400 error and a message (client error)
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

# runs the statment CALL get_menu and sends the restaurant_id that's input as an arguement and stores it as the variable results
    results = dbhelper.run_statment('CALL get_menu(?)', [request.args.get('restaurant_id')])
# if results is equal to a list it will display a 200 message (success), and print the results of the procedure as json
# if it isn't it will display a 500 message (server error)
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)




def post():
# checks the sent data request.headers and the expected data token and stores it as the variable invalid
    invalid = check_endpoint_info(request.headers, ['token'])
# checks the sent data request.json and the expected data description, image_url, name, price and stores it as the variable invalid
    invalid_info = check_endpoint_info(request.json, ['description','image_url','name','price'])
# if the variable invalid is not none it will send back 400 error and a message (client error)
    if(invalid != None or invalid_info != None):
        return make_response(json.dumps(invalid, invalid_info, default=str), 400)

# runs the statment CALL post_menu and sends the
#  'description','image_url','name','price' and the tokens input for the header that's input as an arguement and stores it as the variable results
    results = dbhelper.run_statment('CALL post_menu(?,?,?,?,?)',
    [request.json['description'], request.json['image_url'], request.json['name'], request.json['price'], request.headers['token']])
# if results is equal to a list it will display a 200 message (success),  and print the results of the procedure as json
#  if it isn't it will display a 500 message (server error)
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)