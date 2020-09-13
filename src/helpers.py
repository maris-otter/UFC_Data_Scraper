class total_round_data:#
    round = -1 #tracks the round or if the object is a total
    kd = -1
    sig_strikes = ()
    total_strikes = ()
    sig_strikes_percentage = -1
    take_downs = ()
    take_down_percentage = ()
    sub_att = -1
    passes = -1
    rev = -1

    def print(self):

        # print(self.round)
        print("KD: " + str(self.kd))
        print("Sig Strikes: %s" % (self.sig_stikes,))
        print("Sig strike percentage: %s%%" % str(self.sig_strikes_percentage))
        print("Total strikes: %s" % (self.total_strikes,))
        print("Take downs: %s" % (self.take_downs,))
        print("TD percentage: %s%%" % str(self.take_down_percentage))
        print("Sub att: %s" % str(self.sub_att))
        print("Passes: %s" % str(self.passes))
        print("REV: %s" % str(self.rev))

class sig_strik_round_data: #helper class
    sig_stikes = ()
    sig_strikes_percentage = -1
    head = ()
    body = ()
    leg = ()
    distance = ()
    clinch = ()
    ground = ()

    def print(self):
        print("Sig Strikes: %s" % (self.sig_stikes,))
        print("Sig Strike %%: %s%%" % (self.sig_strikes_percentage,))
        print("Head Strikes: %s" % (self.head,))
        print("Body: %s" % (self.body,))
        print("Leg: %s" % (self.leg,))
        print("Distance: %s" % (self.distance,))
        print("Clinch: %s" % (self.clinch,))
        print("Ground: %s" % (self.ground,))




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

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class fight_details:
    event = ""
    fighter_1 = ""
    fighter_2 = ""
    #fight summary
    finish = "DATA NOT AVAILABLE"
    finish_details = "DATA NOT AVAILABLE"
    round = -1
    fight_time = ()
    referee = ""
    weight_class = "DATA NOT AVAILABLE"
    fighter1_round_data = [] #  "totals" round data list.
    fighter2_round_data = [] #  "totals" round data list.

    #fight tracking stats
    fighter1_sig_strike_data = [] #3d [fighter][round][metrics]
    fighter1_sig_strike_data = [] #3d [fighter][round][metrics]

    def print(self):
        """
        prints basic fight details
        """
        print("Event: %s" % self.event)
        print("Fighter 1: %s" % self.fighter_1)
        print("Fighter 2: %s" % self.fighter_2)
        print("Finish: %s" % self.finish)
        print("Finish Details: %s" % self.finish_details)
        print("Round: %s" % self.round)
        print("Time: %s" % (self.fight_time,))
        print("Referee: %s" % (self.referee))
        print("Weight class: %s" % self.weight_class)

    def print_fighter_stats(self):
        """
        prints every object of fighter 1 and fighter 2 round and sig strike data
        """

        #Print round 1 round data
        print(color.BOLD + "Fighter: %s Round Stats" % self.fighter_1 + color.END)
        x = 0
        for i in self.fighter1_round_data:
            if x == 0:
                print(color.RED + "--------------Totals-------------" + color.END)
            else:
                print(color.BLUE + "--------------Round %s-------------" % x + color.END)

            x += 1
            i.print()

            print("\n\n")


        #Print round 2 round data
        print(color.BOLD + "Fighter: %s Round Stats" % self.fighter_2 + color.END)
        x = 0
        for i in self.fighter2_round_data:
            if x == 0:
                print(color.RED + "--------------Totals-------------" + color.END)
            else:
                print(color.BLUE + "--------------Round %s-------------" % x + color.END)

            x += 1
            i.print()

            print("\n\n")

        ##############################

        #Print round 1 sig data
        print(color.BOLD + "Fighter: %s Round Stats" % self.fighter_1 + color.END)
        x = 0
        for i in self.fighter1_sig_strike_data:
            if x == 0:
                print(color.RED + "--------------Sig strike-------------" + color.END)
            else:
                print(color.BLUE + "--------------Round %s-------------" % x + color.END)

            x += 1
            i.print()

            print("\n\n")

        #Print round 1 sig data
        print(color.BOLD + "Fighter: %s Round Stats" % self.fighter_2 + color.END)
        x = 0
        for i in self.fighter2_sig_strike_data:
            if x == 0:
                print(color.RED + "--------------Sig strike-------------" + color.END)
            else:
                print(color.BLUE + "--------------Round %s-------------" % x + color.END)

            x += 1
            i.print()

            print("\n\n")





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
