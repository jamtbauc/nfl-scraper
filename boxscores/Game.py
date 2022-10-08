from datetime import datetime
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
        self._id = self.__create_ids
        self.__officials = {}
        self.__stadium = ""
    
    ### HELPER METHODS  
    ##### PRIVATE HELPERS 
    def __create_ids(self, date, away, home):
        pass

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
    def extract_game_info(self, text):
        game_info = {}

        text_start = text.find('<div id="all_officials"')
        info_start = text.find('<div class="table_container" id="div_game_info">')
        info = text[info_start:text_start]
        # loop through all rows of html
        while info.find('<tr >') > -1:
            # define row start
            row_start = info.find('<tr >')
            # define row end
            row_end = info.find('</tr>')
            row = info[row_start:row_end]
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
            game_info[header] = stat;
            info = info[row_end + 5:]

        return text[text_start:]

    def extract_officials(self, text):
        referees = {}

        text_start = text.find('<div id="all_expected_points"')
        official_start = text.find('<div class="table_container" id="div_officials">')
        officials = text[official_start:text_start]

        while officials.find('<tr ') > -1:
            row_start = officials.find('<tr ')
            row_end = officials.find('</tr>')
            row = officials[row_start:row_end]
            
            off_pos_start = row.find('"ref_pos" >') + 11
            off_pos_end = row.find('</th>')
            off_pos = row[off_pos_start:off_pos_end]

            off_start = row.find('.htm">') + 6
            off_end = row.find('</a>')
            off = row[off_start:off_end]

            referees[off_pos] = off

            officials = officials[row_end + 5:]

        return text[text_start:]

    def extract_scoring_plays(self, text):
        # create list of plays
        plays = []

        text_start = text.find('<div class="content_grid"')
        scores = text[:text_start]
        # trim to table
        start = scores.find('<div id="all_scoring"')
        scores = scores[start:]
        # trim to tbody
        start = scores.find('tbody')
        scores = scores[start:]

        last_known_qtr = 0
        
        while scores.find('<tr>') > -1:
            row_start = scores.find('<tr>')
            row_end = scores.find('</tr>')
            row = scores[row_start:row_end]
            last_known_qtr = self.extract_scoring_play(row, plays, last_known_qtr)
            scores = scores[row_end + 5:]

        return text[text_start:]

    def extract_scoring_play(self, score, plays, last_known_qtr):
        # extract quarter
        qtr_start = score.find('data-stat="quarter">') + 20
        qtr_end = score.find('</th>')
        qtr = score[qtr_start:qtr_end]
        if qtr == '':
            qtr = last_known_qtr
        else:
            last_known_qtr = qtr
        # extract quarter time
        qtr_time_start = score.find('data-stat="time">') + 17
        qtr_time_end = score.find('</td>')
        qtr_time = score[qtr_time_start:qtr_time_end]
        qtr_time = qtr_time.replace('<', '')
        score = score[qtr_time_end + 5:]
        # extract scoring team
        tm_start = score.find('data-stat="team">') + 17
        tm_end = score.find('</td>')
        score_tm = score[tm_start:tm_end]
        score = score[tm_end + 5:]
        # extract scoring play description
        desc_start = score.find('data-stat="description">') + 24
        desc_end = score.find('</td>')
        desc = score[desc_start:desc_end]
        desc = desc.replace('\n', '')
        html = re.compile('<.*?>')
        desc = re.sub(html, '', desc)
        space = re.compile(' +')
        desc = re.sub(space, ' ', desc)
        score = score[desc_end + 5:]
        # extract visiting score after play
        vis_scr_start = score.find('data-stat="vis_team_score">') + 27
        vis_scr_end = score.find('</td>')
        vis_score = score[vis_scr_start:vis_scr_end]
        score = score[vis_scr_end + 5:]
        # extract home score after play
        hm_scr_start = score.find('data-stat="home_team_score">') + 28
        hm_scr_end = score.find('</td>')
        hm_score = score[hm_scr_start:hm_scr_end]
        score = score[hm_scr_end + 5:]

        plays.append([qtr, qtr_time, score_tm, desc, vis_score, hm_score])
        return last_known_qtr
                
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
        # extract info and trim
        info = self.__extract_score_coach(info)
        # repeat for next team
        info = self.__extract_score_coach(info)

    def extract_team_stats(self, text):
        text_start = text.find('<div id="all_player_offense" class="table_wrapper">')
        stats_start = text.find('<div class="table_container" id="div_team_stats">')

        return text[text_start:]
                
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