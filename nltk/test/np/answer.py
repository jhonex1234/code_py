import configparser
import json
import logging
import re
from sklearn.externals import joblib
import sys
import traceback

import dialog_management

def main(json_params):    
    proba = []
    message = ''
    length = []    
    error = ''
    try:
        config = configparser.ConfigParser()
        config.read('defaults.cfg')
        system = config['system']

        logging.basicConfig(filename=system['path'] + system['error_file'], 
                       level=logging.ERROR, 
                       format='%(asctime)s \t%(message)s', 
                       datefmt='%d/%m/%Y %I:%M:%S %p')

        params = json.loads(json_params)        
        chatbot = dialog_management.Chatbot(system)
        chatbot.session(params['sessionID'], params['isSessionActive'])
        proba, message, length, transfer = chatbot.get_answer(params['message'])
        
    except Exception as err:
        error = err.args[0]
        logging.error(re.sub('\n', '\n' + '\t' * 3, traceback.format_exc()))

    time_per_word = 100
    writing_time = [int(num * time_per_word) for num in length]
    print(json.dumps({'proba': proba, 'result': message, 'sleepMessage': writing_time, 
                      'transfer': transfer, 'error': error}))

main(sys.argv[1])
