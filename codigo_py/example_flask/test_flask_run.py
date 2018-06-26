from flask import Flask
my_app = Flask(__name__)

@my_app.route('/')
def index():
    return "hola mundo"
if __name__ == '__main__':
	my_app.run(debug = True, port = 8000)

