class Team:
    
    team_info = {
        "Arizona Cardinals": ["ARI", "Arizona", "Cardinals"],
        "Atlanta Falcons": ["ATL", "Atlanta", "Falcons"],
        "Baltimore Ravens": ["BAL", "Baltimore", "Ravens"],
        "Buffalo Bills": ["BUF", "Buffalo", "Bills"],
        "Carolina Panthers": ["CAR", "Carolina", "Panthers"],
        "Chicago Bears": ["CHI", "Chicago", "Bears"],
        "Cincinnati Bengals": ["CIN", "Cincinnati", "Bengals"],
        "Cleveland Browns": ["CLE", "Cleveland", "Browns"],
        "Dallas Cowboys": ["DAL", "Dallas", "Cowboys"],
        "Denver Broncos": ["DEN", "Denver", "Broncos"],
        "Detroit Lions": ["DET", "Detroit", "Lions"],
        "Green Bay Packers": ["GNB", "Green Bay", "Packers"],
        "Houston Texans": ["HOU", "Houston", "Texans"],
        "Indianapolis Colts": ["IND", "Indianapolis", "Colts"],
        "Jacksonville Jaguars": ["JAX", "Jacksonville", "Jaguars"],
        "Kansas City Chiefs": ["KAN", "Kansas City", "Chiefs"],
        "Los Angeles Chargers": ["LAC", "Los Angeles", "Chargers"],
        "Los Angeles Rams": ["LAR", "Los Angeles", "Rams"],
        "Las Vegas Raiders": ["LVR", "Las Vegas", "Raiders"],
        "Miami Dolphins": ["MIA", "Miami", "Dolphins"],
        "Minnesota Vikings": ["MIN", "Minnesota", "Vikings"],
        "New Orleans Saints": ["NOR", "New Orleans", "Saints"],
        "New England Patriots": ["NWE", "New England", "Patriots"],
        "New York Giants": ["NYG", "New York", "Giants"],
        "New York Jets": ["NYJ", "New York", "Jets"],
        "Oakland Raiders": ["OAK", "Oakland", "Raiders"],
        "Philadelphia Eagles": ["PHI", "Philadelphia", "Eagles"],
        "Pittsburgh Steelers": ["PIT", "Pittsburgh", "Steelers"],
        "San Diego Chargers": ["SDG", "San Diego", "Chargers"],
        "San Francisco 49ers": ["SFO", "San Francisco", "49ers"],
        "Seattle Seahawks": ["SEA", "Seattle", "Seahawks"],
        "St. Louis Rams": ["STL", "St. Louis", "Rams"],
        "Tampa Bay Buccaneers": ["TAM", "Tampa Bay", "Buccaneers"],
        "Tennessee Titans": ["TEN", "Tennessee", "Titans"],
        "Washington Redskins": ["WAS", "Washington", "Redskins"],
        "Washington Football Team": ["WAS", "Washington", "Football Team"],
        "Washington Commanders": ["WAS", "Washington", "Commanders"],
    }
    
    def __init__(self, name):
        self.name = name
        self.locale = self.team_info[name][1]
        self.mascot = self.team_info[name][2]
        self.abbrev_pff = self.team_info[name][0]
    
    def getAbbrevPff(self):
        return self.abbrev_pff 
     
    def getLocale(self):
        return self.locale
    
    def getMascot(self):
        return self.mascot
        
    def getName(self):
        return self.name
    
    def setAbbrevPff(self, abbrev):
        self.abbrev_pff = abbrev
        
    def setLocale(self, locale):
        self.locale = locale
        
    def setMascot(self, mascot):
        self.mascot = mascot
    
    def setName(self, name):
        self.name = name
    