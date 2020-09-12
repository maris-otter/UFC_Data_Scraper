from bs4 import BeautifulSoup
from tqdm import tqdm #progress bar from github
import requests
import re
from helpers import *
import os
from pathlib import Path
import time

#Constants
DEFAULT_DIRECTORY = "ufc_scraper/src"

#stores html into local directory
def save_html(html, path):
    try:
        with open(path, 'wb') as f:
            f.write(html)
    except Exception:
        print("\n\nAn Exception occured while trying to save %s" % path)

#opens a local html file and returns it as an object
def open_html(path):
    with open(path, 'rb') as f:
        return f.read()

def get_fighter_links():
    """creates a list of links to fighter pages from ufcstat.com

    return: list of fighter links
    """
    #Get Wiki webpage of UFC fighters and save into object "r"
    url = "http://www.ufcstats.com/statistics/fighters?char=a&page=all"

    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    #Start parsing the file
    #Target every link within each row
    parsed_a_tags = soup.find_all('a', href=True)

    #creates a list of all of the links on the page
    href_collection = [a['href'] for a in parsed_a_tags]

    #adds all links of fighter to a list
    links = []
    for item in href_collection:
        if "fighter-details" in item:
            links.append(item)

    #remove any duplicates
    links = list(dict.fromkeys(links))

    return links

def get_fighter_http():
    """
    Save the html page of each fighter in get_fighter_links

    return: list of each fighters http page
    """
    links = get_fighter_links()
    list_of_https = []

    x = 1 #tracks index of for loop below
    for link in links:
        print("Requesting: " + link)
        r = requests.get(link)
        list_of_https.append(r.content)
        print("Saving Fighter %d" % x)
        save_html(r.content, "Fighter %d" % x)
        x += 1

    return list_of_https

#Takes a http from page and creates a fighter object with stats filled
def get_fighter_stats(http_page):
    """
    populates a Fighter() class object with all attributes available on given
    http_page.

    args:
        http_page - a fighter http page with base domain
        "http://www.ufcstats.com/fighter-details/"

    returns: Fighter object
    """
    #Create fighter object
    fighter = Fighter()

    #Get name--------
    page = open_html(http_page)
    soup = BeautifulSoup(page, 'html.parser')

    #Targets html tag with name of fighter
    name_target = soup.find_all("span", class_="b-content__title-highlight")

    #isolates text within tag
    fighter_name = name_target[0].text
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
    sig_strike_defense_regex = re.compile('Str. Def:\s\d\d')
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
    takedown_defense_regex = re.compile('TD\sDef.:\s\d{1,3}')
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

    fighter.print()

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

def append_used_link(link):
    """appends a link to the txt file being used to track all links in directory
    args:
        link - url to the page being tracked
    """
    tracking_filename = 'tracker.txt'

    #if tracking file does not exisit create it
    if not os.path.exists(tracking_filename):
        with open(tracking_filename, 'w'): pass

    try:
        with open(tracking_filename, 'a') as f:
            f.write(link)
            f.write('\n')
    except Exception:
        print("Unable to save URL to %s" % tracking_filename)

def scrape_all_fights(links):
    wanted_working_dir = 'src/test'

    links = get_all_event_history_links()

    if not is_dir_correct(wanted_working_dir):
        exit("Incorrect starting directory. Exiting...")

    #for every event find all of the fights in that event and save the html of
    #that fight to the cwd
    for link in tqdm(links): #tqdm is open source progress bar on for loop
        try:
            get_fight_history_http(requests_url = link)
            append_used_link(link)
        except Exception:
            print("No links found in %s" % link)
            print("Moving to next link")
            pass

#Targets fight history detail links and saves each one to the directory fight_history
def get_fight_history_http(http_page = 'None', requests_url = 'None'):
    """
    requests and saves all https of fights a fighter has had. Takes either a url
    or a http page file path

    args: http_page - any fighters page from "fighter-details" site directory
        requests_url - a url to an event-details page

    raise: Both optional arguments are used
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

    #Removes duplicate links
    links = list(dict.fromkeys(links))
    x = 0
    for item in links:
        r = requests.get(item)
        save_name = item[-16:]
        save_html(r.content, "%s" % save_name)
        x += 1

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

#!!!!!Need to figure out how to use funcition. Return? call func()?
def organize_fight_data(fight_history_collection, http):
    """Seperate round data from "Totals" and "Significant strikes" data.

    args: fight_history_collection - list from parse_table_rows function
    http: fight stat http page in relation to collection
    """
    #Get the round the fight was finished in
    page = open_html(http)
    soup = BeautifulSoup(page, 'html.parser')

    #Find finishing round; convert to int
    round = soup.body.find("i", class_="b-fight-details__text-item")
    round = round.text
    round = " ".join(round.split())
    round = round[7:]
    round = int(round)

    totals = [fight_history_collection[0][0:round+1], fight_history_collection[1][0:round+1]]
    sig_strikes = [fight_history_collection[0][round+1:], fight_history_collection[1][round+1:]]

    fighters = len(sig_strikes)
    rows = len(sig_strikes[0])

    round = len(totals[0]) - 1
    # for fighters in range(fighters):
    #     print("===================Fighter %s===============" % totals[fighters][0][0])
    #     for rows in range(rows):
    #         print("Round: %d------------------"% rows)
    #         sig = assign_sig_data(sig_strikes[fighters][rows])
    #         sig.print()
    #
    #
    #
    #         print("---------------------------\n")

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
        DEFAULT_TUPLE = (-1,-1)
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

    fighters = len(totals)
    rows = len(totals[0])

    round_objects = []
    for fighters in range(fighters):
        for rows in range(rows):
            round_object = round_total_assign(totals[fighters][rows])
            round_objects.append(round_object)


    sig_objects = []
    fighters = len(sig_strikes)
    rows = len(sig_strikes[0])
    for fighters in range(fighters):
        for rows in range(rows):
            sig_object = assign_sig_data(sig_strikes[fighters][rows])
            sig_objects.append(round_object)

#test for organize_fight_data
fight = '2fd0c6d914b77205'
passed_list = parse_table_rows(fight)
organize_fight_data(passed_list, fight)



#Helpers
def is_dir_correct(dir):
    starting_dir = os.getcwd()
    regex = re.search(dir, str(starting_dir))

    if regex is None:
        return False

    return True

def update_fight_history():
    """Deletes all old fight history https in dir and re requests
    saves new updated ones from site
    """
    verify_dir = ["fight_history", "fighter_data_https"]
    #only update if in current file structure

    if not is_dir_correct(DEFAULT_DIRECTORY):
        exit("File structure incorrect. Exiting Program.")

    os.chdir('..')#Go back one Directory
    os.chdir('fight_history')

    files_in_dir = []
    for i in os.listdir():
        files_in_dir.append(i)

    print("Please confirm files to be deleted")
    for i in files_in_dir:
        print(i)

    Keyboard_input = input("Press 'Y' to delete\n")

    if str(Keyboard_input).capitalize() != 'Y':
        print("Exiting...")
        return

    os.mkdir('update')
    os.chdir('update')

def create_file_structure():
    """
    sees if program has correct structure if so returns true.
    If not creates correct dirs and returns false
    """
    verify_dir = ["fight_history", "fighter_data_https"]
    missing_dir = []
    dir_exist = False

    #check to see if fighter_data_https dir exist and fight_history dir exists


        #see if current working directory is correct. If not exit
    current_dir = os.getcwd()
    regex = re.search('src', current_dir)

    if regex is None:
        exit("Fatal error. Current working directory not correct.")

    #go back a dir and see if two dirs exists
    os.chdir("..")
    for i in verify_dir:
        if not os.path.isdir(i):
            print(i + " .....MISSING!")
            missing_dir.append(i)
        else:
            print(i + ".....exists")

    #Free memory
    if len(missing_dir) == 0:
        return True
    else:
        dir_exist = False

    #if they don't exist create dirs
    if not dir_exist:
        for i in verify_dir:
            print("Creating Directory: %s" % i)
            os.mkdir(i)


    return False

# for filename in os.listdir():
#     try:
#         stat_rows = parse_table_rows(filename)
#         organize_fight_data(stat_rows, filename)
#     except:
#         print("unable to parse %s. Moving to next file" % filename)






# scrape_all_fights(get_all_event_history_links())
