class PlayerGameSnap:
    def __init__(self):
        self.id = None
        self.start_pos = None
        self.off_snaps = None
        self.off_snap_pct = None
        self.def_snaps = None
        self.def_snap_pct = None
        self.st_snaps = None
        self.st_snap_pct = None
        
    def getDefSnapPct(self):
        return self.def_snap_pct
    
    def setDefSnapPct(self, pct):
        self.def_snap_pct = pct
    
    def getDefSnaps(self):
        return self.def_snaps
    
    def setDefSnaps(self, snaps):
        self.def_snaps = snaps
    
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id - id
    
    def getOffSnapPct(self):
        return self.off_snap_pct
    
    def setOffSnapPct(self, pct):
        self.off_snap_pct = pct
    
    def getOffSnaps(self):
        return self.off_snaps
    
    def setOffSnaps(self, snaps):
        self.off_snaps = snaps
    
    def getStSnapPct(self):
        return self.st_snap_pct
    
    def setStSnapPct(self, pct):
        self.st_snap_pct = pct
    
    def getStSnaps(self):
        return self.st_snaps
    
    def setStSnaps(self, snaps):
        self.st_snaps = snaps
    
    def getStartPos(self):
        return self.start_pos
    
    def setStartPos(self, pos):
        self.start_pos = pos