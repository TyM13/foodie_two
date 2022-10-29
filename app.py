from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4
import client.client
import restaurant.restaurant
import client_login.client_login
import restaurants.restaurants
import menu.menu


#change conditionals to be correct

app = Flask(__name__)



@app.get('/api/client')
def client_info():
    return client.client.get()



@app.post('/api/client')
def client_post():
    return client.client.post()


@app.patch('/api/client')
def client_patch():
    invalid = check_endpoint_info(request.json['email', 'first_name', 'last_name',
    'image_url', 'username', 'password', request.headers['token']])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

    
    results = dbhelper.run_statment('CALL patch_client(?,?,?,?,?,?)',
    request.json['email', 'first_name', 'last_name','image_url', 'username', 'password'], request.headers['token'])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)



@app.delete('/api/client')
def client_delete():
    invalid = check_endpoint_info(request.headers, ['token'])
    invalid_password = check_endpoint_info(request.json, ['password'])
    #edit below for both
    if(invalid != None or invalid_password != None):
        return make_response(json.dumps(invalid, invalid_password, default=str), 400)




    results = dbhelper.run_statment('CALL delete_client(?,?)', [request.json['password'], request.headers['token']])
    #need statment in if
    if(type(results) == list and len(results[0]) == 1):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)








#--------------------------------CLIENT LOGIN-------------------------------------------------#
#client login


@app.post('/api/client-login')
def login_client():
    return client_login.client_login.post()



# client-login Delete
@app.delete('/api/client-login')
def delete_client():
    invalid = check_endpoint_info(request.json, [''])

    

#------------------------------RESTAURANT-----------------------------------------------#
#restaurant specific info

@app.get('/api/restaurant')
def get_specific_restaurant():
    return restaurant.restaurant.get()


#restaurant signup

@app.post('/api/restaurant')
def restaurant_post():
    return restaurant.restaurant.post()



#----------------------------------RESTAURANTS-----------------------------------------------#
#get restaurants

@app.get('/api/restaurants')
def restaurants_get():
    return restaurants.restaurants.get()



#----------------------------------MENU-----------------------------------------------#
#get specific menu


@app.get('/api/menu')
def menu_get():
    return menu.menu.get()

# post menu

@app.post('/api/menu')
def menu_post():
    return menu.menu.post()




if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5004)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode!")
    app.run(debug=True)








