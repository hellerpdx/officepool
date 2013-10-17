#!/usr/bin/python
# coding: latin-1

from selenium import webdriver
from collections import defaultdict
from private import redirectURL, poolURL, userid, password

# url variables
# redirectURL = 'http://www.cbssports.com/login?xurl=http://nepool.football.cbssports.com/office-pool/standings/live/'
# poolURL = 'http://nepool.football.cbssports.com/office-pool/standings/live/'
week = 1

results = defaultdict(list)

#open Firefox and go to login url
browser = webdriver.Firefox()

def loginInit():
	browser.get(redirectURL+str(week))
	browser.find_element_by_id("userid").clear()
	browser.find_element_by_id("userid").send_keys(userid)
	browser.find_element_by_id("password").clear()
	browser.find_element_by_id("password").send_keys(password)
	browser.find_element_by_id("submitButton").click()
	getPoints()

def getPoints():
	#get Player Name which is the first element in each row of the table
	playerName = browser.find_elements_by_xpath('//*[@id="nflplayerRows"]/*/td[1]')

	#get the weeks total which is the 2nd to last element in each row of the table
	weekPoints = browser.find_elements_by_xpath('//*[@id="nflplayerRows"]/*/td[last()-1]')

	#get the YTD total which is the last element in each row of the table
	#YTDPoints = browser.find_elements_by_xpath('//*[@id="nflplayerRows"]/*/td[last()]')

	#zip the results together
	weekTotal = zip(playerName,weekPoints)

	for name, score in weekTotal:
		a = name.text
		b = score.text
		results[a].append(int(b))
	goToNextWeek()
	
def goToNextWeek():
	global week
	if week < 6:
		week += 1
		browser.get(poolURL+str(week))
		getPoints()
	else:
 		browser.close()
		for key,value in results.iteritems():
			print key,value

loginInit()	

