import csv
from datetime import datetime
from lib.Parser import Parser
import http.client
import json
from time import time

# load all game urls into list
def get_urls(file):
    urls = ()
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            urls += tuple(row)
            
    return urls

### REMOVE WHEN DEV IS DONE
def open_html(file):
    with open(file) as html:
        text = html.read()

        text = bytes(text, "utf-8")
        return text.decode("utf-8", "replace")

# Send get request to url specified at base website. Returns response body
def request_data(conn, url):
        # send GET request
        conn.request("GET", url)
        # retrieve response body from GET request
        resp = conn.getresponse()
        # get html from GET response
        html = resp.read()
        # return html.decode('ISO-8859-1')
        body_str = html.decode("utf-8", "replace")
        # trim body
        body = trim_text(body_str, '<div id="content"', '<div id="nav_bottom"')
        
        return body
    
# Scrape response body for desired information  
def run_scraper():
    # Hold all games
    games = {}
    # hold all urls
    urls = get_urls('links.csv')
    # define base url and get request urls
    base = "www.pro-football-reference.com"
    # open connection to pro-football-reference.com
    conn = http.client.HTTPSConnection(base)
    # create Parser object
    parser = Parser()
    # loop through all urls
    for url in urls:
        if url == '/boxscores/202210270tam.htm':
            print(url)
            # using defined base and request urls, get decoded data
            bytes = request_data(conn, url)
            # trim html to content we need
            text = trim_text(bytes, '<div id="content"', '<div id="footer"')
            ### Declare the sections we need to parse
            parser.setMatchup(trim_text(text, '<div id="content" role="main" class="box">', '<div class="game_summary nohover current">'))
            parser.setScorebox(trim_text(text, '<div class="scorebox">', '<div class="scorebox_meta">'))
            parser.setScoreboxMeta(trim_text(text, '<div class="scorebox_meta">', '<style>'))
            parser.setAllScoring(trim_text(text, '<div class="table_container" id="div_scoring">', '<div class="content_grid">'))
            parser.setGameInfo(trim_text(text, '<div id="all_game_info"', '<div id="all_officials"'))
            parser.setAllOfficials(trim_text(text, '<div id="all_officials"', '<div id="all_expected_points"'))
            parser.setAllTeamStats(trim_text(text, '<div id="all_team_stats"', '<div id="all_player_offense"'))
            parser.setAllPlayerOff(trim_text(text, '<div id="all_player_offense"', '<div id="all_player_defense"'))
            parser.setAllPlayerDef(trim_text(text, '<div id="all_player_defense"', '<div id="all_returns"'))
            parser.setAllReturns(trim_text(text, '<div id="all_returns"', '<div id="all_kicking"'))
            parser.setAllKicking(trim_text(text, '<div id="all_kicking"', '<div id="all_passing_advanced"'))
            parser.setPassingAdv(trim_text(text, '<div id="all_passing_advanced"', '<div id="all_rushing_advanced"'))
            parser.setRushingAdv(trim_text(text, '<div id="all_rushing_advanced"', '<div id="all_receiving_advanced"'))
            parser.setReceivingAdv(trim_text(text, '<div id="all_receiving_advanced"', '<div id="all_defense_advanced"'))
            parser.setDefenseAdv(trim_text(text, '<div id="all_defense_advanced"', '<div id="all_home_starters"'))
            parser.setHomeStarters(trim_text(text, '<div id="all_home_starters"', '<div id="all_vis_starters"'))
            parser.setAwayStarters(trim_text(text, '<div id="all_vis_starters"', '<div id="all_home_snap_counts"'))
            parser.setHomeSnaps(trim_text(text, '<div id="all_home_snap_counts"', '<div id="all_vis_snap_counts"'))
            parser.setAwaySnaps(trim_text(text, '<div id="all_vis_snap_counts"', '<div id="all_home_drives"'))
            parser.setHomeDrives(trim_text(text, '<div id="all_home_drives"', '<div id="all_vis_drives"'))
            parser.setAwayDrives(trim_text(text, '<div id="all_vis_drives"', '<div id="all_pbp"'))
            parser.setPlays(trim_text(text, '<div id="all_pbp"', '<div id="bottom_nav"'))
            
            # extract game date string, home and away teams
            game_date = parser.extract_basic_info()
            today = datetime.today().date()
            if game_date < today:
                parser.parseGame()
       
    # close http connection
    conn.close()
    # write json file using game info
    write_file(json.dumps(games, indent=4))
    
# Trim body of test to start and end
def trim_text(text, start, end):
    start_idx = text.find(start)
    end_idx = text.find(end)

    return text[start_idx:end_idx]

def write_file(game_json):
    with open('json_test.json', 'w') as json_file:
        json_file.write(game_json)

# Main function
if __name__ == "__main__":
    start_time = time()
    try:
        run_scraper()
        print(time() - start_time) 
    except KeyboardInterrupt:
        print(time() - start_time)
        print("Exiting...")