from datetime import datetime

class TeamGameDrive:
    def __init__(self, id, num):
        self.id = int(id)
        self.drive_num = int(num)
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
    
    def setDriveTime(self, value):
        self.drive_time = datetime.strptime(value,"%M:%S").time()
    
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
        self.team_game_id = int(id)
    
    def getTimeStart(self):
        return self.time_start
    
    def setTimeStart(self, value):
        self.time_start = datetime.strptime(value,"%M:%S").time()
    
    def getYdStart(self):
        return self.yd_start
    
    def setYdStart(self, start):
        self.yd_start = start
    
    def getInfo(self):
        info = {
            "id": self.getId(),
            "driveNum": self.getDriveNum(),
            "quarter": self.getQuarter(),
            "timeStart": self.getTimeStart(),
            "ydStart": self.getYdStart(),
            "numPlays": self.getNumPlays(),
            "driveTime": self.getDriveTime(),
            "netYds": self.getNetYds(),
            "driveResult": self.getDriveResult(),
            "teamGameId": self.getTeamGameId()
        }
        
        return info
    
    def mapToTeamGameDrive(self, label, value):
        if label == "quarter":
            self.setQuarter(value)
        elif label == "time_start":
            self.setTimeStart(value)
        elif label == "start_at":
            self.setYdStart(value)
        elif label == "play_count_tip":
            self.setNumPlays(value)
        elif label == "time_total":
            self.setDriveTime(value)
        elif label == "net_yds":
            self.setNetYds(value)
        elif label == "end_event":
            self.setDriveResult(value)
        else:
            print(f"Did not find label {label}")
    