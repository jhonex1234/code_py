import json
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

class editoreplate():
    def __init__(self,file):
        self.file = file
        self.loadJson(file)
        self.name = file
        
    #load template, into json ---
    def loadJson(self,rel_path):
        try:
            path = os.path.join(script_dir, "uploads/"+rel_path)
            self.file =  json.load(open(path,'r+'))
        except OSError:
            self.file = {}
        return self.file
    
    def editJson(self,keyvalue,selectkey,newdata):
        self.file.pop(selectkey)
        newdata = newdata.split('<>')
        self.file[keyvalue] = newdata
        
    def makeJsonData(self,keyvalue,newdata):
        newdata = newdata.split('<>')
        self.file[keyvalue] = newdata
  
    def deleteScript(self,keyvalue):
        self.file.pop(keyvalue)
       
    def makeJson(self,name):
        if(self.file != [] ):
            if(name != ''):
                file = name+'.json'
                self.name = name+'.json'
            else:
                file = self.name
        else:
            file = name+'.json'
            self.name = name+'.json'
         
        file = os.path.join(script_dir, "uploads/"+file)
        with open(file, 'w+', encoding='utf-8') as outfile:
             json.dump(self.file, outfile)
        return self.name
        
    def loadlistkey(self):
        return list(self.file.keys())
    
    def loadmjs(self,key):
        return self.file[key]
         