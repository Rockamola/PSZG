
# Make a CRON Job to dump into a database 
# look at using docker-compose 
# Thenm make into a rest api 
import requests
from bs4 import BeautifulSoup as soup
import json
from pprint import pprint as pp
from datetime import datetime
import pdb
import threading
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.basicConfig(filename = "logs.txt", level = logging.INFO, filemode = "w")

#add logger, change levels 


LOCK = threading.Lock()

#use selenium headless

#birthday converter

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
		return
		# In case there is no birtday (a soup span object) we break
	except Exception as e:
		print("fuck")
		print(e)
		return

	# make new dict entry
	name_bday = { name: bday }

	# Must not be a dupe
	if name not in pornstar_birthday_dict:
		print(f"fresh insert for {name}")
		# insert dict_entry
		with LOCK:
			pornstar_birthday_dict.update(name_bday)
	else:
			print(f"dupe for {name}")



if __name__ == '__main__':
	# log.info('Beginning scraper')
	# create base url for all requests to use
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
	# dedupe
	pornstar_divs = trending_page.select("a[href*='/pornstar/']")
	pornstar_birthday_dict = dict()
	import time
	start_time = time.time()

	# iterate over pornstar divs
	#with ThreadPoolExecutor() as executor:
	for star in pornstar_divs:
		getpornstar(star)
	#write to json
	print(time.time() - start_time)
	pp(pornstar_birthday_dict)
	print(len(pornstar_birthday_dict))


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
