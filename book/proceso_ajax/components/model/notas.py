# -*- coding: utf-8 -*-
#from flask import Flask
#instancia clase
#app = Flask(__name__)#parametro que utiliza __name__
 
#establece la ruta 
#@app.route('/')

#regresa string
#def index():
 #   return 'hola'
#ejecuta el servidor

#if __name__ == '__main__':
#	app.run()
#permite  definir el puerto donde se ejecutara con 
# port=(puerto requerido) la app por defecto inicia en el 
# port 5000
#permite implementar banderas en caso de estar haciendo test con  debug = true/false
#modificaciones e vivo.
#
## -*- coding: utf-8 -*-
from flask import Flask
from flask import request

app = Flask(__name__)#parametro que utiliza __name__

 
@app.route('/')
def index():
    return 'puerto= 7000\ndebug=True'

@app.route('/home')
def other_index():
    return 'puerto= 7000\ndebug=True hogar'


if __name__ == '__main__':
	app.run(debug=True, port= 7000)
#no se puede repetir metodo por ruta /(name dir)

#
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request

app = Flask(__name__)#parametro que utiliza __name__

 
@app.route('/')

def index():
    return 'puerto= 7000\ndebug=True'

@app.route('/params')

def other_index():
	param =  request.args.get('params1','default_param')
	param_dos =  request.args.get('params2','default_param')
	
	return 'parametros es {} {}'.format(param,param_dos)


if __name__ == '__main__':
	app.run(debug=True, port= 7000)

############ho
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request

app = Flask(__name__)#parametro que utiliza __name__

 
@app.route('/')

def index():
    return 'puerto= 7000\ndebug=True'

@app.route('/params/')

@app.route('/params/<name>/')
@app.route('/params/<name>/<lastname>/')
@app.route('/params/<name>/<lastname>/<int:num>')
def other_index(name='por defecto1',lastname='por defecto2',num=0):
	return 'parametros es {} {}'.format(name,lastname,num)


if __name__ == '__main__':
	app.run(debug=True, port= 7000)

