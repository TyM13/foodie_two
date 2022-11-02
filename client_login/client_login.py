from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4




# Client Login

def post():
# checks the sent data request.json and the expected data email, password, and stores it as the variable invalid
    invalid = check_endpoint_info(request.json, ['email','password'])
# if the variable invalid is not equal to none it will send back 400 error and a message (client error)
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)    

# generates a random unique id and sets it as the variable token
    token = uuid4().hex 
    salt = uuid4().hex
# runs the statment CALL client_login and sends 3 arguements, email, password, and the token and salt that was randomly generated and stores it as the variable results
    results = dbhelper.run_statment('CALL client_login(?,?,?,?)',
    [request.json.get('email'), request.json.get('password'), token, salt])
    
# if results is equal to a list and the length of the results at 0 is equal to 2 it will display a 200 message (success), and print the results of the procedure as json
# otherwise if results is equal to a list and the length of the results at 0 is equal to 0 it will display a 400 message (Bad login attempt)
# otherwiseit will display a 500 message (server error)
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    elif(type(results) == list):
        return make_response(json.dumps("Bad login attempt"), 400)
    else:
        return make_response(json.dumps("Sorry there has been an error"), 500) 


# ------------------------------------------------------------------
# client-Login-Delete(logout)
def delete():
# checks the sent data request.headers and the expected data token and stores it as the variable invalid
    invalid_headers = check_endpoint_info(request.headers, ['token'])
# if the variable invalid is not equal to none it will send back 400 error and a message (client error)
    if(invalid_headers != None):
        return make_response(json.dumps(invalid_headers, default=str), 400)
# runs the procedure client_login_delete and requires the header, token to run and stores what happened as results
    results = dbhelper.run_statment('CALL client_login_delete(?)', [request.headers['token']])
# if results is equal to a list it will display a 200 message (success), and print the results of the procedure as json
# if it isn't it will display a 500 message (server error)
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)



