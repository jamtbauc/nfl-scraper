from datetime import date

class Player:
    def __init__(self):
        self.id = None
        self.name = None
        self.college = None
        self.dob = None
        self.career_start = None
        self.career_end = None
    
    def getCareerEnd(self):
        return self.career_end
    
    def getCareerStart(self):
        return self.career_start
    
    def getCollege(self):
        return self.college
    
    def getDOB(self):
        return self.dob
        
    def getId(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def setCareerEnd(self, end):
        self.career_end = end
        
    def setCareerStart(self, start):
        self.career_start = start
        
    def setCollege(self, college):
        self.college = college
        
    def setDOB(self, dob):
        self.dob = dob
        
    def setId(self, id):
        self.id = id
        
    def setName(self, name):
        self.name = name
    
    