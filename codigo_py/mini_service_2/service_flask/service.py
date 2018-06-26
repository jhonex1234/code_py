from flask import Flask
from flask import render_template 
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

from main_extract import read_file
from extractField import extractField
from serviceTrigger import queryField
#instance flask
app_flask = Flask(__name__)
#read('/home/jhonex/document_e/')
#page initial


@app_flask.route('/')
def index():
	return render_template('index.html')


#Extractor_field
@app_flask.route('/nltk/ef/', methods=['GET'])
def get_fields():
   file = read_file()
   return  jsonify({'Campos': file})


#launch error 404
@app_flask.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    #app.run(host='0.0.0.0',debug=True)
    app_flask.run(host='0.0.0.0',debug = True,port=5001)
    ## peticion tiempo
    ## proceso 
    ## wget
