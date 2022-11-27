from datetime import datetime
import json

class TeamGame:
    def __init__(self, id, name, gameId, isHome):
        self.id = id
        self.team_id = name
        self.game_id = gameId
        self.won_toss = False
        self.toss_decision = None
        self.is_home = isHome
        self.is_favored = None
        self.spread = None
        self.over_under = None
        self.first_downs = None
        self.rush_atts = None
        self.rush_yds = None
        self.rush_tds = None
        self.pass_comps = None
        self.pass_atts = None
        self.pass_yds = None
        self.pass_tds = None
        self.pass_ints = None
        self.sacked = None
        self.sack_yds_lost = None
        self.net_pass_yds = None
        self.total_yds = None
        self.fumbles = None
        self.fumbles_lost = None
        self.turnovers = None
        self.penalties = None
        self.penalty_yds = None
        self.third_down_atts = None
        self.third_down_convs = None
        self.fourth_down_atts = None
        self.fourth_down_convs = None
        self.possession_time = None
        self.coach = None
        self.score = None
        
    def getCoach(self):
        return self.coach
    
    def setCoach(self, value):
        self.coach = value
        
    def getFirstDowns(self):
        return self.first_downs
    
    def setFirstDowns(self, firsts):
        self.first_downs = firsts
    
    def getFourthDownAtts(self):
        return self.fourth_down_atts
    
    def setFourthDownAtts(self, atts):
        self.fourth_down_atts = atts
    
    def getFourthDownConvs(self):
        return self.fourth_down_convs
    
    def setFourthDownConvs(self, convs):
        self.fourth_down_convs = convs
    
    def getFumbles(self):
        return self.fumbles
    
    def setFumbles(self, fumbs):
        self.fumbles = fumbs
    
    def getFumblesLost(self):
        return self.fumbles_lost
    
    def setFumblesLost(self, fumbsLost):
        self.fumbles_lost = fumbsLost
    
    def getGameId(self):
        return self.game_id
    
    def setGameId(self, id):
        self.game_id = id
    
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
    
    def getIsFavored(self):
        return self.is_favored
    
    def setIsFavored(self, isFavored):
        self.is_favored = isFavored
    
    def getIsHome(self):
        return self.is_home
    
    def setIsHome(self, isHome):
        self.is_home = isHome
    
    def getNetPassYds(self):
        return self.net_pass_yds
    
    def setNetPassYds(self, yds):
        self.net_pass_yds = yds
    
    def getOverUnder(self):
        return self.over_under
    
    def setOverUnder(self, overUnder):
        self.over_under = overUnder
    
    def getPassAtts(self):
        return self.pass_atts
    
    def setPassAtts(self, atts):
        self.pass_atts = atts
    
    def getPassComps(self):
        return self.pass_comps
    
    def setPassComps(self, comps):
        self.pass_comps = comps
    
    def getPassInts(self):
        return self.pass_ints
    
    def setPassInts(self, ints):
        self.pass_ints = ints
    
    def getPassTds(self):
        return self.pass_tds
    
    def setPassTds(self, tds):
        self.pass_tds = tds
    
    def getPassYds(self):
        return self.pass_yds
    
    def setPassYds(self, yds):
        self.pass_yds = yds
    
    def getPenalties(self):
        return self.penalties
    
    def setPenalites(self, penalties):
        self.penalties = penalties
    
    def getPenaltyYds(self):
        return self.penalty_yds
    
    def setPenaltyYds(self, penYds):
        self.penalty_yds = penYds
    
    def getPossessionTime(self):
        return self.possession_time
    
    def setPossessionTime(self, time):
        self.possession_time = time
    
    def getRushAtts(self):
        return self.rush_atts
    
    def setRushAtts(self, atts):
        self.rush_atts = atts
    
    def getRushTds(self):
        return self.rush_tds
    
    def setRushTds(self, tds):
        self.rush_tds = tds
    
    def getRushYds(self):
        return self.rush_yds
    
    def setRushYds(self, yds):
        self.rush_yds = yds
    
    def getSackYdsLost(self):
        return self.sack_yds_lost
    
    def setSackYdsLost(self, ydsLost):
        self.sack_yds_lost = ydsLost
    
    def getSacked(self):
        return self.sacked
    
    def setSacked(self, sacks):
        self.sacked = sacks
        
    def getScore(self):
        return self.score
    
    def setScore(self, value):
        self.score = value
    
    def getSpread(self):
        return self.spread
    
    def setSpread(self, spread):
        self.spread = spread
    
    def getTeamId(self):
        return self.team_id
    
    def setTeamId(self, id):
        self.team_id = id
    
    def getThirdDownAtts(self):
        return self.third_down_atts
    
    def setThirdDownAtts(self, atts):
        self.third_down_atts = atts
    
    def getThirdDownConvs(self):
        return self.third_down_convs
    
    def setThirdDownConvs(self, convs):
        self.third_down_convs = convs
    
    def getTossDecision(self):
        return self.toss_decision
    
    def setTossDecision(self, decision):
        self.toss_decision = decision
    
    def getTotalYds(self):
        return self.total_yds
    
    def setTotalYds(self, yds):
        self.total_yds = yds
    
    def getTurnovers(self):
        return self.turnovers
    
    def setTurnovers(self, turnovers):
        self.turnovers = turnovers
    
    def getWonToss(self):
        return self.won_toss
    
    def setWonToss(self, didWin):
        self.won_toss = didWin
        
    def mapToTmGm(self, label, value):
        if label == "First Downs":
            self.setFirstDowns(int(value))
        elif label == "Rush-Yds-TDs":
            value = value.split('-', 1)
            atts = value[0]
            right = value[1].rsplit('-', 1)
            print(right)
            self.setRushAtts(int(atts))
            self.setRushYds(int(right[0]))
            self.setRushTds(int(right[1]))
        elif label == "Cmp-Att-Yd-TD-INT":
            stats = value.split('-')
            self.setPassComps(int(stats[0]))
            self.setPassAtts(int(stats[1]))
            self.setPassYds(int(stats[2]))
            self.setPassTds(int(stats[3]))
            self.setPassInts(int(stats[4]))
        elif label == "Sacked-Yards":
            stats = value.split('-')
            self.setSacked(int(stats[0]))
            self.setSackYdsLost(int(stats[1]))
        elif label == "Net Pass Yards":
            self.setNetPassYds(int(value))
        elif label == "Total Yards":
            self.setTotalYds(int(value))
        elif label == "Fumbles-Lost":
            stats = value.split('-')
            self.setFumbles(int(stats[0]))
            self.setFumblesLost(int(stats[1]))
        elif label == "Turnovers":
            self.setTurnovers(int(value))
        elif label == "Penalties-Yards":
            stats = value.split('-')
            self.setPenalites(int(stats[0]))
            self.setPenaltyYds(int(stats[1]))
        elif label == "Third Down Conv.":
            stats = value.split('-')
            self.setThirdDownConvs(int(stats[0]))
            self.setThirdDownAtts(int(stats[1]))
        elif label == "Fourth Down Conv.":
            stats = value.split('-')
            self.setFourthDownConvs(int(stats[0]))
            self.setFourthDownAtts(int(stats[1]))
        elif label == "Time of Possession":
            self.setPossessionTime(datetime.strptime(value, "%M:%S").time())
        
    def getInfo(self):
        info = {
            "id": self.getId(),
            "teamId": self.getTeamId(),
            "gameId": self.getGameId(),
            "wonToss": self.getWonToss(),
            "tossDecision": self.getTossDecision(),
            "isHome": self.getIsHome(),
            "isFavored": self.getIsFavored(),
            "spread": self.getSpread(),
            "overUnder": self.getOverUnder(),
            "firstDowns": self.getFirstDowns(),
            "rushAtts": self.getRushAtts(),
            "rushYds": self.getRushYds(),
            "rushTds": self.getRushTds(),
            "passComps": self.getPassComps(),
            "passAtts": self.getPassAtts(),
            "passYds": self.getPassYds(),
            "passTds": self.getPassTds(),
            "passInts": self.getPassInts(),
            "sacked": self.getSacked(),
            "sackYdsLost": self.getSackYdsLost(),
            "netPassYds": self.getNetPassYds(),
            "totalYds": self.getTotalYds(),
            "fumbles": self.getFumbles(),
            "fumblesLost": self.getFumblesLost(),
            "turnovers": self.getTurnovers(),
            "penalties": self.getPenalties(),
            "penaltyYds": self.getPenaltyYds(),
            "thirdDownAtts": self.getThirdDownAtts(),
            "thirdDownConvs": self.getThirdDownConvs(),
            "fourthDownAtts": self.getFourthDownAtts(),
            "fourthDownConvs": self.getFourthDownConvs(),
            "possessionTime": self.getPossessionTime().isoformat(),
            "coach": self.getCoach(),
            "score": self.getScore()
        }
        return info