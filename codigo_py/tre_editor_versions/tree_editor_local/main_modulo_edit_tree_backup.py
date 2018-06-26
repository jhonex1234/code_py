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
        treeObj =  clTree(str(args['namedoc']),str(args['filesuport']))


        #Create document tree editor 
        if(args['opc'] == "1"):
            namedocument = treeObj.makeJson(args['namedoc'],'','','')

            answer = '!Documento Creado¡'

        if(args['opc'] == "2"):
            answer = treeObj.makeListState(args['val'])
            result = treeObj.getState()
            namedocument = args['namedoc']

        if(args['opc'] =="3"):
            answer = treeObj.makeListTemplates(args['filesuport'])
            namedocument = args['filesuport']
        
        if(args['opc'] == "4"):
            answer = treeObj.loadPKL(args['filesuport'])
            namedocument = args['namedoc']
        if(args['opc'] == "5"):
            #load field type json
            answer = treeObj
            namedocument = args['namedoc']
        if(args['opc'] =="6"):
            answer = treeObj.editState(args['val'],args['modval'])
            result = treeObj.getState()
            namedocument = args['namedoc']
        
        
        answereditortree = {'msj': answer, 'result':result,'error':'','doc_name':namedocument}
    except Exception as err:
        error = err.args[0]
        logging.error(re.sub('\n', '\n' + '\t' * 3, traceback.format_exc()))
        answereditortree = {'msj': '', 'result':'','error':traceback.format_exc(),'doc_name':str(args['namedoc'])}

    print(json.dumps(answereditortree))

main(sys.argv[1])

