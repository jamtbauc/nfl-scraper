import csv
from datetime import date
import http.client
from bs4 import BeautifulSoup
import re
from time import time

def get_data(base, url):
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
        
        return html.decode('ISO-8859-1')
    
def run_scraper():
    # define starting year to gather data
    year = 2011
    today = date.today()
    with open('links.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        while year <= today.year:
            # define base url and get request urls
            base = "www.pro-football-reference.com"
            url = f'/years/{year}/games.htm'
            # using defined base and request urls, get decoded data
            bytes = get_data(base, url)
            # create soup
            soup = BeautifulSoup(bytes, 'html.parser')
            # find all tags matching requirements
            data = soup.find_all(href=re.compile("/boxscores/2"))
            # append all tags to dictionary
            for link in data:
                writer.writerow([link.get('href')])
                
            # increment year to finish loop
            year += 1
    
    
if __name__ == "__main__":
    start_time = time()
    try:
        run_scraper()
        print(time() - start_time) 
    except KeyboardInterrupt:
        print(time() - start_time)
        print("Exiting...")