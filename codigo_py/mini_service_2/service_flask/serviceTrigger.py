# -*- coding: utf-8 -*-
import requests
import psycopg2

def conect_datbase(json_db):
    try:
        cn = psycopg2.connect("dbname= "
                              +json_db['db']+
                              " user= "
                              +json_db['user']+
                              " host= "
                              +json_db['localhost']+
                              " password= "
                              +json_db['pass']+" ")
    except psycopg2.DatabaseError as de:
        if cn:
            cn.rollback()
            print('Error %s'%de)
    return cn

def queryField():
    #dictionary database
    databese_info = {
                 'localhost':'localhost',
                 'user':'postgres',
                 'pass':'',
                 'db':'pqr_electricaribe'
    }
    #query
    while True:
        cn = conect_datbase(databese_info)
        cur = cn.cursor()
        try:
            cur.execute('select * from businesscase where botstate is null')
            dt = cur.fetchall()
            if dt:
            	#Request Extractor field
                r = requests.get("http://localhost:5001/nltk/ef/")
                if r.status_code == 200:
                    print (r.text)
        except psycopg2.DatabaseError as de:
            print("don't worry, i continue->",de)
                    
        finally:
            if cn:
                cn.close()
    
