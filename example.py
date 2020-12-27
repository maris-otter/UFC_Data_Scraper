from UFC_Data_Scraper import scraper as s


#scrape fighter data and save result in json format
scraper = s.Ufc_Data_Scraper()

list_of_fighters = scraper.get_all_fighters()

json_fighter_list = s.Ufc_Data_Scraper().fighter_to_Json(list_of_fighters)

s.Ufc_Data_Scraper().save_json("fighters", json_fighter_list)

#scrape all ufc fights data and save result in json format

list_of_fights =  s.Ufc_Data_Scraper().scrape_all_fights(load_from_dir = False)

json_fights_list = s.Ufc_Data_Scraper().fights_to_Json(list_of_fights)

s.Ufc_Data_Scraper().save_json("all_fights", json_fights_list)
