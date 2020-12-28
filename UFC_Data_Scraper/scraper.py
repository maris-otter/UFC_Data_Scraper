#third party imports
from tqdm import tqdm #progress bar from github

#std imports
import os
import threading
import json
import re
import time

#local imports
from . import helpers

class Ufc_Data_Scraper:
    #Constants
    DEFAULT_DIRECTORY ="UFC_Data_Scraper"
    SAVE_FIGHT_DIR = "fight_history"
    SAVE_FIGHTER_DIR = "fighter_data_https"

    def __init__(self):
        #see if file structure is created
            #if so then continue
        if self.create_file_structure():
            pass
        else:
            print(helpers.color.RED + "\n\nUnable to create file structure \n\n" + helpers.color.END)
            exit()


    def get_all_fighters(self, load_from_dir = False, correct_dir = SAVE_FIGHTER_DIR, save_https = False):
        """
        returns a indexable list of every fighter on ufcstats. Each index is a
        fighter. Provides option to save each fighter http if not loading from
        a directory already

        kwargs:
            load_from_dir - create the list of fighters from a directory that has
                https of fighters saved

            correct_dir - conditional: if load_from_dir false then correct_dir
                represents the directory fighter https will be saved to.
                otherwise current_dir represents which directory to load fighter
                https from
            save_https - optional arguement that if True will save each fighter
                http to a directory based on correct_dir

        return - list of fighter objects
        """

        #handling bad function calls by displaying error and exiting function
        if load_from_dir and save_https != False:
            print("If loading from directory the option to save is not available. Please call again")
            return

        fighters = [] #list of fighter objects

        #Either load from directory and parse data or request each link and parse
        if load_from_dir:
            starting_dir = os.getcwd()#track starting dir to return after call

            os.chdir(correct_dir)
            files = os.listdir()

            print("Parsing fighter https....")
            for file in tqdm(files):
                try:
                    temp = helpers.get_fighter_stats(http_page = file)
                    fighters.append(temp)
                except Exception as e: #print and log exception then continue
                    print(f"An exception occured for file {file}")
                    append_used_link(f"Exception: {e} file: {file}", link_error = True)

            os.chdir(starting_dir)#return to original directory

        else:
            fighter_links = helpers.get_fighter_links()

            print("Parsing each fighter link.....")
            for fighter in tqdm(fighter_links):
                try:
                    if save_https:
                        temp = helpers.get_fighter_stats(http_url = fighter, save = True, dir = correct_dir)
                        fighters.append(temp)
                    else:
                        temp = helpers.get_fighter_stats(http_url = fighter)
                        fighters.append(temp)

                except Exception:
                    pass


        os.chdir(starting_dir)

        if(len(fighters) == 0):
            raise ValueError('Empty fighters list')

        return fighters


    def scrape_all_fights(self, wanted_directory= SAVE_FIGHT_DIR, load_from_dir = True):
        """
        scrapes fight history by either requesting the site locally or parsing data
        from previously scrapped htmls in wanted_directory. Flow of function determined
        by optional load_from_dir.

        kwargs:
            wanted_directory - directory the program should be operating in.
                        IMPORTANT: due to the function deleting files in dir
                                you must be careful selecting wanted_directory
            load_from_dir - if html of fights are already available you can provide
                            a directory and function will parse each file
        """
        original_dir = os.getcwd()

        #Make sure current directory is wanted directory. Change otherwise
        if not helpers.is_dir_correct(wanted_directory):
            try:
                print(f"Changing directory to {wanted_directory}")
                os.chdir(wanted_directory)
            except Exception:
                exit("Incorrect starting directory. Exiting...")

        #make sure directory is clean before getting fight https
        if not load_from_dir:
            if len(os.listdir()) > 0:
                print(f"Directory not clean: {os.getcwd()}")

                directory_files = os.listdir()
                #if the directory is relativly small force manual deletion for safety
                if len(directory_files) < 50:
                    print(helpers.color.RED + "This directory is small. For safety delete manually and call again" + helpers.color.END)
                    os.chdir(original_dir)
                    exit()
                else:
                    input( helpers.color.RED + f"\n\nCleaning Directory. All files in {os.getcwd()} will be deleted press enter to continue or ctr+c to cancel" + helpers.color.END)

                    for file in directory_files:
                        os.remove(file)

                    print("Directory has been cleaned.")

        elif len(os.listdir()) == 0:
            print("Directory is empty. Unable to load from directory")
            return

        #if a directory to load https is not given
        if not load_from_dir:

            #function for thread callling and exception tracking
            def thread_func():

                try:
                    helpers.get_fight_history_http(requests_url= link, save = True)
                except Exception as e:
                    helpers.append_used_link(link, link_error = True)
                    print(f"An Exception occured for {link}")
                    print(f"Exception {e}")
                    print("Moving to next link\n\n")
                    pass

            #for each link create new thread and call get_fight_history_http
            threads = []
            links = helpers.get_all_event_history_links()
            # target = "helpers.get_fight_history_http" #target for threading
            for link in tqdm(links): #tqdm is open source progress bar on for loop
                try:
                    t = threading.Thread(target=thread_func)
                    time.sleep(1)
                    t.start()
                    threads.append(t)
                except Exception as e:
                #Track error in file. Print to console. move to next link
                    helpers.append_used_link(link, link_error = True)
                    print(f"An exception occured creating thread {t}")

            for thread in threads:
                thread.join()

        fights = []
        files = os.listdir()
        print("Creating list of fights...")
        files = list(dict.fromkeys(files))#Remove duplicates

        #for each saved http of a fight: parse the data and create a object
        for file in tqdm(files):
            try:
                parsed_http = helpers.parse_table_rows(file)
                temp_fight = helpers.assign_fight_data(parsed_http, file)
                fights.append(temp_fight)
            except Exception as e:
                helpers.parsing_error_tracker(e, file)


        os.chdir(original_dir)


        if(len(fights) == 0):
            raise ValueError('Empty fights lists')

        return fights


    def create_file_structure(self):
        """
        checks if program has correct directory structure for class. if the structure exists function confirms with a message.
        If structure does not exisit the function propmts user and creates correct dirs and returns false
        """
        print(helpers.color.BOLD + "Checking existing file structure." + helpers.color.END)

        verify_dir = ["fight_history", "fighter_data_https"]
        missing_dir = []
        dir_exist = False
        wanted_directory = self.DEFAULT_DIRECTORY
        #check to see if fighter_data_https dir exist and fight_history dir exists


            #see if current working directory is correct. If not exit
        try:
            current_dir = os.getcwd()
        except Exception:
            print("Unable to get current working directory. Exiting Program")
            exit()

        regex = re.search(wanted_directory, current_dir)

        # if regex is None:
        #     exit(f"Fatal error. Current working directory ({current_dir}) is not correct.")

        for i in verify_dir:
            if not os.path.isdir(i):
                print(i + " .....MISSING!")
                missing_dir.append(i)
            else:
                print(i + ".....exists")



        if len(missing_dir) == 0:
            print(helpers.color.GREEN + "\n\nFile structure already created. All set!!!\n\n" + helpers.color.END)
            return True
        else:
            dir_exist = False

        keyboard_input = input("Creating missing directories. If you want to stop this press n\n") #diag

        #only create file structure if user approves
        if(keyboard_input.upper() == 'N'):
            print("\n\nMust create directories to use package. \n\nexiting....")
            return

        #if they don't exist create dirs
        if not dir_exist:
            for i in verify_dir:
                print("Creating Directory: %s" % i)
                os.mkdir(i)
            print(helpers.color.GREEN + "\n\nAll set!!!\n\n" + helpers.color.END)
            return True
        return False


    @staticmethod
    def fights_to_Json(collection_fights):
        """
        iterates through a collection of fight_details objects and categorizes
        them by event into a dictionary.
        """
        fight_json = {}

        #for all the fights that match the same event add them to a single dict for that event
        #do this for all of the fights
        tracker_dict = {}

        x = 0
        for i in collection_fights:

            if i.event in fight_json:
                #get last numbered fight from tracker_dict
                index = tracker_dict[i.event]

                fight_json[i.event].update({index+1: i.as_json()})
                tracker_dict[i.event] += 1
            else:
                fight_json[i.event] = {1: i.as_json()}
                tracker_dict[i.event] = 1


        return fight_json

    @staticmethod
    def fighter_to_Json(collection_fighters):
        """
        Take a collection of Fighter objects and converts into a dictionary
        args: list of Fighter objects
        return: dictionary of fighter objects
        """
        fighter_dict = {}

        #for every fighter create a new dict entry with name of fighter as key
        # and fighter json as value
        for fighter in collection_fighters:
            fighter_dict[fighter.name] = fighter.as_json()

        return fighter_dict


    @staticmethod
    def save_json(filename, fights_dict):
        """
        saves dict produced by fighter_to_Json or fights_to_Json to a json file

        args:
            filename - name of designated file ie <filename>.json

        """
        with open(f"{filename}.json", "w") as outfile:
             json.dump(fights_dict, outfile)
