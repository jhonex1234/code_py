from sklearn.externals import joblib
import json as js
import os
import sqlite3 as db
import json
import gzip
import pickle
script_dir = os.path.dirname(os.path.abspath(__file__))

class clTree():    
    def __init__(self,namefile,filesuport):
        self.namefile = namefile
        self.filesuport = filesuport
        self.content = {}
        self.route = os.path.join(script_dir, "resource_bd/bd_script/resource_dbtree.sql")
        self.insertItem('')
        self.valdata('')
        self.makeListPkl('')
        self.lengResource = {"len_state":0,"len_model":0}
        self.getdifference()

    def makeState(self,state):
        if(self.namefile != '' and state != ''):
            msj = ''
            if(self.valdata(state)):
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
                       msj = 'Estado agregado, faltan ',cont,' estados mas por agregar'
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

    def valdata(self,state):
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
            sc_list = '!no existen estados asociados para este archivo¡'
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
                msj = self.insertItem(file)
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

    def insertItem(self,lis):
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
            sc_list = ['!no existen estados asociados para este archivo¡']
        return sc_list

    def makeListPkl(self,filepkl):
        if(filepkl != ''):
            models = joblib.load(os.path.join(script_dir,"resource/other/"+filepkl))
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
            sc_list = '!no existen estados asociados para este archivo¡'
        return  sc_list
 

    def makeJson(self,name):
        if(self.content != [] ):
            if(name != ''):
                file = name+'.json'
                self.name = name+'.json'
            else:
                file = self.name
        else:
            file = name+'.json'
            self.name = name+'.json'
         
        file = os.path.join(script_dir, "uploads/"+file)
        with open(file, 'w+', encoding='utf-8') as outfile:
             json.dump(self.content, outfile)
        return self.name