import json

class PlayerGame:
    def __init__(self, id, playerId, gameId):
        self.id = id
        self.player_id = playerId
        self.game_id = gameId
        self.pass_comps = None
        self.pass_atts = None
        self.pass_yds = None
        self.pass_tds = None
        self.pass_ints = None
        self.sacked = None
        self.sack_yds_lost = None
        self.long_pass = None
        self.pass_rating = None
        self.rush_atts = None
        self.rush_yds = None
        self.rush_tds = None
        self.long_rush = None
        self.rec_targets = None
        self.receptions = None
        self.rec_yds = None
        self.rec_tds = None
        self.long_rec = None
        self.fumbles = None
        self.fumbles_lost = None
        self.def_int = None
        self.def_int_yds = None
        self.def_int_tds = None
        self.long_def_int = None
        self.pass_defs = None
        self.def_sacks = None
        self.def_tack_comb = None
        self.def_tack_solo = None
        self.def_tack_assist = None
        self.def_tack_loss = None
        self.def_qb_hits = None
        self.fumble_recs = None
        self.fumble_rec_yds = None
        self.fumble_rec_tds = None
        self.forced_fumbles = None
        self.kick_rets = None
        self.kick_ret_yds = None
        self.avg_kick_ret = None
        self.kick_ret_tds = None
        self.long_kick_ret = None
        self.punt_rets = None
        self.punt_ret_yds = None
        self.avg_punt_ret = None
        self.punt_ret_tds = None
        self.long_punt_ret = None
        self.xpm = None
        self.xpa = None
        self.fgm = None
        self.fga = None
        self.punts = None
        self.punt_yds = None
        self.avg_punt = None
        self.long_punt = None
        
    def getAvgKickRet(self):
        return self.avg_kick_ret
    
    def setAvgKickRet(self, avg):
        self.avg_kick_ret = avg
        
    def getAvgPunt(self):
        return self.avg_punt
    
    def setAvgPunt(self, value):
        self.avg_punt = value
        
    def getAvgPuntRet(self):
        return self.avg_punt_ret
    
    def setAvgPuntRet(self, avg):
        self.avg_punt_ret = avg
        
    def getDefInt(self):
        return self.def_int
    
    def setDefInt(self, int):
        self.def_int = int
        
    def getDefIntTds(self):
        return self.def_int_tds
    
    def setDefIntTds(self, intTds):
        self.def_int_Tds = intTds
        
    def getDefIntYds(self):
        return self.def_int_yds
    
    def setDefIntYds(self, intYds):
        self.def_int_yds = intYds
        
    def getDefQbHits(self):
        return self.def_qb_hits
    
    def setDefQbHits(self, hits):
        self.def_qb_hits = hits
        
    def getDefSacks(self):
        return self.def_sacks
    
    def setDefSacks(self, sacks):
        self.def_sacks = sacks
        
    def getDefTacksAssist(self):
        return self.def_tack_assist
    
    def SetDefTacksAssist(self, tacks):
        self.def_tack_assist = tacks
        
    def getDefTacksComb(self):
        return self.def_tack_comb
    
    def SetDefTacksComb(self, tacks):
        self.def_tack_comb = tacks
        
    def getDefTacksLoss(self):
        return self.def_tack_loss
    
    def SetDefTacksLoss(self, tacks):
        self.def_tack_loss = tacks
        
    def getDefTacksSolo(self):
        return self.def_tack_solo
    
    def SetDefTacksSolo(self, tacks):
        self.def_tack_solo = tacks
        
    def getFga(self):
        return self.fga
    
    def setFga(self, value):
        self.fga = value
        
    def getFgm(self):
        return self.fgm
    
    def setFgm(self, value):
        self.fgm = value
        
    def getForcedFumbles(self):
        return self.forced_fumbles
    
    def setForcedFumbles(self, fumbs):
        self.forced_fumbles = fumbs
        
    def getFumbleRecs(self):
        return self.fumble_recs
    
    def setFumbleRecs(self, recs):
        self.fumble_recs = recs
        
    def getFumbleRecTds(self):
        return self.fumble_rec_tds
    
    def setFumbleRecTds(self, tds):
        self.fumble_rec_tds = tds
        
    def getFumbleRecYds(self):
        return self.fumble_rec_yds
    
    def setFumbleRecYds(self, yds):
        self.fumble_rec_yds = yds
        
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
        
    def getKickRetYds(self):
        return self.kick_ret_tds
    
    def setKickRetYds(self, tds):
        self.kick_ret_tds = tds
        
    def getKickRetYds(self):
        return self.kick_ret_yds
    
    def setKickRetYds(self, yds):
        self.kick_ret_yds = yds
        
    def getKickRets(self):
        return self.kick_rets
    
    def setKickRets(self, rets):
        self.kick_rets = rets
        
    def getLongDefInt(self):
        return self.long_def_int
    
    def setLongDefInt(self, longInt):
        self.long_def_int = longInt
        
    def getLongKickRet(self):
        return self.long_kick_ret
    
    def setLongKickRet(self, long):
        self.long_kick_ret = long
        
    def getLongPass(self):
        return self.long_pass
    
    def setLongPass(self, long):
        self.long_pass = long
        
    def getLongPunt(self):
        return self.long_punt
    
    def setLongPunt(self, value):
        self.long_punt = value
        
    def getLongPuntRet(self):
        return self.long_punt_ret
    
    def setLongPuntRet(self, long):
        self.long_punt_ret = long
        
    def getLongRec(self):
        return self.long_rec
    
    def setLongRec(self, long):
        self.long_rec = long
        
    def getLongRush(self):
        return self.long_rush
    
    def setLongRush(self, long):
        self.long_rush = long
    
    def getPassAtts(self):
        return self.pass_atts
    
    def setPassAtts(self, atts):
        self.pass_atts = atts
    
    def getPassComps(self):
        return self.pass_comps
    
    def setPassComps(self, comps):
        self.pass_comps = comps
        
    def getPassDefs(self):
        return self.pass_defs
    
    def setPassDefs(self, defs):
        self.pass_defs = defs
        
    def getPassInts(self):
        return self.pass_ints
    
    def setPassInts(self, ints):
        self.pass_ints = ints
        
    def getPassRating(self):
        return self.pass_rating
    
    def setPassRating(self, rating):
        self.pass_rating = rating
    
    def getPassTds(self):
        return self.pass_tds
    
    def setPassTds(self, tds):
        self.pass_tds = tds
    
    def getPassYds(self):
        return self.pass_yds
 
    def setPassYds(self, yds):
        self.pass_yds = yds
    
    def getPlayerId(self):
        return self.player_id
    
    def setPlayerId(self, id):
        self.player_id = id
        
    def getPuntRets(self):
        return self.punt_rets
    
    def setPuntRets(self, rets):
        self.punt_rets = rets
        
    def getPuntRetTds(self):
        return self.punt_ret_tds
    
    def setPuntRetTds(self, tds):
        self.punt_ret_tds = tds
        
    def getPuntRetYds(self):
        return self.punt_ret_yds
    
    def setPuntRetYds(self, yds):
        self.punt_ret_yds = yds
        
    def getPunts(self):
        return self.punts
    
    def setPunts(self, value):
        self.punts = value
        
    def getPuntYds(self):
        return self.punt_yds
    
    def setPuntYds(self, value):
        self.punt_yds = value
        
    def getReceptions(self):
        return self.receptions
    
    def setReceptions(self, recs):
        self.receptions = recs
        
    def getRecTargets(self):
        return self.rec_targets
    
    def setRecTargets(self, targets):
        self.rec_targets = targets
        
    def getRecTds(self):
        return self.rec_tds
    
    def setRecTds(self, tds):
        self.rec_tds = tds
        
    def getRecYds(self):
        return self.rec_yds
    
    def setRecYds(self, yds):
        self.rec_yds = yds
        
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
    
    def setSacked(self, sacked):
        self.sacked = sacked
        
    def getXpa(self):
        return self.xpa
    
    def setXpa(self, value):
        self.xpa = value
        
    def getXpm(self):
        return self.xpm
    
    def setXpm(self, value):
        self.xpm = value
        
        
    # MAPPER when parsing html    
    def mapToPlayerGame(self, label, value):
        if label == "pass_cmp":
            self.pass_comps = int(value)
        elif label == "pass_att":
            self.pass_atts = int(value)
        elif label == "pass_yds":
            self.pass_yds = int(value)
        elif label == "pass_td":
            self.pass_tds = int(value)
        elif label =="pass_int":
            self.pass_ints = int(value)
        elif label == "pass_sacked":
            self.sacked = int(value)
        elif label == "pass_sacked_yds":
            self.sack_yds_lost = int(value)
        elif label == "pass_long":
            self.long_pass = int(value)
        elif label == "pass_rating":
            self.pass_rating = float(value)
        elif label == "rush_att":
            self.rush_atts = int(value)
        elif label == "rush_yds":
            self.rush_yds = int(value)
        elif label == "rush_td":
            self.rush_tds = int(value)
        elif label == "rush_long":
            self.long_rush = int(value)
        elif label == "targets":
            self.rec_targets = int(value)
        elif label == "rec":
            self.receptions = int(value)
        elif label == "rec_yds":
            self.rec_yds = int(value)
        elif label == "rec_td":
            self.rec_tds = int(value)
        elif label == "rec_long":
            self.long_rec = int(value)
        elif label == "fumbles":
            self.fumbles = int(value)
        elif label == "fumbles_lost":
            self.fumbles_lost = int(value)
            
    # Return JSON object
    def getInfo(self):
        info = {
            "id": self.getId(),
            "playerId": self.getPlayerId(),
            "tmGameId": self.getGameId(),
            "passComps": self.getPassComps(),
            "passAtts": self.getPassAtts(),
            "passYds": self.getPassYds(),
            "passTds": self.getPassTds(),
            "passInts": self.getPassInts(),
            "sacked": self.getSacked(),
            "sackYdsLost": self.getSackYdsLost(),
            "longPass": self.getLongPass(),
            "passRating": self.getPassRating(),
            "rushAtts": self.getRushAtts(),
            "rushYds": self.getRushYds(),
            "rushTds": self.getRushTds(),
            "longRush": self.getLongRush(),
            "recTargets": self.getRecTargets(),
            "recs": self.getReceptions(),
            "recYds": self.getRecYds(),
            "recTds": self.getRecTds(),
            "longRec": self.getLongRec(),
            "fumbles": self.getFumbles(),
            "fumblesLost": self.getFumblesLost()
        }
        
        return info