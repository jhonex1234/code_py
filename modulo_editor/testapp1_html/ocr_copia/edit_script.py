import json

class editoreplate():
    def __init__(self,file):
        self.file = file
        self.loadJson(file)
        self.findIndex('')
        self.name = file
        
    #load template, into json ---
    def loadJson(self,file):
        try:
            self.file = json.load(open(file))
        except FileNotFoundError as fn:
            self.file = []
            print('error en la carga del archivo',fn)
        return self.file
    
    #find index, method soport ---
    def findIndex(self,keyvalue):
        index = []
        try:
            if (self.file != []):
                   for i in range(0,len(self.file)):
                        if(self.file[i]['id'] == keyvalue):
                            index = self.file.index(self.file[i])
            
        except UnboundLocalError:
            index = ['error']
        return index
    
    ## edit dictionary list
    def editJson(self,keyvalue,newdata):
        if(self.file != []):
            answer = ''
            for i in range(0,len(self.file)):
                if(self.file[i]['id'] == keyvalue):
                    self.file.remove(self.file[i])
                    self.file.append({'id':keyvalue,'length':len(newdata),'message':newdata})
        else:
            answer = 'seleccione una llave'
        return answer
  
    #delete keyvalues and
    def deleteScript(self,keyvalue):
        answer = ''
        if (self.file != [] and keyvalue != ''):
                a = self.findIndex(keyvalue)
                if(a != []):
                    answer = ''
                    self.file.remove(self.file[self.findIndex(keyvalue)])
        else:
            answer = 'seleccione una llave'
        return answer
    
    #create template
    def makeJsonData(self,keyvalue,newdata):
        answer = ''
        if (self.file != []):
            a = self.findIndex(keyvalue)
            if(a == []):
                self.file.append({'id':keyvalue,'length':len(newdata),'message':newdata})
            answer = ''
        else:
            self.file.append({'id':keyvalue,'length':len(newdata),'message':newdata}) 
            answer = 'Template Creado'
        return answer
    
    #make json file, with list 
    def makeJson(self,name):
        if(name == ''):
            answer = 'Creado'
            name = self.name
        else:
            answer = 'Guardado'
        file = name+'.json'
        with open(file, 'w') as outfile:
             json.dump(self.file, outfile)
        return answer
        

    #create list keys load
    def loadlistkey(self):
        listkeys = []
        
        for i in range(0,len(self.file)):
             listkeys.append(self.file[i]['id'])
        return listkeys
    

    #create list keys load
    def loadmjs(self,key):
        msjtem = ''
        
        for i in range(0,len(self.file)):
             if(key == self.file[i]['id']):
                msjtem = self.file[i]['message']
        return msjtem