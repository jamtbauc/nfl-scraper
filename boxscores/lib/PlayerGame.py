import json
import re

class PlayerGame:
    def __init__(self, id, playerId):
        self.id = id
        self.player_id = playerId
        self.game_id = None
        self.pass_comps = 0
        self.pass_atts = 0
        self.pass_yds = 0
        self.pass_tds = 0
        self.pass_ints = 0
        self.sacked = 0
        self.sack_yds_lost = 0
        self.long_pass = 0
        self.pass_rating = 0
        self.rush_atts = 0
        self.rush_yds = 0
        self.rush_tds = 0
        self.long_rush = 0
        self.rec_targets = 0
        self.receptions = 0
        self.rec_yds = 0
        self.rec_tds = 0
        self.long_rec = 0
        self.fumbles = 0
        self.fumbles_lost = 0
        self.def_int = 0
        self.def_int_yds = 0
        self.def_int_tds = 0
        self.long_def_int = 0
        self.pass_defs = 0
        self.def_sacks = 0.0
        self.def_tack_comb = 0
        self.def_tack_solo = 0
        self.def_tack_assist = 0
        self.def_tack_loss = 0
        self.def_qb_hits = 0
        self.fumble_recs = 0
        self.fumble_rec_yds = 0
        self.fumble_rec_tds = 0
        self.forced_fumbles = 0
        self.kick_rets = 0
        self.kick_ret_yds = 0
        self.avg_kick_ret = 0.0
        self.kick_ret_tds = 0
        self.long_kick_ret = 0
        self.punt_rets = 0
        self.punt_ret_yds = 0
        self.avg_punt_ret = 0.0
        self.punt_ret_tds = 0
        self.long_punt_ret = 0
        self.xpm = 0
        self.xpa = 0
        self.fgm = 0
        self.fga = 0
        self.punts = 0
        self.punt_yds = 0
        self.avg_punt = 0.0
        self.long_punt = 0
        self.pass_first_downs = 0 
        self.pass_first_down_pct = 0.0
        self.pass_tgt_yds = 0
        self.pass_tgt_yds_per_att = 0.0
        self.pass_air_yds = 0
        self.pass_air_yds_per_comp = 0.0
        self.pass_air_yds_per_att = 0.0
        self.pass_yac = 0 
        self.pass_yac_per_comp = 0.0
        self.pass_drops = 0 
        self.pass_drop_pct = 0.0
        self.pass_poor_throws = 0 
        self.pass_poor_throw_pct = 0.0 
        self.pass_blitzed = 0
        self.pass_hurried = 0 
        self.pass_hits = 0 
        self.pass_pressured = 0 
        self.pass_pressured_pct = 0.0
        self.rush_scrambles = 0
        self.rush_scrambles_yds_per_att = 0.0 
        self.rush_first_down = 0 
        self.rush_yds_before_contact = 0 
        self.rush_yds_bc_per_rush = 0.0
        self.rush_yac = 0 
        self.rush_yac_per_rush = 0.0
        self.rush_broken_tacks = 0 
        self.rush_broken_tacks_per_rush = 0.0
        self.rec_first_down = 0 
        self.rec_air_yds = 0 
        self.rec_air_yds_per_rec = 0.0
        self.rec_yac = 0 
        self.rec_yac_per_rec = 0.0
        self.rec_adot = 0.0
        self.rec_broken_tacks = 0 
        self.rec_broken_tacks_per_rec = 0.0 
        self.rec_drops = 0 
        self.rec_drop_pct = 0.0
        self.rec_target_int = 0 
        self.rec_pass_rating = 0.0 
        self.def_targets = 0 
        self.def_comps = 0 
        self.def_comp_pct = 0.0
        self.def_comp_yds = 0
        self.def_yds_per_comp = 0.0 
        self.def_yds_per_target = 0.0 
        self.def_comp_tds = 0 
        self.def_pass_rating = 0.0
        self.def_tgt_yds_per_att = 0.0 
        self.def_air_yds = 0 
        self.def_yac = 0 
        self.blitzes = 0 
        self.qb_hurries = 0 
        self.qb_knockdown = 0
        self.pressures = 0 
        self.tacks_missed = 0 
        self.tacks_missed_pct = 0.0
        self.is_starter = False
        self.starting_pos = None
        
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
        self.def_int_tds = intTds
        
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
        
    def getKickRetTds(self):
        return self.kick_ret_tds
    
    def setKickRetTds(self, tds):
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
        
    def getPassFirstDowns(self):
        return self.pass_first_downs
    
    def setPassFirstDowns(self, value):
        self.pass_first_downs = int(value)
    
    def getPassFirstDownPct(self):
        return self.pass_first_down_pct
    
    def setPassFirstDownPct(self, value):
        self.pass_first_down_pct = float(value)
        
    def getPassTgtYds(self):
        return self.pass_tgt_yds
    
    def setPassTgtYds(self, value):
        self.pass_tgt_yds = int(value)
    
    def getPassTgtYdsPerAtt(self):
        return self.pass_tgt_yds_per_att
    
    def setPassTgtYdsPerAtt(self, value):
        self.pass_tgt_yds_per_att = float(value)
        
    def getPassAirYds(self):
        return self.pass_air_yds
    
    def setPassAirYds(self, value):
        self.pass_air_yds = int(value)
        
    def getPassAirYdsPerComp(self):
        return self.pass_air_yds_per_comp
    
    def setPassAirYdsPerComp(self, value):
        self.pass_air_yds_per_comp = float(value)
    
    def getPassAirYdsPerAtt(self):
        return self.pass_air_yds_per_att
    
    def setPassAirYdsPerAtt(self, value):
        self.pass_air_yds_per_att = float(value)

    def getPassYac(self):
        return self.pass_yac
    
    def setPassYac(self, value):
        self.pass_yac = int(value)
        
    def getPassYacPerComp(self):
        return self.pass_yac_per_comp
    
    def setPassYacPerComp(self, value):
        self.pass_yac_per_comp = float(value)
        
    def getPassDrops(self):
        return self.pass_drops
    
    def setPassDrops(self, value):
        self.pass_drops = int(value)
         
    def getPassDropPct(self):
        return self.pass_drop_pct
    
    def setPassDropPct(self, value):
        value = re.findall('[0-9]+', value)
        value = int(value[0])
        self.pass_drop_pct = int(value)
         
    def getPassPoorThrows(self):
        return self.pass_poor_throws
    
    def setPassPoorThrows(self, value):
        self.pass_poor_throws = int(value)
        
    def getPassPoorThrowPct(self):
        return self.pass_poor_throw_pct
    
    def getPassBlitzed(self):
        return self.pass_blitzed
    
    def getPassHurried(self): 
        return self.pass_hurried
    
    def getPassHits(self): 
        return self.pass_hits
    
    def getPassPressured(self): 
        return self.pass_pressured
    
    def getPassPressuredPct(self): 
        return self.pass_pressured_pct
    
    def getRushScrambles(self):
        return self.rush_scrambles
    
    def getRushScramblesYdsPerAtt(self): 
        return self.rush_scrambles_yds_per_att
    
    def getRushFirstDown(self): 
        return self.rush_first_down
    
    def getRushYdsBeforeContact(self): 
        return self.rush_yds_before_contact
    
    def getRushYdsBcPerRush(self):
        return self.rush_yds_bc_per_rush
    
    def getRushYac(self): 
        return self.rush_yac
    
    def getRushYacPerRush(self): 
        return self.rush_yac_per_rush
    
    def getRushBrokenTacks(self):
        return self.rush_broken_tacks
     
    def getRushBrokenTacksPerRush(self):
        return self.rush_broken_tacks_per_rush
    
    def getRecFirstDown(self): 
        return self.rec_first_down
    
    def getRecAirYds(self): 
        return self.rec_air_yds
    
    def getRecAirYdsPerRec(self): 
        return self.rec_air_yds_per_rec
    
    def getRecYac(self): 
        return self.rec_yac
    
    def getRecYacPerRec(self):
        return self.rec_yac_per_rec
    
    def getRecAdot(self): 
        return self.rec_adot
    
    def getRecBrokenTacks(self): 
        return self.rec_broken_tacks
    
    def getRecBrokenTacksPerRec(self): 
        return self.rec_broken_tacks_per_rec
    
    def getRecDrops(self): 
        return self.rec_drops
    
    def getRecDropPct(self):
        return self.rec_drop_pct
    
    def getRecTargetInt(self): 
        return self.rec_target_int
    
    def getRecPassRating(self): 
        return self.rec_pass_rating
    
    def getDefTargets(self): 
        return self.def_targets
    
    def getDefComps(self): 
        return self.def_comps
    
    def getDefCompPct(self):
        return self.def_comp_pct
    
    def getDefCompYds(self): 
        return self.def_comp_yds
    
    def getDefYdsPerComp(self): 
        return self.def_yds_per_comp
    
    def getDefYdsPerTarget(self):
        return self.def_yds_per_target
     
    def getDefCompTds(self): 
        return self.def_comp_tds
    
    def getDefPassRating(self):
        return self.def_pass_rating
    
    def getDefTgtYdsPerAtt(self): 
        return self.def_tgt_yds_per_att
    
    def getDefAirYds(self): 
        return self.def_air_yds
    
    def getDefYac(self): 
        return self.def_yac
    
    def getBlitzes(self):
        return self.blitzes
     
    def getQbHurries(self): 
        return self.qb_hurries
    
    def getQbKnockdown(self):
        return self.qb_knockdown
    
    def getPressures(self): 
        return self.pressures
    
    def getTacksMissed(self):
        return self.tacks_missed
    
    def getTacksMissedPct(self):
        return self.tacks_missed_pct
    
    def getIsStarter(self):
        return self.is_starter
    
    def getStartingPos(self):
        return self.starting_pos
        
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
        elif label == "def_int":
            self.def_int = int(value)
        elif label == "def_int_yds":
            self.def_int_yds = int(value)
        elif label == "def_int_td":
            self.def_int_tds = int(value)
        elif label == "def_int_long":
            self.long_def_int = int(value)
        elif label == "pass_defended":
            self.pass_defs = int(value)
        elif label == "sacks":
            self.def_sacks = float(value)
        elif label == "tackles_combined":
            self.def_tack_comb = int(value)
        elif label == "tackles_solo":
            self.def_tack_solo = int(value)
        elif label == "tackles_assists":
            self.def_tack_assist = int(value)
        elif label == "tackles_loss":
            self.def_tack_loss = int(value)
        elif label == "qb_hits":
            self.def_qb_hits = int(value)
        elif label == "fumbles_rec":
            self.fumble_recs = int(value)
        elif label == "fumbles_rec_yds":
            self.fumble_rec_yds = int(value)
        elif label == "fumbles_rec_td":
            self.fumble_rec_tds = int(value)
        elif label == "fumbles_forced":
            self.forced_fumbles = int(value)
        elif label == "kick_ret":
            self.kick_rets = int(value)
        elif label == "kick_ret_yds":
            self.kick_ret_yds = int(value)
        elif label == "kick_ret_yds_per_ret":
            self.avg_kick_ret = float(value)
        elif label == "kick_ret_td":
            self.kick_ret_tds = int(value)
        elif label == "kick_ret_long":
            self.long_kick_ret = int(value)
        elif label == "punt_ret":
            self.punt_rets = int(value)
        elif label == "punt_ret_yds":
            self.punt_ret_yds = int(value)
        elif label == "punt_ret_yds_per_ret":
            self.avg_punt_ret = float(value)
        elif label == "punt_ret_td":
            self.punt_ret_tds = int(value)
        elif label == "punt_ret_long":
            self.long_punt_ret = int(value)
        elif label == "xpm":
            self.xpm = int(value)
        elif label == "xpa":
            self.xpa = int(value)
        elif label == "fgm":
            self.fgm = int(value)
        elif label == "fga":
            self.fga = int(value)
        elif label == "punt":
            self.punt = int(value)
        elif label == "punt_yds":
            self.punt_yds = int(value)
        elif label == "punt_yds_per_punt":
            self.avg_punt = float(value)
        elif label == "punt_long":
            self.long_punt = int(value)
        elif label == "pass_first_down":
            self.pass_first_downs = int(value)
        elif label == "pass_first_down_pct":
            self.pass_first_down_pct = float(value)
        elif label == "pass_target_yds":
            self.pass_tgt_yds = int(value)
        elif label == "pass_tgt_yds_per_att":
            self.pass_air_yds_per_att = float(value)
        elif label == "pass_air_yds":
            self.pass_air_yds = int(value)
        elif label == "pass_air_yds_per_cmp":
            self.pass_air_yds_per_comp = float(value)
        elif label == "pass_air_yds_per_att":
            self.pass_air_yds_per_att = float(value)
        elif label == "pass_yac":
            self.pass_yac = int(value)
        elif label == "pass_yac_per_cmp":
            self.pass_yac_per_comp = float(value)
        elif label == "pass_drops":
            self.pass_drops = int(value)
        elif label == "pass_drop_pct":
            value = re.findall('[0-9]+', value)
            value = int(value[0])
            self.pass_drop_pct = float(value)
        elif label == "pass_poor_throws":
            self.pass_poor_throws = int(value)
        elif label == "pass_poor_throw_pct":
            value = re.findall('[0-9]+', value)
            value = int(value[0])
            self.pass_poor_throw_pct = float(value)
        elif label == "pass_blitzed":
            self.pass_blitzed = int(value)
        elif label == "pass_hurried":
            self.pass_hurried = int(value)
        elif label == "pass_hits":
            self.pass_hits = int(value)
        elif label == "pass_pressured":
            self.pass_pressured = int(value)
        elif label == "pass_pressured_pct":
            value = re.findall('[0-9]+', value)
            value = int(value[0])
            self.pass_pressured_pct = float(value)
        elif label == "rush_scrambles":
            self.rush_scrambles = int(value)
        elif label == "rush_scrambles_yds_per_att":
            self.rush_scrambles_yds_per_att = float(value)
        elif label == "rush_first_down":
            self.rush_first_down = int(value)
        elif label == "rush_yds_before_contact":
            self.rush_yds_before_contact = int(value)
        elif label == "rush_yds_bc_per_rush":
            self.rush_yds_bc_per_rush = float(value)
        elif label == "rush_yac":
            self.rush_yac = int(value)
        elif label == "rush_yac_per_rush":
            self.rush_yac_per_rush = float(value)
        elif label == "rush_broken_tackles":
            self.rush_broken_tacks = int(value)
        elif label == "rush_broken_tackles_per_rush":
            self.rush_broken_tacks_per_rush = float(value)
        elif label == "rec_first_down":
            self.rec_first_down = int(value)
        elif label == "rec_air_yds":
            self.rec_air_yds = int(value)
        elif label == "rec_air_yds_per_rec":
            self.rec_air_yds_per_rec = float(value)
        elif label == "rec_yac":
            self.rec_yac = int(value)
        elif label == "rec_yac_per_rec":
            self.rec_yac_per_rec = float(value)
        elif label == "rec_adot":
            self.rec_adot = float(value)
        elif label == "rec_broken_tackles":
            self.rec_broken_tacks = int(value)
        elif label == "rec_broken_tackles_per_rec":
            self.rec_broken_tacks_per_rec = float(value)
        elif label == "rec_drops":
            self.rec_drops = int(value)
        elif label == "rec_drop_pct":
            value = re.findall('[0-9]+', value)
            value = int(value[0])
            self.rec_drop_pct = float(value)
        elif label == "rec_target_int":
            self.rec_target_int = int(value)
        elif label == "rec_pass_rating":
            self.rec_pass_rating = float(value)
        elif label == "def_targets":
            self.def_targets = int(value)
        elif label == "def_cmp":
            self.def_comps = int(value)
        elif label == "def_cmp_perc":
            if isinstance(value, str):
                value = re.findall('[0-9]+', value)
                value = float(value[0])
            self.def_comp_pct = float(value)
        elif label == "def_cmp_yds":
            self.def_comp_yds = int(value)
        elif label == "def_yds_per_cmp":
            self.def_yds_per_comp = float(value)
        elif label == "def_yds_per_target":
            self.def_yds_per_target = float(value)
        elif label == "def_cmp_td":
            self.def_comp_tds = int(value)
        elif label == "def_pass_rating":
            self.def_pass_rating = float(value)
        elif label == "def_tgt_yds_per_att":
            self.def_tgt_yds_per_att = float(value)
        elif label == "def_air_yds":
            self.def_air_yds = int(value)
        elif label == "def_yac":
            self.def_yac = int(value)
        elif label == "blitzes":
            self.blitzes = int(value)
        elif label == "qb_hurry":
            self.qb_hurries = int(value)
        elif label == "qb_knockdown":
            self.qb_knockdown = int(value)
        elif label == "pressures":
            self.pressures = int(value)
        elif label == "tackles_missed":
            self.tacks_missed = int(value)
        elif label == "tackles_missed_pct":
            if isinstance(value, str):
                value = re.findall('[0-9]+', value)
                value = float(value[0])
            self.tacks_missed_pct = float(value)
        else:
            print(f"Cannot map {label} for PlayerGame")
            
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
            "fumblesLost": self.getFumblesLost(),
            "defInts": self.getDefInt(),
            "defIntYds": self.getDefIntYds(),
            "defIntTds": self.getDefIntTds(),
            "longDefInt": self.getLongDefInt(),
            "passDefs": self.getPassDefs(),
            "defSacks": self.getDefSacks(),
            "defTackCombined": self.getDefTacksComb(),
            "defTackSolo": self.getDefTacksSolo(),
            "defTackAssists": self.getDefTacksAssist(),
            "defTackForLoss": self.getDefTacksLoss(),
            "defQbHits": self.getDefQbHits(),
            "fumbleRecs": self.getFumbleRecs(),
            "fumbleRecYds": self.getFumbleRecYds(),
            "fumbleRecTds": self.getFumbleRecTds(),
            "forcedFumbles": self.getForcedFumbles(),
            "kickRets": self.getKickRets(),
            "kickRetYds": self.getKickRetYds(),
            "avgKickRet": self.getAvgKickRet(),
            "kickRetTds": self.getKickRetTds(),
            "longKickRet": self.getLongKickRet(),
            "puntRets": self.getPuntRets(),
            "puntRetYds": self.getPuntRetYds(),
            "avgPuntRet": self.getAvgPuntRet(),
            "puntRetTds": self.getPuntRetTds(),
            "longPuntRet": self.getLongPuntRet(),
            "xpm": self.getXpm(),
            "xpa": self.getXpa(),
            "fgm": self.getFgm(),
            "fga": self.getFga(),
            "punts": self.getPunts(),
            "puntYds": self.getPuntYds(),
            "avgPunt": self.getAvgPunt(),
            "longPunt": self.getLongPunt(),
            "passFirstDowns": self.getPassFirstDowns(),
            "passFirstDownPct": self.getPassFirstDownPct(),
            "passTgtYdsPerAtt": self.getPassTgtYdsPerAtt(),
            "passAirYds": self.getPassAirYds(),
            "passAirYdsPerComp": self.getPassAirYdsPerComp(),
            "passAirYdsPerAtt": self.getPassAirYdsPerAtt(),
            "passYac": self.getPassYac(),
            "passYacPerComp": self.getPassYacPerComp(),
            "passDrops": self.getPassDrops(),
            "passDropPct": self.getPassDropPct(),
            "passPoorThrows": self.getPassPoorThrows(),
            "passPoorThrowPct": self.getPassPoorThrowPct(),
            "passBlitzed": self.getPassBlitzed(),
            "passHurried": self.getPassHurried(),
            "passHits": self.getPassHits(),
            "passPressured": self.getPassPressured(),
            "passPressuredPct": self.getPassPressuredPct(),
            "rushScrambles": self.getRushScrambles(),
            "rushScramblesYdsPerAtt": self.getRushScramblesYdsPerAtt(),
            "rushFirstDown": self.getRushFirstDown(),
            "rushYdsBeforeContact": self.getRushYdsBeforeContact(),
            "rushYdsBcPerRush": self.getRushYdsBcPerRush(),
            "rushYac": self.getRushYac(),
            "rushYacPerRush": self.getRushYacPerRush(),
            "rushBrokenTacks": self.getRushBrokenTacks(),
            "rushBrokenTacksPerRush": self.getRushBrokenTacksPerRush(),
            "recFirstDown": self.getRecFirstDown(),
            "recAirYds": self.getRecAirYds(),
            "recAirYdsPerRec": self.getRecAirYdsPerRec(),
            "recYac": self.getRecYac(),
            "recYacPerRec": self.getRecYacPerRec(),
            "recAdot": self.getRecAdot(),
            "recBrokenTacks": self.getRecBrokenTacks(),
            "recBrokenTacksPerRec": self.getRecBrokenTacksPerRec(),
            "recDrops": self.getRecDrops(),
            "recDropPct": self.getRecDropPct(),
            "recTargetInt": self.getRecTargetInt(),
            "recPassRating": self.getRecPassRating(),
            "defTargets": self.getDefTargets(),
            "defComps": self.getDefComps(),
            "defCompPct": self.getDefCompPct(),
            "defCompYds": self.getDefCompYds(),
            "defYdsPerComp": self.getDefYdsPerComp(),
            "defYdsPerTarget": self.getDefYdsPerTarget(),
            "defCompTds": self.getDefCompTds(),
            "defPassRating": self.getDefPassRating(),
            "defTgtYdsPerAtt": self.getDefTgtYdsPerAtt(),
            "defAirYds": self.getDefAirYds(),
            "defYac": self.getDefYac(),
            "blitzes": self.getBlitzes(),
            "qbHurries": self.getQbHurries(),
            "qbKnockdown": self.getQbKnockdown(),
            "pressures": self.getPressures(),
            "tacksMissed": self.getTacksMissed(),
            "tacksMissedPct": self.getTacksMissedPct(),
            "isStarter": self.getIsStarter(),
            "startingPos": self.getStartingPos()
        }
        
        return info