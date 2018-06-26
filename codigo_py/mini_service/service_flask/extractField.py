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
            val_sspd = set(re.findall('\s*sspd\s*(\d{14})\s', cleanText))
            #date sspd
            val_sspd_fe = set(re.findall('sspd\s*\d{14}\s*\s*(\d*)\s*', cleanText))
            #expedient
            val_expedient = set(re.findall('\s(\d*\e)\s', cleanText))  
            #expedient father
            val_expedient_father = set(re.findall('radicado\spadre\s(\d{14})\s', cleanText))
            #number solve of decision 
            val_solve_decision = re.findall('\s*resuelve\s*articulo\s*(primero|1)\s*\w*\s*decision\s*(administrativa|empresarial| )\s*(no|n0| )(\d*)\s', cleanText)
            #date decision
            val_decision_fe = re.findall('\s*resuelve\s*articulo\s*(primero|1)\s*\w*\s*decision\s*(administrativa|empresarial| )\s*(no|n0| )\d{7}(\s*\d*\s\w*\s\d*\s\d*)', cleanText)
            # number_RE
            val_number_re = set(re.findall('\s*(re\d*)\s', cleanText)) 
            # RE_date
            val_re_fe = re.findall('(no|n0| )\s*re\d*\s(\d{2}\s\w*\s\d{4})',cleanText)
            
            #validation
            
            val_number_re = list(val_number_re) + [('', '', '')] + [('', '', '')] + [('', '', '')]
            if val_number_re[0] !=  ('', '', '') and val_number_re[0] != '' and val_number_re[0] != 're':
                  val_number_re = val_number_re[0]
            elif val_number_re[1] !=  ('', '', '') and val_number_re[1] != '' and val_number_re[1] != 're':
                val_number_re = val_number_re[1]
            elif val_number_re[2] !=  ('', '', '')  and val_number_re[2] != '' and val_number_re[2] != 're':
                val_number_re = val_number_re[2]
            else:
                val_number_re = ''
            
            val_re_fe = list(val_re_fe) + [('', '','')] 
            if val_re_fe != [('', '','')]:
                val_re_fe = val_re_fe[0][1] 
            else:
                val_re_fe = ''
                
            val_solve_decision = list(val_solve_decision) + [('', '', '', '')]
            if val_solve_decision != [('', '', '', '')]:
                val_solve_decision = list(val_solve_decision)[0][3]
            else:
                val_solve_decision = ''
            
            val_decision_fe = val_decision_fe + [(' ', ' ', ' ', ' ')]
            if val_decision_fe != [('', '', '', '')]:
                val_decision_fe = list(val_decision_fe)[0][3]
            else:
                val_decision_fe = ''
            
            search_result = list(search_result)+[('')] + [('','')]
            if search_result !=  [('','')]:
                search_result = search_result[0][1]
            else:
                search_result = ''
            
            val_sspd_fe = list(val_sspd_fe)+[('','')]+[('','')]
            if val_sspd_fe[0] != ('',''):
                val_sspd_fe = val_sspd_fe[0]
            else:
                val_sspd_fe = ''
                
            val_expedient_father = list(val_expedient_father)+[('')]
            if val_expedient_father[0] != '':
                val_expedient_father = val_expedient_father[0]
            else:
                val_expedient_father = ''
            val_sspd = list(val_sspd)+[('','')]
            if val_sspd[0] != ('',''):
                val_sspd=val_sspd[0]
            else:
                val_sspd = ''
            
            dc = {'resolucion':search_result,
                          'sspd' : val_sspd,
                          'sspd_fecha' : val_sspd_fe,
                          'expediente_padre' : val_expedient_father, 
                          'num_decision':val_solve_decision,
                          'date_decision' :val_decision_fe,
                          'radication_RE':val_number_re,
                          'date_radication_re':val_re_fe}
            
            objDataBase = TypeDataBase(self.database)
            id_json = objDataBase.serch_id(dc)
            objDataBase.update_casoentescontrol(id_json)
            if dc['id'] != 'none':
                list_doc.append(dc)
        
        print(list_doc)
        return list_doc
    