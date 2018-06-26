import configparser
import json
import logging
import os
import re
import sys
import traceback 

#Class editor tree
from clTree import clTree

def main(json_args):    

    answer = ''
    answereditortree = {'msj': '', 'result':'','error':'','doc_name':''}
    error = ''
    namedocument = ''
    result = []

    try:
        path = os.path.dirname(os.path.abspath(__file__))
        logging.basicConfig(filename=path + '/tree_editor_error.log', 
                            level=logging.ERROR, 
                            format='%(asctime)s \t%(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S %p')

        args = json.loads(json_args)
        
        assert type(args['namedoc']) is str, 'deberia ser de tipo string'    
        treeObj =  clTree(str(args['namedoc']))


        #Create document tree editor 
        if(args['opc'] == "1"):
            namedocument = treeObj.makeJson(args['namedoc'])

            answer = '!Documento Creado¡'

        if(args['opc'] == "2"):
            answer = treeObj.makeJson(args['val'])
            resul_t = treeObj.getState()
            if(resul_t['list']):
                result = resul_t['list']
            else:
                del answer
                answer = resul_t['msj']
            namedocument = args['namedoc']
       
        
        answereditortree = {'msj': answer, 'result':result,'error':'','doc_name':namedocument}
    except Exception as err:
        error = err.args[0]
        logging.error(re.sub('\n', '\n' + '\t' * 3, traceback.format_exc()))
        answereditortree = {'msj': '', 'result':'','error':traceback.format_exc(),'doc_name':str(args['namedoc'])}

    print(json.dumps(answereditortree))

main(sys.argv[1])

