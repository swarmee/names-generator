##  requirements pyyml
import yaml
import random
from flask import Flask
from flask_restplus import Resource, Api
import os

#apiKey = os.environ['apiKey']

app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='Name Generator API',
          description='Uses Census Data from US to generate random names',
          prefix="/v1",
          contact="api.support@swarmee.net",
          contact_url="www.swarmee.net",
          doc='/doc')
app.config.SWAGGER_UI_DOC_EXPANSION = 'full'
app.config.SWAGGER_UI_OPERATION_ID = True
app.config.SWAGGER_UI_REQUEST_DURATION = True

firstNameList = []
lastNameList = []

basePath = './'

for root, directories, filenames in os.walk(basePath):
    for filename in filenames:
        pathAndFileName = os.path.join(root, filename)
        if pathAndFileName.endswith('.yml'):
            if pathAndFileName.__contains__('family_name'):
                with open(pathAndFileName) as file:
                    data = yaml.load(file, Loader=yaml.FullLoader)
                    if isinstance(data, list):
                        for record in data:
                            ldata = {"lastName": record}
                            lastNameList.append(ldata)

            elif pathAndFileName.__contains__('given_name'):
                with open(pathAndFileName) as file:
                    data = yaml.load(file, Loader=yaml.FullLoader)
                    if isinstance(data, list):
                        for record in data:
                            firstName = list(record.keys())[0]
                            gender = record[firstName]['gender']
                            fdata = {"firstName": firstName, "gender": gender}
                            firstNameList.append(fdata)
                    elif isinstance(data, dict):
                        firstName = list(data.keys())[0]
                        gender = data[firstName]['gender']
                        fdata = {"firstName": firstName, "gender": gender}
                        firstNameList.append(fdata)


@api.route('/name')
class GenerateName(Resource):
    def get(self):
        name = random.choice(firstNameList)
        name['lastName'] = random.choice(lastNameList)['lastName'].title()
        if name['gender'] == 'unisex':
            name['gender'] = 'unknown'
        name['firstName'] = name['firstName'].title()
        name['fullName'] = name['firstName'] + ' ' + name['lastName']
        return name


if __name__ == '__main__':
    app.run(debug=False, threaded=True)
