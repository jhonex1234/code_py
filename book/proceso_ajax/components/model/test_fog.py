# -*- coding: utf-8 -*-
from flask import Flask
#instancia clase
app = Flask(__name__)#parametro que utiliza __name__
 
#establece la ruta 
@app.route('/')

#regresa string
def index():
    return 'hola'
#ejecuta el servidor

if __name__ == '__main__':
	app.run()
#permite  definir el puerto donde se ejecutara con 
# port=(puerto requerido) la app por defecto inicia en el 
# port 5000
#permite implementar banderas en caso de estar haciendo test con  debug = true/false
#modificaciones e vivo.
#
#
#

