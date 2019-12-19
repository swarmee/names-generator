##  imports
import yaml
import random
from flask import Flask, request
import requests
from flask_restplus import Resource, Api
import os
from functools import wraps

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
bsbs = res.json()
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


@pns.route('/getaddress')
class GenerateName(Resource):
    def get(self):
        account = random.choice(bsbs)
        return account


def getDomesticBankAccounts(domesticEntity):
    domesticEntity = {'party': {'account': []}}
    for x in range(0, 1):
        bankAccount = {}
        accountQuery = {
            "query": {
                "function_score": {
                    "functions": [{
                        "random_score": {}
                    }]
                }
            },
            "size": 1
        }
        #if len(domesticEntity['bankAccounts']) > 0:
        #  accountQuery                       = {"query":{"function_score":{"query":{"nested":{"path":"activity.role.party.address","query":{"match":{"activity.role.party.address.suburb":domesticEntity['bankAccounts'][0]['suburb']}}}},"functions":[{"random_score":{}}]}},"size":1}
        accountDetails = es.search(index='bsbs', body=accountQuery)
        bankAccount['institutionName'] = accountDetails['hits']['hits'][0][
            '_source']['bsbDetails']['institutionName'].title()
        bankAccount['institutionCode'] = accountDetails['hits']['hits'][0][
            '_source']['bsbDetails']['financialInstitutionCode']
        bankAccount['bankStateBranchCode'] = accountDetails['hits']['hits'][0][
            '_source']['bsbDetails']['bankStateBranchCode']
        bankAccount['branchName'] = accountDetails['hits']['hits'][0][
            '_source']['activity'][0]['role'][0]['party'][0]['name'][0][
                'fullName']
        bankAccount['streetAddress'] = accountDetails['hits']['hits'][0][
            '_source']['activity'][0]['role'][0]['party'][0]['address'][0][
                'streetAddress'].title()
        try:
            bankAccount['postcode'] = accountDetails['hits']['hits'][0][
                '_source']['activity'][0]['role'][0]['party'][0]['address'][0][
                    'postcode']
        except:
            bankAccount['postcode'] = '2000'
        try:
            bankAccount['suburb'] = accountDetails['hits']['hits'][0][
                '_source']['activity'][0]['role'][0]['party'][0]['address'][0][
                    'suburb'].title()
        except:
            bankAccount['suburb'] = 'Sydney'
        bankAccount['state'] = accountDetails['hits']['hits'][0]['_source'][
            'activity'][0]['role'][0]['party'][0]['address'][0]['state']
        bankAccount['accountNumber'] = fake.numerify(text="##-###-####")
        domesticEntity['party']['account'].append(bankAccount)
    return domesticEntity


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
