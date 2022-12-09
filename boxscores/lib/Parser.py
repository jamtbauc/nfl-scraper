import csv
from datetime import datetime
from lib.Game import Game
from lib.GameWeather import GameWeather
from lib.Official import Official
from lib.OfficialGame import OfficialGame
from lib.PlayByPlay import PlayByPlay
from lib.Player import Player
from lib.PlayerGame import PlayerGame
from lib.PlayerGameSnap import PlayerGameSnap
from lib.ScoringPlay import ScoringPlay
from lib.Stadium import Stadium
from lib.Team import Team
from lib.TeamGame import TeamGame
from lib.TeamGameDrive import TeamGameDrive
import re

class Parser:
    rem_html = re.compile('<.*?>')
    
    # hold all objects
    teams = {}
    games = {}
    team_gms = {}
    stadiums = {}
    scoring_plays = {}
    gm_weathers = {}
    officials = {}
    off_gms = {}
    play_by_plays = {}
    players = {}
    player_gms = {}
    player_gm_snaps = {}
    tm_gm_drives = {}
    errors = []
    
    # hold id counters
    tm_game_id = 1
    scoring_play_id = 1
    gm_weather_id = 1
    off_gm_id = 1
    player_gm_id = 1
    player_gm_snap_id = 1
    team_gm_drive_id = 1
    play_by_play_id = 1
    
    def __init__(self):
        # define text blocks
        self._matchup = None
        self._scorebox = None
        self._scorebox_meta = None
        self._all_scoring = None
        self._game_info = None
        self._all_officials = None
        self._all_team_stats = None
        self._all_player_off = None
        self._all_player_def = None
        self._all_returns = None
        self._all_kicking = None
        self._passing_adv = None
        self._rushing_adv = None
        self._receiving_adv = None
        self._defense_adv = None
        self._home_starters = None
        self._away_starters = None
        self._home_snaps = None
        self._away_snaps = None
        self._home_drives = None
        self._away_drives = None
        self._plays = None
        
        # define objects specific to one  (RESET AT END OF parseGame)
        self.game = {}
        self.away_team = {}
        self.home_team = {}
        self.player_games = {}
        self.starters = {}
    
#     ### HELPER METHODS 
    def setMatchup(self, text):
        self._matchup = text 
        
    def setScorebox(self, text):
        self._scorebox = text
        
    def setScoreboxMeta(self, text):
        self._scorebox_meta = text
        
    def setAllScoring(self, text):
        self._all_scoring = text
        
    def setGameInfo(self, text):
        self._game_info = text
        
    def setAllOfficials(self, text):
        self._all_officials = text
        
    def setAllTeamStats(self, text):
        self._all_team_stats = text
        
    def setAllPlayerOff(self, text):
        self._all_player_off = text
        
    def setAllPlayerDef(self, text):
        self._all_player_def = text
        
    def setAllReturns(self, text):
        self._all_returns = text
        
    def setAllKicking(self, text):
        self._all_kicking = text
        
    def setPassingAdv(self, text):
        self._passing_adv = text
        
    def setRushingAdv(self, text):
        self._rushing_adv = text
        
    def setReceivingAdv(self, text):
        self._receiving_adv = text
        
    def setDefenseAdv(self, text):
        self._defense_adv = text
        
    def setHomeStarters(self, text):
        self._home_starters = text
        
    def setAwayStarters(self, text):
        self._away_starters = text
        
    def setHomeSnaps(self, text):
        self._home_snaps = text
        
    def setAwaySnaps(self, text):
        self._away_snaps = text
        
    def setHomeDrives(self, text):
        self._home_drives = text
        
    def setAwayDrives(self, text):
        self._away_drives = text
        
    def setPlays(self, text):
        self._plays = text
        
    def addErrorUrl(self, url):
        self.errors.append(url)
        
    # extract date, home and away teams from header
    def extract_basic_info(self):
        # trim data to matchup only
        idx = self._matchup.find("<h1>") + 4
        e_idx = self._matchup.find("</h1>")
        info = self._matchup[idx:e_idx]
        # trim data to week only
        week_idx = self._matchup.find('.htm">') + 6
        week_e_idx = self._matchup.find("</a>")
        week = self._matchup[week_idx:week_e_idx]
        # split title into teams and date
        info = info.split(" - ")
        # separate into name vars
        matchup = info[0]
        date_str = info[1]
        # if there are two dashes in the string check for matchup
        if matchup.find(" at ") < 0 and matchup.find(" vs. ") < 0:
            matchup = info[1]
            date_str = info[2]
            
        if matchup.find(" at ") > -1:
            matchup = matchup.split(" at ")
        elif matchup.find(" vs. ") > -1:
            matchup = matchup.split(" vs. ")
            
        away = None
        home = None
          
        # get away team name
        away_name = matchup[0].strip()
        # if team doesn't already exist in teams list, create new team
        if away_name not in self.teams:
            away = Team(away_name)
            self.teams[away_name] = away
        else:
            away = self.teams[away_name]
        
        # get home team name
        home_name = matchup[1].strip()
        # if team doesn't exist in teams list, create new team
        if home_name not in self.teams:
            home = Team(home_name)
            self.teams[home_name] = home
        else:
            home = self.teams[home_name]
        
        date_trimmed = self.remove_date_formals(date_str)
        date = datetime.strptime(date_trimmed, "%B %d, %Y")
        
        # create game object
        self.game = Game(date, week, away.getAbbrevPff(), home.getAbbrevPff())
        # add game to game list
        if self.game.getId() not in self.games:
            self.games[self.game.getId()] = self.game
        
        # create single game team games
        self.away_team = TeamGame(self.getNextTmGmId(), away_name, self.game.getId(), False)
        self.team_gms[self.away_team.getId()] = self.away_team
        
        self.home_team = TeamGame(self.getNextTmGmId(), home_name, self.game.getId(), True)
        self.team_gms[self.home_team.getId()] = self.home_team
    
#     ##### PRIVATE HELPERS 
    def __extract_time(self, time_str):
        am_pm = time_str[-2:]
        if am_pm == "am":
            am_pm = "AM"
        else:
            am_pm = "PM"
            
        time_str = time_str[:-2] + am_pm
        
        date_str = self.game.getDate().strftime("%B %d, %Y")
        date_str += " " + time_str
        
        self.game.setDate(datetime.strptime(date_str, "%B %d, %Y %I:%M%p"))

    def __extract_score_coach(self, info):
        tm_start = info.find('.htm">') + 6
        tm_end = info.find('</a>\n')
        team = info[tm_start:tm_end]
        # find next score info
        score_start = info.find('class="score">') + 14
        info_scr = info[score_start:]
        score_end = info_scr.find('</div>')
        score = info_scr[:score_end]
        # find next coach info
        coach_start = info.find('</strong>: ') + 11
        info_coach = info[coach_start:]
        coach_end = info_coach.find('</a>')
        coach_html = info_coach[:coach_end]
        coach = re.sub(self.rem_html, '', coach_html)
        coach = coach.strip()
        # assign score and coach to team
        if team == self.away_team.getTeamId():
            self.away_team.setScore(int(score))
            self.away_team.setCoach(coach)
        elif team == self.home_team.getTeamId():
            self.home_team.setScore(int(score))
            self.home_team.setCoach(coach)
            
        return
    
#     ##### PUBLIC HELPERS
    def extract_drives(self, text):
        is_home = False
        if text.find('home_drives') > -1:
            is_home = True

        start = text.find('<tbody>')
        drives = text[start:]
        
        last_qtr = 0
        
        while drives.find('<tr ') > -1:
            row_start = drives.find('<tr ')
            row_end = drives.find('</tr>')
            row = drives[row_start:row_end]
            
            num_start = row.find('data-stat="drive_num" >') + 23
            num_end = row.find('</th>')
            num = row[num_start:num_end]
            
            gm_drive = TeamGameDrive(self.getNextTmGmDriveId(), num)

            row = row[num_end + 5:]
            while row.find('data-stat="') > -1:
                lbl_start = row.find('data-stat="') + 11
                lbl_end = row.find('" >')
                label = row[lbl_start:lbl_end]

                if label.find('" csk="') > -1:
                    end = label.find('" csk="')
                    label = label[:end]

                data_end = row.find('</td>')
                data = row[lbl_end + 3:data_end]
                data = re.sub(self.rem_html, '', data)
                
                if label == "quarter":
                    if data:
                        last_qtr = data
                    else:
                        data = last_qtr
                
                gm_drive.mapToTeamGameDrive(label, data)

                row = row[data_end + 5:]
                
            if is_home:
                gm_drive.setTeamGameId(self.home_team.getId())
            else:
                gm_drive.setTeamGameId(self.away_team.getId())
                
            if gm_drive not in self.tm_gm_drives:
                self.tm_gm_drives[gm_drive.getId()] = gm_drive
            
            drives = drives[row_end + 5:]

    def extract_game_info(self):
        # loop through all rows of html
        while self._game_info.find('<tr >') > -1:
            # define row start
            row_start = self._game_info.find('<tr >')
            # define row end
            row_end = self._game_info.find('</tr>')
            row = self._game_info[row_start:row_end]
            # define game info cat
            head_start = row.find('="info" >') + 9
            head_end = row.find('</th>')
            header = row[head_start:head_end]
            # define game info stat
            stat_start = row.find('="stat" >') + 9
            stat_end = row.find('</td>')
            stat = row[stat_start:stat_end]
            # remove html from stats
            html = re.compile('<.*?>')
            stat = re.sub(html, '', stat)
            
            if header == "Won Toss":
                stat = stat.split(" ")
                won_toss = stat[0]
                # check if away team won toss
                if won_toss in self.away_team.getTeamId():
                    self.away_team.setWonToss(True)
                    if len(stat) > 1:
                        self.away_team.setTossDecision(stat[1])
                # check if home team won toss
                if won_toss in self.home_team.getTeamId():
                    self.home_team.setWonToss(True)
                    if len(stat) > 1:
                        self.home_team.setTossDecision(stat[1])
            elif header == "Roof":
                if stat.find("(") > -1:
                    temp = stat.split("(")
                    stat = temp[0]
                    roof = temp[1]
                    roof = roof.replace(")", "")
                    self.games[self.game.getId()].setRoofType(roof)
                self.stadiums[self.game.getStadiumId()].setRoof(stat)
            elif header == "Surface":
                self.stadiums[self.game.getStadiumId()].setSurface(stat.strip())
            elif header == "Weather":
                weather = stat.split(',')
                temp = 0
                humidity = 0.0
                wind = 0
                
                for item in weather:
                    if "degrees" in item:
                        temp = re.findall('[0-9]+', item)
                        temp = int(temp[0])
                    elif "relative humidity" in item:
                        humidity = re.findall('[0-9]+', item)
                        humidity = int(humidity[0])
                    elif "wind" in item and "no" not in item:
                        wind = re.findall('[0-9]+', item)
                        wind = int(wind[0])
                        
                gm_weather = GameWeather(self.getNextGmWeatherId(), temp, humidity, wind, self.game.getId())
                if gm_weather.getId() not in self.gm_weathers:
                    self.gm_weathers[gm_weather.getId()] = gm_weather 
                
            elif header == "Vegas Line":
                if stat == 'Pick':
                    self.away_team.setIsFavored(False);
                    self.away_team.setSpread(0);
                    
                    self.home_team.setIsFavored(False);
                    self.home_team.setSpread(0);
                else:
                    split = stat.find('-')
                    favored = stat[:split].strip()
                    
                    spread = float(stat[split:])
                    
                    if favored in self.away_team.getTeamId():
                        self.away_team.setIsFavored(True)
                        self.home_team.setIsFavored(False)
                        self.away_team.setSpread(spread)
                        self.home_team.setSpread(spread * -1)
                    
                    if favored in self.home_team.getTeamId():
                        self.home_team.setIsFavored(True)
                        self.away_team.setIsFavored(False)
                        self.home_team.setSpread(spread)
                        self.away_team.setSpread(spread * -1)     
                        
            elif header == "Over/Under":
                stat = stat.split(" ")
                stat = float(stat[0])
                
                self.away_team.setOverUnder(stat)
                self.home_team.setOverUnder(stat)
            
            self._game_info = self._game_info[row_end + 5:]

    def extract_officials(self):
        official_start = self._all_officials.find('<div class="table_container" id="div_officials">')
        officials = self._all_officials[official_start:]

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
                    if off not in self.officials:
                        self.officials[off] = Official(off)
                    
                    off_gm = OfficialGame(self.getNextOffGmId(), self.officials[off].getName(), self.game.getId(), off_pos)
                    if off_gm.getId() not in self.off_gms:
                        self.off_gms[off_gm.getId()] = off_gm

            officials = officials[row_end + 5:]

    def extract_plays(self):
        start = self._plays.find('<tbody>')
        plays = self._plays[start:]

        count = 0
        
        while plays.find('<tr ') > -1:
            count += 1
            row_start = plays.find('<tr ')
            row_end = plays.find('</tr>')
            row = plays[row_start:row_end]
            
            play = PlayByPlay(self.getNextPlayId(), count, self.game.getId())
            
            while row.find('data-stat="') > -1:
                if row.find('thead') < 0:
                    if row.find('class=" score" >') > -1:
                        skip = row.find('class=" score" >') + 16
                        row = row[skip:]
                    elif row.find('class="divider" >') > -1:
                        skip = row.find('class="divider" >') + 17
                        row = row[skip:]

                    lbl_start = row.find('data-stat="') + 11
                    lbl_end = row.find('" >')
                    label = row[lbl_start:lbl_end]

                    if label:
                        if label.find('" csk=') > -1:
                            end = label.find('" csk=')
                            label = label[:end]

                        data_end = row.find('</t')
                        data = row[lbl_end + 3:data_end]
                        data = re.sub(self.rem_html, '', data)
                        
                        play.mapToPlayByPlay(label, data)
            
                    row = row[data_end + 5:]
                else:
                    row = row[row_end + 5:]

            if play.detail:
                if play not in self.play_by_plays:
                    self.play_by_plays[play.getId()] = play
            else:
                self.play_by_play_id -= 1
                count -= 1
            
            plays = plays[row_end + 5:]

    def extract_player_stats(self, text):
        # Vars to hold player and team as we loop through rows
        team = None
        player_gm = None
        
        start = text.find('<tbody>')
        data = text[start:]
        
        while data.find('<tr >') > -1:
            row_start = data.find('<tr >')
            row_end = data.find('</tr>')
            row = data[row_start:row_end]
            
            while row.find('data-stat="') > -1:
                ds_start = row.find('data-stat="') + 11
                ds_end = row.find('" >')
                ds = row[ds_start:ds_end]
                
                stat_end = row.find('</t')
                stat = row[ds_end + 3:stat_end]
                stat = stat.replace('\n', '')
                stat = stat.replace("   ", '')
                
                if ds == "player":
                    id_start = stat.find('href="') + 6
                    id_end = stat.find(".htm")
                    id = stat[id_start:id_end]
                    id = re.sub('/.*/.*/','', id)
                    
                    html = re.compile('<.*?>')
                    stat = re.sub(html, '', stat)
                    
                    if stat == '':
                        stat = 0
                    
                    player = None
                       
                    # check if player id in master players list 
                    if id not in self.players:
                        player = Player(id, stat)
                        self.players[id] = player
                    else:
                        player = self.players[id]
                    
                        
                    if player:
                        # check if player_gm is in single game player_games list
                        if player.getId() not in self.player_games:
                            # create new player game object
                            player_gm = PlayerGame(self.getNextPlyrGmId(), player.getId())
                            # add to master list
                            self.player_gms[player_gm.getId()] = player_gm
                            # add to single game list with this id as value
                            self.player_games[player.getId()] = player_gm.getId()
                        # if player_gm exists for this game
                        else:
                            # get master list id from this game player_game list
                            player_gm_id = self.player_games[player.getId()]
                            # retrieve master player_gm
                            player_gm = self.player_gms[player_gm_id]
                        
                elif ds == "team":
                    html = re.compile('<.*?>')
                    stat = re.sub(html, '', stat)
                    
                    if stat == '':
                        stat = 0
                        
                    team = stat
                    # Set player team game
                    if team == self.teams[self.away_team.getTeamId()].getAbbrevPff():
                        player_gm.setGameId(self.away_team.getId())
                    elif team == self.teams[self.home_team.getTeamId()].getAbbrevPff():
                        player_gm.setGameId(self.home_team.getId())
                else:
                    html = re.compile('<.*?>')
                    stat = re.sub(html, '', stat)
                    
                    if stat == '':
                        stat = 0
                        
                    player_gm.mapToPlayerGame(ds, stat)
                
                row = row[stat_end + 5:]
            
            data = data[row_end + 5:]
                     
    def extract_scorebox(self):
        data = self._scorebox.split('<div class="media-item logo loader">')
        self.__extract_score_coach(data[1])
        self.__extract_score_coach(data[2])

    def extract_scorebox_meta(self):
        start = self._scorebox_meta.find('</div>') + 6
        info = self._scorebox_meta[start:]
        
        while info.find('<strong>') > -1:
            d_start = info.find('<strong>') + 8
            d_end = info.find('</div>')
            data = info[d_start:d_end]
            data = re.sub(self.rem_html, '', data)
            
            data = data.split(": ")
            label = data[0]
            stat = data[1]
            
            if label == "Attendance":
                stat = stat.replace(',' , '')
                self.game.setAttendance(int(stat.strip()))
            elif label == "Stadium":
                stadium_nm = stat.strip()
                if stadium_nm not in self.stadiums:
                    self.stadiums[stadium_nm] = Stadium(stadium_nm)
                self.game.setStadiumId(stadium_nm)
            elif label == "Start Time":
                self.__extract_time(stat.strip())
            elif label == "Time of Game":
                time = stat.strip()
                time = datetime.strptime(time, "%H:%M").time()
                self.game.setGameDuration(time)
                
            info = info[d_end + 6:]         

    def extract_scoring_plays(self):
        # trim to tbody
        start = self._all_scoring.find('<tbody>') + 7
        scores = self._all_scoring[start:]

        last_known_qtr = 0
        
        while scores.find('<tr >') > -1:
            play = ScoringPlay(self.getNextScoringPlayId())
            
            if play not in self.scoring_plays:
                self.scoring_plays[play.getId()] = play
            
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
            if qtr == "OT":
                play.setQtr(5)
            else:
                play.setQtr(int(qtr))
            
            time_start = row.find('data-stat="time" >') + 18
            time_end = row.find('</td>')
            time = row[time_start:time_end]
            play.setQtrTimeRem(datetime.strptime(time,"%M:%S").time())
            
            team_start = row.find('data-stat="team" >') + 18
            team = row[team_start:]
            team_end = team.find('</td>')
            team = team[:team_end]
            if team in self.away_team.getTeamId():
                play.setScoringTeamId(self.away_team.getId())
            if team in self.home_team.getTeamId():
                play.setScoringTeamId(self.home_team.getId())
            
            desc_start = row.find('data-stat="description" >') + 25
            desc = row[desc_start:]
            desc_end = desc.find('</td>')
            desc = desc[:desc_end]
            desc = re.sub(self.rem_html, '', desc)
            play.setDescription(desc)
            
            a_scr_start = row.find('data-stat="vis_team_score" >') + 28
            a_scr = row[a_scr_start:]
            a_scr_end = a_scr.find('</td>')
            a_scr = a_scr[:a_scr_end]
            play.setAwayScore(int(a_scr))
            
            h_scr_start = row.find('data-stat="home_team_score" >') + 29
            h_scr = row[h_scr_start:]
            h_scr_end = h_scr.find('</td>')
            h_scr = h_scr[:h_scr_end]
            play.setHomeScore(int(h_scr))
            
            scores = scores[row_end + 5:]

    def extract_snaps(self, text):
    
        start = text.find('<tbody>')
        snaps = text[start:]
        
        while snaps.find('<tr >') > -1:
            row_start = snaps.find('<tr >')
            row_end = snaps.find('</tr>')
            row = snaps[row_start:row_end]

            id_start = row.find('append-csv="') + 12
            id = row[id_start:]
            id_end = id.find('" ')
            id = id[:id_end]
            
            name_start = row.find('data-stat="player" >') + 20
            name_end = row.find('</a>')
            name = row[name_start:name_end]

            html = re.compile('<.*?>')
            name = re.sub(html, '', name)

            player = None

            if id not in self.players:
                player = Player(id, name)
                self.players[player.getId()] = player
            else:
                player = self.players[id]

            player_gm = None

            if player:
                # check if player_gm is in single game player_games list
                if player.getId() not in self.player_games:
                    # create new player game object
                    player_gm = PlayerGame(self.getNextPlyrGmId(), player.getId())
                    # Set player team game
                    if text.find('all_home_starters'):
                        player_gm.setGameId(self.home_team.getId())
                    elif text.find('all_vis_starters'):
                        player_gm.setGameId(self.away_team.getId())
                    # add to master list
                    self.player_gms[player_gm.getId()] = player_gm
                    # add to single game list with this id as value
                    self.player_games[player.getId()] = player_gm.getId()
                # if player_gm exists for this game
                else:
                    # get master list id from this game player_game list
                    player_gm_id = self.player_games[player.getId()]
                    # retrieve master player_gm
                    player_gm = self.player_gms[player_gm_id]

            row = row[name_end + 4:]
            player_gm_snap = None

            if player and player_gm:
                player_gm_snap = PlayerGameSnap(self.getNextPlayerGmSnapId(), player_gm.getId())

            while row.find('data-stat="') > -1:
                lbl_start = row.find('data-stat="') + 11
                lbl_end = row.find('" >')
                label = row[lbl_start:lbl_end]

                data_end = row.find('</td>')
                data = row[lbl_end + 3:data_end]

                player_gm_snap.mapToPlayerGmSnap(label, data)

                row = row[data_end + 5:]

            if player_gm_snap:
                if player_gm_snap not in self.player_gm_snaps:
                    self.player_gm_snaps[player_gm_snap.getId()] = player_gm_snap
            else:
                print(f"Cannot add player_gm_snap")
            
            snaps = snaps[row_end + 5:]

    def extract_starters(self, text):
        start = text.find('<tbody>')
        starters = text[start:]
        
        while starters.find('<tr ') > -1:
            player = None
            
            row_start = starters.find('<tr ')
            row_end = starters.find('</tr>')
            row = starters[row_start:row_end]
            
            id_start = row.find('append-csv="') + 12
            id = row[id_start:]
            id_end = id.find('" ')
            id = id[:id_end]
            
            name_start = row.find('data-stat="player" >') + 20
            name_end = row.find('</a>')
            name = row[name_start:name_end]

            html = re.compile('<.*?>')
            name = re.sub(html, '', name)
            
            if id not in self.players:
                player = Player(id, name)
                self.players[player.getId()] = player
            else:
                player = self.players[id]

            pos_start = row.find('data-stat="pos" >') + 17
            pos_end = row.find('</td>')
            pos = row[pos_start:pos_end]
            
            if player:
                player_gm = None
                # check if player_gm is in single game player_games list
                if player.getId() not in self.player_games:
                    # create new player game object
                    player_gm = PlayerGame(self.getNextPlyrGmId(), player.getId())
                    # set player team game
                    if text.find('all_home_starters'):
                        player_gm.setGameId(self.home_team.getId())
                    elif text.find('all_vis_starters'):
                        player_gm.setGameId(self.away_team.getId())
                    # add to master list
                    self.player_gms[player_gm.getId()] = player_gm
                    # add to single game list with this id as value
                    self.player_games[player.getId()] = player_gm.getId()
                # if player_gm exists for this game
                else:
                    # get master list id from this game player_game list
                    player_gm_id = self.player_games[player.getId()]
                    # retrieve master player_gm
                    player_gm = self.player_gms[player_gm_id]
                    
                player_gm.is_starter = True
                player_gm.starting_pos = pos

            starters = starters[row_end + 5:]

    def extract_team_stats(self):
        start = self._all_team_stats.find('<tbody')
        text = self._all_team_stats[start:]
        
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
            self.away_team.mapToTmGm(label, vis_stat)
            
            home_start = row.find('home_stat" >') + 12
            home_end = row.find('</td></tr>') - 4
            home_stat = row[home_start:home_end]
            self.home_team.mapToTmGm(label, home_stat)
            
            text = text[row_end + 5:]
            
    def getNextGmWeatherId(self):
        temp = self.gm_weather_id
        self.gm_weather_id += 1
        return temp
    
    def getNextOffGmId(self):
        temp = self.off_gm_id
        self.off_gm_id += 1
        return temp
    
    def getNextPlyrGmId(self):
        temp = self.player_gm_id
        self.player_gm_id += 1
        return temp

    def getNextPlayerGmSnapId(self):
        temp = self.player_gm_snap_id
        self.player_gm_snap_id += 1
        return temp
    
    def getNextScoringPlayId(self):
        temp = self.scoring_play_id
        self.scoring_play_id += 1
        return temp
    
    def getNextTmGmId(self):
        temp = self.tm_game_id
        self.tm_game_id += 1
        return temp
    
    def getNextTmGmDriveId(self):
        temp = self.team_gm_drive_id
        self.team_gm_drive_id += 1
        return temp
    
    def getNextPlayId(self):
        temp = self.play_by_play_id
        self.play_by_play_id += 1
        return temp

    def loadCsvGames(self, file):
        max_date = "20180906"
        with open(file, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader)

            for row in reader:
                id = row[0]
                date = row[1]
                season = row[2]
                week = row[3]
                attendance = row[4]
                stadium_id = row[5]
                game_dur = row[6]
                roof_type = row[7]

                game = Game(
                    date,
                    week,
                    id[-6:-3],
                    id[:-3]
                )

                # ensure we keep existing id
                game.setId(id)

                game.setDate(date)
                game.setSeason(season)
                game.setWeek(week)
                game.setAttendance(attendance)
                game.setStadiumId(stadium_id)
                game.setGameDuration(game_dur)
                game.setRoofType(roof_type)

                if game not in self.games:
                    self.games[id] = game

                max_comp_str = datetime.strftime(game.getDate().date(), "%Y%m%d")
                if max_comp_str > max_date:
                    max_date = max_comp_str

        return max_date

    def loadCsvGameWeather(self, file):
        with open(file, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader)
            
            for row in reader:
                id = row[0]
                temp = row[1]
                humidity = row[2]
                wind = row[3]
                game_id = row[4]

                gm_weather = GameWeather(id, temp, humidity, wind, game_id)
                gm_weather.setId(id)
                gm_weather.setTemp(temp)
                gm_weather.setHumidity(humidity)
                gm_weather.setWind(wind)
                gm_weather.setGameId(game_id)

                comp_id = gm_weather.getId()

                if comp_id not in self.gm_weathers:
                    self.gm_weathers[id] = gm_weather

                if comp_id > self.gm_weather_id:
                    self.gm_weather_id = comp_id + 1
    
    def loadCsvOfficials(self, file):
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            
            for row in reader:
                name = row[0]
                official = Official(name)
                
                if official not in self.officials:
                    self.officials[name] = official
                    
    def loadCsvOfficialGames(self, file):
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            
            for row in reader:
                id = row[0]
                position = row[1]
                name = row[2]
                game_id = row[3]
                
                official_game = OfficialGame(id, name, game_id, position)
                official_game.setId(id)
                
                id = official_game.getId()
                if id not in self.off_gms:
                    self.off_gms[id] = official_game
                    
                if id > self.off_gm_id:
                    self.off_gm_id = id + 1
    
    def parseGame(self):
        # extract scores and coaches
        self.extract_scorebox()
        # extract scorebox meta
        self.extract_scorebox_meta()
        ### OPTIMIZATION: Starting from here can be ran concurrently
        # extract all scoring
        self.extract_scoring_plays()
        # extract basic game info
        self.extract_game_info()
        # extract game officials
        self.extract_officials()
        # extract team stats
        self.extract_team_stats()
        # extract player offense
        self.extract_player_stats(self._all_player_off)
        # extract player defense
        self.extract_player_stats(self._all_player_def)
        # extract player returns
        self.extract_player_stats(self._all_returns)
        # extract player kicking/punting
        self.extract_player_stats(self._all_kicking)
        # extract advanced passing
        self.extract_player_stats(self._passing_adv)
        # extract advanced rushing
        self.extract_player_stats(self._rushing_adv)
        # extract advanced receiving
        self.extract_player_stats(self._receiving_adv)
        # extract advanced defense
        self.extract_player_stats(self._defense_adv)
        # extract home starters
        self.extract_starters(self._home_starters)
        # extract away starters
        self.extract_starters(self._away_starters)
        # extract home snaps
        self.extract_snaps(self._home_snaps)
        # extract away snaps
        self.extract_snaps(self._away_snaps)
        # extract home drives
        self.extract_drives(self._home_drives)
        # extract away drives
        self.extract_drives(self._away_drives)
        # extract play by plays
        self.extract_plays()
        
        # Rest single game dicts
        self.game = {}
        self.away_team = {}
        self.home_team = {}
        self.player_games = {}
        self.starters = {}
    
    # Remove 'st', 'nd', 'rd', 'th', from date
    def remove_date_formals(self, date):
        formals = ("st", "nd", "rd", "th")
        for ending in formals:
            idx = date.find(ending)
            if idx > -1:
                date = date[:idx] + date[idx+2:]
        
        return date
    
    # write all files
    def writeFiles(self):
        with open("csv/stadiums.csv", "w") as file:
            fieldnames = [
                'name', 
                'city', 
                'state', 
                'surface', 
                'roof'
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for stadium in self.stadiums:
                writer.writerow(self.stadiums[stadium].getInfo())
         
        with open("csv/games.csv", "w") as file:
            fieldnames = [
                "id", 
                "date", 
                "season", 
                "week", 
                "attendance", 
                "stadium_id", 
                "game_duration", 
                "roof_type"
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for game in self.games:
                writer.writerow(self.games[game].getInfo())
                
        with open("csv/teams.csv", "w") as file:
            fieldnames = [
                "name", 
                "locale", 
                "mascot", 
                "abbrev_pff"
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for team in self.teams:
                writer.writerow(self.teams[team].getInfo())
                
        with open("csv/team_games.csv", "w") as file:
            fieldnames = [
                "id", 
                "team_id", 
                "game_id", 
                "won_toss", 
                "toss_decision", 
                "is_home", 
                "is_favored",
                "spread", 
                "over_under", 
                "first_downs", 
                "rush_atts", 
                "rush_yds", 
                "rush_tds", 
                "pass_comps",
                "pass_atts", 
                "pass_yds", 
                "pass_tds", 
                "pass_ints", 
                "sacked", 
                "sack_yds_lost", 
                "net_pass_yds",
                "total_yds", 
                "fumbles", 
                "fumbles_lost", 
                "turnovers", 
                "penalties", 
                "penalty_yds",
                "third_down_atts", 
                "third_down_convs", 
                "fourth_down_atts", 
                "fourth_down_convs", 
                "possession_time",
                "coach",
                "score"
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for team in self.team_gms:
                writer.writerow(self.team_gms[team].getInfo())

        with open("csv/team_game_drives.csv", "w") as file:
            fieldnames = [
                'id', 
                'drive_num', 
                'quarter', 
                'time_start', 
                'yd_start', 
                'num_plays', 
                'drive_time', 
                'net_yds', 
                'drive_result', 
                'team_game_id'
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for drive in self.tm_gm_drives:
                writer.writerow(self.tm_gm_drives[drive].getInfo())       

        with open("csv/scoring_plays.csv", "w") as file:
            fieldnames = [
                'id', 
                'scoring_team_id',
                'home_score',  
                'away_score', 
                'qtr', 
                'qtr_time_rem', 
                'description'
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for scoring_play in self.scoring_plays:
                writer.writerow(self.scoring_plays[scoring_play].getInfo())
            
        with open("csv/gm_weathers.csv", "w") as file:
            fieldnames = [
                'id', 
                'temp',
                'humidity', 
                'wind', 
                'game_id'
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for gm_weather in self.gm_weathers:
                writer.writerow(self.gm_weathers[gm_weather].getInfo())
                
        with open("csv/officials.csv", "w") as file:
            fieldnames = [
                'name', 
                'career_start', 
                'career_end', 
                'jersey_num'
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for official in self.officials:
                writer.writerow(self.officials[official].getInfo())
                
        with open("csv/off_gms.csv", "w") as file:
            fieldnames = [
                'id', 
                'ref_position', 
                'official_id', 
                'game_id'
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for off_gm in self.off_gms:
                writer.writerow(self.off_gms[off_gm].getInfo())
                
        with open("csv/players.csv", "w") as file:
            fieldnames = [
                'id', 
                'name', 
                'college', 
                'dob', 
                'career_start', 
                'career_end'
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for player in self.players:
                writer.writerow(self.players[player].getInfo())
                
        with open("csv/player_games.csv", "w") as file:
            fieldnames = [
                'id', 
                'player_id', 
                'tmGame_id', 
                'pass_comps', 
                'pass_atts', 
                'pass_yds',
                'pass_tds', 
                'pass_ints', 
                'sacked', 
                'sack_yds_lost', 
                'long_pass', 
                'pass_rating',
                'rush_atts', 
                'rush_yds', 
                'rush_tds', 
                'long_rush', 
                'rec_targets', 
                'recs',
                'rec_yds', 
                'rec_tds', 
                'long_rec', 
                'fumbles', 
                'fumbles_lost', 
                'def_ints',
                'def_int_yds', 
                'def_int_tds', 
                'long_def_int', 
                'pass_defs', 
                'def_sacks',
                'def_tack_combined', 
                'def_tack_solo', 
                'def_tack_assists', 
                'def_tack_for_loss',
                'def_qb_hits', 
                'fumble_recs', 
                'fumble_rec_yds', 
                'fumble_rec_tds', 
                'forced_fumbles',
                'kick_rets', 
                'kick_ret_yds', 
                'avg_kick_ret', 
                'kick_ret_tds', 
                'long_kick_ret',
                'punt_rets', 
                'punt_ret_yds', 
                'avg_punt_ret', 
                'punt_ret_tds', 
                'long_punt_ret',
                'xpm', 
                'xpa', 
                'fgm', 
                'fga', 
                'punts', 
                'punt_yds', 
                'avg_punt', 
                'long_punt',
                'pass_first_downs', 
                'pass_first_down_pct', 
                'pass_tgt_yds', 
                'pass_tgt_yds_per_att', 
                'pass_air_yds',
                'pass_air_yds_per_comp', 
                'pass_air_yds_per_att', 
                'pass_yac', 
                'pass_yac_per_comp',
                'pass_drops', 
                'pass_drop_pct', 
                'pass_poor_throws', 
                'pass_poor_throw_pct', 
                'pass_blitzed',
                'pass_hurried', 
                'pass_hits', 
                'pass_pressured', 
                'pass_pressured_pct', 
                'rush_scrambles',
                'rush_scrambles_yds_per_att', 
                'rush_first_down', 
                'rush_yds_before_contact', 
                'rush_yds_bc_per_rush',
                'rush_yac', 
                'rush_yac_per_rush', 
                'rush_broken_tacks', 
                'rush_broken_tacks_per_rush',
                'rec_first_down', 
                'rec_air_yds', 
                'rec_air_yds_per_rec', 
                'rec_yac', 
                'rec_yac_per_rec',
                'rec_adot', 
                'rec_broken_tacks', 
                'rec_broken_tacks_per_rec', 
                'rec_drops', 
                'rec_drop_pct',
                'rec_target_int', 
                'recPassRating', 
                'def_targets', 
                'def_comps', 
                'def_comp_pct',
                'def_comp_yds', 
                'def_yds_per_comp', 
                'def_yds_per_target', 
                'def_comp_tds', 
                'def_pass_rating',
                'def_tgt_yds_per_att', 
                'def_air_yds', 
                'def_yac', 
                'blitzes', 
                'qb_hurries', 
                'qb_knockdown',
                'pressures', 
                'tacks_missed', 
                'tacks_missed_pct', 
                'is_starter', 
                'starting_pos'
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for player_gm in self.player_gms:
                writer.writerow(self.player_gms[player_gm].getInfo())

        with open("csv/player_game_snaps.csv", "w") as file:
            fieldnames = [
                'id', 
                'player_game_id', 
                'start_pos', 
                'off_snaps', 
                'off_snap_pct', 
                'def_snaps', 
                'def_snap_pct', 
                'st_snaps', 
                'st_snap_pct'
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for player in self.player_gm_snaps:
                writer.writerow(self.player_gm_snaps[player].getInfo())
                   
        with open("csv/play_by_plays.csv", "w") as file:
            fieldnames = [
                "id", 
                "qtr", 
                "qtr_time_rem", 
                "down", 
                "yds_to_go", 
                "yd_start",
                "score_away", 
                "score_home", 
                "detail", 
                "exp_pts_before", 
                "exp_pts_after",
                "seq", 
                "game_id"
            ]
            writer = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for play in self.play_by_plays:
                writer.writerow(self.play_by_plays[play].getInfo())
            
        with open("csv/errors.csv", "w") as file:
            writer = csv.writer(file, delimiter=',')
            for url in self.errors:
                writer.writerow([url])
        