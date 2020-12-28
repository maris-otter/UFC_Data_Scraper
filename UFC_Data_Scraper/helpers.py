#third party imports
from tqdm import tqdm #progress bar from github
from bs4 import BeautifulSoup

#Std library imports
import requests
import re
import os
import csv

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

    def __new__(cls):
        instance = super(total_round_data, cls).__new__(cls)
        return instance

    def __init__(self):
        self.round = -1
        self.kd = -1
        self.sig_strikes = ()
        self.total_strikes = ()
        self.sig_strikes_percentage = -1
        self.take_downs = ()
        self.take_down_percentage = ()
        self.sub_att = -1
        self.passes = -1
        self.rev = -1

    def as_json(self):
        """
        creates dictionary out of values stored in class
        """
        dict = {
                "kd": self.kd, "sig_strikes": self.sig_stikes,
                "total_strikes": self.total_strikes,
                "sig_strikes_percentage": self.sig_strikes_percentage,
                "take_downs": self.take_downs,
                "take_down_percentage": self.take_down_percentage,
                "sub_att": self.sub_att, "passes": self.passes, "rev": self.rev
                }
        return dict
    # def csv(self):
    #     return f"{self.round},{self.kd},{(self.sig_strikes,)},{(self.total_strikes,)}, {self.sig_strikes_percentage}, {(self.take_downs,)},{(self.take_down_percentage,)}, {self.sub_att}, {self.passes}, {self.rev}"



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

    def __init__(self):
        self.sig_stikes = ()
        self.sig_strikes_percentage = -1
        self.head = ()
        self.body = ()
        self.leg = ()
        self.distance = ()
        self.clinch = ()
        self.ground = ()

    def __new__(cls):
        instance = super(sig_strik_round_data, cls).__new__(cls)
        return instance

    def csv(self):
        return f"{(self.sig_stikes,)},{self.sig_strikes_percentage},{(self.head,)},{(self.body,)},{(self.leg,)},{(self.distance,)},{(self.clinch,)},{(self.ground,)}"

    def print(self):
        print("Sig Strikes: %s" % (self.sig_stikes,))
        print("Sig Strike %%: %s%%" % (self.sig_strikes_percentage,))
        print("Head Strikes: %s" % (self.head,))
        print("Body: %s" % (self.body,))
        print("Leg: %s" % (self.leg,))
        print("Distance: %s" % (self.distance,))
        print("Clinch: %s" % (self.clinch,))
        print("Ground: %s" % (self.ground,))

    def as_json(self):
        """
        creates dictionary out of values stored in class
        """
        dict = {
                "sig_stikes": self.sig_stikes,
                "sig_strikes_percentage": self.sig_strikes_percentage,
                "head": self.head, "body": self.body, "leg": self.leg,
                "distance": self.distance, "clinch": self.clinch,
                "ground": self.ground
                }
        return dict

class f_history:
    wins = -1
    loss = -1
    no_contest = -1

    def __new__(cls):
        instance = super(f_history, cls).__new__(cls)
        return instance

    def __init__(self):
        self.wins = -1
        self.loss = -1
        self.no_contest = -1

class career_stats:
    splm = 0
    sig_acc = 0
    sig_absorbed = 0
    sig_strike_defense = 0
    average_takedown = 0
    takedown_acc = 0
    takedown_defense = 0
    sub_average = 0

    def __new__(cls):
        instance = super(career_stats, cls).__new__(cls)
        return instance

    def __init__(self):
        self.splm = 0
        self.sig_acc = 0
        self.sig_absorbed = 0
        self.sig_strike_defense = 0
        self.average_takedown = 0
        self.takedown_acc = 0
        self.takedown_defense = 0
        self.sub_average = 0

class color:#taken from Stack overflow
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
    winner = -2
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
    fighter1_sig_strike_data = [] #list of sig_strik_round_data objects
    fighter2_sig_strike_data = [] #list of sig_strik_round_data objects

    def __new__(cls):
        instance = super(fight_details, cls).__new__(cls)
        return instance

    def __init__(self):
        self.event = ""
        self.fighter_1 = ""
        self.fighter_2 = ""
        self.winner = -2
        self.finish = ""
        self.finish_details = ""
        self.round = -1
        self.fight_time = ()
        self.referee = ""
        self.weight_class = ""
        self.fighter1_round_data = []
        self.fighter2_round_data = []


    def print(self):
        """
        prints basic fight details
        """
        print("Event: %s" % self.event)
        print("Fighter 1: %s" % self.fighter_1)
        print("Fighter 2: %s" % self.fighter_2)
        print(f"Winner: Fighter {self.winner}")
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
        print(color.BOLD + f"Fighter: {self.fighter_1} Round Stats"  + color.END)
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
        print(color.BOLD + f"Fighter: {self.fighter_2} Round Stats"  + color.END)
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
        print(color.BOLD + f"Fighter: {self.fighter_1} Round Stats"  + color.END)
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
        print(color.BOLD + f"Fighter: {self.fighter_2} Round Stats" + color.END)
        x = 0
        for i in self.fighter2_sig_strike_data:
            if x == 0:
                print(color.RED + "--------------Sig strike-------------" + color.END)
            else:
                print(color.BLUE + "--------------Round %s-------------" % x + color.END)

            x += 1
            i.print()

            print("\n\n")

    def as_json(self):
        """
        iterates through round_data and fight_data list and creates and returns
        Json
        """
        fighter1_json = {}
        fighter2_json = {}
        totals1_json = {}
        totals2_json = {}
        sig1_json = {}
        sig2_json = {}

        #iteratae through list and create sub dictionaries in above dicts
        index = 0
        for round in range(len(self.fighter1_round_data)):
            #first round will be denotes with 'overall'
            if round == 0:
                totals1_json['overall'] = self.fighter1_round_data[round].as_json()
                totals2_json['overall'] = self.fighter2_round_data[round].as_json()
                sig1_json['overall'] = self.fighter1_sig_strike_data[round].as_json()
                sig2_json['overall'] = self.fighter2_sig_strike_data[round].as_json()
            else:
                totals1_json[round] = self.fighter1_round_data[round].as_json()
                totals2_json[round] = self.fighter2_round_data[round].as_json()
                sig1_json[round] = self.fighter1_sig_strike_data[round].as_json()
                sig2_json[round] = self.fighter2_sig_strike_data[round].as_json()

        fighter1_json = {'Totals': totals1_json, 'Significant': sig1_json}
        fighter2_json = {'Totals': totals2_json, 'Significant': sig2_json}

        fight_details_json = {
                            'event': self.event, 'fighter1': self.fighter_1,
                            'fighter2': self.fighter_2, 'winner': self.winner,
                            'finish': self.finish, 'finish_details': self.finish_details,
                            "rounds": self.round, "fight_time": self.fight_time,
                            "referee": self.referee, "weight_class": self.weight_class,
                            'Fighter_1': fighter1_json, 'Fighter_2': fighter2_json
                            }

        return fight_details_json


class Fighter:
    name = ""
    height = ()
    weight = -1
    reach = -1
    stance = -1 # 1 = orthodox 2 = southpaw 3 = Switch
    DOB = ()
    history = f_history()
    career_stat = career_stats()
    record = f_history()
    fights = [] #list of fight_details objects

    def __new__(cls):
        instance = super(Fighter, cls).__new__(cls)
        return instance

    def __init__(self):
        self.name = ""
        self.height = ()
        self.weight = -1
        self.reach = -1
        self.stance = -1
        self.DOB = ()
        self.history = f_history()
        self.career_stat = career_stats()
        self.record = f_history()
        self.fights = []

    def print(self):
        print( "Fighter name: " + self.name)
        print(str(self.history.wins)  + "-" + str(self.history.loss) + "-" + str(self.history.no_contest))
        print( str(self.height))
        print("Weight: " + str(self.weight))
        print("Reach: " + str(self.reach))
        print("Stance: " + str(self.stance))
        print(self.DOB)
        print("Sig strike per minute: " + str(self.career_stat.splm))
        print("Sig strike acc: " + str(self.career_stat.sig_acc))
        print("Sig strike absorbed: " + str(self.career_stat.sig_absorbed))
        print("Sig strike defense: " + str(self.career_stat.sig_strike_defense))
        print("Average Takedowns: " + str(self.career_stat.average_takedown))
        print("Takedown acc: " + str(self.career_stat.takedown_acc))
        print("Takedown defense: " + str(self.career_stat.takedown_defense))
        print("Sub average: " + str(self.career_stat.sub_average))
        print("---------------------------------\n")

    def as_json(self):
#chagned self.record to self.history
        dict = {
                "name": self.name, "height": self.height, "weight": self.weight,
                "reach": self.reach, "stance": self.stance, "DOB": self.DOB,
                "wins": self.history.wins, "loss": self.history.loss,
                "no_contest": self.history.no_contest, "splm": self.career_stat.splm,
                "sig_acc": self.career_stat.sig_acc,
                "sig_absorbed": self.career_stat.sig_absorbed,
                "sig_strike_defense": self.career_stat.sig_strike_defense,
                "average_takedown": self.career_stat.average_takedown,
                "takedown_acc": self.career_stat.takedown_acc,
                "takedown_defense": self.career_stat.takedown_defense,
                "sub_average": self.career_stat.sub_average
                }
        return dict


#begin helper funcitions
#Helpers

#Constants
SAVE_FIGHT_DIR = "fight_history"
SAVE_FIGHTER_DIR = "fighter_data_https"

def is_dir_correct(dir):
    """
    check if the current working directory is dir passed as argument

    True: current directory is the directory passed
    False: current directory is not the directory passed
    """
    starting_dir = os.getcwd()
    regex = re.search(dir, str(starting_dir))

    if regex is None:
        return False

    return True

def save_html(html, path):
    try:
        with open(path, 'wb') as f:
            f.write(html)
    except Exception as e:
        print("\n\nAn Exception occured while trying to save %s" % path)
        print(e)

#opens a local html file and returns it as an object
def open_html(path):
    with open(path, 'rb') as f:
        return f.read()

def get_fighter_links():
    """creates a list of links to fighter pages from ufcstat.com

    return: list of fighter links
    """
    #create a list of each letter in alphabet
    list_alphabet = []

    alpha = 'a'
    for i in range(0, 26):
        list_alphabet.append(alpha)
        alpha = chr(ord(alpha) + 1)

    #Get all links to fighters by going throgh each letter in 'char=%s'
    #Append each set of links to the oveerall links
    print("Finding all fighter links.....")
    index = 0
    links = []
    for letters in tqdm(list_alphabet):
        url = "http://www.ufcstats.com/statistics/fighters?char={}&page=all".format(letters)

        r = requests.get(url)


        soup = BeautifulSoup(r.content, 'html.parser')

        #Start parsing the file
        #Target every link within each row
        parsed_a_tags = soup.find_all('a', href=True)

        #creates a list of all of the links on the page
        href_collection = [a['href'] for a in parsed_a_tags]

        #adds all links of fighter to a list
        temp_links = []
        for item in href_collection:
            if "fighter-details" in item:
                temp_links.append(item)

        #remove any duplicates
        temp_links = list(dict.fromkeys(temp_links))

        links.extend(temp_links)

    return links

def get_fighter_http(dir, save_to_dir=False):
    """
    Save the html page of each fighter in get_fighter_links

    return: list of each fighters http page
    """
    links = get_fighter_links()
    list_of_https = []

    print("Getting fighter https....")
    x = 1 #tracks index of for loop below
    for link in tqdm(links):
        r = requests.get(link)
        list_of_https.append(r.content)

        if(save_to_dir == True):
            save_html(r.content, f"{dir}/Fighter {x}")

        x += 1

    return list_of_https

#Takes a http from page and creates a fighter object with stats filled
def get_fighter_stats(http_page='None', http_url='None', save = False, dir = SAVE_FIGHTER_DIR):
    """
    populates a Fighter() class object with all attributes available on given
    http_page.

    args:
        http_page - a fighter http page with base domain
        "http://www.ufcstats.com/fighter-details/"

    returns: Fighter object
    """
    if save == True and dir == None:
        print("get_fighter_stats called incorrectly. Optional arguments wrong")
        exit()

    #Create fighter object
    fighter = Fighter()

    #Based on which optional argument used. Create BeautifulSoup object
    if http_page != 'None':
        page = open_html(http_page)
        soup = BeautifulSoup(page, 'html.parser')
    elif http_url != 'None':
        page = requests.get(http_url)

        if save:
            save_html(page.content, f"{dir}/{http_url[-16:]}")

        soup = BeautifulSoup(page.content, 'html.parser')
    else:
        print("get_fighter_stats() used incorrectly")
        raiseS


    #Get name--------
    #Targets html tag with name of fighter
    name_target = soup.find_all("span", class_="b-content__title-highlight")

    #isolates text within tag
    if not len(name_target) == 0:
        fighter_name = name_target[0].text
    else:
        fighter_name = "UNABLE TO GET NAME"

    fighter_name =' '.join(fighter_name.split())

    # assigns name
    fighter.name = fighter_name

    #Get record--------
    record_target = soup.find_all("span", class_="b-content__title-record")
    fight_record_raw = record_target[0].text # Record: ?-?-?

    #clean string
    fight_record_raw =' '.join(fight_record_raw.split())

    #remove first 8 characters from record
    fight_record_clean = fight_record_raw[8:14]
    fight_record_clean = fight_record_clean.split("-")

    #assign win, loss, and no contest to fighter object
    fighter.history.wins = fight_record_clean[0]
    fighter.history.loss = fight_record_clean[1]

    #Blank string gets assigned as 0
    if not fight_record_clean[2]:
        fighter.history.no_contest = 0
    else:
        fighter.history.no_contest = fight_record_clean[2]


    #Get rows of the fighters basic information
    stat_rows = soup.find_all("li", class_="b-list__box-list-item b-list__box-list-item_type_block")

    stat_rows_text = []

    #iterate through all rows of stats and delete extra white space.
    i = 0
    for tags in stat_rows:
        temp = stat_rows[i].text
        temp = ' '.join(temp.split())

        #Doesn't allow empty strings to be appended to list
        if temp:
            stat_rows_text.append(temp)
        i +=1


    height_raw = stat_rows_text[0]
    #Removes "Height:" from string and leaves ?' ?"
    height_clean = height_raw[7:]

    #Remove characters from height
    height_clean = height_clean.replace('"', ' ')
    height_clean = height_clean.replace("'", ' ')


    #Assign height to fighter object
    fighter.height = height_clean.split()

    #get weight--------
    weight = stat_rows_text[1]
    weight_regex = re.compile('\d{2,3}') #Create regex object for search
    weight = weight_regex.search(weight) #Find pattern

    #Assign weight if data is available
    try:
        weight = weight.group()#use result as weight
    except AttributeError:
        weight = -1#No data for reach

    fighter.weight = weight

    #Get reach----------
    reach = stat_rows_text[2]
    reach_regex = re.compile('\d\d')
    reach = reach_regex.search(reach)#search for two digits that form reach

    #Assign reach if data is available
    try:
        reach = reach.group()
    except AttributeError:
        reach = -1 #no data for reach


    fighter.reach = reach#Assign reach to fighter

    # get stance ... 1 or 2 ... check class def
    stance = stat_rows_text[3]
    stance = stance[8:]

    if stance == "Orthodox":
        fighter.stance = 1  #orthodox
    elif stance == "Southpaw":
        fighter.stance = 2 # southpaw
    elif stance == "Switch":
        fighter.stance = 3
    else:
        fighter.stance = -1 #Error parsing if executed

    #Get DOB
    DOB = stat_rows_text[4]
    DOB = DOB[4:]

    fighter.DOB = DOB.split()

    #Start parsing carreer stats
    career_stat_rows = soup.find_all("ul", class_="b-list__box-list b-list__box-list_margin-top")

    carrer_stat_text = []

    i = 0
    #iterate through rows retrieve text and remove white space
    for item in career_stat_rows:
        temp = career_stat_rows[i].text
        temp = ' '.join(temp.split())
        carrer_stat_text.append(temp)
        i += 1

    #Get splm
    splm_regex = re.compile('SLpM:\s\d.\d\d')
    splm = splm_regex.search(carrer_stat_text[0])

    #If search returns a result then assign result to splm var
    try:
        splm = splm.group()
    except AttributeError:
        splm = -1 #no data for reach

    if splm != -1:
        fighter.career_stat.splm = splm[6:]

    #Get str acc
    sig_acc_regex = re.compile('Str.\sAcc.:\s\d\d')
    sig_acc = sig_acc_regex.search(carrer_stat_text[0])

    #assign search result to var if found
    try:
        sig_acc = sig_acc.group()
    except AttributeError:
        sig_acc = -1 #no data for reach

    #if in proper format take substring for assignment to fighter object
    if sig_acc != -1 :
        sig_acc = sig_acc[11:]

    fighter.career_stat.sig_acc = sig_acc

    #Get SApM
    sapm_regex = re.compile('SApM:\s\d.\d\d')
    sapm = sapm_regex.search(carrer_stat_text[0])

    try:
        sapm = sapm.group()
    except AttributeError:
        sapm = -1

    if sapm != -1:
        sapm = sapm[6:]

    fighter.career_stat.sig_absorbed = sapm

    #Get Significant Strike Defence
    sig_strike_defense_regex = re.compile('Str. Def:\s\d{1,3}')
    sig_strike_defence = sig_strike_defense_regex.search(carrer_stat_text[0])

    try:
        sig_strike_defence = sig_strike_defence.group()
    except AttributeError:
        sig_strike_defence = -1

    if sig_strike_defence != -1:
        sig_strike_defence = sig_strike_defence[10:]

    fighter.career_stat.sig_strike_defense = sig_strike_defence

    #Get TD avg
    td_avg_regex = re.compile('TD\sAvg.:\s\d.\d\d')
    td_avg = td_avg_regex.search(carrer_stat_text[1])

    try:
        td_avg = td_avg.group()
    except AttributeError:
        td_avg = -1

    if td_avg != -1:
        td_avg = td_avg[9:]

    fighter.career_stat.average_takedown = td_avg

    #Get takedown_acc

    takedown_acc_regex = re.compile('TD\sAcc.:\s\d{1,3}')
    takedown_acc = takedown_acc_regex.search(carrer_stat_text[1])

    try:
        takedown_acc = takedown_acc.group()
    except AttributeError:
        takedown_acc = -1

    if takedown_acc != -1:
        takedown_acc = takedown_acc[9:]

    fighter.career_stat.takedown_acc = takedown_acc

    #Get takedown_defense
    takedown_defense_regex = re.compile('TD\sDef.:\s\d{1,3}%')
    takedown_defense = takedown_acc_regex.search(carrer_stat_text[1])

    try:
        takedown_defense = takedown_defense.group()
    except AttributeError:
        takedown_defense = -1

    if takedown_defense != -1:
        takedown_defense = takedown_defense[9:]

    fighter.career_stat.takedown_defense = takedown_defense


    #Get sub_average
    sub_average_regex = re.compile('Sub.\sAvg.:\s\d.\d')
    sub_average = sub_average_regex.search(carrer_stat_text[1])

    try:
        sub_average = sub_average.group()
    except AttributeError:
        sub_average = -1

    if sub_average != -1:
        sub_average = sub_average[11:]

    fighter.career_stat.sub_average = sub_average

    return fighter

def get_all_a_tags(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    #Get all links on the page
    parsed_a_tags = soup.find_all('a', href=True)
    href_collection = [a['href'] for a in parsed_a_tags]

    return href_collection

def get_all_event_history_links():
    """From ufcstat website finds all completed fights and saves
    the http into the current working directory

    """
    url = "http://www.ufcstats.com/statistics/events/completed?page=all"

    href_collection = get_all_a_tags(url)
    #Add all links to list that have event-details in them
    links = []
    for i in href_collection:
        site_regex = re.search('event-details', i)
        if site_regex is not None:
            links.append(i)

    links = list(dict.fromkeys(links))

    return links

def append_used_link(link, tracker = False, link_error = False):
    """appends a link to the txt file being used to track all links in directory
    args:
        link - url to the page being tracked
    """
    tracking_filename = 'saved_http_tracker.txt'
    error_filename = 'error_tracker.txt'

    #for parsing links
    if tracker:
        #if tracking file does not exisit create it
        if not os.path.exists(tracking_filename):
            with open(tracking_filename, 'w'): pass

        try:
            with open(tracking_filename, 'a') as f:
                f.write(link)
                f.write('\n')
        except Exception:
            print("Unable to save URL to %s" % tracking_filename)
    elif link_error:
        if not os.path.exists(error_filename):
            with open(error_filename, 'w'): pass

        try:
            with open(error_filename, 'a') as f:
                f.write(link)
                f.write('\n')
        except Exception:
            print("Unable to save URL to %s" % error_filename)
    else:
        raise

def parsing_error_tracker(error, error_file, filename='parsing_error.txt'):
    if not os.path.exists(filename):
        with open(filename, 'w'): pass

    try:
        with open(filename, 'a') as f:
            f.write(str(error))
            f.write('\n')
            f.write(error_file)
            f.write('\n\n')
    except Exception as e:
        print(e)
        print(f"An error occured appending ({error}) to {filename}")
        raise

# TODO: See if append_used_link is being used twice here and above func
def get_fight_history_http(http_page = 'None', requests_url = 'None', save = False):
    """
    requests and saves all https of fights a fighter has had. Takes either a url
    or a http page file path

    args: http_page - any fighters page from "fighter-details" site directory
        requests_url - a url to an event-details page

    kwargs: save - if save is true each http will be saved to directory

    Exception: Both optional arguments are used

    returns: list of https
    """

    if requests_url == 'None':
        page = open_html(http_page)
        soup = BeautifulSoup(page, 'html.parser')

    elif requests_url != 'None':
        page = requests.get(requests_url)
        soup = BeautifulSoup(page.content, 'html.parser')
    else:
        print("get_fight_history_http used incorrectly. Only one argument")
        raise

    #Start parsing the file
    #Target every link within each row
    parsed_a_tags = soup.find_all('a', href=True)

    #creates a list of all of the links on the page
    href_collection = [a['href'] for a in parsed_a_tags]

    #adds all links of fighter to a list
    links = []
    for item in href_collection:
        if "fight-details" in item:
            links.append(item)

    if len(links) == 0:
        raise

    https = []
    #Removes duplicate links
    links = list(dict.fromkeys(links))
    x = 0
    for item in links:
        r = requests.get(item)
        if save:
            save_name = item[-16:]
            save_html(r.content, "%s" % save_name)
            append_used_link(item, tracker = True)
        else:
            https.append(r.content)
        x += 1

    return https

def parse_table_rows(http):
    """
    parses all fight data from html file into a list that splits both individual
    fight data and specific row data
    args:
        http - fight-details http from ufcstats.com

    returns: 3d list; [fighter][data row][column of data row]

    """
    try:
        page = open_html(http)
    except Exception:
        print("Error in parse_table_rows. Unable to open file %s" % http)
        return

    soup = BeautifulSoup(page, 'html.parser')

    names = ()
    temp = []
    #Get fighter names
    x = 0
    for tag in soup.find_all('h3', class_="b-fight-details__person-name"):
        for anchor in tag.find_all('a'):
            temp.append(anchor.text)

    names = temp

    #Get table columns and add to list for further parsing
    stat_col = []
    for tag in soup.find_all('td', class_="b-fight-details__table-col"):
        for anchor in tag.find_all(class_="b-fight-details__table-text"):
            stat_col.append(anchor.text)


    fighter_1 = []
    fighter_2 = []

    #Even index go to fighter 1. Odd go to fighter 2 based on format of scrape
    x = 0
    for items in stat_col:
        if x % 2 == 0: #if on even index assing to certain fighter
            items = ' '.join(items.split()) #Remove extra white space
            fighter_1.append(items)
        else:#odd index assign to other fighters
            items = ' '.join(items.split())#Remove extra white space
            fighter_2.append(items)

        x += 1

    try:
        stat_rows = [split_html_data_list(fighter_1,fighter_1[0]),
                    split_html_data_list(fighter_2,fighter_2[0])]
    except Exception:
        raise

    return stat_rows

def split_html_data_list(collection, fighter_name):
    """Splits the list of parsed html data into smaller chunks.

    Splits the list of parsed html data based on the fighter's name, which
    is the mod that starts a new row.

    """
    indices = [i for i, x in enumerate(collection) if x == fighter_name]
    collection_of_collections = [None] * (len(indices))
    for i in range(len(indices)):
        if i == len(indices) - 1 :
            collection_of_collections[i] = collection[indices[i]:]
        else:
            collection_of_collections[i] = collection[indices[i]:indices[i+1]]
    return collection_of_collections

def assign_fight_data(fight_history_collection, http):
    """Seperate round data from "Totals" and "Significant strikes" data. Then
    scrape remaining data from http and assign to fight-details object

    args: fight_history_collection - list from parse_table_rows function
    http: fight stat http page in relation to collection

    returns: fight_details object
    """
    #open http page
    page = open_html(http)
    soup = BeautifulSoup(page, 'html.parser')

    #Find finishing round; convert to int
    round = soup.body.find("i", class_="b-fight-details__text-item")
    round = round.text
    round = " ".join(round.split())
    round = round[7:]
    round = int(round)


    #Get event
    title_raw = soup.find(class_='b-link')
    title = title_raw.text
    title = " ".join(title.split())

    #Get list of raw base details
    base_fight_details_raw = soup.find_all(class_="b-fight-details__text-item")
    base_fight_details = []

    #parse raw list for attributes

    #remove white space
    for i in base_fight_details_raw:
        temp = i.text
        temp = " ".join(temp.split())
        base_fight_details.append(temp)

    #Get finish
    finish = soup.find('i', class_="b-fight-details__text-item_first")
    finish = finish.text
    finish = " ".join(finish.split())
    finish = finish[8:]

    #get finish details
    finish_details = soup.find_all('p', class_="b-fight-details__text")
    finish_details = finish_details[1].text
    finish_details = " ".join(finish_details.split())
    finish_details = finish_details[9:]

    #Get time
    time_regex = re.search('\d:\d\d', base_fight_details[1])

    try:
        time = time_regex.group()
        time = time.split()
    except Exception:
        time = (-1,-1)

    #Get ref
    referee = base_fight_details[3]
    referee = referee[9:]

    #Get weight class
    weight_raw = soup.find(class_="b-fight-details__fight-title")
    weight = weight_raw.text
    weight = " ".join(weight.split())

    #Split totals and sig strike data based on number of rounds
    totals = [fight_history_collection[0][0:round+1], fight_history_collection[1][0:round+1]]
    sig_strikes = [fight_history_collection[0][round+1:], fight_history_collection[1][round+1:]]

    #Assign round and sig stike data for fighter 1
    fighter1_round_data = [round_total_assign(totals[0][i]) for i in range(len(totals[0]))]
    fighter1_sig_strike_data = [assign_sig_data(sig_strikes[0][i]) for i in range(len(sig_strikes[0]))]

    #Assign round and sig stike data for fighter 2
    fighter2_round_data = [round_total_assign(totals[1][i]) for i in range(len(totals[1]))]
    fighter2_sig_strike_data =  [assign_sig_data(sig_strikes[1][i]) for i in range(len(sig_strikes[1]))]

    #Get the winner
    winner_raw = soup.find_all(class_ = "b-fight-details__person")

    winner_clean_text = []
    for i in winner_raw:
        i = i.text
        i =  ' '.join(i.split())
        winner_clean_text.append(i)

    winner = 0 #Default value
    if winner_clean_text[0][0] == 'W':
        winner = 1
    elif winner_clean_text[1][0] == 'W':
        winner = 2
    else: #only will execute if an error occured
        winner = -1



    fight = fight_details()

    fight.event = title
    fight.fighter_1 = totals[0][0][0]
    fight.fighter_2 = totals[1][0][0]
    fight.finish = finish
    fight.finish_details = finish_details
    fight.round = round
    fight.fight_time = time
    fight.referee = referee
    fight.weight_class = weight
    fight.fighter1_round_data = fighter1_round_data
    fight.fighter2_round_data = fighter2_round_data
    fight.fighter1_sig_strike_data = fighter1_sig_strike_data
    fight.fighter2_sig_strike_data = fighter2_sig_strike_data
    fight.winner = winner

    return fight

def round_total_assign(totals_collection):
    """
    cleans and assigns a row of data from totals produced in organize_fight_data

    args:
        totals_collection - a single row or round of fight data from totals

    return:
        total_round_data object with all attributes entered excluding round
        finished
    """
    round_data_return = total_round_data()

    #Ignore first index - this is name

    #clean and assign knock downs
    round_data_return.kd = int(totals_collection[1])

    #clean and assign sig_strike totals
    ratio_regex = re.compile('\d{1,3}')
    ratio = ratio_regex.findall(totals_collection[2])
    try:
        round_data_return.sig_stikes = (int(ratio[0]),int(ratio[1]))
    except Exception:
        round_data_return.sig_stikes = (-1,-1)

    #clean and assign sig strike percentage
    ratio_regex = re.compile('\d{1,2}')
    ratio = ratio_regex.search(totals_collection[3])
    try:
        round_data_return.sig_strikes_percentage = ratio.group()
    except Exception:
        round_data_return.sig_strikes_percentage = -1

    #Clean and assign total strikes
    ratio_regex = re.compile('\d{1,3}')
    ratio = ratio_regex.findall(totals_collection[4])
    try:
        round_data_return.total_strikes = (int(ratio[0]), int(ratio[1]))
    except Exception:
        round_data_return.total_strikes = (-1,-1)

    #Clean and assign TD
    ratio = ratio_regex.findall(totals_collection[5])
    try:
        round_data_return.take_downs = (int(ratio[0]), int(ratio[1]))
    except Exception:
        round_data_return.take_downs = (-1,-1)

    #clean and assign take down percentage
    ratio_regex = re.compile('\d{1,2}')
    ratio = ratio_regex.search(totals_collection[6])
    try:
         round_data_return.take_down_percentage = int(ratio.group())
    except Exception:
         round_data_return.take_down_percentage = -1

    #clean and assign sub attributes
    round_data_return.sub_att = totals_collection[7]

    #Clean and assign pass
    round_data_return.passes = totals_collection[8]

    #Clean and assign rev
    round_data_return.rev = totals_collection[9]

    return round_data_return

def assign_sig_data(sig_collection):
    """cleans and assigns row of data produced by organized_fight_data

    args: sig_collection - a single row or round of fight data from sig_strikes

    returns:
        sig_strik_round_data object with all attributes entered excluding round
        finished
    """
    DEFAULT_TUPLE = (-2,-2)
    DEFAULT_VALUE = -1
    sig_round_data = sig_strik_round_data()

    #clean sig strike ratio data
    ratio_regex = re.compile('\d{1,3}')
    ratio = ratio_regex.findall(sig_collection[1])

    #attempt to assign data. If no pattern found assign -1
    try:
        sig_round_data.sig_stikes = (int(ratio[0]), int(ratio[1]))
    except Exception:
        sig_round_data.sig_stikes = DEFAULT_TUPLE

    #clean sig strike percentage
    percentage_regex = re.compile('\d{1,2}')
    ratio = percentage_regex.search(sig_collection[2])

    #attempt to assign percentage. if no pattern found assign -1
    try:
        sig_round_data.sig_strikes_percentage = ratio.group()
    except Exception:
        sig_strik_round_data.sig_strikes_percentage = DEFAULT_VALUE

    #clean head strikes ratio data
    ratio = ratio_regex.findall(sig_collection[3])

    #attempt to assign
    try:
        sig_round_data.head = (int(ratio[0]), int(ratio[1]))
    except Exception:
        sig_round_data.head = DEFAULT_TUPLE


    #clean body strikes ratio data
    ratio = ratio_regex.findall(sig_collection[4])

    #attempt to assign
    try:
        sig_round_data.body = (int(ratio[0]),int(ratio[1]))
    except Exception:
        sig_round_data.body = DEFAULT_TUPLE

    #clean leg ratio data
    ratio = ratio_regex.findall(sig_collection[5])

    #attempt to assign
    try:
        sig_round_data.leg = (int(ratio[0]), int(ratio[1]))
    except Exception:
        sig_round_data.leg = DEFAULT_TUPLE

    #Clean distance ratio data
    ratio = ratio_regex.findall(sig_collection[6])

    try:
        sig_round_data.distance = (int(ratio[0]), int(ratio[1]))
    except Exception:
        sig_round_data.distance = DEFAULT_TUPLE

    #clean clinch ratio data
    ratio = ratio_regex.findall(sig_collection[7])

    try:
        sig_round_data.clinch = (int(ratio[0]), int(ratio[1]))
    except Exception:
        sig_round_data.clinch = DEFAULT_TUPLE

    ratio = ratio_regex.findall(sig_collection[8])

    try:
        sig_round_data.ground = (int(ratio[0]), int(ratio[1]))
    except Exception:
        sig_round_data.clinch = DEFAULT_TUPLE

    return sig_round_data
