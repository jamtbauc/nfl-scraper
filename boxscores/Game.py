from datetime import datetime
from Player import Player

class Game:
    ### dictionary with abbrev as key and corresponding team as the value
    abbrevs = {
        "ARI": "Arizona Cardinals",
        "ATL": "Atlanta Falcons",
        "BAL": "Baltimore Ravens",
        "BUF": "Buffalo Bills",
        "CAR": "Carolina Panthers",
        "CHI": "Chicago Bears",
        "CIN": "Cincinnati Bengals",
        "CLE": "Cleveland Browns",
        "DAL": "Dallas Cowboys",
        "DEN": "Denver Broncos",
        "DET": "Detroit Lions",
        "GNB": "Green Bay Packers",
        "HOU": "Houston Texans",
        "IND": "Indianapolis Colts",
        "JAX": "Jacksonville Jaguars",
        "KAN": "Kansas City Chiefs",
        "LAC": "Los Angeles Chargers",
        "LAR": "Los Angeles Rams",
        "LVR": "Las Vegas Raiders",
        "MIA": "Miami Dolphins",
        "MIN": "Minnesota Vikings",
        "NOR": "New Orleans Saints",
        "NWE": "New England Patriots",
        "NYG": "New York Giants",
        "NYJ": "New York Jets",
        "PHI": "Philadelphia Eagles",
        "PIT": "Pittsburgh Steelers",
        "SEA": "Seattle Seahawks",
        "SFO": "San Francisco 49ers",
        "TAM": "Tampa Bay Buccaneers",
        "TEN": "Tennessee Titans",
        #### WASHINGTON NAME LIST
        "WAS": {2021: "Washington Football Team", 2022: "Washington Commanders"}
    }
    
    def __init__(self, away, home, date):
        self.__attendance = ""
        self.__away = away
        self.__away_coach = ""
        self.__away_def_players = []
        self.__away_off_players = []
        self.__away_score = -1
        self.__away_starters = {}
        self.__date = date
        self.__home = home
        self.__home_coach = ""
        self.__home_def_players = []
        self.__home_off_players = []
        self.__home_score = -1
        self.__home_starters = {}
        self.__officials = {}
        self.__stadium = ""
        
    ### SETTER METHODS SORTED ALPHABETICALLY
    def set_away_coach(self, coach):
        self.__away_coach = coach
           
    def set_away_score(self, score):
        self.__away_score = score
        
    def set_home_coach(self, coach):
        self.__home_coach = coach
        
    def set_home_score(self, score):
        self.__home_score = score
       
    ### GETTER METHODS SORTED ALPHABETICALLY
    def get_attendance(self):
        return self.__attendance
    
    def get_away(self):
        return self.__away
    
    def get_away_coach(self):
        return self.__away_coach
    
    def get_away_score(self):
        return self.__away_score
    
    def get_date(self):
        return self.__date
    
    def get_home(self):
        return self.__home
    
    def get_home_coach(self):
        return self.__home_coach
    
    def get_home_score(self):
        return self.__home_score
    
    def get_stadium(self):
        return self.__stadium
    
    ### HELPER METHODS  
    ##### PRIVATE HELPERS
    def __add_off_player(self, player):
        abbrev = player.get_team()
        
        if abbrev != "":
            if abbrev in self.abbrevs:
                team = self.abbrevs[abbrev]
                
                if team == self.__home:
                    self.__home_off_players.append(player)
                elif team == self.__away:
                    self.__away_off_players.append(player)
                    
    def __add_def_player(self, player):
        abbrev = player.get_team()
        
        if abbrev != "":
            if abbrev in self.abbrevs:
                team = self.abbrevs[abbrev]
                
                if team == self.__home:
                    self.__home_def_players.append(player)
                elif team == self.__away:
                    self.__away_def_players.append(player)
        
    def __extract_time(self, time_str):
        am_pm = time_str[-2:]
        if am_pm == "am":
            am_pm = "AM"
        else:
            am_pm = "PM"
            
        time_str = time_str[:-2] + am_pm
        
        date_str = self.__date.strftime("%B %m, %Y")
        date_str += " " + time_str
        
        self.__date = self.__date.strptime(date_str, "%B %m, %Y %I:%M%p")
    
    ##### PUBLIC HELPERS  
    def extract_coaches(self, coaches):
        for c in coaches:
            coach = c.text[7:]
            if self.__home_coach == "":
                self.__home_coach = coach
            else:
                self.__away_coach = coach
                
    def extract_player_stats(self, stats_soup, type):
        table = stats_soup.find("tbody")
        stats = table.find_all("tr")
        for row in stats:
            player = row.find("th")
            player = Player(player.text)
            
            nums = row.find_all("td")
            
            for n in nums:
                cat = n.get("data-stat")
                stat = n.text
                
                player.add_stat(cat, stat)
                
            if type == "Offense":
                self.__add_off_player(player)
            else:
                self.__add_def_player(player)
            
    def extract_officials(self, official_soup):
        ref_positions = official_soup.find_all("th")
        refs = official_soup.find_all("a")
        for i in range(len(ref_positions)):
            pos = ref_positions[i].text
            ref = refs[i].text
            if pos not in self.__officials:
                self.__officials[pos] = ""
            self.__officials[pos] = ref
                
    def extract_scorebox_meta(self, game_data):
        search_str = game_data.text
        time_idx = search_str.index("Start Time: ")
        stadium_idx = search_str.index("Stadium: ")
        attendance_idx = search_str.index("Attendance: ")
        length_idx = search_str.index("Time of Game: ")
        
        self.__extract_time(search_str[time_idx+12:stadium_idx])
        
        self.__stadium = search_str[stadium_idx+9:attendance_idx]  
        
        attendance = search_str[attendance_idx+12:length_idx]
        attendance = attendance.replace(',', '')
        self.__attendance = int(attendance)

    def extract_scores(self, scores):
        for s in scores:
            if self.__home_score < 0:
                self.__home_score = int(s.text)
            else:
                self.__away_score = int(s.text)
    
    def extract_starters(self, starter_soup, type):
        table = starter_soup.find("tbody")
        players = table.find_all("a")
        positions = table.find_all("td")
        
        for i in range(len(players)):
            pos = positions[i].text
            player = players[i].text
            if type == "Home":
                if pos not in self.__home_starters:
                    self.__home_starters[pos] = []
                
                self.__home_starters[pos].append(player)
            else:
                if pos not in self.__away_starters:
                    self.__away_starters[pos] = []
                
                self.__away_starters[pos].append(player)
                
    def print_game_info(self):
        print(f"{self.__date}: {self.__away}-{self.__away_score} at {self.__home}-{self.__home_score}")
        
        print(f"{self.__away_coach} vs {self.__home_coach}")
        
        print(f"{self.__away} Off Players Count: {len(self.__away_off_players)}")
            
        print(f"{self.__away} Def Players Count: {len(self.__away_def_players)}")
            
        print(f"{self.__home} Off Players Count: {len(self.__home_off_players)}")
            
        print(f"{self.__home} Def Players Count: {len(self.__home_def_players)}")
        
        print(f"Officials Count: {len(self.__officials)}")
        
    def get_game_as_list(self):
        return [
            self.__attendance,
            self.__away,
            self.__away_coach,
            self.__away_def_players,
            self.__away_off_players,
            self.__away_score,
            self.__away_starters,
            self.__date,
            self.__home,
            self.__home_coach,
            self.__home_def_players,
            self.__home_off_players,
            self.__home_score,
            self.__home_starters,
            self.__officials,
            self.__stadium
        ]