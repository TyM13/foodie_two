from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds
from uuid import uuid4


app = Flask(__name__)

@app.get('/api/client')
def client_info():
    invalid = check_endpoint_info(request.args, ['client_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)


    results = dbhelper.run_statment('CALL get_client(?)',
    [request.args.get('client_id')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)


#---------------------------------------------------------------------------------#

@app.post('/api/client')
def client_post():
    invalid = check_endpoint_info(request.json, ['client_email', 'client_fn', 'client_ln',
     'client_img', 'client_username', 'client_password'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

    token = uuid4().hex
    results = dbhelper.run_statment('CALL post_client(?,?,?,?,?,?,?,?)', [request.json.get('client_email'), request.json.get('client_fn'), request.json.get('client_ln'),
    request.json.get('client_img'), request.json.get('client_username'), request.json.get('client_password'), token])
    if(type(results) == list):
        return make_response(json.dumps(token, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)







if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5004)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode!")
    app.run(debug=True)