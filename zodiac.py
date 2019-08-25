from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as zUrl
from pymongo import MongoClient


client = MongoClient("mongodb://127.0.0.1:27017/?authSource=admin")

database = client["STARS"]

zodiac_collection = database["mycol"]

url = 'https://www.horoscope.com/zodiac-signs'

page = zUrl(url)

z_read = page.read()
page.close()

z_parse = soup(z_read, 'html.parser')

containers = z_parse.findAll('div', {'class' : 'no-events' })

signs = [(i.find('h4').text) for i in containers]

dates = [(j.find('p').text) for j in containers]

signs_dict = dict(zip(dates, signs))

zodiac_collection.insert_one({"zodiac_info" : signs_dict })
