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
    namedocument = ''
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        logging.basicConfig(filename=path + '/error.log', 
                            level=logging.ERROR, 
                            format='%(asctime)s \t%(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S %p')

        args = json.loads(json_args)
        
        assert type(args['namedoc']) is str, 'message deberia ser de tipo string'    
        templateObj =  editoreplate(str(args['namedoc']))
       
        if(args['namedoc'] != '' ):
            namedocument = args['namedoc']
        
        if(args['opc'] == "4" and args['opc']):
            namedocument = args['namedoc']
            answer = templateObj.deleteScript(str(args['keyvalue']))
            namedocument = templateObj.makeJson('')
     
        if (args['opc'] == "3" ):
            namedocument = args['namedoc']
            answer = templateObj.loadmjs(str(args['keyvalue']))
        
        if (args['opc'] == "5" ):
                templateObj.makeJsonData(args['keyvalue'],args['message'])

        if(args['opc'] =="6"):
            namedocument = args['namedoc']
            templateObj.editJson(args['keyvalue'],args['message'])
        
        if (args['opc'] == "7"):
            templateObj.makeJsonData(str(args['keyvalue']),str(args['message']))
            namedocument = templateObj.makeJson(args['namedoc'])
            answer = ''

        if(args['opc'] != "7" or args['opc'] != "4"):
            namedocument = templateObj.makeJson('')

        returnkeys = templateObj.loadlistkey()
        #Send Response
        answereditoreplate = {'msj': answer, 'result':returnkeys,'error':'','doc_name':namedocument}
    except Exception as err:
        error = err.args[0]
        logging.error(re.sub('\n', '\n' + '\t' * 3, traceback.format_exc()))
        answereditoreplate = {'msj': '', 'result':'','error':traceback.format_exc(),'doc_name':str(args['namedoc'])}
    
    print(json.dumps(answereditoreplate))

main(sys.argv[1])

