import configparser
import json
import logging
import os
import re
import sqlite3
import sys
import traceback

from sklearn.externals import joblib

import dialog_management

def main(json_args):    
    debug = ''
    message = ''
    length = []
    transfer = False   
    error = ''
    try:
        path = os.path.dirname(os.path.abspath(__file__)) + '/ai_agent_resources/'
        config = configparser.ConfigParser()
        config.read(path + 'defaults.cfg')
        system = config['system']

        logging.basicConfig(filename=path + system['error_file'], 
                            level=logging.ERROR, 
                            format='%(asctime)s \t%(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S %p')

        args = json.loads(json_args)
        assert type(args['sessionID']) is str, 'sessionId deberia ser de tipo string'
        # assert type(args['isSessionActive']) is bool, 'isSessionActive deberia ser de tipo bool'
        assert type(args['message']) is str, 'message deberia ser de tipo string'

        connection = sqlite3.connect(path + system['database'])                
        chatbot = dialog_management.Chatbot(path, system, connection)
        chatbot.session(args['sessionID'], args['isSessionActive'])
        debug, message, length, transfer = chatbot.get_answer(args['message'])
        connection.close()
        
    except Exception as err:
        error = err.args[0]
        logging.error(re.sub('\n', '\n' + '\t' * 3, traceback.format_exc()))

    time_per_word = 70
    writing_time = [int(num * time_per_word) for num in length]
    print(json.dumps({'debug': debug, 'result': message, 'transfer': transfer, 'sleepMessage': writing_time, 
                      'crmCommand': '', 'crmAttributes': [],
                      'error': error}))

main(sys.argv[1])
