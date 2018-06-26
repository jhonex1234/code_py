from sklearn.externals import joblib
import json as js
import os
import sqlite3 as db
import json
import gzip
import pickle
from graphviz import Digraph
script_dir = os.path.dirname(os.path.abspath(__file__))

class clTree():    
    def __init__(self,namefile,filesuport,namefilemodel):
        #route resource database
        self.route = os.path.join(script_dir, "resource_bd/bd_script/resource_dbtree.sql")
        self.modeload = {}
        self.namefile = namefile
        self.filesuport = filesuport
        self.nameview = ''
        
        self.tree_config = {'initial_state': '','templates': [],'max_attempts': 0,
            'topics':{'pendiente':'pendiente'},'transitions':[],'models': [],'final_state' : ''}
        
        self.insertItemTemplate('')

        self.validateStatedata('')

        self.makeListPkl(namefilemodel)
        self.validateTemplate('','','','')
        self.validatetrasition('','','','')
        
        self.lengResource = {"len_state":0,"len_model":0}
        self.getdifference()
    
    def getTreeConfig(self):
        return self.tree_config
    
    def getNameView(self):
        return self.nameview

    def getlabelmodel(self,typemodel):
        if(typemodel):
            returnlist = self.modeload[typemodel]['classifier'].classes_
        else:
             returnlist = ['Archivo modelos no cargado']   
        return returnlist


    def makeListState(self,state):
        if(self.namefile != '' and state != ''):
            msj = ''
            if(self.validateStatedata(state)):
                msj = '!La clave no se pudo crear ya exite¡'
            else:
                cn = db.connect(self.route)
                cur = cn.cursor()
                name_file = self.namefile
                cur.execute("insert into tbl_listState (nameFile,keylistState) values ('%s','%s')"%(name_file.replace('.json',''),state))
                
                cn.commit()
                cur.close()
                cont = self.getdifference()
                if(self.lengResource['len_model'] != 0):
                    if(self.lengResource['len_model'] >= self.lengResource['len_state']):
                        if(cont == 0):
                            msj = 'Estado agregado, tiene '+str(cont)+' modelos sin usar'
                        else:
                             msj = 'Estado agregado, tiene '+str(cont)+' modelos sin usar'
                         
                    else:
                         if(cont == 0):
                            msj = 'Estado Cargado, Usted tiene la misma cantidad de modelo y estados'

                         else:
                            msj = 'Estado Cargado, Usted tiene mas estados que modelos'
                else:
                    msj = 'Estado Cargado, Recuerde cargar, el paquete de modelos'
        else:
            msj = ''
        return msj   

    def validateStatedata(self,state):
        li_1 = []
        cn = db.connect(self.route)
        cur = cn.cursor()
        name_file = self.namefile
        cur.execute('SELECT keylistState FROM tbl_listState where nameFile="%s" and keylistState="%s"'%(name_file.replace('.json',''),state))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        return sc_list

    def getState(self):
        li_1 = []
        cn = db.connect(self.route)
        cur = cn.cursor()
        name_file = self.namefile
        cur.execute("SELECT keylistState FROM tbl_listState where nameFile='%s'"%(name_file.replace('.json','')))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        if(sc_list):
            sc_list = [list(i) for i in sc_list]
            for i in sc_list:
                li_1.append(i[0])
            sc_list = li_1

        else:
            sc_list = ['!no existen estados asociados para este archivo¡']
        self.lengResource['len_state'] = len(sc_list)
        return  sc_list

    def deleteState(self,state):
        cn = db.connect(self.route)
        cur = cn.cursor()
        name_file = self.namefile
        cur.execute('DELETE FROM tbl_listState WHERE keylistState="%s" AND nameFile="%s"'%(state,name_file.replace('.json','')))
        cn.commit()
        cur.close()
        msj = '!Eliminado¡'
        return msj

    def editState(self,state,modState):
        try:    
            cn = db.connect(self.route)
            cur = cn.cursor()
            name_file = self.namefile
            cur.execute('UPDATE tbl_listState SET keylistState="%s" WHERE nameFile="%s" AND keylistState="%s"'%(modState, name_file.replace('.json',''),state ))
            cn.commit()
            cur.close()
            msj = '!Editado¡'
        except sqlite3.Error as e:
            msj = 'ocurrio un error en le proce de edicion: '%e
        return msj

    def makeListTemplates(self,fileTemplate):
        path = os.path.join(script_dir,"resource/other/"+fileTemplate)
        if(fileTemplate):   
            try:
                file =  json.load(open(path,'r+'))
                file = list(file.keys())
                msj =  self.insertItemTemplate(file)
            except OSError as err:
                msj = "!No se pudo cargar archivo¡{0}".format(err)
        else:
            msj = '!Ingresa un Archivo¡'
        return msj
    
    def getdifference(self):
        li_1 = []
        li_2 = []
        cn = db.connect(self.route)
        cur = cn.cursor()
        name_file = self.namefile
        
        cur.execute("SELECT keylistState FROM tbl_listState where nameFile='%s'"%(name_file.replace('.json','')))
        sc_list = cur.fetchall()
        
        cur.execute("SELECT keyLabelPkl FROM tbl_LabelPkl where nameFile='%s'"%(name_file.replace('.json','')))
        sc_list2 = cur.fetchall()        
        
        cn.commit()
        cur.close()
        if(sc_list2):
            sc_list2 = [list(i) for i in sc_list2]
            for i in sc_list2:
                li_2.append(i[0])
            sc_list2 = li_2

        if(sc_list):
            sc_list = [list(i) for i in sc_list]
            for i in sc_list:
                li_1.append(i[0])
            sc_list = li_1

        self.lengResource['len_state'] = len(sc_list)
        self.lengResource['len_model'] = len(sc_list2)
        com_msj = 0 
        if(self.lengResource['len_model'] >= self.lengResource['len_state']):
            com_msj = self.lengResource['len_model'] - self.lengResource['len_state']
        else:
            com_msj = self.lengResource['len_state'] - self.lengResource['len_model']
        return  com_msj

    def insertItemTemplate(self,lis):
        if(lis):
            for row in lis:
                cn = db.connect(self.route)
                cur = cn.cursor()
                name_file = self.namefile
                cur.execute('delete from tbl_keyslabel where nameFile="%s" and keylabel="%s"'%(name_file.replace('.json',''),row))
                cur.execute('INSERT INTO tbl_keyslabel (nameFile ,keylabel) VALUES ("%s","%s")'%(name_file.replace('.json',''),row))
                
                cn.commit()
                cur.close()

                msj = '!Lista creada¡'
        else:
            msj = ''
        return  msj

    def getListKeyLabel(self):
        li_1 = []
        cn = db.connect(self.route)
        cur = cn.cursor()
        name_file = self.namefile
        cur.execute("SELECT keylabel FROM tbl_keyslabel where nameFile='%s'"%(name_file.replace('.json','')))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        if(sc_list):
            sc_list = [list(i) for i in sc_list] 
            for i in sc_list:
                li_1.append(i[0])
            
            sc_list = li_1
        else:
            sc_list = ['!no existen plantillas asociados para este archivo¡']
        return sc_list

    def makeListPkl(self,filepkl):
        if(filepkl != ''):
            models = joblib.load(os.path.join(script_dir,"resource/other/"+filepkl))
            self.modeload = models
        else:
            models = ''
        return list(models)

    def loadPKL(self,namedoc):
        msj = ''
        if(namedoc):
            namedoc = self.makeListPkl(namedoc)
            self.lengResource['len_model'] =len(namedoc)
            for row in namedoc:
                cn = db.connect(self.route)
                cur = cn.cursor()
                name_file = self.namefile
                cur.execute('delete from tbl_LabelPkl where nameFile="%s" and keyLabelPkl="%s"'%(name_file.replace('.json',''),row))
                cur.execute('INSERT INTO tbl_LabelPkl (nameFile, keyLabelPkl) VALUES ("%s","%s")'%(name_file.replace('.json',''),row))
                cn.commit()
                cur.close()

            msj = 'quedo cargado'
        else:
            msj = 'no se pudo cargar datos'
        return msj

    def deleteAllContent(self):
        cn = db.connect(self.route)
        cur = cn.cursor()
        cur.execute('delete from tbl_keyslabel;')
        cur.execute('delete from tbl_listState;')
        cur.execute('delete from tbl_LabelPkl;')
        cn.commit()
        cur.close()

    def getloadPKL(self):
        li_1 = []
        cn = db.connect(self.route)
        cur = cn.cursor()
        name_file = self.namefile
        cur.execute("SELECT keyLabelPkl FROM tbl_LabelPkl where nameFile='%s'"%(name_file.replace('.json','')))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        if(sc_list):
            sc_list = [list(i) for i in sc_list]
            for i in sc_list:
                li_1.append(i[0])
            sc_list = li_1
        else:
            sc_list = ['!no existen estados asociados para este archivo¡']
        return  sc_list
    
    def searchmodel(self,i_d,label,state,topic):
        flag = True 
        if(i_d != '' and state  != '' ):     

            try:    
                model = self.tree_config['models']
                for i in  model:
                    if(i['id'] == i_d and i['label'] == label and i['state'] == state and i['topic'] == topic):
                        flag = False
            except KeyError as err:
                print('el archivo cargado no tiene la estructura correcta')
        return flag
    
    def makemodel(self,i_d,label,state,topic):
        if(self.searchmodel(i_d,state)):
            self.tree_config['models'].append({'id': i_d,'label':label, 'state': state,'topic':topic})
            msj = 'Exito al agregar modelo'
        else:
            msj = 'Error al crear modelo'
        return msj

    def loadTreeConfig(self):
        resource = {"final_state":0,}
        if(self.namefile):   
            try:
                path = os.path.join(script_dir, "resource/other/"+self.namefile) 
                file =  json.load(open(path,'r+'))
                self.tree_config['templates'] = file['templates']
                self.tree_config['topics'] = file['topics']
                self.tree_config['models'] = file['models']
                self.tree_config['transitions'] = file['transitions']
                self.tree_config['initial_state'] = file['initial_state']
                self.tree_config['final_state'] = file['final_state']
                self.tree_config['max_attempts'] = file['max_attempts']
                msj = '!Recursos cargados¡'
            except KeyError as err:
                  msj = '!No se pudo cargar archivo\n la estructura del archivo no es compatible¡'
            
            except OSError:
                msj = '!No se pudo cargar archivo, Archivo inexistente¡'
        else:
            msj = '!Ingresa un Archivo¡'
        return msj
    
    def generateModelView(self,namefile):
        msj = ''
        
        path = os.path.join(script_dir, "resource/other/"+namefile)       
        try:
            file = json.load(open(path,'r+'))
            self.nameview = namefile.replace('.json','')
            self.nameview = self.nameview +'-graph'+'.gv.'
            test_graph =  Digraph('state_machine',filename=self.nameview,format='png',directory=script_dir+"/img/")
            self.nameview = self.nameview +'png'
            test_graph.attr('graph',rankdir='UD',size='100',ranksep='2equally')

            test_graph.attr('node',shape='circle',fontcolor='white',fontsize='12',style='filled',fillcolor='blue')

            for test_item in file['transitions']:
                test_graph.edge(test_item['starting_state'].upper(),
                                test_item['ending_state'].upper(),
                                label=test_item['label'])
            save = test_graph.render()
            msj = 'grafica generada exitosamente'
        except OSError as err:
            msj = 'archivo no encontrado'
            self.nameview = msj
        return msj

    def maketemplate(self,i_d,label,state,topic):
        msj = ''
        if(self.validateTemplate(i_d,label,state,topic)):
            self.tree_config['templates'].append({'id': i_d,'label': label,'state': state,'topic': topic})
            msj = 'Template agregado'
        else: 
            msj = 'Error al agregar template'
        
        return msj
    
    def validatetrasition(self,endstate, is_forboo,label,ini_state):
        flag = True 
        if(endstate != '' and is_forboo != '' and label != '' and ini_state != ''):    
            try:    
                model = self.tree_config['transitions']
                for i in  model:
                    if(i['ending_state'] == endstate and i['is_forced'] == is_forboo and i['label'] == label and i['starting_state'] == ini_state):
                        flag = False
            except KeyError as err:
                print('el archivo cargado no tiene la estructura correcta')
        return flag

    
    def maketrasition(self,endstate, is_forboo,label,ini_state):
        if(self.validatetrasition(endstate, is_forboo,label,ini_state)):    
            self.tree_config['transitions'].append({'ending_state': endstate, 
                                           'is_forced': is_forboo, 
                                           'label': label,
                                           'starting_state': ini_state})
            msj = 'Transicion agregada'
        else:
            msj = 'Error al agregar template'
        return msj


    

    def validateTemplate(self,i_d,label,state,topic):
        flag = True 
        if(i_d != '' and state  != '' and label != '' ):     

            try:    
                model = self.tree_config['templates']
                for i in  model:
                    if(i['id'] == i_d and i['state'] == state and i['label'] == label and i['topic'] == topic):
                        flag = False
            except KeyError as err:
                print('el archivo cargado no tiene la estructura correcta')
        return flag
    


    def makeFile(self,name,final_state, initial_state,max_attempts):
        self.tree_config['final_state'] = final_state
        self.tree_config['initial_state'] = initial_state
        self.tree_config['max_attempts'] = max_attempts
        if(self.namefile != '' ):    
            self.namefile = self.namefile.replace('.json','')
            self.namefile = self.namefile+'.json'
            file = self.namefile
        else:
            name = name.replace('.json','')
            name = name+'.json'
            file = name 
            self.namefile = name
         
        file = os.path.join(script_dir, "uploads/"+file)
        with open(file, 'w+', encoding='utf-8') as outfile:
             json.dump(self.tree_config, outfile)
        return self.namefile