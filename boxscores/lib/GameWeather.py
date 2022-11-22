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
    
    def setId(self, id):
        self.id = id
        
    def getGameId(self):
        return self.game_id
    
    def setGameId(self, id):
        self.game_id = id
        
    def getHumidity(self):
        return self.humidity
    
    def setHumidity(self, humidity):
        self.humidity = humidity
        
    def getTemp(self):
        return self.temp
    
    def setTemp(self, temp):
        self.temp = temp
        
    def getWind(self):
        return self.wind
    
    def setWind(self, wind):
        self.wind = wind
    
    def getInfo(self):
        info = {
            "id": self.getId(),
            "temp": self.getTemp(),
            "humidity": self.getHumidity(),
            "wind": self.getWind(),
            "gameId": self.getGameId()
        }
        
        return info
        