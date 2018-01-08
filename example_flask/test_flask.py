my_app = Flask(__name__)

@my_app.route('/')
def index():
    return "hola mundo"

my_app.run()

