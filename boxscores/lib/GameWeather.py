import json

class GameWeather:
    def __init__(self, id, temp, humidity, wind, gameId):
        self.id = id
        self.temp = temp
        self.humidity = humidity
        self.wind = wind
        self.game_id = gameId
        
    def getId(self):
        return self.id
    
    def setId(self, value):
        if id:
            self.id = int(value)
        
    def getGameId(self):
        return self.game_id
    
    def setGameId(self, value):
        if value:
            self.game_id = str(value)
        
    def getHumidity(self):
        return self.humidity
    
    def setHumidity(self, value):
        try:
            self.humidity = int(value)
        except:
            self.humidity = 0
        
    def getTemp(self):
        return self.temp
    
    def setTemp(self, temp):
        try:
            self.temp = int(temp)
        except:
            self.temp = 0
        
    def getWind(self):
        return self.wind
    
    def setWind(self, value):
        try:
            self.wind = int(value)
        except:
            self.wind = 0
    
    def getInfo(self):
        info = {
            "id": self.getId(),
            "temp": self.getTemp(),
            "humidity": self.getHumidity(),
            "wind": self.getWind(),
            "gameId": self.getGameId()
        }
        
        return info
        