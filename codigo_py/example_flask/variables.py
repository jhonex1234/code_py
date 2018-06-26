#!/usr/bin/env python
# -*- conding: utf-8 -*-
from flask import Flask
from flask import render_template 

my_app = Flask(__name__, template_folder = "templates_test/")

@my_app.route('/user/<name>/')
def user(name='jhonex'):
  age = 22
  my_list = [1,2,3,4]
  return render_template('user.html', name=name, age=age, my_list=my_list)

	
if __name__ == '__main__':
	my_app.run(debug = True, port = 8000)


