from tqdm import tqdm #progress bar from github
from helpers import *
import os


class Ufc_Data_Scraper:
    #Constants
    DEFAULT_DIRECTORY ="UFC_Data_Scraper/UFC_Data_Scraper"

    def __init__(self):
        #see if file structure is created
            #if so then continue
        if self.create_file_structure():
            pass
        else:
            print(color.RED + "\n\nUnable to create file structure \n\n" + color.END)
            raise Exception



    def get_all_fighters(self, load_from_dir = False, correct_dir = SAVE_FIGHTER_DIR, save_https = False):
        """
        returns a indexable list of every fighter on ufcstats. Each index is a
        fighter. Provides option to save each fighter http if not loading from
        a directory already


        args:
            load_from_dir - create the list of fighters from a directory that has
                https of fighters saved

            correct_dir - conditoinal: if load_from_dir false then correct_dir
                represents the directory fighter https will be saved to.
                otherwise current_dir represents which directory to load fighter
                https from
            save_https - optional arguement that if True will save each fighter
                http to a directory based on correct_dir

        return - list of fighter objects
        """

        #handling bad function calls by displaying error and exiting function
        if load_from_dir and (correct_dir != None or save_https != False):
            print("If loading from directory the option to save is not available. Please call again")
            return

        fighters = [] #list of fighter objects

        fighter_links = get_fighter_links()

        print("Parsing each fighter link.....")
        index = 1
        for fighter in tqdm(fighter_links):
            try:
                #load fighter details from requesting or from local storage
                if load_from_dir:
                    temp = get_fighter_stats("{}/{}".format(correct_dir, index))

                else:
                    if save_https:
                        temp = get_fighter_stats(http_url = fighter, save = True, dir = correct_dir)
                    else:
                        temp = get_fighter_stats(http_url = fighter)


                fighters.append(temp)

                index += 1
            except Exception:
                pass


        return fighters


    def scrape_all_fights(self, wanted_directory= SAVE_FIGHT_DIR, load_from_dir = True):
        """ uses all event links form get_all_event_history_links and saves all fight
        https to wanted_working_dir.
        """
        original_dir = os.getcwd()

        #Make sure current directory is wanted directory. Change otherwise
        if not is_dir_correct(wanted_directory):
            try:
                print(f"Changing directory to {wanted_directory}")
                os.chdir(wanted_directory)
            except Exception:
                exit("Incorrect starting directory. Exiting...")

        #if a directory to load https is not given
        if not load_from_dir:
            #for every event find all of the fights in that event and save the html of
            #that fight to the cwd
            links = get_all_event_history_links()
            for link in tqdm(links): #tqdm is open source progress bar on for loop
                try:
                    get_fight_history_http(requests_url = link)
                    append_used_link(link)
                except Exception:
                    print(f"No links found in {link}")
                    print("Moving to next link")
                    pass

        fights = []
        files = os.listdir()
        print("Creating list of fights...")
        files = list(dict.fromkeys(files))#Remove duplicates

        #for each saved http of a fight: parse the data and create a object
        for file in tqdm(files):
            try:
                parsed_http = parse_table_rows(file)
                temp_fight = assign_fight_data(parsed_http, file)
                fights.append(temp_fight)
            except Exception as e:
                print(e)
                print(f"\nError parsing file: ({file}) please check exception.\n")

        try:
            pickle_list(fights, 'fights.pickle')
            print("List has been pickled")
        except Exception as e:
            print(e)
            print("An exception occured while pickling....")

        os.chdir(original_dir)

        return fights


    # TODO: See if it is useful to call this with constructor
    def create_file_structure(self):
        """
        sees if program has correct structure if so returns true.
        If not creates correct dirs and returns false
        """
        print(color.BOLD + "Checking file structure. A specific structure must exist or be created to use this package at this time" + color.END)

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

        regex = re.search(
        wanted_directory, current_dir)

        if regex is None:
            exit(f"Fatal error. Current working directory ({current_dir}) is not correct.")

        for i in verify_dir:
            if not os.path.isdir(i):
                print(i + " .....MISSING!")
                missing_dir.append(i)
            else:
                print(i + ".....exists")



        if len(missing_dir) == 0:
            print(color.GREEN + "\n\nFile structure already created. ALl set!!!\n\n" + color.END)
            return True
        else:
            dir_exist = False

        keyboard_input = input("Creating missing directories. If you want to stop this press n") #diag

        #only create file structure if user approves
        if(keyboard_input.upper() == 'N'):
            print("\n\nNot creating and exiting....")
            return

        #if they don't exist create dirs
        if not dir_exist:
            for i in verify_dir:
                print("Creating Directory: %s" % i)
                os.mkdir(i)
            print(color.GREEN + "\n\nAll set!!!\n\n" + color.END)
            return True
        return False
