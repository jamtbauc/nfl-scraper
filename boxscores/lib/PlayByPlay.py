from datetime import datetime

class PlayByPlay:
    def __init__(self, id, seq, game_id):
        self.id = id
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
        self.seq = seq
        self.game_id = game_id
        
    def mapToPlayByPlay(self, label, value):
        if label == "quarter":
            self.setQtr(value)
        elif label == "qtr_time_remain":
            self.setQtrTimeRem(value)
        elif label == "down":
            self.setDown(value)
        elif label == "yds_to_go":
            self.setYdsToGo(value)
        elif label == "location":
            self.setYdStart(value)
        elif label == "pbp_score_aw":
            self.setScoreAway(value)
        elif label == "pbp_score_hm":
            self.setScoreHome(value)
        elif label == "detail":
            self.setDetail(value)
        elif label == "exp_pts_before":
            self.setExpPointsBefore(value)
        elif label == "exp_pts_after":
            self.setExpPointsAfter(value)
        else:
            print(f"Cannot map {label} for PlayByPlay")
        
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
        return self.game_id
    
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
    
    def setQtrTimeRem(self, value):
        if value:
            self.qtr_time_rem = datetime.strptime(value,"%M:%S").time()
        else:
            self.qtr_time_rem = value
    
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
            "id": self.getId(),
            "qtr": self.getQtr(),
            "qtr_time_rem": self.getQtrTimeRem(),
            "down": self.getDown(),
            "yds_to_go": self.getYdsToGo(),
            "yd_start": self.getYdStart(),
            "score_away": self.getScoreAway(),
            "score_home": self.getScoreHome(),
            "detail": self.getDetail(),
            "exp_pts_before": self.getExpPointsBefore(),
            "exp_pts_after": self.getExpPointsAfter(),
            "seq": self.getSeq(),
            "game_id": self.getGameId()
        }
        
        return info
        