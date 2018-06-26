from flask import Flask
from flask import request 
my_app = Flask(__name__)

@my_app.route('/')
def index():
    return "hola mundo"

#http://127.0.0.1:8000/params?params1=found_params_url
@my_app.route('/params')
def params():
	#params1 = param if empy for default param1 = not_found_params
    params = request.args.get('params1','not_found_params')
    return 'The param is {}'.format(params)


if __name__ == '__main__':
	my_app.run(debug = True, port = 8000)


