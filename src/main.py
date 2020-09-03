from bs4 import BeautifulSoup
import requests
import re



#stores html into local directory
def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)

#opens a local html file and returns it as an object
def open_html(path):
    with open(path, 'rb') as f:
        return f.read()


#returns each fighters webpage link in a list to be parsed
def get_fighter_links():
    """puts all fighter links into a list from ufcstat.com
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


#request the http of each fighter and returns list of links
def get_fighter_http():
    links = get_fighter_links()
    list_of_links = []

    x = 1 #tracks index of for loop below
    for link in links:
        print("Requesting: " + link)
        r = requests.get(link)
        list_of_links.append(r.content)
        save_html(r.content, "fighter_data_https/Fighter %d" % x)
        x += 1

    return list_of_links

#Takes a http from page and creates a fighter object with stats filled
def get_fighter_stats(http_page):
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
    weight_regex = re.compile('\d\d\d') #Create regex object for search
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
    stance = stance[7:]

    if stance == "Orthodox":
        fighter.stance = 1  #orthodox
    elif stance == "Southpaw":
        fighter.stance = 2 # southpaw
    elif stance == "Switch":
        fighter.stance = 3
    else:
        fighter.stance = 0 #Error parsing if executed

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

    takedown_acc_regex = re.compile('TD\sAcc.:\s\d\d')
    takedown_acc = takedown_acc_regex.search(carrer_stat_text[1])

    try:
        takedown_acc = takedown_acc.group()
    except AttributeError:
        takedown_acc = -1

    if takedown_acc != -1:
        takedown_acc = takedown_acc[9:]

    fighter.career_stat.takedown_acc = takedown_acc

    #Get takedown_defense
    takedown_defense_regex = re.compile('TD\sDef.:\s\d\d')
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


#Targets fight history detail links and saves each one to the directory fight_history
def get_fight_history_http(http_page):
    page = open_html(http_page)

    soup = BeautifulSoup(page, 'html.parser')

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

    #Removes duplicate links
    links = list(dict.fromkeys(links))
    x = 0
    for item in links:
        r = requests.get(item)
        save_html(r.content, "fight_history/Fight %d" % (x))
        x+=1




def parse_table_rows(http):
    """
    parses all fight data from html file into a list that splits both individual
    fight data and specific row data
    args:
        http - fight-details http from ufcstats.com

    returns: 2d list; 1st index is 0 or 1 representing one of the two fighters
    in the fight. 2nd index represent a row of data from page.

    """
    page = open_html(http)

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

    stat_rows = [split_html_data_list(fighter_1,fighter_1[0]),
                split_html_data_list(fighter_2,fighter_2[0])]

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

    #totals fighter one
    #   : [0][0]
    #   : [1][0]

    #sig strikes totals
    #   : [0][num_of_rounds + 1]
    #   : [1][num_of_rounds + 1]
    #
    # # print("Totals for fighter one are:")
    # print(fight_history_collection[0][0])
    # print("Totals for fighter two are:")
    # print(fight_history_collection[1][0])
    # print("---------------------------\n\n")
    #
    # print("Sig totals for fighter one are: ")
    # print(fight_history_collection[0][round+1])
    # print("Sig totals for fighter two are:")
    # print(fight_history_collection[1][round+1])
    # print("---------------------------\n\n")

    totals = [fight_history_collection[0][0:round+1], fight_history_collection[1][0:round+1]]
    sig_strikes = [fight_history_collection[0][round+1:], fight_history_collection[1][round+1:]]

    assign_fight_data(totals, sig_strikes)

def assign_fight_data(totals_collection, sig_strike_collection):
    """turns collection data into proper format and assigns to fight_details
    object.

    args:
        totals_collection: collection produced from organize_fight_data from
            parse_table_rows = [fighter][row][column]
        sig_strike_collection: collection produced from organize_fight_data
                                = [fighter][row][column]
    """

    fight = fight_details()
    #assign totals-------------------

    #Assign names to fight_details
    fight.fighter_1 = totals_collection[0][0]
    print(fight.fighter_1)
    #clean and Assign knock downs

    #clean and assign sig sig_strikes

    # clean and assign sig strike percentage

    #clean and assign  total strikes

    #clean and assign TD

    #C & A TD %

    #C & A SUB att

    #C & A pass

    #C & A REV

    #C & A other

    # print(totals_collection[0][0][2])
    ratio_regex = re.compile('\d{1,3}')
    ratio = ratio_regex.findall(totals_collection[0][0][2])


fight_history_path = "/Users/nathankrieger/Desktop/Projects/ufc_scraper/fight_history"

organize_fight_data(parse_table_rows("%s/Fight 7" % fight_history_path),
                                    "%s/Fight 7" % fight_history_path)
