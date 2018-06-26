	#!/usr/bin/env python
# -*- conding: utf-8 -*-
from flask import Flask
from flask import render_template 

my_app = Flask(__name__)

@my_app.route('/')
def index():
    return render_template('index.html')

@my_app.route('/shop')
def shop():
   list_name = ['jhon','juan','marcela']
   return render_template('shop.html',list=list_name)

if __name__ == '__main__':
	my_app.run(debug = True, port = 8000)


