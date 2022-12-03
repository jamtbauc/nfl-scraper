import csv
from datetime import datetime
from time import time

class dkPlayer:
    def __init__(self, name, pos, team):
        self.id = None
        self.name = name
        self.position = pos
        self.team = team
        self.salary = None
        self.loc = None
        self.opponent = None
        self.time = None
        self.avg_pts = None
    
    def setId(self, val):
        self.id = int(val)
        
    def setSalary(self, val):
        self.salary = int(val)
        
    def setAvgPts(self, val):
        self.avg_pts = float(val)
        
    def setGameInfo(self, val):
        items = val.split(' ')
        
        matchup = items[0]
        date_str = items[1]
        time_str = items[2]
        
        tms = matchup.split('@')
        if tms[0] == self.team:
            self.opponent = tms[1]
            self.loc = 'Away'
        else:
            self.opponent = tms[0]
            self.loc = 'Home'
            
        dt_str = date_str + " " + time_str
        self.time = datetime.strptime(dt_str, "%m/%d/%Y %I:%M%p")
        
    def printInfo(self):
        info = {
            "id": self.id,
            "name": self.name,
            "pos": self.position,
            "team": self.team,
            "salary": self.salary,
            "loc": self.loc,
            "opp": self.opponent,
            "date": self.time.isoformat(),
            "avg_pts": self.avg_pts
        }
        

def run_report(file_name):
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        
        for row in reader:
            player = dkPlayer(
                row[2],
                row[0],
                row[7],                
            )
            
            player.setId(row[3])
            player.setSalary(row[5])
            player.setAvgPts(row[8])
            player.setGameInfo(row[6])
            player.printInfo()

# Main function
if __name__ == "__main__":
    start_time = time()
    try:
        run_report("DKSalaries.csv")
        print(time() - start_time) 
    except KeyboardInterrupt:
        print(time() - start_time)
        print("Exiting...")