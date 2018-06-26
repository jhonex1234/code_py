import json
#read json file, return list
def loadJson(file):
    try:
        file = json.load(open(file))
    except FileNotFoundError:
        file = []
    return file

#make json file, with list 
def makeJson(data,name):
    file = name+'.json'
    with open(file, 'w') as outfile:
         json.dump(data, outfile)

#find index, method soport ---
def findIndex(listdata,keyvalue):
    index = []
    try:
        if (listdata != []):
               for i in range(0,len(listdata)):
                    if(listdata[i]['id'] == keyvalue):
                        index = listdata.index(listdata[i])
        else:
            index = 1
    except UnboundLocalError:
        index = 1
    return index

## edit dictionary list
def editJson(listdata,keyvalue,newdata):
    if(listdata != []):
        for i in range(0,len(listdata)):
            if(listdata[i]['id'] == keyvalue):
                listdata.remove(listdata[i])
                listdata.append({'id':keyvalue,'length':len(newdata),'message':newdata})
    else:
        listdata = 'seleccione una llave'
    return listdata

#delete keyvalues and
def deleteScript(listdata,keyvalue):
    if (listdata != [] and keyvalue != ''):    
        listdata.remove(listdata[findIndex(listdata,keyvalue)])
    else:
        listdata = 'seleccione una llave'
    return listdata

#create template
def makeJsonData(listdata,keyvalue,newdata):
    if (listdata != []):
        a = findIndex(listdata,keyvalue)
        if(a != [''] and a != 1):
            listdata.append({'id':keyvalue,'length':len(newdata),'message':newdata})
    else:
        listdata.append({'id':keyvalue,'length':len(newdata),'message':newdata})
    return listdata

#create list keys
def loadlistkey(listjson):
    listkeys = []
    for i in range(0,len(read_json)):
         listkeys.append(read_json[i]['id'])
    return listkeys