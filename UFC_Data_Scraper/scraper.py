from tqdm import tqdm #progress bar from github
from helpers import *
import os


class Ufc_Data_Scraper:
    #Constants
    DEFAULT_DIRECTORY = "ufc_scraper/UFC_Data_Scraper"

    def __init__(self):
        #see if file structure is created
            #if so then continue
        if self.create_file_structure():
            pass
        else:
            print(color.RED + "\n\nUnable to create file structure \n\n" + color.END)
            raise Exception

            #if not then create the correct file structure and file trackers


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


        return fighters


    def scrape_all_fights(self, wanted_directory='src/test'):
        """ uses all event links form get_all_event_history_links and saves all fight
        https to wanted_working_dir.
        """


        links = get_all_event_history_links()

        if not is_dir_correct(wanted_directory):
            try:
                print("Changing directory to {}".format(wanted_directory))
                os.chdir(wanted_directory)
            except Exception:
                exit("Incorrect starting directory. Exiting...")

        input()
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

    def update_fight_history(self):
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
        wanted_directory = "ufc_scraper/ufc_data_scraper"
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









# dir = "test/fighters"
# get_fighter_http(dir, save_to_dir = True)
# fights = get_all_fighters(load_from_dir = True, correct_dir= dir)


# #test
# #test for organize_fight_data
# fight = 'test/fights/2fd0c6d914b77205'
# passed_list = parse_table_rows(fight)
# assign_fight_data(passed_list, fight)
