#librerias
from glob import glob
import nltk 
from nltk import tokenize
from nltk.corpus import stopwords
# nombrando la libreria
import numpy as np
import pandas as pd
import re
from time import time
from unicodedata import normalize

#ruta1

filelist = glob('/home/jhon/proyectos/natural_language_processing/entes_de_control/resolucion_entes/entes_de_control_test/part1/*.txt')

#ruta 2

#filelist = glob('/home/jhon/proyectos/natural_language_processing/entes_de_control/resolucion_entes/*.txt')

#tupla
letters = []
for file in filelist:
    #apertura de todos los documentos que concuerden con la condicion
    with open(file, 'r') as txtfile: 
        letters.append((tokenize.word_tokenize(txtfile.read()), re.match('.*/(.*)-.*', file).group(1)))  
letters = pd.DataFrame(letters, columns=['Text', 'Name'])
letters = pd.DataFrame([(np.concatenate(letters[letters.Name == name].Text.values), name) 
                        for name in letters.Name.unique()], columns=['Text', 'Name'])
				    letters
def cleanDocs(letters):
    start = time()
    clean_letters = []
    for _, letter in letters.iterrows():
	#proceso de normalizacion
        words = [normalize('NFKD', word.lower()).encode('ascii', 'ignore').decode('utf-8') for word in letter['Text']]
        # is alphabetic character, not is a stopword, not is a custom word, has at least three letters, 
        # has at least one vowel, has at least one consonant
        words = [word for word in words if word not in stopwords.words('spanish')]
        clean_letters.append(' '.join(words))
	#impresion de tiempo de ejecucion
    print('Cleaning took %.2f seconds' % (time() - start))
    return pd.DataFrame(clean_letters)

dup = letters.insert(1, 'CleanText', cleanDocs(letters))
#seleccion de elemento en la tupla
letters.CleanText[letters.Name == 'userFile1498252121094'].values[0]

def context(target_word, tar_passage, left_margin = 10, right_margin = 10):
    tokens = tokenize.word_tokenize(tar_passage)
    text = nltk.Text(tokens)
    c = nltk.ConcordanceIndex(text.tokens, key = lambda s: s.lower())
    concordance_txt = [text.tokens[offset - left_margin : offset + right_margin]
                       for offset in c.offsets(target_word)]
    return [''.join([x + ' ' for x in con_sub]) for con_sub in concordance_txt]
cleanText = re.sub('[^\w\s]', '', letters[letters.Name == 'userFile1498252121094'].CleanText.values[0])
val1=re.findall('(\d{16})', cleanText)
val2=re.findall('sspd\s*(\d{14})', cleanText)
numero=set(re.findall('\s(\d{14})\s', cleanText))
val3=set(numero)-set(val2)

#print(set(re.findall('re\s*(\d{13})', cleanText)))
print(val1)
print(val2)
print(val3)


resoluciones = ['requerir', 'apertura de investigacion', 'sancion', 'archivar', 'confirmar', 'revocar', 
                'rechazar', 'tramitar', 'improcedente', 'rechazo', 'procedente', 'modificar', 'inhibirse', 
                'no acceder', 'corregir', 'aclarar']
for resolucion in resoluciones:
    coincidence = re.findall(resolucion + ' ', cleanText)
    if coincidence:
        print(coincidence)
    #elif coincidence !=0:
     #   print("no coincidence")
        
results = context('modificar', cleanText, 0, 10)
for result in results:
    print(result)

print(cleanText)

