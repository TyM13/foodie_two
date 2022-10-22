from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4
import client.client
import restaurant.restaurant


app = Flask(__name__)



@app.get('/api/client')
def client_info():
    return client.client.get()



@app.post('/api/client')
def client_post():
    return client.client.post




#---------------------------------------------------------------------------------#
#client login


@app.post('/api/client-login')
def client_login():
    invalid = check_endpoint_info(request.json, ['email','password'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)    

    token = uuid4().hex
    results = ('CALL client_login(?,?,?)',
    [request.json.get('email'), request.json.get('password'), token])
    
    if(type(results) == list and results[0][0] == 1):
        return make_response(json.dumps(results, default=str), 200)
    elif(type(results) == list and results[0][0] == 0):
        return make_response(json.dumps("Bad login attempt"), 400)
    else:
        return make_response(json.dumps("Sorry there has been an error"), 500) 
    

#---------------------------------------------------------------------------------#
#restaurant specific info

@app.get('/api/restaurant')
def get_specific_restaurant():
    return restaurant.restaurant.get




#---------------------------------------------------------------------------------#
#restaurant signup


if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5004)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode!")
    app.run(debug=True)