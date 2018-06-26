from flask import Flask, render_template
from flask_socketio import SocketIO,send
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Response,request

app = Flask(__name__,template_folder="com_template")
app.config['SECRET_KEY'] = 'secret'
Socketio = SocketIO(app)

@app.route('/')
def index():
	return "why not, use html?"
@app.route('/test_html')
def main_test():
	return  render_template('index.html')

@Socketio.on('message')
def handlMessage(msj):
	print("Message: "+msj)
	send(msj, broadcast = True)

if __name__ == '__main__':
	Socketio.run(app, debug=True,)