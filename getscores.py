#!/usr/bin/python
# coding: latin-1

from selenium import webdriver
from collections import defaultdict
from private import redirectURL, poolURL, userid, password

# start with week 1 and then increment in the goToNextWeek function
week = 1

#establish the dictionary for results
results = defaultdict(list)

#open Firefox and go to login url
browser = webdriver.Firefox()


# login and then call function to gather points
def loginInit():
	browser.get(redirectURL+str(week))
	browser.find_element_by_id("userid").clear()
	browser.find_element_by_id("userid").send_keys(userid)
	browser.find_element_by_id("password").clear()
	browser.find_element_by_id("password").send_keys(password)
	browser.find_element_by_id("submitButton").click()
	getPoints()

#gather player name and weeks results, zip, add to results and then call function for next week
def getPoints():
	playerName = browser.find_elements_by_xpath('//*[@id="nflplayerRows"]/*/td[1]')
	weekPoints = browser.find_elements_by_xpath('//*[@id="nflplayerRows"]/*/td[last()-1]')

	#get the YTD total which is the last element in each row of the table
	#YTDPoints = browser.find_elements_by_xpath('//*[@id="nflplayerRows"]/*/td[last()]')
	
	weekTotal = zip(playerName,weekPoints)

	for name, score in weekTotal:
		a = name.text
		b = score.text
		results[a].append(int(b))
	
	goToNextWeek()
	
# increment the week count and make sure that only active weeks are called
# need to add a date check in here so it works automatically
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

