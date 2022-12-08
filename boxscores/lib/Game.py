from datetime import datetime

class Game:
    def __init__(self, date, week, away_abbrev, home_abbrev):
        if isinstance(date, datetime):
            self.date = date
        else:
            self.setDate(date)

        # Set game season
        date = self.date.date()
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
        self.week = week
        self.attendance = None
        self.stadium_id = None
        self.game_duration = None
        self.roof_type = None
        
    # GETTERS AND SETTERS   
    def getAttendance(self):
        return self.attendance
    
    def setAttendance(self, value):
        if value != '':
            self.attendance = int(value)
        else:
            self.attendance = 0
        
    def getDate(self):
        return self.date
    
    def setDate(self, value):
        try:
            self.date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except:
            self.date = datetime.strptime("1900-01-01T0:00:00", "%Y-%m-%dT%H:%M:%S")
        
    def getGameDuration(self):
        if self.game_duration:
            return self.game_duration
        else:
            return 0
    
    def setGameDuration(self, value):
        duration = None

        if isinstance(value, str):
            duration = datetime.strptime(value, "%H:%M:%S")
        else:
            duration = value

        # hours to minutes
        h_t_m = duration.hour * 60
        # sum minutes
        mins = h_t_m + duration.minute
        # minutes to seconds
        m_t_s = mins * 60
        # sum seconds
        secs = m_t_s + duration.second

        self.game_duration = secs

    
    def getId(self):
        return self.id
    
    def setId(self, value):
        if value:
            self.id = value
        else:
            self.id = '99990011YYYZZZ'
    
    def getSeason(self):
        return self.season
    
    def setSeason(self, value):
        try:
            self.season = int(value)
        except:
            self.season = 9999

    def getStadiumId(self):
        return self.stadium_id
    
    def setStadiumId(self, value):
        if isinstance(value, str):
            self.stadium_id = value
        else:
            self.stadium_id = "N/A"
    
    def getWeek(self):
        return self.week
        
    def setWeek(self, value):
        if isinstance(value, str):
            self.week = value
        else:
            self.week = str(value)
        
    def getRoofType(self):
        return self.roof_type
    
    def setRoofType(self, value):
        if isinstance(value, str):
            self.roof_type = value
        else:
            self.roof_type = "N/A"
    
    # OUTPUT FUNCTIONS
    def getInfo(self):
        info = {
            "id": self.getId(),
            "date": self.getDate().isoformat(),
            "season": self.getSeason(),
            "week": self.getWeek(),
            "attendance": self.getAttendance(),
            "stadiumId": self.getStadiumId(),
            "gameDuration": self.getGameDuration(),
            "roofType": self.getRoofType()  
        }
        
        return info