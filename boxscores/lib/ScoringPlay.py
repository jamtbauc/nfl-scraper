from datetime import time
import json

class ScoringPlay:
    def __init__(self, id):
        self.id = id
        self.home_score = None
        self.scoring_team_id = None
        self.away_score = None
        self.qtr = None
        self.qtr_time_rem = None
        self.description = None
        
    def getAwayScore(self):
        return self.away_score
    
    def setAwayScore(self, score):
        self.away_score = score
        
    def getDescription(self):
        return self.description
    
    def setDescription(self, descr):
        self.description = descr
        
    def getHomeScore(self):
        return self.home_score
    
    def setHomeScore(self, score):
        self.home_score = score
        
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
        
    def getScoringTeamId(self):
        return self.scoring_team_id
    
    def setScoringTeamId(self, id):
        self.scoring_team_id = id
        
    def getInfo(self):
        info = {
            "id": self.getId(),
            "scoring_team_id": self.getScoringTeamId(),
            "home_score": self.getHomeScore(),
            "away_score": self.getAwayScore(),
            "qtr": self.getQtr(),
            "qtr_time_rem": self.getQtrTimeRem().isoformat(),
            "description": self.getDescription()
        }
        
        return info
        