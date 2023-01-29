import csv
from datetime import datetime
import http.client
from lib.Parser import Parser
from time import time, sleep

# load all game urls into list
def get_urls(file):
    urls = ()
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            urls += tuple(row)
            
    return urls

# Send get request to url specified at base website. Returns response body
def request_data(conn, url):
        print(url)
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
def run_scraper(last_file_update, url_stop):
    # hold all urls
    urls = get_urls('links.csv')
    # define base url and get request urls
    base = "www.pro-football-reference.com"
    # open connection to pro-football-reference.com
    conn = http.client.HTTPSConnection(base)
    # create Parser object
    parser = Parser()
    # load existing db items into array
    url_start = parser.loadCsvGames(f"./csv/{last_file_update}games.csv")
    print(f"Updating with urls starting at: {url_start}")
    parser.loadCsvGameWeather(f"./csv/{last_file_update}gm_weathers.csv")
    parser.loadCsvOfficials(f"./csv/{last_file_update}officials.csv")
    parser.loadCsvOfficialGames(f"./csv/{last_file_update}off_gms.csv")
    parser.loadCsvPlayByPlays(f"./csv/{last_file_update}play_by_plays.csv")
    parser.loadCsvPlayers(f"./csv/{last_file_update}players.csv")
    parser.loadCsvPlayerGames(f"./csv/{last_file_update}player_games.csv")
    parser.loadCsvPlayerGameSnaps(f"./csv/{last_file_update}player_game_snaps.csv")
    parser.loadCsvScoringPlays(f"./csv/{last_file_update}scoring_plays.csv")
    parser.loadCsvStadiums(f"./csv/{last_file_update}stadiums.csv")
    parser.loadCsvTeams(f"./csv/{last_file_update}teams.csv")
    parser.loadCsvTeamGames(f"./csv/{last_file_update}team_games.csv")
    parser.loadCsvTeamGameDrive(f"./csv/{last_file_update}team_game_drives.csv")
    # loop through all urls
    for url in urls:
        url_date = url[11:19]
        if url_date > url_start and url_date < url_stop:
            try:
                bytes = request_data(conn, url)
                sleep(3)
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
                
                parser.extract_basic_info()
                parser.parseGame()
            except:
                parser.addErrorUrl(url)
                
    # close http connection
    conn.close()
    
    # write files
    parser.writeFiles()
    
# Trim body of test to start and end
def trim_text(text, start, end):
    start_idx = text.find(start)
    end_idx = text.find(end)

    return text[start_idx:end_idx]

# Main function
if __name__ == "__main__":
    start_time = time()
    try:
        # Param 1: last file update date
        # Parama 2: Day to stop
        run_scraper("20230129", "20230128")
        print(time() - start_time) 
    except KeyboardInterrupt:
        print(time() - start_time)
        print("Exiting...")