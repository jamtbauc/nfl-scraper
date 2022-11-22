from datetime import time

class PlayByPlay:
    def __init__(self):
        self.id = None
        self.qtr = None
        self.qtr_time_rem = None
        self.down = None
        self.yds_to_go = None
        self.yd_start = None
        self.score_away = None
        self.score_home = None
        self.detail = None
        self.exp_pts_before = None
        self.exp_pts_after = None
        self.seq = None
        self.game_id = None
        
    def getDetail(self):
        return self.detail
    
    def setDetail(self, detail):
        self.detail = detail
        
    def getDown(self):
        return self.down
    
    def setDown(self, down):
        self.down = down
    
    def getExpPointsAfter(self):
        return self.exp_pts_after
    
    def setExpPointsAfter(self, pts):
        self.exp_pts_after = pts
    
    def getExpPointsBefore(self):
        return self.exp_pts_before
    
    def setExpPointsBefore(self, pts):
        self.exp_pts_before = pts
    
    def getGameId(self):
        return self.id
    
    def setGameId(self, id):
        self.game_id = id
    
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
    
    def getQtr(self):
        return self.qtr
    
    def setQtr(self, qtr):
        self.qtr = qtr
    
    def getQtrTimeRem(self):
        return self.qtr_time_rem
    
    def setQtrTimeRem(self, time):
        self.qtr_time_rem = time
    
    def getScoreAway(self):
        return self.score_away
    
    def setScoreAway(self, score):
        self.score_away = score
    
    def getScoreHome(self):
        return self.score_home
    
    def setScoreHome(self, score):
        self.score_home = score
    
    def getSeq(self):
        return self.seq
    
    def setSeq(self, seq):
        self.seq = seq  
    
    def getYdStart(self):
        return self.yd_start
    
    def setYdStart(self, start):
        self.yd_start = start
    
    def getYdsToGo(self):
        return self.yds_to_go
    
    def setYdsToGo(self, yds):
        self.yds_to_go = yds
    
    def getInfo(self):
        info = {
            
        }
        
        return info
        