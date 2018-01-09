	#!/usr/bin/env python
# -*- conding: utf-8 -*-
from flask import Flask
from flask import render_template 

my_app = Flask(__name__)

@my_app.route('/')
def index():
   title = "step_flask"
   return render_template('index.html',title=title)

if __name__ == '__main__':
	my_app.run(debug = True, port = 8000)


