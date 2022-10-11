from cmath import inf
from datetime import datetime
from sqlite3 import Row
from tracemalloc import start
from Player import Player
import re

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
        "Oakland Raiders": "OAK",
        "Philadelphia Eagles": "PHI",
        "Pittsburgh Steelers": "PIT",
        "San Diego Chargers": "SDG",
        "San Francisco 49ers": "SFO",
        "Seattle Seahawks": "SEA",
        "St. Louis Rams": "STL",
        "Tampa Bay Buccaneers": "TAM",
        "Tennessee Titans": "TEN",
        "Washington Football Team": "WAS",
        "Washington Commanders": "WAS"
    }
    
    def __init__(self, date, away, home):
        self.__attendance = 0
        self.__away = away
        self.__away_coach = ""
        self.__away_def_players = {}
        self.__away_exp_points = {}
        self.__away_kp_players = {}
        self.__away_off_players = {}
        self.__away_ret_players= {}
        self.__away_score = -1
        self.__away_starters = {}
        self.__away_team_stats = {}
        self.__date = date
        self.__game_duration = 0
        self.__home = home
        self.__home_coach = ""
        self.__home_def_players = {}
        self.__home_exp_points = {}
        self.__home_kp_players = {}
        self.__home_off_players = {}
        self.__home_ret_players = {}
        self.__home_score = -1
        self.__home_starters = {}
        self.__home_team_stats = {}
        self.__officials = {}
        self.__over_under = 0
        self.__roof = ""
        self.__scoring_plays = []
        self.__stadium = ""
        self.__surface = ""
        self.__spread = 0
        self.__weather = ""
        self.__won_toss = ""
    
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
        tm_start = info.find('<strong>') + 8
        tm_end = info.find('</strong>')
        team = info[tm_start:tm_end]
        info = info[tm_start:]
        # remove <a href... from Team name
        html = re.compile('<.*?>')
        team = re.sub(html, '', team)
        team = team.strip()
        # find next score info
        score_start = info.find('<div class="score">') + 19
        score = info[score_start:]
        score_end = score.find('</div>')
        score = score[:score_end]
        # find next coach info
        coach_start = info.find('<div class="datapoint"')
        coach = info[coach_start:]
        coach_start = coach.find(': ') + 2
        coach = coach[coach_start:]
        coach_end = coach.find('</a>')
        coach = coach[:coach_end]
        coach = re.sub(html, '', coach)
        coach = coach.strip()
        # assign score and coach to team
        if team == self.__away:
            self.__away_score = score
            self.__away_coach = coach
        elif team == self.__home:
            self.__home_score = score
            self.__home_coach = coach

        # trim info
        info_start = info.find('<div class="media-item logo loader">')
        return info[info_start:]
    
    def __extract_scoring_play(self, row, last_known_qtr):
        scoring_play = {}
        
        qtr_start = row.find('<th ')
        qtr_end = row.find('</th>')
        qtr = row[qtr_start:qtr_end]
        
        html = re.compile('<.*?>')
        qtr = re.sub(html, '', qtr)
        
        if qtr == '':
            qtr = last_known_qtr
        else:
            last_known_qtr = qtr
            
        scoring_play["quarter"] = qtr
            
        row = row[qtr_end:]
        while row.find('<td ') > -1:
            start = row.find('<td ')
            end = row.find('</td>')

            info = row[start:end]
            
            data_stat_start = info.find('data-stat="') + 11
            data_stat_end = info.find('">')
            data_stat = info[data_stat_start:data_stat_end]
            
            stat = info.replace('\n', '')
            stat = stat.replace('   ', '')
            stat = stat.strip()
            html = re.compile('<.*?>')
            stat = re.sub(html, '', stat)
            
            if data_stat != '':
                scoring_play[data_stat] = stat
            
            
            row = row[end + 5:]
        
        return last_known_qtr, scoring_play
    
    ##### PUBLIC HELPERS 
    def extract_exp_points_added(self, text):
        exp_pts_start = text.find('tbody')
        exp_pts = text[exp_pts_start:]
        
        while exp_pts.find('<tr') > -1:
            row_start = exp_pts.find('<tr')
            row_end = exp_pts.find('</tr>')
            row = exp_pts[row_start:row_end]
            
            tm_start = row.find('"team_name" >') + 13
            tm_end = row.find('</th>')
            tm = row[tm_start:tm_end]
            
            while row.find('<td ') > -1:
                label_start = row.find('data-stat=') + 11
                label_end = row.find('" >')
                label = row[label_start:label_end]
                if label != "team_name":
                    stat_start = row.find('>') + 1
                    stat_end = row.find('</td>')
                    stat = row[stat_start:stat_end]
                    
                    if tm in self.__away:
                        self.__away_exp_points[label] = stat
                    elif tm in self.__home:
                        self.__home_exp_points[label] = stat
                
                row = row[row.find('</td>') + 5:]
                
            
            exp_pts = exp_pts[row_end + 4:]
    
    def extract_game_info(self, text):
        # loop through all rows of html
        while text.find('<tr >') > -1:
            # define row start
            row_start = text.find('<tr >')
            # define row end
            row_end = text.find('</tr>')
            row = text[row_start:row_end]
            # define game info cat
            head_start = row.find('="info" >')
            head_end = row.find('</th>')
            header = row[head_start + 9:head_end]
            # define game info stat
            stat_start = row.find('="stat" >')
            stat_end = row.find('</td>')
            stat = row[stat_start + 9:stat_end]
            # remove html from stats
            html = re.compile('<.*?>')
            stat = re.sub(html, '', stat)
            
            if header == "Won Toss":
                self.__won_toss = stat
            elif header == "Roof":
                self.__roof = stat
            elif header == "Surface":
                self.__surface = stat
            elif header == "Weather":
                self.__weather = stat
            elif header == "Vegas Line":
                self.__spread = stat
            elif header == "Over/Under":
                self.__over_under = stat
            
            text = text[row_end + 5:]

    def extract_officials(self, text):
        official_start = text.find('<div class="table_container" id="div_officials">')
        officials = text[official_start:]

        while officials.find('<tr ') > -1:
            row_start = officials.find('<tr ')
            row_end = officials.find('</tr>')
            row = officials[row_start:row_end]
            
            off_pos_start = row.find('"ref_pos" >') + 11
            off_pos_end = row.find('</th>')
            if off_pos_start > -1 and off_pos_end > -1:
                off_pos = row[off_pos_start:off_pos_end]

                off_start = row.find('.htm">') + 6
                off_end = row.find('</a>')
                if off_start > -1 and off_end > -1:
                    off = row[off_start:off_end]
                    self.__officials[off_pos] = off

            officials = officials[row_end + 5:]

    def extract_player_offense(self, text):
        # Vars to hold player and team as we loop through rows
        team = ""
        player = ""
        
        off_start = text.find('<tbody>')
        offense = text[off_start:]
        
        while offense.find('<tr>') > -1:
            row_start = offense.find('<tr>')
            row_end = offense.find('</tr>')
            row = offense[row_start:row_end]
            
            while row.find('data-stat="') > -1:
                ds_start = row.find('data-stat="') + 11
                ds_end = row.find('">')
                ds = row[ds_start:ds_end]
                
                stat_end = row.find('</t')
                stat = row[ds_end + 2:stat_end]
                stat = stat.replace('\n', '')
                stat = stat.replace("   ", '')
                
                html = re.compile('<.*?>')
                stat = re.sub(html, '', stat)
                
                if stat == '':
                    stat = 0
                
                if ds == "player":
                    player = stat
                elif ds == "team":
                    team = stat
                else:
                    if self.abbrevs[self.__away] == team:
                        if player not in self.__away_off_players:
                            self.__away_off_players[player] = {}
                        
                        self.__away_off_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        if player not in self.__home_off_players:
                            self.__home_off_players[player] = {}
                        
                        self.__home_off_players[player][ds] = stat
                
                row = row[stat_end + 5:]
            
            offense = offense[row_end + 5:]
            
    def extract_player_defense(self, text):
        # Vars to hold player and team as we loop through rows
        team = ""
        player = ""
        
        def_start = text.find('<tbody>')
        defense = text[def_start:]
        
        while defense.find('<tr>') > -1:
            row_start = defense.find('<tr>')
            row_end = defense.find('</tr>')
            row = defense[row_start:row_end]
            
            while row.find('data-stat="') > -1:
                ds_start = row.find('data-stat="') + 11
                ds_end = row.find('">')
                ds = row[ds_start:ds_end]
                
                stat_end = row.find('</t')
                stat = row[ds_end + 2:stat_end]
                stat = stat.replace('\n', '')
                stat = stat.replace("   ", '')
                
                html = re.compile('<.*?>')
                stat = re.sub(html, '', stat)
                
                if stat == '':
                    stat = 0
                
                if ds == "player":
                    player = stat
                elif ds == "team":
                    team = stat
                else:
                    if self.abbrevs[self.__away] == team:
                        if player not in self.__away_def_players:
                            self.__away_def_players[player] = {}
                        
                        self.__away_def_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        if player not in self.__home_def_players:
                            self.__home_def_players[player] = {}
                        
                        self.__home_def_players[player][ds] = stat
                
                row = row[stat_end + 5:]
            
            defense = defense[row_end + 5:]
            
    def extract_player_returns(self, text):
        # Vars to hold player and team as we loop through rows
        team = ""
        player = ""
        
        ret_start = text.find('<tbody>')
        returns = text[ret_start:]
        
        while returns.find('<tr>') > -1:
            row_start = returns.find('<tr>')
            row_end = returns.find('</tr>')
            row = returns[row_start:row_end]
            
            while row.find('data-stat="') > -1:
                ds_start = row.find('data-stat="') + 11
                ds_end = row.find('">')
                ds = row[ds_start:ds_end]
                
                stat_end = row.find('</t')
                stat = row[ds_end + 2:stat_end]
                stat = stat.replace('\n', '')
                stat = stat.replace("   ", '')
                
                html = re.compile('<.*?>')
                stat = re.sub(html, '', stat)
                
                if stat == '':
                    stat = 0
                
                if ds == "player":
                    player = stat
                elif ds == "team":
                    team = stat
                else:
                    if self.abbrevs[self.__away] == team:
                        if player not in self.__away_ret_players:
                            self.__away_ret_players[player] = {}
                        
                        self.__away_ret_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        if player not in self.__home_ret_players:
                            self.__home_ret_players[player] = {}
                        
                        self.__home_ret_players[player][ds] = stat
                
                row = row[stat_end + 5:]
            
            returns = returns[row_end + 5:]

    def extract_scoring_plays(self, text):
        # trim to tbody
        start = text.find('tbody')
        text = text[start:]

        last_known_qtr = 0
        
        while text.find('<tr>') > -1:
            row_start = text.find('<tr>') + 4
            row_end = text.find('</tr>') + 5
            row = text[row_start:row_end]
            
            last_known_qtr, play = self.__extract_scoring_play(row, last_known_qtr)
            self.__scoring_plays.append(play)
            
            text = text[row_end:]
                
    def extract_scorebox_meta(self, text):
        while text.find('<strong>') > -1:
            start = text.find('<strong>')
            text = text[start:]
            
            end = text.find('</div>')
            info = text[:end]
            
            html = re.compile('<.*?>')
            info = re.sub(html, '', info)
            
            info = info.split(': ')
            type = info[0]
            info = info[1]
            
            if type == "Attendance":
                self.__attendance = info
            elif type == "Stadium":
                self.__stadium = info
            elif type == "Start Time":
                self.__extract_time(info)
            elif type == "Time of Game":
                self.__game_duration = info
                
            text = text[end:]

    def extract_scorebox(self, text):
        text = self.__extract_score_coach(text)
        self.__extract_score_coach(text)

    def extract_team_stats(self, text):
        start = text.find('<tbody')
        text = text[start:]
        
        while text.find('<tr') > -1:
            row_start = text.find('<tr ')
            row_end = text.find('</tr>')
            row = text[row_start:row_end]
            
            label_start = row.find('"stat" >') + 8
            label_end = row.find('</th>')
            label = row[label_start:label_end]
            
            vis_start = row.find('vis_stat" >') + 11
            vis_end = row.find('</td>')
            vis_stat = row[vis_start:vis_end]
            self.__away_team_stats[label] = vis_stat
            
            home_start = row.find('home_stat" >') + 12
            home_end = row.find('</td></tr>') - 4
            home_stat = row[home_start:home_end]
            self.__home_team_stats[label] = home_stat
            
            text = text[row_end + 5:]
    
    def extract_kick_punt(self, text):
        # Vars to hold player and team as we loop through rows
        team = ""
        player = ""
        
        kp_start = text.find('<tbody>')
        k_punts = text[kp_start:]
        
        while k_punts.find('<tr >') > -1:
            row_start = k_punts.find('<tr >')
            row_end = k_punts.find('</tr>')
            row = k_punts[row_start:row_end]
            
            while row.find('data-stat="') > -1:
                ds_start = row.find('data-stat="') + 11
                ds_end = row.find('" >')
                ds = row[ds_start:ds_end]
                
                stat_end = row.find('</t')
                stat = row[ds_end + 3:stat_end]
                stat = stat.replace('\n', '')
                stat = stat.replace("   ", '')
                
                html = re.compile('<.*?>')
                stat = re.sub(html, '', stat)
                
                if stat == '':
                    stat = 0
                
                if ds == "player":
                    player = stat
                elif ds == "team":
                    team = stat
                else:
                    if self.abbrevs[self.__away] == team:
                        if player not in self.__away_kp_players:
                            self.__away_kp_players[player] = {}
                        
                        self.__away_kp_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        if player not in self.__home_kp_players:
                            self.__home_kp_players[player] = {}
                        
                        self.__home_kp_players[player][ds] = stat
                
                row = row[stat_end + 5:]
            
            k_punts = k_punts[row_end + 5:]
                
    def print_game_info(self):
        print(f"{self.__date}: {self.__stadium} | {self.__attendance} in attendance | Duration: {self.__game_duration}")

        print(f"Favored: {self.__spread} | Over/Under: {self.__over_under}")
        
        print(f"Weather: {self.__weather}")
        
        print(f"Roof: {self.__roof} | Surface: {self.__surface}")

        print(f"{self.__away}-{self.__away_score} at {self.__home}-{self.__home_score}")
        
        print(f"{self.__away_coach} vs {self.__home_coach}")
        
        print(f"Scoring Plays Count: {len(self.__scoring_plays)}")
        
        print(f"{self.__away} Off Players Count: {len(self.__away_off_players)}")
            
        print(f"{self.__away} Def Players Count: {len(self.__away_def_players)}")
            
        print(f"{self.__away} Ret Players Count: {len(self.__away_ret_players)}")
        
        print(f"{self.__away} Kick/Punt Players Count: {len(self.__away_kp_players)}")
        
        print(f"{self.__home} Off Players Count: {len(self.__home_off_players)}")
            
        print(f"{self.__home} Def Players Count: {len(self.__home_def_players)}")
        
        print(f"{self.__home} Ret Players Count: {len(self.__home_ret_players)}")
        
        print(f"{self.__home} Kick/Punt Players Count: {len(self.__home_kp_players)}")
        
        print(f"Officials Count: {len(self.__officials)}")
        
        print(f"{self.__away} (Away) Expected Points: {self.__away_exp_points}")
        
        print(f"{self.__home} (Home) Expected Points: {self.__home_exp_points}")
        
        print(f"{self.__away} Team Stats: {self.__away_team_stats}")
        
        print(f"{self.__home} Team Stats: {self.__home_team_stats}")
        
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