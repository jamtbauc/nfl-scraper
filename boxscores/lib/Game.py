from datetime import datetime

class Game:
    def __init__(self, date, week, away_abbrev, home_abbrev):
        # Set game season
        date = date.date()
        month = date.month
        year = date.year
        if month < 9:
            self.season = year - 1
        else:
            self.season = year
            
        # Create date string for id
        date_str = date.strftime('%Y%m%d')
        
        self.id = date_str + away_abbrev + home_abbrev
        self.date = date
        self.season = None
        self.week = week
        self.attendance = None
        self.stadium_id = None
        self.game_duration = None
        self.roof_type = None
        
    # GETTERS AND SETTERS   
    def getAttendance(self):
        return self.attendance
    
    def setAttendance(self, attendance):
        self.attendance = attendance
        
    def getDate(self):
        return self.date
    
    def setDate(self, date):
        self.date = date
        
    def getGameDuration(self):
        if self.game_duration:
            return self.game_duration
        else:
            return datetime.strptime(0, "%S")
    
    def setGameDuration(self, value):
        self.game_duration = value
    
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
    
    def getSeason(self):
        return self.season
    
    def setSeason(self, date):
        month = date.month
    
    def getStadiumId(self):
        return self.stadium_id
    
    def setStadiumId(self, id):
        self.stadium_id = id
    
    def getWeek(self):
        return self.week
        
    def setWeek(self, week):
        self.week = week
        
    def getRoofType(self):
        return self.roof_type
    
    def setRoofType(self, value):
        self.roof_type = value
    
    # OUTPUT FUNCTIONS
    def getInfo(self):
        info = {
            "id": self.getId(),
            "date": self.getDate().isoformat(),
            "season": self.getSeason(),
            "week": self.getWeek(),
            "attendance": self.getAttendance(),
            "stadiumId": self.getStadiumId(),
            "gameDuration": self.getGameDuration().isoformat(),
            "roofType": self.getRoofType()  
        }
        
        return info