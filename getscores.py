#!/usr/bin/python
# coding: latin-1

from selenium import webdriver
from collections import defaultdict
from private import redirectURL, poolURL, userid, password
import csv
import re
from collections import Counter
# import pandas
# import vincent
import redis
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer

DEBUG = True

if DEBUG == False:
    url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
    r = redis.StrictRedis(host=url.hostname, port=url.port, password=url.password)
else:
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

#open Firefox and go to login url
browser = webdriver.Firefox()

#right now I am just manually changing the week to get the latest week's scores. 
# it would be possible to use goToNextWeek() to automate this to pull everything
# down in one session
week = 9

# login and then call function to gather data
def loginCBS():
	browser.get(poolURL+str(week))
	# browser.get(redirectURL)
	browser.find_element_by_id("userid").clear()
	browser.find_element_by_id("userid").send_keys(userid)
	browser.find_element_by_id("password").clear()
	browser.find_element_by_id("password").send_keys(password)
	browser.find_element_by_id("submitButton").click()
	# get_points()
	get_all_picks()
	# get_player_picks()

# strips out high score and no pick indicators from score
def only_num(x):
	return re.sub(r"\D","",x)

# used to get just the team name from the results
def only_alpha(x):
	return re.sub(r"\W|\d","",x)

def get_player_picks():
	html = browser.page_source
	# we only care about the picks table
	picksTable = SoupStrainer(id="nflplayerRows")
	soup = bs(html,parse_only=picksTable)
	for player in soup.find_all(class_="left"):
		correct = []
		incorrect =[]
		for cpick in player.find_next_siblings(class_="correct"):
			correct.append(only_alpha(cpick.get_text()))
		for ipick in player.find_next_siblings(class_="incorrect"):
			incorrect.append(only_alpha(ipick.get_text())) 
		for c in correct:
			r.rpush(player.get_text()+"CO", c)
		for i in incorrect:
			r.rpush(player.get_text()+"IN", i)
	browser.close()
	print "Got Week",week

def get_all_picks():
	html = browser.page_source
	# we only care about the picks table
	picksTable = SoupStrainer(id="nflplayerRows")
	soup = bs(html,parse_only=picksTable)
	correct = [only_alpha(x.get_text()) for x in soup.find_all(class_="correct")]
	for c in correct:
		r.zincrby('correct',c,1)
	incorrect = [only_alpha(x.get_text()) for x in soup.find_all(class_="incorrect")]
	for i in incorrect:
		r.zincrby('incorrect',i,1)
	browser.close()
	print "Got Week",week

#gather player name and score by week
def get_points():
	pN = browser.find_elements_by_xpath('//*[@id="layoutRailRight"]/div[1]/table[2]/tbody/*/td[2]')
	wk1obj = browser.find_elements_by_xpath('//*[@id="layoutRailRight"]/div[1]/table[2]/tbody/*/td[3]')
	wk2obj = browser.find_elements_by_xpath('//*[@id="layoutRailRight"]/div[1]/table[2]/tbody/*/td[4]')
	wk3obj = browser.find_elements_by_xpath('//*[@id="layoutRailRight"]/div[1]/table[2]/tbody/*/td[5]')
	wk4obj = browser.find_elements_by_xpath('//*[@id="layoutRailRight"]/div[1]/table[2]/tbody/*/td[6]')
	wk5obj = browser.find_elements_by_xpath('//*[@id="layoutRailRight"]/div[1]/table[2]/tbody/*/td[7]')
	wk6obj = browser.find_elements_by_xpath('//*[@id="layoutRailRight"]/div[1]/table[2]/tbody/*/td[8]')
	wk7obj = browser.find_elements_by_xpath('//*[@id="layoutRailRight"]/div[1]/table[2]/tbody/*/td[9]')
	wk8obj = browser.find_elements_by_xpath('//*[@id="layoutRailRight"]/div[1]/table[2]/tbody/*/td[10]')
	wk9obj = browser.find_elements_by_xpath('//*[@id="layoutRailRight"]/div[1]/table[2]/tbody/*/td[11]')
	
	print "Got all the data now piecing it together"
	
	# convert elements to text and strip out unneeded characters
	playerName = [x.text for x in pN]
	wk1 = [only_num(x.text) for x in wk1obj]
	wk2 = [only_num(x.text) for x in wk2obj]
	wk3 = [only_num(x.text) for x in wk3obj]
	wk4 = [only_num(x.text) for x in wk4obj]
	wk5 = [only_num(x.text) for x in wk5obj]
	wk6 = [only_num(x.text) for x in wk6obj]
	wk7 = [only_num(x.text) for x in wk7obj]
	wk8 = [only_num(x.text) for x in wk8obj]
	wk9 = [only_num(x.text) for x in wk9obj]
	
	print "its zipped now creating the list of dicts"
	
	data = {'wk1': wk1,
			'wk2': wk2,
			'wk3': wk3,
			'wk4': wk4,
			'wk5': wk5,
			'wk6': wk6,
			'wk7': wk7,
			'wk8': wk8,
			'wk9': wk9}
		
	# create the dataframe
	
	print "now creating the dataform"
	
	df = pandas.DataFrame(data, index = playerName)

	print "sending to csv"
	
	df.to_csv('weekscores.csv')
		
	browser.close()
	
# # increment the week count and make sure that only active weeks are called
# # need to add a date check in here so it works automatically
def goto_next_week():
	global week
	if week < 10:
		week += 1
		browser.get(poolURL+str(week))
		getPicks()
	else:
 		browser.close()
		# writeCSV()
# 
# # take all of the scores and put them in a tab delimted file
# def writeCSV():
# 	with open('results.tsv','wb') as tsvfile:
# 		writer = csv.writer(tsvfile, delimiter='\t')
# 		writer.writerow(["Week", "Name", "Score"])
# 		for i in weekscores:
# 			writer.writerow(i)
			
#get the party started
loginCBS()	

