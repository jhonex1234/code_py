# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)#parametro que utiliza __name__

 
@app.route('/')

def index():
    return 'puerto= 7000\ndebug=True'

@app.route('/temp_1')
def index_x(name='none'):
	return render_template('index.html',name=name)

if __name__ == '__main__':
	app.run(debug=True, port= 7000)

