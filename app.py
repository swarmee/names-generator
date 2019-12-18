##  imports
import yaml
import random
from flask import Flask, request
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
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
try:
    apiKey = os.environ['apiKey']
except:
    apiKey = 'default'

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


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        if not token:
            return {'message': 'Token is missing.'}, 401
        if token != apiKey:
            return {'message': 'Your token is wrong!'}, 401
        #print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)

    return decorated


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


@api.route('/name')
class GenerateName(Resource):
    @token_required
    def get(self):
        name = random.choice(firstNameList)
        name['lastName'] = random.choice(lastNameList)['lastName']
        name['firstName'] = name['firstName']
        name['fullName'] = name['firstName'] + ' ' + name['lastName']
        return name


if __name__ == '__main__':
    app.run(debug=False, threaded=True, host='0.0.0.0')
