from bs4 import BeautifulSoup
import requests

class f_history:
    wins = 0
    loss = 0
    no_contest = 0

class Fighter:
    name = ""
    height = ()
    weight = 0
    reach = 0
    stance = 0 # 1 = orthodox 2 = southpaw
    history = f_history()


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
    #Get Wiki webpage of UFC fighters and save into object "r"
    url = "http://www.ufcstats.com/statistics/fighters?char=a&page=all"

    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    #Start parsing the file
    #Target every link within each row
    parsed_a_tags = soup.find_all('a', href=True)

    #creates a list of all of the links on the page
    href_collection = [a['href'] for a in parsed_a_tags]

    #reduces the links on the
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

    #Get name
    page = open_html(http_page)
    soup = BeautifulSoup(page, 'html.parser')

    #Targets html tag with name of fighter
    name_target = soup.find_all("span", class_="b-content__title-highlight")

    #isolates text within tag
    fighter_name = name_target[0].text

    # assigns name
    fighter.name = name_target

    #Get record
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
    fighter.history.no_contest = fight_record_clean[2]


    #Get rows of the fighters basic information
    stat_rows = soup.find_all("li", class_="b-list__box-list-item b-list__box-list-item_type_block")

    height_raw = stat_rows[0].text
    height_clean =' '.join(height_raw.split())
    #Removes "Height:" from string and leaves ?' ?"
    height_clean = height_clean[8:]


    #Remove characters from height
    height_clean = height_clean.replace('"', '')
    height_clean = height_clean.replace("'", '')

    #Assign height to fighter object
    fighter.height = height_clean.split()

    print(fighter.height[0])




    #get weight
    #Get reach
    # get stance ... 1 or 2 ... check class def




get_fighter_stats("fighter_data_https/Fighter 2")
