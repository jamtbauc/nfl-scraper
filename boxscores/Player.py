class Player:
    def __init__(self, name):
        self.__name = name
        self.__team = ""
        self.__stats = {}
        
    ### GETTER METHODS
    def get_name(self):
        return self.__name
    
    def get_stats(self):
        return self.__stats
    
    def get_team(self):
        return self.__team
    
    ## HELPER METHODS
    def add_stat(self, cat, stat):
        if cat == "team":
            self.__team = stat
        else:
            if cat not in self.__stats:
                self.__stats[cat] = -1
                
            if stat == '':
                self.__stats[cat] = 0
            else:
                self.__stats[cat] = float(stat)
                
    def print_player(self):
        print(self.__name)
        print("Stats:")
        for key in self.__stats:
            print(f"\t{key}: {self.__stats[key]}")
            
        