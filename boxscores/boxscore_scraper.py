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
    # remove used data from text
    text = text[e_idx:]
    idx = text.find("<div")
    text = text[idx:]

    return text, game
        
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
    games = {}
    # define base url and get request urls
    base = "www.pro-football-reference.com"
    url = "/boxscores/202109090tam.htm"
    # using defined base and request urls, get decoded data
    # bytes = request_data(base, url)
    text = open_html("./page.html")
    # trim html to content we need
    text = trim_text(text, '<div id="content"', '<div id="footer"')
    # extract game date string, home and away teams
    text, game = extract_basic_info(text)
    # extract scores and coaches
    text = game.extract_scorebox(text)
    # extract scorebox meta
    text = game.extract_scorebox_meta(text)
    # extract linescores
    text = game.extract_scoring_plays(text)

    print(text[:30])
    game.print_game_info() 

        
if __name__ == "__main__":
    start_time = time()
    try:
        run_scraper()
        print(time() - start_time) 
    except KeyboardInterrupt:
        print(time() - start_time)
        print("Exiting...")