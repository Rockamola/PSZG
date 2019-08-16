
import requests
from bs4 import BeautifulSoup as soup
import json
from pprint import pprint as pp
from datetime import datetime
import pdb
import logging
import threading
from pymongo import MongoClient



#need try/except for if incompleteread pops
#logging configuration
logger = logging.getLogger("basic")
logger.setLevel(logging.INFO)
#format
log_format = "%(asctime)s %(filename)s: %(message)s"
#config for log output
logging.basicConfig(filename = "log.txt", format = log_format,
    datefmt = "%Y-%m-%d %H:%M:%S")
logger.info("information message")
logger.error("information message")
#connect with port and host
try:
    client = MongoClient("mongodb://127.0.0.1:27017/?authSource=admin")
    print("Successfully connected to MongoDB")
except pymongo.error.ConnectionFailure:
    logger.error("Connection Failed")
#access database and authenticate
bday_database = client["starbdaydatabase"]
#access table
bday_collection = bday_database["mycol"]



#locking dict
LOCK = threading.Lock()

#function for converting birthdays if not in desired format
def get_bday_datetime(bday):
    try:
        item = datetime.strptime(bday, "%b %d, %Y")
    except Exception:
        print(f"First datetime conversion failed for {bday}, trying second format")
        try:
            item = datetime.strptime(bday, "%Y-%m-%d") # other datetime fmt
        except Exception:
            print(f"Second datetime conversion failed for {bday}, returning None")
            # str replace -0001 with 9999
            return None

    new_bday = datetime.strftime(item, "%b %d, %Y") # may throw an error if its already right, not sure
    return new_bday

def getpornstar(star):
    # get individual page hrefs
    href = star.attrs['href']
    # scrape individual page
    resp = requests.get(base_url + href)
    resp.raise_for_status()
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
        # In case there is no birtday (a soup span object) we break
    except Exception as e:
        print("fuck")
        print(e)
        logger.info(f"{name} was not entered into the database")
        return
    # make new dict entry
    name_bday = { name: bday }
    # Must not be a dupe
    if name not in pornstar_birthday_dict:
        print(f"fresh insert for {name}")
        logging.info(f"{name} has been added")
        with LOCK:
            pornstar_birthday_dict.update(name_bday)

if __name__ == '__main__':
    logger.info(f"Scraping started at {datetime.now()}")
    # create base url for all requests
    base_url = "http://pornhub.com"
    # query params for trending page
    query_params = "/pornstars/?o=t"
    # scrape trending page
    resp = requests.get(base_url + query_params)
    resp.raise_for_status()
    # log.debug("Base url response resp.text")
    # create soup for the trending page
    trending_page = soup(resp.text, "lxml")
    # extract pornstar hrefs
    pornstar_divs = trending_page.select("a[href*='/pornstar/']")
    pornstar_birthday_dict = dict()
    #start_time = time.time()
    # iterate over pornstar divs
    for star in pornstar_divs:
        getpornstar(star)
        #if star in bday_collection:
            #need to scan database, and avoid insert if already in
        #else:
        pornstar_birthday_dict.update()
    #insert into database

        bday_collection.insert_one(pornstar_birthday_dict)
        logger.info("Database entry successful")

    #print(time.time() - start_time)
    #pp(pornstar_birthday_dict)
    #print(len(pornstar_birthday_dict))
    #porn_json = json.dumps(pornstar_birthday_dict)
    #print(porn_json)
  

    #assign id for inserting into db?
#TO-DO/ remove dictionary, replace with varibales containing item names for tables,
#insert with iteration indivudually into db


@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def submittance():
	form = LoginForm()
	#if form.validate_on_submit(submit_1):
		#flash("Congrats. You're entering the site")
	#return redirect(url_for('pszg'))
	#if form.validate_on_submit(submit_2):

	return render_template('login.html', form = form)
	


@app.route('/pszg')
def pszg():
	info = "Wanna see how it works"
	return render_template('pszg.html', info = info)	

if __name__ == '__main__':
	app.run(Debug = True)
