# -*- coding: utf-8 -*-
from glob import glob
import nltk 
from nltk import tokenize
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import re
from time import time
from unicodedata import normalize
from typeDataBase import TypeDataBase
pd.set_option('display.max_colwidth',-1)


class extractField():

    def __init__(self,filelist,json_database):
        self.filelist = glob(filelist+'*.txt')
        self.database = json_database
        
    def organizeDocs(self):
        letters = []
        if self.filelist:
            for file in self.filelist:
                #apertura de todos los documentos que concuerden con la condicion
                with open(file, 'r') as txtfile:
                    letters.append((tokenize.word_tokenize(txtfile.read()), re.match('.*/(.*)-.*', file).group(1)))  
            letters = pd.DataFrame(letters, columns=['Text', 'Name'])
            letters = pd.DataFrame([(np.concatenate(letters[letters.Name == name].Text.values), name) 
                                    for name in letters.Name.unique()], columns=['Text', 'Name'])
            self.filelist = letters
        else:
            print('not found file txt')
        return self.filelist
    
    def cleanDocs(self):
        start = time()
        clean_letters = []
        letters = self.filelist   
        try:
            for _, letter in letters.iterrows():
            #proceso de normalizacion
                words = [normalize('NFKD', word.lower()).encode('ascii', 'ignore').decode('utf-8')
                         for word in letter['Text']]
                # is alphabetic character, not is a stopword, not is a custom word, has at least three letters, 
                # has at least one vowel, has at least one consonant
                words = [word for word in words if word not in stopwords.words('spanish')]
                clean_letters.append(' '.join(words))
            #impresion de tiempo de ejecucion
            print('Cleaning took %.2f seconds' % (time() - start))
            clean_letters = pd.DataFrame(clean_letters)
            self.filelist.insert(1,'CleanText', clean_letters)
        except ValueError and AttributeError:
            print('verify route')
            
        return self.filelist
        
    def extractFields(self):
        nom_ar=0
        list_doc=[]
        letters = self.filelist
        while (nom_ar<=(len(letters)-1)):
            cleanText = re.sub('[^\w\s]', '', letters[letters.Name == letters['Name'][nom_ar]].CleanText.values[0])
            nom_ar=nom_ar+1

            search_result  = re.findall('\s*resuelve\s*articulo\s*(primero|1)\s*(\w*)', cleanText)
            # number sspd
            val_sspd = set(re.findall('\s*sspd\s(\d{14})\s', cleanText))
            #date sspd
            val_sspd_fe = set(re.findall('sspd\s*\d*\sfecha\s*(\d*\S*|\d)', cleanText))
            #expedient
            val_expedient = set(re.findall('\s(\d*\e)\s', cleanText))  
            #expedient father
            val_expedient_father = set(re.findall('radicado\spadre\s(\d{14})\s+|$', cleanText))
            #number solve of decision 
            val_solve_decision = re.findall('\s*resuelve\s*articulo\s*(primero|1)\s*\w*\s*decision\s*(administrativa| )\s*(no|n0| )(\d*)\s+|$', cleanText)
            #date decision
            val_decision_fe = re.findall('\s*resuelve\s*articulo\s*(primero|1)\s*\w*\s*decision\s*(administrativa| )\s*(no|n0| )\d{7}(\s*\d*\s\w*\s\d*\s\d*)+|$', cleanText)
            # number_RE
            val_number_re = set(re.findall('(no|n0| )\s*(re\d*)\s+|$', cleanText)) 
            # RE_date
            val_re_fe = re.findall('(no|n0| )\s*re\d*\s(\d{2}\s\w*\s\d{4})+|$',cleanText)
 
            if list(val_number_re) != [('', '')]:
                if list(val_number_re)[1][1] != '':
                    val_number_re = list(val_number_re)[1][1]
                elif list(val_number_re)[0][1] != '':
                    val_number_re = list(val_number_re)[0][1]
            else:
                val_number_re = list(val_number_re)[0][0]

            dc = {'resolucion':search_result[0][1],
                          'sspd' : list(val_sspd)[0],
                          'sspd_fecha' : list(val_sspd_fe)[0],
                          'expediente_padre' : list(val_expedient_father)[1], 
                          'num_decision':list(val_solve_decision)[0][3],
                          'date_decision' :list(val_decision_fe)[0][3],
                          'radication_RE':val_number_re,
                          'date_radication_re':list(val_re_fe)[0][1]}
            
            objDataBase = TypeDataBase(self.database)
            id_json = objDataBase.serch_id(dc)
            objDataBase.update_casoentescontrol(id_json)
            list_doc.append(dc)
    #add the list_doc to attribute of class     
        #letters.insert(1, 'dictionaryDoc', list_doc)
       # self.filelist = letters
        print(list_doc)
        return list_doc
    