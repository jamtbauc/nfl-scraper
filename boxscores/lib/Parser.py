import json
import re
from lib.PlayerWhole import Player
from lib.Game import Game
from lib.Official import Official
from lib.OfficialGame import OfficialGame
from lib.ScoringPlay import ScoringPlay
from lib.Stadium import Stadium
from lib.Team import Team
from lib.TeamGame import TeamGame
from lib.GameWeather import GameWeather
from datetime import datetime

class Parser:
    rem_html = re.compile('<.*?>')
    
    # hold all objects
    teams = {}
    games = {}
    stadiums = {}
    scoring_plays = {}
    gm_weathers = {}
    officials = {}
    off_gms = {}
    
    # hold id counters
    tm_game_id = 1
    scoring_play_id = 1
    gm_weather_id = 1
    off_gm_id = 1
    
    
    def __init__(self):
        # define text blocks
        self._matchup = ""
        self._scorebox = ""
        self._scorebox_meta = ""
        self._all_scoring = ""
        self._game_info = ""
        self._all_officials = ""
        self._all_team_stats = ""
        self._all_player_off = ""
        self._all_player_def = ""
        self._all_returns = ""
        self._all_kicking = ""
        self._passing_adv = ""
        self._rushing_adv = ""
        self._receiving_adv = ""
        self._defense_adv = ""
        self._home_starters = ""
        self._away_starters = ""
        self._home_snaps = ""
        self._away_snaps = ""
        self._home_drives = ""
        self._away_drives = ""
        self._plays = ""
        
        # define objects specific to one game
        self.game = ""
        self.away_team = ""
        self.home_team = ""
    
    ### HELPER METHODS 
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
        self._home_drives
        
    def setAwayDrives(self, text):
        self._away_drives
        
    def setPlays(self, text):
        self._plays = text
        
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
          
        # get away team name
        away_name = matchup[0].strip()
        # if team doesn't already exist in teams list, create new team
        if away_name not in self.teams:
            away = Team(away_name)
            self.teams[away_name] = away
        
        # get home team name
        home_name = matchup[1].strip()
        # if team doesn't exist in teams list, create new team
        if home_name not in self.teams:
            home = Team(home_name)
            self.teams[home_name] = home
        
        date_trimmed = self.remove_date_formals(date_str)
        date = datetime.strptime(date_trimmed, "%B %d, %Y")
        
        # create game object
        self.game = Game(date, week, away.getAbbrevPff(), home.getAbbrevPff())
        # add game to game list
        if self.game.getId() not in self.games:
            self.games[self.game.getId()] = self.game
        
        # create team game objects
        self.away_team = TeamGame(self.getNextTmGmId(), away_name, self.game.getId(), False)
        self.home_team = TeamGame(self.getNextTmGmId(), home_name, self.game.getId(), True)
        
        return date.date()
    
    ##### PRIVATE HELPERS 
    def __extract_time(self, time_str):
        am_pm = time_str[-2:]
        if am_pm == "am":
            am_pm = "AM"
        else:
            am_pm = "PM"
            
        time_str = time_str[:-2] + am_pm
        
        date_str = self.game.getDate().strftime("%B %m, %Y")
        date_str += " " + time_str
        
        self.game.setDate(datetime.strptime(date_str, "%B %m, %Y %I:%M%p"))

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
            self.away_team.setScore(score)
            self.away_team.setCoach(coach)
        elif team == self.home_team.getTeamId():
            self.home_team.setScore(score)
            self.home_team.setCoach(coach)
            
        return
    
    ##### PUBLIC HELPERS
    def extract_drives(self, text):
        is_home = False
        if text.find('home_drives') > -1:
            is_home = True

        start = text.find('<tbody>')
        drives = text[start:]
        
        while drives.find('<tr ') > -1:
            row_start = drives.find('<tr ')
            row_end = drives.find('</tr>')
            row = drives[row_start:row_end]
            
            num_start = row.find('data-stat="drive_num" >') + 23
            num_end = row.find('</th>')
            num = row[num_start:num_end]

            row = row[num_end + 5:]
            drive = {}
            drive["drive_num"] = num
            drive["game_id"] = self.__id
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
                
                drive[label] = data

                row = row[data_end + 5:]
                
            if is_home:
                self.__home_drives.append(drive)
            else:
                self.__away_drives.append(drive)
            
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
                self.stadiums[self.game.getStadiumId()].setRoof(stat)
            elif header == "Surface":
                self.stadiums[self.game.getStadiumId()].setSurface(stat.strip())
            elif header == "Weather":
                weather = stat.split(',')
                
                temp = re.findall('[0-9]+', weather[0])
                
                humidity = re.findall('[0-9]+', weather[1])
                
                gm_weather = GameWeather(self.getNextGmWeatherId(), int(temp[0]), int(humidity[0]), self.game.getId())
                if gm_weather.getId() not in self.gm_weathers:
                    self.gm_weathers[gm_weather.getId()] = gm_weather
                
                if weather[2]:
                    wind = re.findall('[0-9]', weather[2])
                    gm_weather.setWind(int(wind[0]))
                
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

    def extract_plays(self, text):
        start = text.find('<tbody>')
        plays = text[start:]

        count = 0
        
        while plays.find('<tr ') > -1:
            count += 1
            row_start = plays.find('<tr ')
            row_end = plays.find('</tr>')
            row = plays[row_start:row_end]
            
            play = {}
            
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
                        
                        play[label] = data
            
                    row = row[data_end + 5:]
                else:
                    row = row[row_end + 5:]

            if play:
                self.__play_by_play.append(play)
            
            plays = plays[row_end + 5:]

    def extract_player_stats(self, text):
        # Vars to hold player and team as we loop through rows
        team = ""
        player = ""
        
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
                            plyr = Player(player, self.__away_id, self.__id)
                            self.__away_players[player] = plyr.get_stats()
                        
                        self.__away_players[player][ds] = stat
                    elif self.abbrevs[self.__home] == team:
                        if player not in self.__home_players:
                            plyr = Player(player, self.__home_id, self.__id)
                            self.__home_players[player] = plyr.get_stats()
                        
                        self.__home_players[player][ds] = stat
                
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
                time = datetime.strptime(time, "%H:%M").time().isoformat()
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
        is_home = False
        if text.find('home_snap') > -1:
            is_home = True

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

            row = row[player_end + 4:]

            while row.find('data-stat="') > -1:
                lbl_start = row.find('data-stat="') + 11
                lbl_end = row.find('" >')
                label = row[lbl_start:lbl_end]

                data_end = row.find('</td>')
                data = row[lbl_end + 3:data_end]

                if is_home:
                    if player not in self.__home_players:
                        plyr = Player(player, self.__home_id, self.__id)
                        self.__home_players[player] = plyr.get_stats()
                    self.__home_players[player]["snaps"][label] = data
                else:
                    if player not in self.__away_players:
                        plyr = Player(player, self.__away_id, self.__id)
                        self.__away_players[player] = plyr.get_stats()
                    self.__away_players[player]["snaps"][label] = data

                row = row[data_end + 5:]
            
            snaps = snaps[row_end + 5:]

    def extract_starters(self, text):
        start = text.find('<tbody>')
        starters = text[start:]
        
        while starters.find('<tr ') > -1:
            row_start = starters.find('<tr ')
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
                if text.find('home_starters') > -1:
                    if player not in self.__home_players:
                        plyr = Player(player, self.__home_id, self.__id)
                        self.__home_players[player] = plyr.get_stats()
                    self.__home_players[player]["is_starting"] = True
                    self.__home_players[player]["starting_pos"] = pos
                elif text.find('vis_starters') > -1:
                    if player not in self.__away_players:
                        plyr = Player(player, self.__away_id, self.__id)
                        self.__away_players[player] = plyr.get_stats()
                    self.__away_players[player]["is_starting"] = True
                    self.__away_players[player]["starting_pos"] = pos
            
            starters = starters[row_end + 5:]

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
            
    def get_date(self):
        return self.__date
    
    def get_game_dict(self):
        game = {
                    "id": self.__id,
                    "week": self.__week,
                    "date": self.__date.date().isoformat(),
                    "away": {
                        "id": self.__away_id,
                        "game_id": self.__id,
                        "team": self.__away,
                        "abbrev_pff": self.abbrevs[self.__away],
                        "score": self.__away_score,
                        "coach": self.__away_coach,
                        "team_stats": self.__away_team_stats,
                        "players": self.__away_players,
                        "drives": self.__away_drives
                        },
                    "home": {
                        "id": self.__home_id,
                        "game_id": self.__id,
                        "team": self.__home,
                        "abbrev_pff": self.abbrevs[self.__home],
                        "score": self.__home_score,
                        "coach": self.__home_coach,
                        "team_stats": self.__home_team_stats,
                        "players": self.__home_players,
                        "drives": self.__home_drives
                        },
                    "start_time": self.__date.time().isoformat(),
                    "stadium": {
                        "name": self.__stadium,
                        "roof_type": self.__roof,
                        "surface": self.__surface
                    },
                    "attendance": self.__attendance,
                    "scoring_plays": self.__scoring_plays,
                    "won_toss": self.__won_toss,
                    "toss_decision": self.__toss_decision,
                    "duration": self.__game_duration,
                    "weather": {
                        "temp" : self.__temp,
                        "humidity": self.__humidity,
                        "wind": self.__wind
                    },
                    "vegas": {
                        "favored": self.__favored_team,
                        "spread": self.__spread,
                        "over/under": self.__over_under
                    },
                    "officials": self.__officials,
                    "play_by_play": self.__play_by_play
                }
        
        return game
    
    def get_game_id(self):
        return self.__id
    
    def get_game_json(self):
        return json.dumps(self.get_game_dict(), indent=4)
    
    ### Printing functions
    def get_away_json(self):
        away = {
                    "id": self.__away_id,
                    "game_id": self.__id,
                    "team": self.__away,
                    "abbrev_pff": self.abbrevs[self.__away],
                    "score": self.__away_score,
                    "coach": self.__away_coach,
                    "drives": self.__away_drives
                }
        
        return json.dumps(away, indent=4)
    
    def get_away_drives(self):
        return json.dumps(self.__away_drives, indent=4)
    
    def get_away_players(self):        
        return json.dumps(self.__away_players, indent = 4)
    
    def get_away_tm_stats_json(self):
        return self.__away_team_stats
    
    def get_game_obj_json(self):
        game = {
                    "id": self.__id,
                    "week": self.__week,
                    "date": self.__date.date().isoformat(),
                    "start_time": self.__date.time().isoformat(),
                    "attendance": self.__attendance,
                    "won_toss": self.__won_toss,
                    "toss_decision": self.__toss_decision,
                    "duration": self.__game_duration
                }
        
        return json.dumps(game, indent=4)
    
    def getNextGmWeatherId(self):
        temp = self.gm_weather_id
        self.gm_weather_id += 1
        return temp
    
    def getNextOffGmId(self):
        temp = self.off_gm_id
        self.off_gm_id += 1
        return temp
    
    def getNextScoringPlayId(self):
        temp = self.scoring_play_id
        self.scoring_play_id += 1
        return temp
    
    def getNextTmGmId(self):
        temp = self.tm_game_id
        self.tm_game_id += 1
        return temp
    
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
        # # extract player offense
        # self.extract_player_stats()
        # # extract player defense
        # self.extract_player_stats()
        # # extract player returns
        # self.extract_player_stats()
        # # extract player kicking/punting
        # self.extract_player_stats()
        # # extract advanced passing
        # self.extract_player_stats()
        # # extract advanced rushing
        # self.extract_player_stats()
        # # extract advanced receiving
        # self.extract_player_stats()
        # # extract advanced defense
        # self.extract_player_stats()
        # # extract home starters
        # self.extract_starters()
        # # extract away starters
        # self.extract_starters()
        # # extract home snaps
        # self.extract_snaps()
        # # extract away snaps
        # self.extract_snaps()
        # # extract home drives
        # self.extract_drives()
        # # extract away drives
        # self.extract_drives()
        # # extract play by plays
        # self.extract_plays()
        
        print(self.away_team.getInfo())
        print(self.game.getInfo())
        print(self.stadiums[self.game.getStadiumId()].getInfo())
        print(self.scoring_plays[1].getInfo())
        print(self.gm_weathers[1].getInfo())
        print(self.officials["Carl Cheffers"].getInfo())
        print(self.off_gms[1].getInfo())
    
    # Remove 'st', 'nd', 'rd', 'th', from date
    def remove_date_formals(self, date):
        formals = ("st", "nd", "rd", "th")
        for ending in formals:
            idx = date.find(ending)
            if idx > -1:
                date = date[:idx] + date[idx+2:]
        
        return date
        