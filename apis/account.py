import json
import random
from flask import Flask, request
from flask_restplus import Resource, Api, Namespace
import os
from datetime import date, datetime
from faker import Faker
import security

fake = Faker('en_AU')

## load bsb data into memory
with open('./resources/bsbs.json') as json_file:
    bsbs = json.load(json_file)

api = Namespace('account', description='Account Namespace')


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


@api.route('/random')
class GenerateName(Resource):
    @security.token_required
    def get(self):
        account = Generate_Account()
        return account
