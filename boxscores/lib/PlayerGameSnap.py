import re

class PlayerGameSnap:
    def __init__(self, id, player_gm_id):
        self.id = id
        self.player_gm_id = player_gm_id
        self.start_pos = None
        self.off_snaps = None
        self.off_snap_pct = None
        self.def_snaps = None
        self.def_snap_pct = None
        self.st_snaps = None
        self.st_snap_pct = None
        
    def getDefSnapPct(self):
        return self.def_snap_pct
    
    def setDefSnapPct(self, value):
        temp = re.findall('[0-9]+', value)
        self.def_snap_pct = float(temp[0])
    
    def getDefSnaps(self):
        return self.def_snaps
    
    def setDefSnaps(self, value):
        self.def_snaps = int(value)
    
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
    
    def getOffSnapPct(self):
        return self.off_snap_pct
    
    def setOffSnapPct(self, value):
        temp = re.findall('[0-9]+', value)
        self.off_snap_pct = float(temp[0])
    
    def getOffSnaps(self):
        return self.off_snaps
    
    def setOffSnaps(self, value):
        self.off_snaps = int(value)

    def getPlayerGameId(self):
        return self.player_gm_id

    def setPlayerGameId(self, value):
        self.player_gm_id = value
    
    def getStSnapPct(self):
        return self.st_snap_pct
    
    def setStSnapPct(self, value):
        temp = re.findall('[0-9]+', value)
        self.st_snap_pct = float(temp[0])
    
    def getStSnaps(self):
        return self.st_snaps
    
    def setStSnaps(self, value):
        self.st_snaps = int(value)
    
    def getStartPos(self):
        return self.start_pos
    
    def setStartPos(self, value):
        self.start_pos = value

    def mapToPlayerGmSnap(self, label, value):
        if label == "pos":
            self.setStartPos(value)
        elif label == "offense":
            self.setOffSnaps(value)
        elif label == "off_pct":
            self.setOffSnapPct(value)
        elif label == "defense":
            self.setDefSnaps(value)
        elif label == "def_pct":
            self.setDefSnapPct(value)
        elif label == "special_teams":
            self.setStSnaps(value)
        elif label == "st_pct":
            self.setStSnapPct(value)
        else:
            print(f"Could not set {label} to {value} for playerGmSnap ID: {self.getId()}")
        
    def getInfo(self):
        info = {
            "id": self.getId(),
            "playerGmId": self.getPlayerGameId(),
            "startPos": self.getStartPos(),
            "offSnaps": self.getOffSnaps(),
            "offSnapPct": self.getOffSnapPct(),
            "defSnaps": self.getDefSnaps(),
            "defSnapPct": self.getDefSnapPct(),
            "stSnaps": self.getStSnaps(),
            "stSnapPct": self.getStSnapPct()
        }
        
        return info