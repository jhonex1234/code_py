import configparser
import json
import logging
import os
import re
import sys
import traceback

from edit_script import editoreplate

def main(json_args):    
    
    answer = ''
    relaod = ''
    returnkeys = []
    answereditoreplate = {'msj': '', 'result':''}
    error = ''
    
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        #config = configparser.ConfigParser()
        #config.read(path + 'defaults.cfg')
        #system = config['system']

        logging.basicConfig(filename=path + 'error.log', 
                            level=logging.ERROR, 
                            format='%(asctime)s \t%(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S %p')

        args = json.loads(json_args)
        
        #assert type(args['opc']) is int, 'no hay opcion seleccionada'
        assert type(args['namedoc']) is str, 'message deberia ser de tipo string'    
        templateObj =  editoreplate(args['namedoc'])
        returnkeys = templateObj.loadlistkey()
        answer = ''  
        answereditoreplate = {'msj': answer, 'result':returnkeys}
    
    except Exception as err:
        error = err.args[0]
        logging.error(re.sub('\n', '\n' + '\t' * 3, traceback.format_exc()))
        answereditoreplate = {'msj': 'error', 'result':'error'}
    
    print(json.dumps(answereditoreplate))

main(sys.argv[1])
