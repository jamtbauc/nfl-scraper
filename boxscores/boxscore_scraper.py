from cgitb import html, text
from itertools import tee
from sqlite3 import Date
from bs4 import BeautifulSoup
from bs4 import SoupStrainer as strainer
from bs4 import Comment
import csv
from datetime import datetime
from Game import Game
import http.client
import re
from time import time

def extract_basic_info(text):
    idx = text.find("<h1>")
    e_idx = text.find("</h1>")
    info = text[idx+4:e_idx]
    # split title into teams and date
    info = info.split(" - ")
    # separate into name vars
    matchup = info[0]
    matchup = matchup.split(" at ")
    away = matchup[0]
    home = matchup[1]
    date = info[1]
    date = remove_date_formals(date)
    date = datetime.strptime(date, "%B %d, %Y")
    # create game object
    game = Game(date, away, home)

    return game
        
def remove_date_formals(date):
    formals = ("st", "nd", "rd", "th")
    for ending in formals:
        idx = date.find(ending)
        if idx > -1:
            date = date[:idx] + date[idx+2:]
    
    return date

def request_data(base, url):
        ### open connection to nfl.com
        conn = http.client.HTTPSConnection(base)
        ### send GET request
        conn.request("GET", url)
        ### retrieve response body from GET request
        resp = conn.getresponse()
        ### get html from GET response
        html = resp.read()
        ### close httpsconnection
        conn.close()
        
        #return html.decode('ISO-8859-1')
        return html.decode("utf-8", "replace")

def trim_text(text, start, end):
    start_idx = text.find(start)
    end_idx = text.find(end)

    return text[start_idx:end_idx]

### REMOVE WHEN DEV IS DONE
def open_html(file):
    with open(file) as html:
        text = html.read()

        text = bytes(text, "utf-8")
        return text.decode("utf-8", "replace")

    
def run_scraper():
    # Hold all games
    games = []
    # Hold all teams
    teams = []
    # Hold all players
    players = []
    # Hold all officials
    officials = []
    # Hold all stadiums
    stadiums = []

    # define base url and get request urls
    base = "www.pro-football-reference.com"
    url = "/boxscores/202109090tam.htm"
    # using defined base and request urls, get decoded data
    # bytes = request_data(base, url)
    text = open_html("./page.html")
    # trim html to content we need
    text = trim_text(text, '<div id="content"', '<div id="footer"')

    ### Declare the sections we need to parse
    matchup = trim_text(text, '<div id="content" role="main" class="box">', '<div class="section_wrapper setup_commented commented" id="all_other_scores">')
    scorebox = trim_text(text, '<div class="scorebox">', '<div class="scorebox_meta">')
    scorebox_meta = trim_text(text, '<div class="scorebox_meta">', '<style>')
    all_scoring = trim_text(text, '<div class="table_container" id="div_scoring">', '<div class="content_grid">')
    game_info = trim_text(text, '<div id="all_game_info"', '<div id="all_officials"')
    all_officials = trim_text(text, '<div id="all_officials"', '<div id="all_expected_points"')
    expected_pts = trim_text(text, '<div id="all_expected_points"', '<div id="all_team_stats"')
    all_team_stats = trim_text(text, '<div id="all_team_stats"', '<div id="all_player_offense"')
    all_player_off = trim_text(text, '<div id="all_player_offense"', '<div id="all_player_defense"')
    all_player_def = trim_text(text, '<div id="all_player_defense"', '<div id="all_returns"')
    all_returns = trim_text(text, '<div id="all_returns"', '<div id="all_kicking"')
    all_kicking = trim_text(text, '<div id="all_kicking"', '<div id="all_passing_advanced"')
    passing_adv = trim_text(text, '<div id="all_passing_advanced"', '<div id="all_rushing_advanced"')
    rushing_adv = trim_text(text, '<div id="all_rushing_advanced"', '<div id="all_receiving_advanced"')
    receiving_adv = trim_text(text, '<div id="all_receiving_advanced"', '<div id="all_defense_advanced"')
    defense_adv = trim_text(text, '<div id="all_defense_advanced"', '<div id="all_home_starters"')
    home_starters = trim_text(text, '<div id="all_home_starters"', '<div id="all_vis_starters"')
    away_starters = trim_text(text, '<div id="all_vis_starters"', '<div id="all_home_snap_counts"')
    home_snaps = trim_text(text, '<div id="all_home_snap_counts"', '<div id="all_vis_snap_counts"')
    away_snaps = trim_text(text, '<div id="all_vis_snap_counts"', '<div id="all_home_drives"')
    home_drives = trim_text(text, '<div id="all_home_drives"', '<div id="all_vis_drives"')
    away_drives = trim_text(text, '<div id="all_vis_drives"', '<div id="all_pbp"')
    plays = trim_text(text, '<div id="all_pbp"', '<div id="bottom_nav"')



    # extract game date string, home and away teams
    game = extract_basic_info(matchup)
    # extract scores and coaches
    game.extract_scorebox(scorebox)
    # extract scorebox meta
    game.extract_scorebox_meta(scorebox_meta)
    ### OPTIMIZATION: Starting from here can be ran concurrently
    # extract all scoring
    game.extract_scoring_plays(all_scoring)
    # extract basic game info
    game.extract_game_info(game_info)
    # extract game officials
    game.extract_officials(all_officials)
    # extract expected points
    game.extract_exp_points_added(expected_pts)
    # extract team stats
    game.extract_team_stats(all_team_stats)
    # extract player offense
    game.extract_player_stats(all_player_off)
    # extract player defense
    game.extract_player_stats(all_player_def)
    # extract player returns
    game.extract_player_stats(all_returns)
    # extract player kicking/punting
    game.extract_player_stats(all_kicking)
    # extract advanced passing
    game.extract_player_stats(passing_adv)
    # extract advanced rushing
    game.extract_player_stats(rushing_adv)
    # extract advanced receiving
    game.extract_player_stats(receiving_adv)
    # extract advanced defense
    game.extract_player_stats(defense_adv)
    # extract home starters
    game.extract_starters(home_starters)
    # extract away starters
    game.extract_starters(away_starters)
    # extract home snaps
    game.extract_snaps(home_snaps)
    # extract away snaps
    game.extract_snaps(away_snaps)
    # extract home drives
    game.extract_drives(home_drives)
    # extract away drives
    game.extract_drives(away_drives)
    # extract play by plays
    game.extract_plays(plays)

    game.print_game_info() 

        
if __name__ == "__main__":
    start_time = time()
    try:
        run_scraper()
        print(time() - start_time) 
    except KeyboardInterrupt:
        print(time() - start_time)
        print("Exiting...")