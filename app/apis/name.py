##  imports
import random
from flask_restplus import Resource, Api, Namespace
from flask import request
from datetime import date, datetime
from functools import wraps
import json
from functools import wraps
import security

## load name data into memory
with open('./resources/firstNameList.json') as json_file:
    firstNameList = json.load(json_file)
with open('./resources/lastNameList.json') as json_file:
    lastNameList = json.load(json_file)

api = Namespace('name', description='Name Namespace')


def Generate_Name():
    name = random.choice(firstNameList)
    name['lastName'] = random.choice(lastNameList)['lastName']
    name['firstName'] = name['firstName']
    name['fullName'] = name['firstName'] + ' ' + name['lastName']
    return name


@api.route('/random')
class GenerateName(Resource):
    @security.token_required
    def get(self):
        print(request.headers)
        response = Generate_Name()
        return response, 200