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
    
    rem_html = re.compile('<.*?>')
    
    def __init__(self, date, away, home):
        self.__attendance = 0
        self.__away = away
        self.__away_coach = ""
        self.__away_drives = {}
        self.__away_exp_points = {}
        self.__away_players = {}
        self.__away_score = -1
        self.__away_snaps = {}
        self.__away_starters = {}
        self.__away_team_stats = {}
        self.__date = date
        self.__game_duration = 0
        self.__home = home
        self.__home_coach = ""
        self.__home_drives = {}
        self.__home_exp_points = {}
        self.__home_players = {}
        self.__home_score = -1
        self.__home_snaps = {}
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
        info = info[tm_start:]
        tm_end = info.find('</strong>')
        team = info[:tm_end]
        # remove <a href... from Team name
        team = re.sub(self.rem_html, '', team)
        team = team.strip()
        # find next score info
        score_start = info.find('class="score">') + 14
        score = info[score_start:]
        score_end = score.find('</div>')
        score = score[:score_end]
        # find next coach info
        coach_start = info.find('class="datapoint"') + 17
        coach = info[coach_start:]
        coach_start = coach.find(': ') + 2
        coach = coach[coach_start:]
        coach_end = coach.find('</a>')
        coach = coach[:coach_end]
        coach = re.sub(self.rem_html, '', coach)
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
    
    ##### PUBLIC HELPERS
    def extract_adv_defense(self, text):
        # Vars to hold player and team as we loop through rows
        team = ""
        player = ""
        
        start = text.find('<tbody>')
        adv_def = text[start:]
        
        while adv_def.find('<tr >') > -1:
            row_start = adv_def.find('<tr >')
            row_end = adv_def.find('</tr>')
            row = adv_def[row_start:row_end]
            
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
                        if player not in self.__away_players:
                            self.__away_players[player] = {}    
                        self.__away_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        if player not in self.__home_players:
                            self.__home_players[player] = {} 
                        self.__home_players[player][ds] = stat
                
                row = row[stat_end + 5:]
            
            adv_def = adv_def[row_end + 5:]
    
    def extract_adv_passing(self, text):
        # Vars to hold player and team as we loop through rows
        team = ""
        player = ""
        
        start = text.find('<tbody>')
        adv_pass = text[start:]
        
        while adv_pass.find('<tr >') > -1:
            row_start = adv_pass.find('<tr >')
            row_end = adv_pass.find('</tr>')
            row = adv_pass[row_start:row_end]
            
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
                        self.__away_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        self.__home_players[player][ds] = stat
                
                row = row[stat_end + 5:]
            
            adv_pass = adv_pass[row_end + 5:]

    def extract_adv_receiving(self, text):
        # Vars to hold player and team as we loop through rows
        team = ""
        player = ""
        
        start = text.find('<tbody>')
        adv_rec = text[start:]
        
        while adv_rec.find('<tr >') > -1:
            row_start = adv_rec.find('<tr >')
            row_end = adv_rec.find('</tr>')
            row = adv_rec[row_start:row_end]
            
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
                        self.__away_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        self.__home_players[player][ds] = stat
                
                row = row[stat_end + 5:]
            
            adv_rec = adv_rec[row_end + 5:]

    def extract_adv_rushing(self, text):
        # Vars to hold player and team as we loop through rows
        team = ""
        player = ""
        
        start = text.find('<tbody>')
        adv_rush = text[start:]
        
        while adv_rush.find('<tr >') > -1:
            row_start = adv_rush.find('<tr >')
            row_end = adv_rush.find('</tr>')
            row = adv_rush[row_start:row_end]
            
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
                        self.__away_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        self.__home_players[player][ds] = stat
                
                row = row[stat_end + 5:]
            
            adv_rush = adv_rush[row_end + 5:]

    def extract_away_drives(self, text):
        start = text.find('<tbody>')
        snaps = text[start:]
        
        while snaps.find('<tr ') > -1:
            row_start = snaps.find('<tr ')
            row_end = snaps.find('</tr>')
            row = snaps[row_start:row_end]
            
            num_start = row.find('data-stat="drive_num" >') + 23
            num_end = row.find('</th>')
            num = row[num_start:num_end]
            if num not in self.__away_drives:
                self.__away_drives[num] = {}
            
            qtr_start = row.find('data-stat="quarter" >') + 21
            qtr_end = row.find('</td>')
            qtr = row[qtr_start:qtr_end]
            self.__away_drives[num]["Quarter"] = qtr

            time_start = row.find('data-stat="time_start" ') + 25
            time = row[time_start:]
            skip = time.find('>') + 1
            time = time[skip:]
            time_end = time.find('</td>')
            time = time[:time_end]
            self.__away_drives[num]["Time Start"] = time

            yard_start = row.find('data-stat="start_at" >') + 22
            yard = row[yard_start:]
            yard_end = yard.find('</td>')
            yard = yard[:yard_end]
            if not yard:
                yard = self.abbrevs[self.__away] + " 50"
            self.__away_drives[num]["Yard Start"] = yard

            plays_start = row.find('Penalty">') + 9
            plays = row[plays_start:]
            plays_end = plays.find('</span>')
            plays = plays[:plays_end]
            self.__away_drives[num]["Num Plays"] = plays

            tot_start = row.find('data-stat="time_total" ') + 25
            tot = row[tot_start:]
            skip = tot.find('>') + 1
            tot = tot[skip:]
            tot_end = tot.find('</td>')
            tot = tot[:tot_end]
            self.__away_drives[num]["Total Time"] = tot

            net_start = row.find('data-stat="net_yds" >') + 21
            net = row[net_start:]
            net_end = net.find('</td>')
            net = net[:net_end]
            self.__away_drives[num]["Net Yards"] = net

            res_start = row.find('data-stat="end_event" >') + 23
            res = row[res_start:]
            res_end = res.find('</td>')
            res = res[:res_end]
            self.__away_drives[num]["Result"] = res
            
            snaps = snaps[row_end + 5:]

    def extract_away_snaps(self, text):
        start = text.find('<tbody>')
        snaps = text[start:]
        
        while snaps.find('<tr >') > -1:
            row_start = snaps.find('<tr >')
            row_end = snaps.find('</tr>')
            row = snaps[row_start:row_end]
            
            player_start = row.find('data-stat="player" >') + 20
            player_end = row.find('</a>')
            player = row[player_start:player_end]

            html = re.compile('<.*?>')
            player = re.sub(html, '', player)

            self.__away_snaps[player] = {}

            osnap_start = row.find('data-stat="offense" >') + 21
            osnap = row[osnap_start:]
            osnap_end = osnap.find('</td>')
            osnap = osnap[:osnap_end]
            self.__away_snaps[player]["Offense"] = osnap
            
            osnappct_start = row.find('data-stat="off_pct" >') + 21
            osnap_pct = row[osnappct_start:]
            osnappct_end = osnap_pct.find('</td>')
            osnap_pct = osnap_pct[:osnappct_end]
            self.__away_snaps[player]["Offense Pct"] = osnap_pct

            dsnap_start = row.find('data-stat="defense" >') + 21
            dsnap = row[dsnap_start:]
            dsnap_end = dsnap.find('</td>')
            dsnap = dsnap[:dsnap_end]
            self.__away_snaps[player]["Defense"] = dsnap
            
            dsnappct_start = row.find('data-stat="def_pct" >') + 21
            dsnap_pct = row[dsnappct_start:]
            dsnappct_end = dsnap_pct.find('</td>')
            dsnap_pct = dsnap_pct[:dsnappct_end]
            self.__away_snaps[player]["Defense Pct"] = dsnap_pct

            stsnap_start = row.find('data-stat="defense" >') + 21
            stsnap = row[stsnap_start:]
            stsnap_end = stsnap.find('</td>')
            stsnap = stsnap[:stsnap_end]
            self.__away_snaps[player]["Special Teams"] = stsnap
            
            stsnappct_start = row.find('data-stat="def_pct" >') + 21
            stsnap_pct = row[stsnappct_start:]
            stsnappct_end = stsnap_pct.find('</td>')
            stsnap_pct = stsnap_pct[:stsnappct_end]
            self.__away_snaps[player]["Special Teams Pct"] = stsnap_pct
            
            snaps = snaps[row_end + 5:]

    def extract_away_starters(self, text):
        start = text.find('<tbody>')
        starters = text[start:]
        
        while starters.find('<tr >') > -1:
            row_start = starters.find('<tr >')
            row_end = starters.find('</tr>')
            row = starters[row_start:row_end]
            
            player_start = row.find('data-stat="player" >') + 20
            player_end = row.find('</a>')
            player = row[player_start:player_end]

            html = re.compile('<.*?>')
            player = re.sub(html, '', player)

            pos_start = row.find('data-stat="pos" >') + 17
            pos_end = row.find('</td>')
            pos = row[pos_start:pos_end]

            if pos:
                self.__away_starters[player] = pos
            
            starters = starters[row_end + 5:]

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

    def extract_home_drives(self, text):
        start = text.find('<tbody>')
        snaps = text[start:]
        
        while snaps.find('<tr ') > -1:
            row_start = snaps.find('<tr ')
            row_end = snaps.find('</tr>')
            row = snaps[row_start:row_end]
            
            num_start = row.find('data-stat="drive_num" >') + 23
            num_end = row.find('</th>')
            num = row[num_start:num_end]
            if num not in self.__home_drives:
                self.__home_drives[num] = {}
            
            qtr_start = row.find('data-stat="quarter" >') + 21
            qtr_end = row.find('</td>')
            qtr = row[qtr_start:qtr_end]
            self.__home_drives[num]["Quarter"] = qtr

            time_start = row.find('data-stat="time_start" ') + 25
            time = row[time_start:]
            skip = time.find('>') + 1
            time = time[skip:]
            time_end = time.find('</td>')
            time = time[:time_end]
            self.__home_drives[num]["Time Start"] = time

            yard_start = row.find('data-stat="start_at" >') + 22
            yard = row[yard_start:]
            yard_end = yard.find('</td>')
            yard = yard[:yard_end]
            if not yard:
                yard = self.abbrevs[self.__home] + " 50"
            self.__home_drives[num]["Yard Start"] = yard

            plays_start = row.find('Penalty">') + 9
            plays = row[plays_start:]
            plays_end = plays.find('</span>')
            plays = plays[:plays_end]
            self.__home_drives[num]["Num Plays"] = plays

            tot_start = row.find('data-stat="time_total" ') + 25
            tot = row[tot_start:]
            skip = tot.find('>') + 1
            tot = tot[skip:]
            tot_end = tot.find('</td>')
            tot = tot[:tot_end]
            self.__home_drives[num]["Total Time"] = tot

            net_start = row.find('data-stat="net_yds" >') + 21
            net = row[net_start:]
            net_end = net.find('</td>')
            net = net[:net_end]
            self.__home_drives[num]["Net Yards"] = net

            res_start = row.find('data-stat="end_event" >') + 23
            res = row[res_start:]
            res_end = res.find('</td>')
            res = res[:res_end]
            self.__home_drives[num]["Result"] = res
            
            snaps = snaps[row_end + 5:]

    def extract_home_snaps(self, text):
        start = text.find('<tbody>')
        snaps = text[start:]
        
        while snaps.find('<tr >') > -1:
            row_start = snaps.find('<tr >')
            row_end = snaps.find('</tr>')
            row = snaps[row_start:row_end]
            
            player_start = row.find('data-stat="player" >') + 20
            player_end = row.find('</a>')
            player = row[player_start:player_end]

            html = re.compile('<.*?>')
            player = re.sub(html, '', player)

            self.__home_snaps[player] = {}

            osnap_start = row.find('data-stat="offense" >') + 21
            osnap = row[osnap_start:]
            osnap_end = osnap.find('</td>')
            osnap = osnap[:osnap_end]
            self.__home_snaps[player]["Offense"] = osnap
            
            osnappct_start = row.find('data-stat="off_pct" >') + 21
            osnap_pct = row[osnappct_start:]
            osnappct_end = osnap_pct.find('</td>')
            osnap_pct = osnap_pct[:osnappct_end]
            self.__home_snaps[player]["Offense Pct"] = osnap_pct

            dsnap_start = row.find('data-stat="defense" >') + 21
            dsnap = row[dsnap_start:]
            dsnap_end = dsnap.find('</td>')
            dsnap = dsnap[:dsnap_end]
            self.__home_snaps[player]["Defense"] = dsnap
            
            dsnappct_start = row.find('data-stat="def_pct" >') + 21
            dsnap_pct = row[dsnappct_start:]
            dsnappct_end = dsnap_pct.find('</td>')
            dsnap_pct = dsnap_pct[:dsnappct_end]
            self.__home_snaps[player]["Defense Pct"] = dsnap_pct

            stsnap_start = row.find('data-stat="defense" >') + 21
            stsnap = row[stsnap_start:]
            stsnap_end = stsnap.find('</td>')
            stsnap = stsnap[:stsnap_end]
            self.__home_snaps[player]["Special Teams"] = stsnap
            
            stsnappct_start = row.find('data-stat="def_pct" >') + 21
            stsnap_pct = row[stsnappct_start:]
            stsnappct_end = stsnap_pct.find('</td>')
            stsnap_pct = stsnap_pct[:stsnappct_end]
            self.__home_snaps[player]["Special Teams Pct"] = stsnap_pct
            
            snaps = snaps[row_end + 5:]

    def extract_home_starters(self, text):
        start = text.find('<tbody>')
        starters = text[start:]
        
        while starters.find('<tr >') > -1:
            row_start = starters.find('<tr >')
            row_end = starters.find('</tr>')
            row = starters[row_start:row_end]
            
            player_start = row.find('data-stat="player" >') + 20
            player_end = row.find('</a>')
            player = row[player_start:player_end]

            html = re.compile('<.*?>')
            player = re.sub(html, '', player)

            pos_start = row.find('data-stat="pos" >') + 17
            pos_end = row.find('</td>')
            pos = row[pos_start:pos_end]

            if pos:
                self.__home_starters[player] = pos
            
            starters = starters[row_end + 5:]

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
                        if player not in self.__away_players:
                            self.__away_players[player] = {}
                        
                        self.__away_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        if player not in self.__home_players:
                            self.__home_players[player] = {}
                        
                        self.__home_players[player][ds] = stat
                
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
                        if player not in self.__away_players:
                            self.__away_players[player] = {}
                        
                        self.__away_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        if player not in self.__home_players:
                            self.__home_players[player] = {}
                        
                        self.__home_players[player][ds] = stat
                
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
                        if player not in self.__away_players:
                            self.__away_players[player] = {}
                        
                        self.__away_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        if player not in self.__home_players:
                            self.__home_players[player] = {}
                        
                        self.__home_players[player][ds] = stat
                
                row = row[stat_end + 5:]
            
            returns = returns[row_end + 5:]

    def extract_plays(self, text):
        start = text.find('<tbody>')
        plays = text[start:]
        
        while plays.find('<tr ') > -1:
            row_start = plays.find('<tr ')
            row_end = plays.find('</tr>')
            row = plays[row_start:row_end]
            
            qtr_start = row.find('data-stat="quarter" >') + 21
            qtr_end = row.find('</th>')
            qtr = row[qtr_start:qtr_end]
            if qtr.find("onecell") < 0 and qtr.find("aria-label") < 0:
                pass # do something here

            rem_time_start = row.find('data-stat="qtr_time_remain" >') + 29
            rem_time = row[rem_time_start:]
            rem_time_end = rem_time.find('</a>')
            rem_time = rem_time[:rem_time_end]
            if rem_time.find("aria-label") < 0 and rem_time.find("onecell") < 0:
                html = re.compile('<.*?>')
                rem_time = re.sub(html, '', rem_time)
                
            down_start = row.find('data-stat="down" >') + 18
            down = row[down_start:]
            down_end = down.find('</a>')
            down = down[:down_end]
            if down.find("aria-label") < 0 and down.find("onecell") < 0:
                html = re.compile('<.*?>')
                down = re.sub(html, '', down)
                print(down)
            
            plays = plays[row_end + 5:]

    def extract_scorebox(self, text):
        text = self.__extract_score_coach(text)
        self.__extract_score_coach(text)

    def extract_scorebox_meta(self, text):
        start = text.find('</div>') + 6
        info = text[start:]
        
        while info.find('<strong>') > -1:
            d_start = info.find('<strong>') + 8
            d_end = info.find('</div>')
            data = info[d_start:d_end]
            data = re.sub(self.rem_html, '', data)
            
            data = data.split(": ")
            label = data[0]
            stat = data[1]
            
            if label == "Attendance":
                self.__attendance = stat
            elif label == "Stadium":
                self.__stadium = stat
            elif label == "Start Time":
                self.__extract_time(stat)
            elif label == "Time of Game":
                self.__game_duration = stat
                
            info = info[d_end + 6:]         

    def extract_scoring_plays(self, text):
        # trim to tbody
        start = text.find('<tbody>') + 7
        scores = text[start:]

        last_known_qtr = 0
        
        while scores.find('<tr >') > -1:
            play = {}
            
            row_start = scores.find('<tr >') + 5
            row_end = scores.find('</tr>')
            row = scores[row_start:row_end]
            
            qtr_start = row.find('data-stat="quarter" >') + 21
            qtr_end = row.find('</th>')
            qtr = row[qtr_start:qtr_end]
            if qtr:
                last_known_qtr = qtr
            else:
                qtr = last_known_qtr
            play["quarter"] = qtr
            
            time_start = row.find('data-stat="time" >') + 18
            time_end = row.find('</td>')
            time = row[time_start:time_end]
            play["time"] = time
            
            team_start = row.find('data-stat="team" >') + 18
            team = row[team_start:]
            team_end = team.find('</td>')
            team = team[:team_end]
            play["team"] = team
            
            desc_start = row.find('data-stat="description" >') + 25
            desc = row[desc_start:]
            desc_end = desc.find('</td>')
            desc = desc[:desc_end]
            desc = re.sub(self.rem_html, '', desc)
            play["description"] = desc
            
            a_scr_start = row.find('data-stat="vis_team_score" >') + 28
            a_scr = row[a_scr_start:]
            a_scr_end = a_scr.find('</td>')
            a_scr = a_scr[:a_scr_end]
            play["away_team_score"] = a_scr
            
            h_scr_start = row.find('data-stat="home_team_score" >') + 29
            h_scr = row[h_scr_start:]
            h_scr_end = h_scr.find('</td>')
            h_scr = h_scr[:h_scr_end]
            play["away_team_score"] = h_scr
            
            self.__scoring_plays.append(play)
            
            scores = scores[row_end + 5:]

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
                        if player not in self.__away_players:
                            self.__away_players[player] = {}
                        
                        self.__away_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        if player not in self.__home_players:
                            self.__home_players[player] = {}
                        
                        self.__home_players[player][ds] = stat
                
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
        
        print(f"{self.__away} Players Count: {len(self.__away_players)}")
        
        print(f"{self.__home} Players Count: {len(self.__home_players)}")
        
        print(f"Officials Count: {len(self.__officials)}")
        
        print(f"{self.__away} (Away) Expected Points: {self.__away_exp_points}")
        
        print(f"{self.__home} (Home) Expected Points: {self.__home_exp_points}")
        
        print(f"{self.__away} Team Stats: {self.__away_team_stats}")
        
        print(f"{self.__home} Team Stats: {self.__home_team_stats}")

        print(f"{self.__away} Starters: {self.__away_starters}")

        print(f"{self.__home} Starters: {self.__home_starters}")

        print(f"{self.__away} Players with Snaps: {len(self.__away_snaps)}")

        print(f"{self.__home} Players with Snaps: {len(self.__home_snaps)}")

        print(f"{self.__away} Drives")
        for drive in self.__home_drives:
            print(self.__home_drives[drive])

        print(f"{self.__home} Drives:")
        for drive in self.__away_drives:
            print(self.__away_drives[drive])

        # for player in self.__away_players:
        #     print(f"{player}*************")
        #     for stat in self.__away_players[player]:
        #         print(f"{stat}: {self.__away_players[player][stat]}")
        
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