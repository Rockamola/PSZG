from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as zUrl
import json
from pprint import pprint as pp



url = 'https://www.horoscope.com/zodiac-signs'

page = zUrl(url)

z_read = page.read()
page.close()

z_parse = soup(z_read, 'html.parser')

containers = z_parse.findAll('div', {'class' : 'no-events' })

signs = [(i.find('h4').text) for i in containers]

dates = [(j.find('p').text) for j in containers]

dick = dict(zip(dates, signs))

with open('zodiac.json', mode = 'w') as new_file:
	(json.dump(dick, new_file))


#something like {'Aries'['Mar.21' : 'Apr.20']} you get the idea