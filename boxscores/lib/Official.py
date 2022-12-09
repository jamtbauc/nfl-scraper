import json

class Official:
    def __init__(self, name):
        self.name = name
        self.career_start = None
        self.career_end = None
        self.jersey_num = None
        
    def getCareerEnd(self):
        return self.career_end
    
    def getCareerStart(self):
        return self.career_start
    
    def getJerseyNum(self):
        return self.jersey_num
    
    def getName(self):
        return self.name.strip()
    
    def setCareerEnd(self, end):
        self.career_end = end
        
    def setCareerStart(self, start):
        self.career_start = start
        
    def setName(self, name):
        self.name = name
        
    def setJerseyNum(self, num):
        self.jersey_num = num
        
    def getInfo(self):
        info = {
            "name": self.getName(),
            "career_start": self.getCareerStart(),
            "career_end": self.getCareerEnd(),
            "jersey_num": self.getJerseyNum()
        }
        
        return info