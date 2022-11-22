from datetime import time

class TeamGameDrive:
    def __init__(self):
        self.id = None
        self.drive_num = None
        self.quarter = None
        self.time_start = None
        self.yd_start = None
        self.num_plays = None
        self.drive_time = None
        self.net_yds = None
        self.drive_result = None
        self.team_game_id = None
        
    def getDriveNum(self):
        return self.drive_num
    
    def setDriveNum(self, num):
        self.drive_num = num
    
    def getDriveResult(self):
        return self.drive_result
    
    def setDriveResult(self, result):
        self.drive_result = result
    
    def getDriveTime(self):
        return self.drive_time
    
    def setDriveTime(self, time):
        self.drive_time = time
    
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
    
    def getNetYds(self):
        return self.net_yds
    
    def setNetYds(self, yds):
        self.net_yds = yds
    
    def getNumPlays(self):
        return self.num_plays
    
    def setNumPlays(self, num):
        self.num_plays= num
    
    def getQuarter(self):
        return self.quarter
    
    def setQuarter(self, quarter):
        self.quarter = quarter
    
    def getTeamGameId(self):
        return self.team_game_id
    
    def setTeamGameId(self, id):
        self.team_game_id = id
    
    def getTimeStart(self):
        return self.time_start
    
    def setTimeStart(self, time):
        self.time_start = time
    
    def getYdStart(self):
        return self.yd_start
    
    def setYdStart(self, start):
        self.yd_start = start
    
    def getInfo(self):
        info = {
            
        }
        
        return info
    