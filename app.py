from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api.TransformHandler import AdjustContrastHandler, BlurHandler, ApplyKernelHandler, CombineImageHandler, \
    BrightenHandler

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)
api = Api(app)


@app.route('/')
def helloworld():
    return {'status': 'success', 'message': 'hello world'}


api.add_resource(BrightenHandler, '/flask/brighten')
api.add_resource(AdjustContrastHandler, '/flask/contrast')
api.add_resource(BlurHandler, '/flask/blur')
api.add_resource(ApplyKernelHandler, '/flask/kernel')
api.add_resource(CombineImageHandler, '/flask/combine')

