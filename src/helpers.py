class total_round_data:#
    kd = -1
    sig_strikes = ()
    sig_strikes_percentage = -1
    take_downs = -1
    sub_att = -1
    passes = -1
    rev = -1

class sig_strik_round_data: #helper class
    sig_stikes = ()
    sig_strikes_percentage = -1
    head = ()
    body = ()
    leg = ()
    distance = ()
    clinch = ()
    ground = ()


class f_history:
    wins = -1
    loss = -1
    no_contest = -1

class career_stats:
    splm = 0
    sig_acc = 0
    sig_absorbed = 0
    sig_strike_defense = 0
    average_takedown = 0
    takedown_acc = 0
    takedown_defense = 0
    sub_average = 0


class fight_details:
    event = ""
    fighter_1 = ""
    fighter_2 = ""
    #fight summary
    finish = "DATA NOT AVAILABLE"
    round = -1
    time = ()#################
    ref = ""
    weight_class = "DATA NOT AVAILABLE"
    round_data = [] # 3d "totals" round data list. [fighter][round][metrics]

    #fight tracking stats
    sig_strike_data = [] #3d [fighter][round][metrics]


class f_history:
    wins = -1
    loss = -1
    no_contest = -1

class career_stats:
    splm = 0
    sig_acc = 0
    sig_absorbed = 0
    sig_strike_defense = 0
    average_takedown = 0
    takedown_acc = 0
    takedown_defense = 0
    sub_average = 0

class Fighter:
    name = ""
    height = ()
    weight = 0
    reach = 0
    stance = 0 # 1 = orthodox 2 = southpaw
    DOB = ()
    history = f_history()
    career_stat = career_stats()
    record = f_history()
    fights = [] #list of fight_details objects


    def print(self):
        print( "Fighter name: " + self.name)
        print(str(self.history.wins)  + "-" + str(self.history.loss) + "-" + str(self.history.no_contest))
        print( str(self.height))
        print("Weight: " + str(self.weight))
        print("Reach: " + str(self.reach))
        print("Stance: " + str(self.stance))
        print(self.DOB)
        print("Sig strike per minute: " + self.career_stat.splm)
        print("Sig strike acc: " + str(self.career_stat.sig_acc))
        print("Sig strike absorbed: " + str(self.career_stat.sig_absorbed))
        print("Sig strike defense: " + str(self.career_stat.sig_strike_defense))
        print("Average Takedowns: " + self.career_stat.average_takedown)
        print("Takedown acc: " + str(self.career_stat.takedown_acc))
        print("Takedown defense: " + str(self.career_stat.takedown_defense))
        print("Sub average: " + self.career_stat.sub_average)
        print("---------------------------------\n")
