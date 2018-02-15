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
    answereditoreplate = {'msj': '', 'result':'','error':'','doc_name':''}
    error = ''
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        logging.basicConfig(filename=path + '/error.log', 
                            level=logging.ERROR, 
                            format='%(asctime)s \t%(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S %p')

        args = json.loads(json_args)
        
        assert type(args['namedoc']) is str, 'message deberia ser de tipo string'    
        templateObj =  editoreplate(args['namedoc'])
        returnkeys = templateObj.loadlistkey()
        
        #if(args['opc'] == 1 and args['opc']):
        if (args['opc'] == "3" ):
            answer = templateObj.loadmjs(str(args['keyvalue']))
            
        if (args['opc'] =="7"):
            del templateObj
            answer = 'ingrese un valor'
            returnkeys = 'ingrese un valor'

        answereditoreplate = {'msj': answer, 'result':returnkeys,'error':'','doc_name':args['namedoc']}
    except Exception as err:
        error = err.args[0]
        logging.error(re.sub('\n', '\n' + '\t' * 3, traceback.format_exc()))
        answereditoreplate = {'msj': args['keyvalue'], 'result':'','error':error,'doc_name':str(args['namedoc'])}
    
    print(json.dumps(answereditoreplate))

main(sys.argv[1])

