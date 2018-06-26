from flask import Flask
from flask import request 
my_app = Flask(__name__)

@my_app.route('/')
def index():
    return "hola mundo"

#http://127.0.0.1:8000/params?params1=found_params_url
@my_app.route('/params/')
@my_app.route('/params/<name>/')
@my_app.route('/params/<name>/<int:num>/')
def params(name = 'not_found_param',num = 0):
	return 'The param is {} {}'.format(name,num)


if __name__ == '__main__':
	my_app.run(debug = True, port = 8000)


