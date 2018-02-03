# -*- coding: utf-8 -*-
import json
import psycopg2
import pg
from datetime import datetime

class TypeDataBase():
    def __init__(self,json_db):
        self.database = json_db
        self.cn = ''
        self.dic={'id':'','sspd':'','error':''}
        self.conect_database(json_db)
        self.update_flag(self.dic)
        
    def conect_database(self,json_db):
        try:
            self.cn = psycopg2.connect("dbname= "
                                  +json_db['db']+
                                  " user= "
                                  +json_db['user']+
                                  " host= "
                                  +json_db['localhost']+
                                  " password= "
                                  +json_db['pass']+" ")
        except psycopg2.DatabaseError as de:
            if self.cn:
                self.cn.rollback()
                print('Error %s'%de)
        return self.cn
    
    def serch_id(self,json):
        self.cn = self.conect_database(self.database)
        cur = self.cn.cursor()
        id_bu = ''
        try:
            cur.execute("select id from businesscase where serial='%s' AND botstate is null"%(json['sspd']))
            id_bu = cur.fetchall()
        except psycopg2.DatabaseError as de:
             json['error'] = 'Error %s'%de
        finally:
            if self.cn:
                self.cn.close()
        if id_bu:
                json['id'] = id_bu[0][0]
        else:
            json["id"] ='none'
                
        return json
    
    def update_flag(self,jso_n):
        self.cn = self.conect_database(self.database)
        cur = self.cn.cursor()
        try:
            cur.execute("update businesscase set botstate=%s where id=%s"%(1,jso_n['id']))
            self.cn.commit()
        except psycopg2.DatabaseError as de:
            jso_n['error'] = 'Error %s'%de
        finally:
            if self.cn:
                self.cn.close()
                
    def update_casoentescontrol(self,json):
        self.cn = self.conect_database(self.database)
        cur = self.cn.cursor()
        try:
            cur.execute("update casoentescontrol set documentoantecesor=%s,numerodecisionempresaeca=%s,"+
                        "numeroradicadoportico=%s where id=%s",(json['expediente_padre'],json['num_decision'], json['radication_RE'],json['id']))
            self.cn.commit()
            self.update_flag(json)
        except psycopg2.DatabaseError as de:
            json['error'] = 'Error %s'%de
        finally:
            if self.cn:
                self.cn.close()
        