from bs4 import BeautifulSoup
from bs4 import SoupStrainer as strainer
from bs4 import Comment
import csv
from datetime import datetime
from Game import Game
import http.client
import re
from time import time

def extract_basic_info(data):
        away = data[0]
        
        rem  = data[1]
        rem = rem.split(" - ")
        home = rem[0]
        date = remove_date_formals(rem[1])
        date = datetime.strptime(date, "%B %m, %Y")
        
        return away, date, home
        
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
    
def run_scraper():
    games = {}
    # define base url and get request urls
    base = "www.pro-football-reference.com"
    url = "/boxscores/202109090tam.htm"
    # using defined base and request urls, get decoded data
    bytes = request_data(base, url)
    # create soup
    head = strainer("head")
    soup = BeautifulSoup(bytes, 'html.parser', parse_only=head)
    title = soup.title.text[:-29]
    
    # extract away team, game date, and home team from webpage title
    away, date, home = extract_basic_info(title.split(" at "))
    
    # create new game object
    game = Game(away, home, date)
    
    # extract away score and home score
    # create strainer to save memory by parsing only scorebox div
    scorebox = strainer(class_="scorebox")
    # create soup using strainer (reduces amount of code bs4 has to parse)
    scorebox_soup = BeautifulSoup(bytes, 'html.parser', parse_only=scorebox)
    game.extract_scores(scorebox_soup.find_all(class_="score"))
    
    # extract away coach and home coach
    game.extract_coaches(scorebox_soup.find_all(class_="datapoint"))
    
    # extract attendance, stadium, and start time
    game.extract_scorebox_meta(scorebox_soup.find(class_="scorebox_meta"))
    
    # extract offensive stats for both teams
    # create new strainer to only parse all_player_offense div
    offense = strainer(id="div_player_offense")
    offense_soup = BeautifulSoup(bytes, 'html.parser', parse_only=offense)
    game.extract_player_stats(offense_soup, "Offense")
    
    # webpage uses javascript to populate some tables
    # parse comments to extract needed data
    ## create new strainer to only parse main div code
    main_soup = BeautifulSoup(bytes, 'html.parser')
    comments = main_soup.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        if "div_officials" in comment:
            official_soup = BeautifulSoup(comment, 'html.parser')
            game.extract_officials(official_soup)
        elif "div_player_defense" in comment:
            defense_soup = BeautifulSoup(comment, 'html.parser')
            game.extract_player_stats(defense_soup, "Defense")
        elif "div_home_starters" in comment:
            starter_soup = BeautifulSoup(comment, 'html.parser')
            game.extract_starters(starter_soup, "Home")
        elif "div_vis_starters" in comment:
            starter_soup = BeautifulSoup(comment, 'html.parser')
            game.extract_starters(starter_soup, "Away")
            
    with open('test_game.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(game.get_game_as_list())
        
if __name__ == "__main__":
    start_time = time()
    try:
        run_scraper()
        print(time() - start_time) 
    except KeyboardInterrupt:
        print(time() - start_time)
        print("Exiting...")