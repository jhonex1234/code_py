# -*- coding: utf-8 -*-
import psycopg2
import pg


class TypeDataBase():
    def __init__(self,json_db):
        self.database = json_db
        self.cn = ''
        self.conect_datbase(json_db)
    def conect_datbase(self,json_db):
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
        self.cn = self.conect_datbase(self.database)
        cur = self.cn.cursor()
        try:
            cur.execute("select id from businesscase where serial='"+json['sspd']+"'")
            id_bu = cur.fetchall()
            if id_bu:
                json['id'] = id_bu[0][0]
                curup = self.cn.cursor()
            try:
                cur.execute("update businesscase set description=%s where id=%s",(json['date_decision'],json['id']))
                self.cn.commit()
                id_bu = cur.fetchall()
                if id_bu:
                    json['id'] = str(id_bu[0][0])
            except psycopg2.DatabaseError as de:
                if self.cn:
                    cur=''    
        except psycopg2.DatabaseError as de:
            if self.cn:
                cur=''
        finally:
            if self.cn:
                self.cn.close()
        return json
    def update_casoentescontrol(self,json):
        self.cn = self.conect_datbase(self.database)
        cur = self.cn.cursor()
        try:
            try:
                cur.execute("UPDATE public.casoentescontrol SET  documentoantecesor=%s,numerodecisionempresaeca=%s, numeroradicadoportico=%s WHERE id=%s",
                (json['expediente_padre'],json['num_decision'],json['radication_RE'],json['id']))
                self.cn.commit()
            except KeyError as k:
                if self.cn:
                    cur=''
        except psycopg2.DatabaseError as de:
            if self.cn:
                cur = ''                
        finally:
            if self.cn:
                self.cn.close()