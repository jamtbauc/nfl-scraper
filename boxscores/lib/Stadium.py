import json

class Stadium:
    def __init__(self, name):
        self.name = name
        self.city = None
        self.state = None
        self.surface = None
        self.roof = None
        
    def getCity(self):
        return self.city
    
    def getName(self):
        return self.name
    
    def getRoof(self):
        return self.roof
    
    def getState(self):
        return self.state
    
    def getSurface(self):
        return self.surface
    
    def setCity(self, city):
        self.city = city
        
    def setName(self, name):
        self.name = name
        
    def setRoof(self, roof):
        self.roof = roof
        
    def setState(self, state):
        self.state = state
        
    def setSurface(self, surface):
        self.surface = surface
        
    def getInfo(self):
        info = {
            "name": self.getName(),
            "city": self.getCity(),
            "state": self.getState(),
            "surface": self.getSurface(),
            "roof": self.getRoof()
        }
        
        return info