from datetime import datetime
import numbers
from re import template
from Player import Player

class Game:
    ### dictionary with abbrev as key and corresponding team as the value
    abbrevs = {
        "Arizona Cardinals": "ARI",
        "Atlanta Falcons": "ATL",
        "Baltimore Ravens": "BAL",
        "Buffalo Bills": "BUF",
        "Carolina Panthers": "CAR",
        "Chicago Bears": "CHI",
        "Cincinnati Bengals": "CIN",
        "Cleveland Browns": "CLE",
        "Dallas Cowboys": "DAL",
        "Denver Broncos": "DEN",
        "Detroit Lions": "DET",
        "Green Bay Packers": "GNB",
        "Houston Texans": "HOU",
        "Indianapolis Colts": "IND",
        "Jacksonville Jaguars": "JAX",
        "Kansas City Chiefs": "KAN",
        "Los Angeles Chargers": "LAC",
        "Los Angeles Rams": "LAR",
        "Las Vegas Raiders": "LVR",
        "Miami Dolphins": "MIA",
        "Minnesota Vikings": "MIN",
        "New Orleans Saints": "NOR",
        "New England Patriots": "NWE",
        "New York Giants": "NYG",
        "New York Jets": "NYJ",
        "Philadelphia Eagles": "PHI",
        "Pittsburgh Steelers": "PIT",
        "Seattle Seahawks": "SEA",
        "San Francisco 49ers": "SFO",
        "Tampa Bay Buccaneers": "TAM",
        "Tennessee Titans": "TEN",
        "Washington Football Team": "WAS",
        "Washington Commanders": "WAS"
    }
    
    def __init__(self, date, away, home):
        self.__attendance = 0
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
    
    ### HELPER METHODS  
    ##### PRIVATE HELPERS  
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

    def __extract_score_coach(self, info):
        # trim unwanted info
        start = info.find('<strong')
        info = info[start:]
        # find which team the info is for
        start = info.find('.htm">') + 6
        stop = info.find('</a>')
        team = info[start:stop]
        info = info[stop:]
        # find next score info
        start = info.find('<div class="score">')
        info = info[start:]
        stop = info.find('</div>')
        score = info[19:stop]
        # find next coach info
        start = info.find('<div class="datapoint"')
        info = info[start:]
        start = info.find('.htm">') + 6
        stop = info.find('</a>')
        coach = info[start:stop]
        info = info[stop:]
        # assign score and coach to team
        if team == self.__away:
            self.__away_score = score
            self.__away_coach = coach
        elif team == self.__home:
            self.__home_score = score
            self.__home_coach = coach

        return info
    
    ##### PUBLIC HELPERS  
    def extract_score_plays(self, text):
        text_start = text.find('<div class="content_grid"')
        scores = text[:text_start]

        print(scores)

        return text[text_start:]
                
    def extract_scorebox_meta(self, text):
        beg = text.index('</strong>: ')
        text_break = text.find('<div class="linescore_wrap">')
        meta = text[beg:text_break]
        meta_end = text.find('<style>')
        meta = meta[:meta_end]
        # extract time from scorebox meta
        start = meta.find('</strong>: ') + 11
        end = meta.find('</div>')
        self.__extract_time(meta[start:end])
        meta = meta[end:]
        # extract stadium
        start = meta.find('.htm">') + 6
        end = meta.find('</a>')
        self.__stadium = meta[start:end]
        meta = meta[end+4:]
        # extract attendance
        start = meta.find('.htm">') + 6
        end = meta.find('</a>')
        att = meta[start:end]
        self.__attendance = int(att.replace(',', ''))
        meta = meta[end+4:]

        return text[text_break:]

    def extract_scorebox(self, text):
        # trim info
        s_idx = text.find('<div class="scorebox')
        e_idx = text.find('<div class="scorebox_meta')
        info = text[s_idx:e_idx]
        # extract info and trim
        info = self.__extract_score_coach(info)
        # repeat for next team
        info = self.__extract_score_coach(info)

        return text[e_idx:]
                
    def print_game_info(self):
        print(f"{self.__date}: {self.__stadium} | {self.__attendance} in attendance")

        print(f"{self.__away}-{self.__away_score} at {self.__home}-{self.__home_score}")
        
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