import json

class OfficialGame:
    def __init__(self, id, off_id, gm_id, pos):
        self.id = id
        self.ref_position = pos
        self.official_id = off_id
        self.game_id = gm_id
        
    def getGameId(self):
        return self.game_id
    
    def getId(self):
        return self.id
    
    def getOfficialId(self):
        return self.official_id
    
    def getRefPosition(self):
        return self.ref_position
    
    def setGameId(self, id):
        self.game_id = id
        
    def setId(self, value):
        try:
            self.id = int(value)
        except:
            self.id = None
        
    def setOfficialId(self, id):
        self.official_id = id
        
    def setRefPosition(self, pos):
        self.ref_position = pos
        
    def getInfo(self):
        info = {
            "id": self.getId(),
            "ref_position": self.getRefPosition(),
            "official_id": self.getOfficialId(),
            "game_id": self.getGameId()
        }
        
        return info