from flask import Flask
from flask import render_template 
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

#instance flask
app_flask = Flask(__name__)

#page initial
@app_flask.route('/')
def index():
	return render_template('index.html')

'''
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
 return jsonify({'tasks': tasks})
'''

#404
@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    #app.run(host='0.0.0.0',debug=True)
    app.run(debug = True, port = 8000)
