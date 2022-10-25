from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4
import client.client
import restaurant.restaurant
import client_login.client_login


app = Flask(__name__)



@app.get('/api/client')
def client_info():
    return client.client.get()



@app.post('/api/client')
def client_post():
    return client.client.post()







#---------------------------------------------------------------------------------#
#client login
# NEED HELP WITH UNDERSTANDING ERROR W/ TEACHER

@app.post('/api/client-login')
def login_client():
    return client_login.client_login.post()



@app.delete('/api')
def delete_client():
    invalid = check_endpoint_info(request.json, [''])

    

#---------------------------------------------------------------------------------#
#restaurant specific info

@app.get('/api/restaurant')
def get_specific_restaurant():
    return restaurant.restaurant.get()




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