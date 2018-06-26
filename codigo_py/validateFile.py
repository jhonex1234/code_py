import os
import pandas as pd

with open('/home/tesla/Desktop/Tareas etiquetado/Audios Colpensiones/origin_text.txt','r') as file:
    fileOrigin = file.read()

filenames_original = [item.split('\t')[-1] for item in fileOrigin.split(',')]
filenames_assigned = {}

for filename in filenames_original:
    person_name = filename.split('/')[1]
    audio_name = filename.split('/')[-1]
    if person_name not in filenames_assigned:
        filenames_assigned[person_name] = [audio_name]
    else:
        filenames_assigned[person_name].append(audio_name)

def validateExistFileByTagger(dic):
    listFileNotFound = []
    for tagger in list(dic.keys()):
        dicNotFound = {"tagger":tagger,"filenotfound":""}
        for file in dic[tagger]:
            if file in os.listdir('/home/tesla/Desktop/Tareas etiquetado/Audios Colpensiones/{0}/Por etiquetar/'.format(tagger)):
                print('greate')
            elif file in os.listdir('/home/tesla/Desktop/Tareas etiquetado/Audios Colpensiones/{0}/Etiquetado/Buenos/'.format(tagger)):
                 print('regreate')
            elif file in os.listdir('/home/tesla/Desktop/Tareas etiquetado/Audios Colpensiones/{0}/Etiquetado/Malos/'.format(tagger)):
                 print('regreate')
            elif file in os.listdir('/home/tesla/Desktop/Tareas etiquetado/Audios Colpensiones/{0}/Etiquetado/Regular/'.format(tagger)):
                 print('regreate')
            #
            elif file in os.listdir('/home/tesla/Desktop/Tareas etiquetado/Audios Colpensiones/{0}/Etiquetado/Silencio/'.format(tagger)):
                 print('regreate')
            else:
                dicNotFound['filenotfound'] = file
                listFileNotFound.append(dicNotFound)
    return listFileNotFound
prueba = validateExistFileByTagger(filenames_assigned)
pd.DataFrame(prueba)