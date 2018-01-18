from flask import Flask
from flask import render_template 
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from main_extract import read_file
from extractField import extractField

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

#new task
@app_flask.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
 if not request.json or not 'title' in request.json:
  abort(400)
 task = {
  'id': tasks[-1]['id'] + 1,
  'title': request.json['title'],
  'description': request.json.get('description', ""),
  'done': False
 }
 tasks.append(task)
 return jsonify({'task': task}), 201

@app_flask.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    #app.run(host='0.0.0.0',debug=True)
    app_flask.run(host='0.0.0.0',debug = True)
    ## peticion tiempo
    ## proceso 
    ## wget
