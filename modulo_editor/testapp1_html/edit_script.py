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
    
    def editJson(self,keyvalue,newdata):
        self.file[keyvalue] = newdata
        return self.file[keyvalue]

    def makeJsonData(self,keyvalue,newdata):
        self.file[keyvalue] = newdata
  
    def deleteScript(self,keyvalue):
        return self.file.pop(keyvalue)
       
    def makeJson(self,name):
        if(self.name != '' ):
            self.name = self.name
        else:
            self.name = name+'.json'
        file = os.path.join(script_dir, "uploads/"+self.name)
        with open(file, 'w+') as outfile:
             json.dump(self.file, outfile)
        return self.name
        
    def loadlistkey(self):
        return list(self.file.keys())
    
    def loadmjs(self,key):
        return self.file[key]
         