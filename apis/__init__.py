from flask_restplus import Api
from flask import Flask, request
from .name import api as name
from .account import api as account

## environment variables
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(authorizations=authorizations,
          security='apikey',
          version='1.0',
          title='Name Generator API',
          description='Uses Census Data from US to generate random names',
          prefix="/v1",
          contact="api.support@swarmee.net",
          contact_url="www.swarmee.net")

api.add_namespace(name, path='/name')
api.add_namespace(account, path='/account')
# ...
#api.add_namespace(nsX)