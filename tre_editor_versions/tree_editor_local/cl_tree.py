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
        self.route = '/home/jhonex/Documentos/codigo/codigo_py_soport/tree_editor/resource_bd/bd_script/resource_dbtree.sql'
        self.insertItem('')
        self.valdata('')
        self.makeListPkl('')
    #make state
    def makeState(self,state):
        if(self.namefile != '' and state != ''):
            msj = ''
            if(self.valdata(state)):
                msj = '!La clave no se pudo crear ya exite¡'
            else:
                cn = db.connect(self.route)
                cur = cn.cursor()
                cur.execute("insert into tbl_listState (nameFile,keylistState) values ('%s','%s')"%(self.namefile,state))
                cn.commit()
                cur.close()
                msj = '!clave creada¡'
        return msj   
    #attend method makestate
    def valdata(self,state):
        cn = db.connect(self.route)
        cur = cn.cursor()
        cur.execute('SELECT keylistState FROM tbl_listState where nameFile="%s" and keylistState="%s"'%(self.namefile,state))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        return sc_list
    #return list items
    def getState(self):
        cn = db.connect(self.route)
        cur = cn.cursor()
        cur.execute("SELECT keylistState FROM tbl_listState where nameFile='%s'"%(self.namefile))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        if(sc_list):
            sc_list = sc_list
        else:
            sc_list = '!no existen estados asociados para este archivo¡'
        return  [list(i) for i in sc_list]
    #delete state
    def deleteState(self,state):
        cn = db.connect(self.route)
        cur = cn.cursor()
        cur.execute('DELETE FROM tbl_listState WHERE keylistState="%s" AND nameFile="%s"'%(state,self.namefile))
        cn.commit()
        cur.close()
        msj = '!Eliminado¡'
        return msj
    #edit state 
    def editState(self,state,modState):
        cn = db.connect(self.route)
        cur = cn.cursor()
        cur.execute('UPDATE tbl_listState SET keylistState="%s" WHERE nameFile="%s" AND keylistState="%s"'%(modState, self.namefile,state ))
        cn.commit()
        cur.close()
        msj = '!Editado¡'
        return msj
    #load and make list item of file type json
    def makeListTemplates(self,fileTemplate):
        if(fileTemplate):   
            try:
                file =  json.load(open(fileTemplate,'r'))
                file = list(file.keys())
                msj = self.insertItem(file)
            except OSError:
                msj = '!No se pudo cargar archivo¡'
        else:
            msj = '!Ingresa un Archivo¡'
        return msj
    #method suport makeListTemplates
    def insertItem(self,lis):
        if(lis):
            for row in lis:
                cn = db.connect(self.route)
                cur = cn.cursor()
                cur.execute('INSERT INTO tbl_keyslabel (nameFile ,keylabel) VALUES ("%s","%s")'%(self.namefile,row))
                cn.commit()
                cur.close()
                msj = '!Lista creada¡'
        else:
            msj = ''
        return  msj
    #return list items template
    def getListKeyLabel(self):
        cn = db.connect(self.route)
        cur = cn.cursor()
        cur.execute("SELECT keylabel FROM tbl_keyslabel where nameFile='%s'"%(self.namefile))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        if(sc_list):
            sc_list = [list(i) for i in sc_list] 
        else:
            sc_list = '!no existen estados asociados para este archivo¡'
        return sc_list
    #method simulation load of type pkl 
    def makeListPkl(self,filepkl):
        listpkl = []
        if(filepkl != ''):
            listpkl = ['usuario','teste','nuevo']
        return listpkl
    #load and make list itemspkl
    def loadPKL(self,namedoc):
        msj = ''
        if(namedoc):
            namedoc = self.makeListPkl(namedoc)
            for row in namedoc:
                cn = db.connect(self.route)
                cur = cn.cursor()
                cur.execute('INSERT INTO tbl_LabelPkl (nameFile, keyLabelPkl) VALUES ("%s","%s")'%(self.namefile,row))
                cn.commit()
                cur.close()
            msj = 'quedo cargado'
        else:
            msj = 'no se pudo cargar datos'
        return msj
    #return list pkl
    def getloadPKL(self):
        cn = db.connect(self.route)
        cur = cn.cursor()
        cur.execute("SELECT keyLabelPkl FROM tbl_LabelPkl where nameFile='%s'"%(self.namefile))
        sc_list = cur.fetchall()
        cn.commit()
        cur.close()
        if(sc_list):
            sc_list = sc_list
        else:
            sc_list = '!no existen estados asociados para este archivo¡'
        return  [list(i) for i in sc_list]
