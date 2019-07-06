from app import app
from app.forms import LoginForm
import os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as zUrl
from flask import render_template, request, url_for, redirect
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

def json_output():
	#url path
	url = 'https://www.horoscope.com/zodiac-signs'
	#open url
	page = zUrl(url)
	#read url
	z_read = page.read()
	page.close()
	#read into beautifulsoup
	z_parse = soup(z_read, 'html.parser')
	#parse html tags
	containers = z_parse.findAll('div', {'class' : 'no-events' })
	#iterate html tags
	signs = [(i.find('h4').text) for i in containers]
	#iterate second html tags
	dates = [(j.find('p').text) for j in containers]
	#coverting into dictionary
	dick = dict(zip(signs, dates))
	#saving data into json form
	data = json.dumps(dick)

def porn_bday():
	#url path
	url = 'https://www.pornhub.com/pornstars?o=t'
	#geckodriver path
	chromedriver = '/usr/bin/chromedriver'
	#calling firefox options
	options = webdriver.ChromeOptions()
	#adding option to run headless
	options.add_argument('headless')
	#calling webdriver to work with webpage
	driver = webdriver.Chrome(executable_path = chromedriver,
		chrome_options = options)
	driver.get(url)
	#finding element to access profile
	star_button = driver.find_element_by_css_selector("a[href*='/pornstar/']")
	#click javascript link
	click = driver.execute_script('arguments[0].click();', star_button)
	#waiting for page to fully load
	wait = WebDriverWait(driver, 10)
	try:
		wait.until(EC.url_contains('-'))
	except TimeOutException:
		print("Unable to load")
	#getting redirected url of stars profile
	new_url = driver.current_url
	#opening url
	page = zUrl(new_url)
	#reading into beautifulsoup
	try:
		p_read = page.read()
		page.close()
	except AssertionError as e:
		print(e)
		print('Shit no read')
	#parsing with beautifulsoup
	p_parse = soup(p_read, 'lxml')
	#iterating over profiles, grabbing name
	names = [item.text.strip() for item in p_parse.select('div.name')]

	def stars_bday():
		#parse stars birthday
		try:
			b_day = p_parse.find('span', itemprop='birthDate')
		except AssertionError as e:
			print(e)
			print('Shit did not read')
		#zip together both parsings
		full_list = dict(zip(names, b_day))
		#write to json
		bday_data = json.dumps(full_list)


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
