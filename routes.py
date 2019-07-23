
# Make a CRON Job to dump into a database 
# look at using docker-compose 
# Thenm make into a rest api 
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime

# create base url for all requests to use
base_url = "http://pornhub.com"
# query params for trending page
query_params = "/pornstars/?o=t"

# scrape trending page
resp = requests.get(base_url + query_params)
resp.raise_for_status()

# create soup for the trending page
trending_page = soup(resp.text, "lxml")

# extract pornstar hrefs
# dedupe
pornstar_divs = trending_page.select("a[href*='/pornstar/']")
pornstar_birthday_dict = dict()

# iterate over pornstar divs 
for star in pornstar_divs:
	# get individual page hrefs
	href = star.attrs['href']
	print(href)
	# scrape individual page
	resp = requests.get(base_url + href)
	print(resp)
	resp.raise_for_status()
	
	# build individual pornstar soup
	individual_pornstar_page = soup(resp.text, "lxml")

	# extract name
	name = [item.text.strip() for item in individual_pornstar_page.select('div.name')][0]
	print(name)

	# Try to extract the birthday from the soup span
	try:
		bday_span = individual_pornstar_page.find('span', itemprop = 'birthDate')
		bday = bday_span.text
		print(bday)
	except AttributeError:
		print("No birthday, skipping")
		continue
		# In case there is no birtday (a soup span object) we break
	except Exception as e:
		print("fuck")
		print(e)

	# make new dict entry
	name_bday = { name: bday }

	# Must not be a dupe
	if name not in pornstar_birthday_dict:
		print("fresh insert")
		# insert dict_entry
		pornstar_birthday_dict.update(name_bday)
	else:
		print("dupe skipping")

#write to json
from pprint import pprint as pp
pp(pornstar_birthday_dict)
print(len(pornstar_birthday_dict))

import json
porn_json = json.dumps(pornstar_birthday_dict)
print(porn_json)

# Python datetime library to normalize
def normalize_datetime(bday_str, porn_json): 
	converter = datetime()

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
