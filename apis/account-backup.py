###
# python3 -mpip install flask-bcrypt flask-restplus Flask-Migrate pyjwt Flask-Script  flask_testing
#
# ##  imports
import json
import random
from flask import Flask, request
import requests
from flask_restplus import Resource, Api
import os
from datetime import date, datetime
from faker import Faker
from functools import wraps

## environment variables
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
try:
    apiKey = os.environ['apiKey']
except:
    apiKey = 'default'

print(apiKey)

fake = Faker('en_AU')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        if not token:
            return {'message': 'Token is missing.'}, 401
        if token != apiKey:
            return {'message': 'Your token is wrong, wrong, wrong!!!'}, 401
        return f(*args, **kwargs)

    return decorated


app = Flask(__name__)
api = Api(app,
          authorizations=authorizations,
          security='apikey',
          version='1.0',
          title='Name Generator API',
          description='Uses Census Data from US to generate random names',
          prefix="/v1",
          contact="api.support@swarmee.net",
          contact_url="www.swarmee.net"
          #          ,          doc='/doc'
          )
app.config.SWAGGER_UI_DOC_EXPANSION = 'full'
app.config.SWAGGER_UI_OPERATION_ID = True
app.config.SWAGGER_UI_REQUEST_DURATION = True
app.config.SWAGGER_UI_JSONEDITOR = True

## load name data into memory
with open('firstNameList.json') as json_file:
    firstNameList = json.load(json_file)
with open('lastNameList.json') as json_file:
    lastNameList = json.load(json_file)

## load bsb data into memory
with open('bsbs.json') as json_file:
    bsbs = json.load(json_file)

pns = api.namespace('name', description='Name Namespace')
ans = api.namespace('account', description='Account Namespace')


def Generate_Name():
    name = random.choice(firstNameList)
    name['lastName'] = random.choice(lastNameList)['lastName']
    name['firstName'] = name['firstName']
    name['fullName'] = name['firstName'] + ' ' + name['lastName']
    return name


@pns.route('/random')
class GenerateName(Resource):
    @token_required
    def get(self):
        print(request.headers)
        response = Generate_Name()
        return response, 200


## comment
def Generate_Account():
    account = random.choice(bsbs)
    bankAccount = {}
    bankAccount['institutionName'] = account['bsb']['content']['bsbDetails'][
        'institutionName'].title()
    bankAccount['institutionCode'] = account['bsb']['content']['bsbDetails'][
        'financialInstitutionCode']
    bankAccount['bankStateBranchCode'] = account['bsb']['content'][
        'bsbDetails']['bankStateBranchCode']
    bankAccount['branchName'] = account['bsb']['content']['activity'][0][
        'role'][0]['party'][0]['name'][0]['fullName']
    bankAccount['streetAddress'] = account['bsb']['content']['activity'][0][
        'role'][0]['party'][0]['address'][0]['streetAddress'].title()
    try:
        bankAccount['postcode'] = account['bsb']['content']['activity'][0][
            'role'][0]['party'][0]['address'][0]['postcode']
    except:
        bankAccount['postcode'] = '2000'
    try:
        bankAccount['suburb'] = account['bsb']['content']['activity'][0][
            'role'][0]['party'][0]['address'][0]['suburb'].title()
    except:
        bankAccount['suburb'] = 'Sydney'
    bankAccount['state'] = account['bsb']['content']['activity'][0]['role'][0][
        'party'][0]['address'][0]['state']
    bankAccount['accountNumber'] = fake.numerify(text="##-###-####")
    return bankAccount


@ans.route('/random')
class GenerateName(Resource):
    @token_required
    def get(self):
        if Auth_apiKey(request.args.to_dict()):
            account = Generate_Account()
            return account
        else:
            return {"error": "apiKey error"}, 401


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
