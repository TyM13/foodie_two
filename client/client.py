from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4

#---------------------------------------------------------------------------------#
#client-info-get

def get():
# checks the sent data request.args and the expected data client_id and stores it as the variable invalid
    invalid = check_endpoint_info(request.args, ['client_id'])
# if the variable invalid is not none it will send back 400 error and a message (client error)
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

# runs the statment CALL get_client and sends the client_id as an arguement and stores it as the variable results
    results = dbhelper.run_statment('CALL get_client(?)',
    [request.args.get('client_id')])
# if results is equal to a list it will display a 200 message (success), and print the results of the procedure as json 
# if it isn't it will display a 500 message (server error)
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)


#---------------------------------------------------------------------------------#
#client-signup-post

def post():
# checks the sent data request.json and the expected data, email, first_name, last_name, image_url, username, password, and stores it as the variable invalid
    invalid = check_endpoint_info(request.json, ['email', 'first_name', 'last_name',
     'image_url', 'username', 'password'])
# if the variable invalid is not none it will send back 400 error and a message (client error)
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

# generates a random unique id and sets it as the variable token
    token = uuid4().hex
# runs the statment CALL post_client and sends 7 arguement 1 being the token that was randomly generated and stores it as the variable results
    results = dbhelper.run_statment('CALL post_client(?,?,?,?,?,?,?)', [request.json.get('email'), request.json.get('first_name'), request.json.get('last_name'),
    request.json.get('image_url'), request.json.get('username'), request.json.get('password'), token])

# if results is equal to a list it will display a 200 message (success), and print the results of the procedure as json
# if it isn't it will display a 500 message (server error)
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)

#---------------------------------------------------------------------------------#

def delete():
# checks the sent data request.headers and the expected data token, sets as variable invalid
    invalid = check_endpoint_info(request.headers, ['token'])
# checks the sent data request.json and the expected data password, sets as variable invalid_password
    invalid_password = check_endpoint_info(request.json, ['password'])
    #edit below for both
    if(invalid != None or invalid_password != None):
        return make_response(json.dumps(invalid, invalid_password, default=str), 400)



# runs the statment CALL delete_client and sends 2 arguement 1 being the password and the token as a header that was randomly generated and stores it as the variable results
    results = dbhelper.run_statment('CALL delete_client(?,?)', [request.json['password'], request.headers['token']])
# if results is equal to a list and tuple returned is 0 nothing has been deleted if it returns a  1 something was deleted,
#  it will display a 200 message (success), and print the results of the procedure as json 
# if it isn't it will display a 500 message (server error)
    if(type(results) == list and (results[0][0]) == 1):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)