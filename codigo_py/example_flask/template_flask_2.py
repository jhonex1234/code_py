#!/usr/bin/env python
# -*- conding: utf-8 -*-
from flask import Flask
from flask import render_template 

my_app = Flask(__name__, template_folder = "templates_test/")

@my_app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	my_app.run(debug = True, port = 8000)


