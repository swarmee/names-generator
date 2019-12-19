##  imports
import yaml
import random
from flask import Flask, request
import requests
from flask_restplus import Resource, Api
import os
from datetime import date, datetime
from faker import Faker

## environment variables
firstNameList = []
lastNameList = []
basePath = './'
unisexNameChoices = ['Male', 'Female']
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'query',
        #        'in': 'header',
        'name': 'apikey'
    }
}
try:
    apikey = os.environ['apikey']
except:
    apikey = 'default'

fake = Faker('en_AU')

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

for root, directories, filenames in os.walk(basePath):
    for filename in filenames:
        pathAndFileName = os.path.join(root, filename)
        if pathAndFileName.endswith('.yml'):
            if pathAndFileName.__contains__('family_name'):
                with open(pathAndFileName) as file:
                    data = yaml.load(file, Loader=yaml.FullLoader)
                    if isinstance(data, list):
                        for record in data:
                            ldata = {"lastName": record.title()}
                            lastNameList.append(ldata)

            elif pathAndFileName.__contains__('given_name'):
                with open(pathAndFileName) as file:
                    data = yaml.load(file, Loader=yaml.FullLoader)
                    if isinstance(data, list):
                        for record in data:
                            firstName = list(record.keys())[0]
                            gender = record[firstName]['gender']
                            if gender == 'unisex':
                                gender = random.choice(unisexNameChoices)
                            fdata = {
                                "firstName": firstName.title(),
                                "gender": gender.title()
                            }
                            firstNameList.append(fdata)
                    elif isinstance(data, dict):
                        firstName = list(data.keys())[0]
                        gender = data[firstName]['gender']
                        if name['gender'] == 'unisex':
                            name['gender'] = random.choice(unisexNameChoices)
                        fdata = {
                            "firstName": firstName.title(),
                            "gender": gender.title()
                        }
                        firstNameList.append(fdata)

bsbs = requests.get('https://api.swarmee.net/v1/dataset/bsbs/?batchSize=10000',
                    auth=('example', 'form'))
bsbs = bsbs.json()
bsbs = bsbs['bsbs']['content']

pns = api.namespace('name', description='Name Namespace')


def Generate_Name():
    name = random.choice(firstNameList)
    name['lastName'] = random.choice(lastNameList)['lastName']
    name['firstName'] = name['firstName']
    name['fullName'] = name['firstName'] + ' ' + name['lastName']
    return name


@pns.route('/random')
class GenerateName(Resource):
    def get(self):
        requestDetails = request.args.to_dict()
        suppliedapikey = None
        print(requestDetails)
        if requestDetails.get('apikey', None) != None:
            if isinstance(requestDetails['apikey'], str):
                suppliedapikey = requestDetails['apikey']
        print(suppliedapikey)
        print(apikey)
        if suppliedapikey == apikey:
            response = Generate_Name()
            return response, 200
        else:
            return {"error": "apikey error"}, 401


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


@pns.route('/randomaccount')
class GenerateName(Resource):
    def get(self):
        account = Generate_Account()
        return account


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
