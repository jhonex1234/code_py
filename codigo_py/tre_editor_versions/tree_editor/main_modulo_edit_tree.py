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
    opcintern = 0 
    setid = 0
    namevi = '' 

    try:
        path = os.path.dirname(os.path.abspath(__file__))
        logging.basicConfig(filename=path + '/tree_editor_error.log', 
                            level=logging.ERROR, 
                            format='%(asctime)s \t%(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S %p')

        args = json.loads(json_args)
        
        assert type(args['namedoc']) is str, 'deberia ser de tipo string'    
        treeObj =  clTree(str(args['namedoc']),str(args['filesuport']),args['namefilemodel'])


        #Create document tree editor 
        if(args['opc'] == "1"):
            namedocument = treeObj.makeFile(args['namedoc'],
                                            args['final_state'],
                                            args['initial_state'],
                                            args['max_attempts'])

            answer = '!Documento Creado¡'

        if(args['opc'] == "2"):
            answer = treeObj.makeListState(args['val'])
            namedocument = args['namedoc']

        if(args['opc'] =="3"):
            answer = treeObj.makeListTemplates(args['filesuport'])
            namedocument = args['filesuport']
            

        
        if(args['opc'] == "4"):
            answer = treeObj.loadPKL(args['filesuport'])
            namedocument = args['namedoc']

        if(args['opc'] == "5"):
            #load field type json
            treeObj.loadTreeConfig()
            treeObj.generateModelView(args['filesuport'])
            namevi = treeObj.getNameView()
            namedocument = args['namedoc']
            opcintern = 1
            setid = 1

        if(args['opc'] =="6"):
            answer = treeObj.editState(args['val'],args['modval'])
            namedocument = args['namedoc']


        #interaction edit fileconfig

        if(args['opc'] == "61"):
            answer = treeObj.makemodel(args['model'],args['state'])
            makeFile(args['namedoc'],args['final_state'],args['initial_state'] ,args['max_attempts'])
            opcintern = 1
            setid = 1
            

        if(args['opc'] == "62"):
            answer = treeObj.maketemplate(args['model'],args['label'],
                                        args['state'],args['topic'])
            opcintern = 1
        
        if(args['opc'] == "63"):
            answer = treeObj.maketemplate(args['model'],args['label'],
                                        args['state'],args['topic'])
            opcintern = 1
        
        if(args['opc'] ==  "64"):
            answer = treeObj.maketrasition(args['endstate'],
                args['is_forboo'],args['label'],args['ini_state'])
            opcintern = 1
            
        getfile = treeObj.getTreeConfig()  
        result = treeObj.getState()
        pkl_list = treeObj.getloadPKL()
        template_list = treeObj.getListKeyLabel()
        topic_list = treeObj.getListKeyLabel()
        getlabelmodel = list(treeObj.getlabelmodel(args['modelselect']))


        if(opcintern == 0):
            answereditortree = {
                                'msj': answer, 
                                'result':result,
                                'error':'',
                                'doc_name':namedocument,
                                'pkl_list':pkl_list,
                                'template_list':template_list,
                                'topic_list':topic_list,
                                'getlabelmodel':getlabelmodel}
        else:
            answereditortree = {
                                'error':'',
                                'nameView':namevi,
                                'response_getid':setid,
                                'response_getstate':result,
                                'response_getpkl':pkl_list,
                                'response_gettemplate':template_list,
                                'response_gettopic':topic_list,
                                'response_getlabelpkl':getlabelmodel,
                                'response_gettransitions':getfile['transitions'],
                                'response_getmodels':getfile['models'],
                                'response_gettemplates':getfile['templates'],
                                'response_gettopics':getfile['topics'],
                                'response_getstateinit':getfile['initial_state'],
                                'response_getmax_attempts':getfile['max_attempts'],
                                'response_getfinal_state':getfile['final_state']
                                }

        namedocument = treeObj.makeFile(args['namedoc'],
                                        args['final_state'],
                                        args['initial_state'],
                                        args['max_attempts'])
                        
    except Exception as err:
        error = err.args[0]
        logging.error(re.sub('\n', '\n' + '\t' * 3, traceback.format_exc()))
        answereditortree = {'msj': '', 'result':'','error':traceback.format_exc(),'doc_name':str(args['namedoc'])}

    print(json.dumps(answereditortree))

main(sys.argv[1])

