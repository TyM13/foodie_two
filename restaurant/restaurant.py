from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4
from apihelper import fill_optional_data

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





def patch():
# checks the sent data request.headers and the expected data token, sets as variable invalid
    invalid = check_endpoint_info(request.headers, ['token']) 
# if the variable invalid is not none it will send back 400 error and a message (client error)
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)
        
# requests the token as a header and gets the client info for later use
    results = dbhelper.run_statment('CALL get_restaurant_token(?)', [request.headers.get('token')])
# if the results type is not equal to a list it will send back 400 error and a message (client error)
    if(type(results) != list):
        return make_response(json.dumps(results), 400)

# it will request info at results at the index 0 and fill in all the information it got from the get restaurant
    results = fill_optional_data(request.json, results[0], ['email','name','address','phone_number','bio','city','profile_url','banner_url','password'])
# runs the procedure patch_restaurant and will takes the changed infomation and overwrite the existing information and save it in results
    results = dbhelper.run_statment('CALL patch_restaurant(?,?,?,?,?,?,?,?,?,?)',
    [results['email'], results['name'], results['address'], results['phone_number'], results['bio'],
    results['city'], results['profile_url'], results['banner_url'], results['password'], request.headers['token']])

# if results is equal to a list it will display a 200 message (success), and print the results of the procedure as json
# if it isn't it will display a 500 message (server error)
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)


def delete():
# checks the sent data request.headers and the expected data token, sets as variable invalid
    invalid = check_endpoint_info(request.headers, ['token'])
# checks the sent data request.json and the expected data password, sets as variable invalid_password
    invalid_password = check_endpoint_info(request.json, ['password'])
    if(invalid != None or invalid_password != None):
        return make_response(json.dumps(invalid, invalid_password, default=str), 400)


# runs the statment CALL delete_restaurant and sends 3 arguement 1 being the password and the token as a header and salt that was randomly generated and stores it as the variable results
    results = dbhelper.run_statment('CALL delete_restaurant(?,?,?)', [request.json['password'], request.headers['token'], request.json['salt']])
# if results is equal to a list and tuple returned is 0 nothing has been deleted if it returns a  1 something was deleted,
#  it will display a 200 message (success), and print the results of the procedure as json 
# if it isn't it will display a 500 message (server error)
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)



#old delete


# def delete():
#     invalid = check_endpoint_info(request.headers, ['token'])
#     invalid_password = check_endpoint_info(request.json, ['password'])
#     if(invalid == None or invalid_password == None):
#         return make_response(json.dumps(invalid, invalid_password ,default=str), 400)


#     results = dbhelper.run_statment('CALL delete_restaurant(?,?)', [request.json.get('password'), request.headers['token']])
#     if(type(results) == list):
#         return make_response(json.dumps(results, default=str), 200)
#     else:
#         return make_response(json.dumps(results, default=str), 500)