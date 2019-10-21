import requests
from bs4 import BeautifulSoup as soup
import json
from datetime import datetime
import pdb
import logging
import threading
from pymongo import MongoClient
from bson import json_util
import pandas as pd


#thread locking for dictionaries
LOCK = threading.Lock()

#logging configuration
logger = logging.getLogger("basic")
logger.setLevel(logging.INFO)
#logging format
log_format = "%(asctime)s %(filename)s: %(message)s"
#config for log output
logging.basicConfig(filename = "log.txt", format = log_format,
    datefmt = "%Y-%m-%d %H:%M:%S")
logger.info("information message")
logger.error("information message")

#connect with port and host for mongodb
try:
    client = MongoClient("mongodb://127.0.0.1:27017/?authSource=admin")
    print("Successfully connected to MongoDB")
except pymongo.error.ConnectionFailure:
    logger.error("Connection Failed")
#access database
bday_database = client["STARS"]
#access collection in database
bday_collection = bday_database["mycol"]


#function for converting birthdays if not in desired format
def get_bday_datetime(bday):
    '''
    Conversion for improper birthday format scraped for stars.
    Converts 2001-01-01 format to Jan 01, 2001 format, in order to return proper zodiac sign.
    '''
    try:
        item = datetime.strptime(bday, "%Y-%m-%d")
    except Exception:
        print(f"First datetime conversion failed for {bday}, trying second format")
        try:
            item = datetime.strptime(bday, "%b %d, %Y") # other datetime fmt
        except Exception:
            print(f"Second datetime conversion failed for {bday}, returning None")
            # str replace -0001 with 9999
            return None
    #desired format 
    new_bday = datetime.strftime(item, "%Y-%m-%d") # may throw an error if its already right, not sure
    return new_bday

def getpornstar(star):
    # get individual page hrefs
    href = star.attrs['href']
    # scrape individual page
    try:
        resp = requests.get(base_url + href)
        resp.raise_for_status()
    except requests.exceptions.ChunkedEncodingError:
        logger.error(f"Connection broken for {resp} reading at {datetime.now()}" )
    # build individual pornstar soup
    individual_pornstar_page = soup(resp.text, "lxml")
    # extract name
    name = [item.text.strip() for item in individual_pornstar_page.select('div.name')][0]
    # Try to extract the birthday from the soup span
    try:
        bday_span = individual_pornstar_page.find('span', itemprop = 'birthDate')
        bday_str = bday_span.text
        print(f"Trying to convert {name} {bday_str}")
        bday = get_bday_datetime(bday_str)
        if not bday:
            return
    except AttributeError:
        print(f"No birthday for {name}, skipping")
        logger.info(f"No birthday for {name}")
        return
        #wondering if all theses returns is causing the duplicate iteration?
        # In case there is no birtday (a soup span object) we breakda
    except Exception as e:
        print("fuck")
        print(e)
        logger.info(f"{name} was not entered into the database")
        return
    # make new dict entry
    name_bday = {name : bday}
    # Must not be a dupe
    if name not in pornstar_birthday_dict:
        print(f"fresh insert for {name}")
        logging.info(f"{name} has been added")
        with LOCK:
            pornstar_birthday_dict.update(name_bday)

   
if __name__ == "__main__":
    #log start of scrapping
    #logger.info(f"Scraping started at {datetime.now()}")
    # create base url for all requests star-related
    base_url = "http://pornhub.com"
    # query params for trending star page
    query_params = "/pornstars/?o=t"
    # scrape trending page
    try:
        resp = requests.get(base_url + query_params)
        resp.raise_for_status()
    except requests.exceptions.ChunkedEncodingError:
        logger.error(f"Connection broken for {resp} reading at {datetime.now()}")
    # log.debug("Base url response resp.text")
    # create soup for the trending page
    trending_page = soup(resp.text, "lxml")
    # extract pornstar hrefs
    pornstar_divs = trending_page.select("a[href*='/pornstar/']")
    #dictionary containing stars names/birthdays
    pornstar_birthday_dict = dict()
    #dataframe
    p_stars_data = pd.DataFrame
    #start_time = time.time()
    #call getpornstar func, iterate to store to dictionary
    for star in pornstar_divs:
        getpornstar(star)
        pornstar_birthday_dict.update()
    #create dataframe variable, same as with dictionary, apply same logic as with dictionary, but with date conversion as it insert?
    #look into if date format can be used in for loop with pandas dataframe

    #format before sticking into dataframe, move bday_convert here?

    star_data = pd.DataFrame(list(pornstar_birthday_dict.items()),
            columns = ["stars", "birthdays"])
    star_data["birthdays"] = star_data["birthdays"].astype("datetime64")

    dates_range_aqua = pd.DataFrame(data = {"zodiac_dates" : pd.date_range(start = "1980-01-20", end = "2000-12-31")})
    pdb.set_trace()
    
    frames = [star_data, dates_range_aqua]

    result = pd.concat(frames, sort = False)


    
    for i in star_data:
        bday_stf = star_data.sort_index()
        zod_stf = dates_range_aqua.sort_index()
        if bday_stf == dates_range_aqua:
            print({star_data.keys : "aquaris"})


    '''
        for column in dates_range_aqua[pd.date_range]:
            bday_obj = star_data[birthdays]
            print(bday_obj.values)'''
    '''

   
        if star_data == dates_range_aqua:
            print({star_data.keys() :"aquaris"})'''


        #would need a nested for loop for dates range
        
    #star_data["birthdays"] = star_data["birthdays"].dt.strftime("%Y%m%d").astype(int)
    #star_data.to_csv("bday_info.csv",index = False, header = True)

    #TO-DO: create module with functions containing all zodiac dates. import, use that to iterate over,
    #then can avoid all this hard-coding nonsense, maybe[[[[]]]]

    #to_datetime(star_data["birthdays"], format = "%Y-%m-%d"

    #str.replace("-", "").astype(int) .astype("datetime64")

    #TO-DO, try convert birthday to %m-%d, then pass just that in, start/end will be Jan 20, Feb 20