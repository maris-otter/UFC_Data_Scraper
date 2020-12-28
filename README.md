UFC_Data_Scraper
===============
UFC_Data_Scraper uses Beautiful Soup API to scrape fight and fighter data from ufcstats.com and returns data in a JSON format.


Install
--------
To install UFC_Data_Scraper:
```bash
pip install UFC_Data_Scraper
```


Usage
-----

### Step 1
Create instance of Ufc_Data_Scraper object:  
`scraper = s.Ufc_Data_Scraper()`
### Step 2
Choose class method for getting fighter or Fights data:

`list_of_fighters = scraper.get_all_fighters()`

or

`list_of_fights =  scraper.scrape_all_fights()`

### Step 3
Convert from list of fighter or fight objects into list of dictionaries:

`json_fighter_list = s.Ufc_Data_Scraper().fighter_to_Json(list_of_fighters)`

 or
 
`json_fights_list = s.Ufc_Data_Scraper().fights_to_Json(list_of_fights)`

### Step 4
Save dictionaries into Json:

`s.Ufc_Data_Scraper().save_json("<name of JSON file>", json_fighter_list)`

JSON Format
------------
The format of both fighter and fight data saved to .json files are described in JSON_spec folder 
