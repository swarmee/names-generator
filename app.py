from flask import Flask
from apis import api

app = Flask(__name__)
api.init_app(app)

app.config.SWAGGER_UI_DOC_EXPANSION = 'full'
app.config.SWAGGER_UI_OPERATION_ID = True
app.config.SWAGGER_UI_REQUEST_DURATION = True

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)