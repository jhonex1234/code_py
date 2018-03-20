import joblib
import json as js
import os
import sqlite3 as db
import json
import gzip
import pickle

class clTree():
    
    def __init__(self,namefile):
        self.namefile = namefile
        self.route = '/home/jhonex/Documentos/codigo/codigo_py_soport/tre_editor_versions/tree_editor_local/resource_bd/bd_script/resource_dbtree.sql'
        self.tree_config = {'initial_state': '','templates': [],'max_attempts': 0,
            'topics':{'pendiente':'pendiente'},'transitions':[],'models': [],'final_state' : ''}
        self.insertItemTemplate('')
        self.validateStatedata('')
        self.makeListPkl('')
        self.searchmodel('','')
        self.validateTemplate('','','','')
        self.validatetrasition('','','','')
        
    def getTreeConfig(self):
        return self.tree_config
    
    def makeListState(self,state):
        if(self.namefile != '' and state != ''):
            msj = ''
            if(self.validateStatedata(state)):
                msj = '!La clave no se pudo crear ya exite¡'
            else:
                cn = db.connect(self.route)
                cur = cn.cursor()
                cur.execute("insert into tbl_listState (nameFile,keylistState) values ('%s','%s')"%(self.namefile,state))
                cn.commit()
                cur.close()
                msj = '!clave creada¡'
        return msj   
    
    def validateStatedata(self,state):
        li_1 = []
        cn = db.connect(self.route)
        cur = cn.cursor()
        cur.execute('SELECT keylistState FROM tbl_listState where nameFile="%s" and keylistState="%s"'%(self.namefile,state))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        return sc_list
    
    def getState(self):
        li_1 = []
        cn = db.connect(self.route)
        cur = cn.cursor()
        cur.execute("SELECT keylistState FROM tbl_listState where nameFile='%s'"%(self.namefile))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        if(sc_list):
            sc_list = [list(i) for i in sc_list]
            for i in sc_list:
                li_1.append(i[0])
            sc_list = li_1
        else:
            sc_list = '!no existen estados asociados para este archivo¡'
        return  sc_list
    
    def deleteState(self,state):
        cn = db.connect(self.route)
        cur = cn.cursor()
        cur.execute('DELETE FROM tbl_listState WHERE keylistState="%s" AND nameFile="%s"'%(state,self.namefile))
        cn.commit()
        cur.close()
        msj = '!Eliminado¡'
        return msj
    
    def editState(self,state,modState):
        cn = db.connect(self.route)
        cur = cn.cursor()
        cur.execute('UPDATE tbl_listState SET keylistState="%s" WHERE nameFile="%s" AND keylistState="%s"'%(modState, self.namefile,state ))
        cn.commit()
        cur.close()
        msj = '!Editado¡'
        return msj
    
    def makeListTemplates(self,fileTemplate):
        if(fileTemplate):   
            try:
                file =  json.load(open(fileTemplate,'r'))
                file = list(file.keys())
                msj = self.insertItemTemplate(file)
            except OSError:
                msj = '!No se pudo cargar archivo¡'
        else:
            msj = '!Ingresa un Archivo¡'
        return msj
    
    def insertItemTemplate(self,lis):
        if(lis):
            for row in lis:
                cn = db.connect(self.route)
                cur = cn.cursor()
                cur.execute('delete from tbl_keyslabel where nameFile="%s" and keylabel="%s"'%(self.namefile,row))
                cur.execute('INSERT INTO tbl_keyslabel (nameFile ,keylabel) VALUES ("%s","%s")'%(self.namefile,row))
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
        cur.execute("SELECT keylabel FROM tbl_keyslabel where nameFile='%s'"%(self.namefile))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        if(sc_list):
            sc_list = [list(i) for i in sc_list] 
            for i in sc_list:
                li_1.append(i[0])
            
            sc_list = li_1
        else:
            sc_list = '!no existen estados asociados para este archivo¡'
        return sc_list
    
    def makeListPkl(self,filepkl):
        if(filepkl != ''):
            models = joblib.load(filepkl)
        else:
            models = ''
        return list(models)
    
    def loadPKL(self,namedoc):
        msj = ''
        if(namedoc):
            namedoc = self.makeListPkl(namedoc)
            for row in namedoc:
                cn = db.connect(self.route)
                cur = cn.cursor()
                cur.execute('delete from tbl_LabelPkl where nameFile="%s" and keyLabelPkl="%s"'%(self.namefile,row))
                cur.execute('INSERT INTO tbl_LabelPkl (nameFile, keyLabelPkl) VALUES ("%s","%s")'%(self.namefile,row))
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
        cur.execute("SELECT keyLabelPkl FROM tbl_LabelPkl where nameFile='%s'"%(self.namefile))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        if(sc_list):
            sc_list = [list(i) for i in sc_list]
            for i in sc_list:
                li_1.append(i[0])
            sc_list = li_1
        else:
            sc_list = '!no existen estados asociados para este archivo¡'
        return  sc_list
      
    def searchmodel(self,i_d,state):
        flag = True 
        if(i_d != '' and state  != '' ):     

            try:    
                model = self.tree_config['models']
                for i in  model:
                    if(i['id'] == i_d and i['state'] == state):
                        flag = False
            except KeyError as err:
                print('el archivo cargado no tiene la estructura correcta')
        return flag
    
    def makemodel(self,i_d,state):
        if(self.searchmodel(i_d,state)):
            self.tree_config['models'].append({'id': i_d, 'state': state})
            msj = 'Exito al agregar modelo'
        else:
            msj = 'Error al crear modelo'
        return msj
    
    def loadTreeConfig(self):
        resource = {"final_state":0,}
        if(self.namefile):   
            try:
                try:
            
                    file =  json.load(open(self.namefile,'r'))
                    self.tree_config['templates'] = file['templates']
                    self.tree_config['topics'] = file['topics']
                    self.tree_config['models'] = file['templates']
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
    def maketemplate(self,i_d,label,state,topic):
        msj = ''
        if(self.validateTemplate(i_d,label,state,topic)):
            self.tree_config['templates'].append({'id': i_d,'label': label,'state': state,'topic': topic})
            msj = 'Template agregado'
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
    def makeFile(self,name,final_state, initial_state,max_attempts):
        self.tree_config['final_state'] = final_state
        self.tree_config['initial_state'] = initial_state
        self.tree_config['max_attempts'] = max_attempts
        if(self.tree_config != {} ):
            if(name != ''):
                file = name+'.json'
                self.name = name+'.json'
            else:
                file = self.name
        else:
            file = name+'.json'
            self.name = name+'.json'

        with open(file, 'w', encoding='utf-8') as outfile:
             json.dump(self.tree_config, outfile)
        return self.name 
