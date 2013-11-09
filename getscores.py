#!/usr/bin/python
# coding: latin-1

from selenium import webdriver
from collections import defaultdict
from private import redirectURL, poolURL, userid, password
import csv
import re
from collections import Counter
import pandas
import vincent
import redis

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
week = 1

# login and then call function to gather data
def loginInit():
	browser.get(poolURL+str(week))
	# browser.get(redirectURL)
	browser.find_element_by_id("userid").clear()
	browser.find_element_by_id("userid").send_keys(userid)
	browser.find_element_by_id("password").clear()
	browser.find_element_by_id("password").send_keys(password)
	browser.find_element_by_id("submitButton").click()
	# getPoints()
	# getPicks()
	getPlayerPicks()

# strips out high score and no pick indicators from score
def onlyNum(x):
	return re.sub(r"\D","",x)

# used to get just the team name from the results
def onlyAlpha(x):
	return re.sub(r"\W|\d","",x)


def getPlayerPicks():
	playerobj = browser.find_elements_by_class_name('bg2'["left"])
	for i in playerobj:
		print i.text



def getPicks():
	correctobj = browser.find_elements_by_class_name('correct')
	incorrectobj = browser.find_elements_by_class_name('incorrect')
	correct = [onlyAlpha(x.text) for x in correctobj]
	incorrect = [onlyAlpha(x.text) for x in incorrectobj]
	for i in correct:
		r.zincrby('correct',i,1)
	for i in incorrect:
		r.zincrby('incorrect',i,1)
	
	# print Counter(correct) 
	# print Counter(incorrect)
	browser.close()

#gather player name and score by week
def getPoints():
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
	wk1 = [onlyNum(x.text) for x in wk1obj]
	wk2 = [onlyNum(x.text) for x in wk2obj]
	wk3 = [onlyNum(x.text) for x in wk3obj]
	wk4 = [onlyNum(x.text) for x in wk4obj]
	wk5 = [onlyNum(x.text) for x in wk5obj]
	wk6 = [onlyNum(x.text) for x in wk6obj]
	wk7 = [onlyNum(x.text) for x in wk7obj]
	wk8 = [onlyNum(x.text) for x in wk8obj]
	wk9 = [onlyNum(x.text) for x in wk9obj]
	
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
# def goToNextWeek():
# 	global week
# 	if week < 10:
# 		week += 1
# 		browser.get(poolURL+str(week))
# 		getPicks()
# 	else:
#  		browser.close()
# 		writeToCSV()
# 
# # take all of the scores and put them in a tab delimted file
# def writeToCSV():
# 	with open('results.tsv','wb') as tsvfile:
# 		writer = csv.writer(tsvfile, delimiter='\t')
# 		writer.writerow(["Week", "Name", "Score"])
# 		for i in weekscores:
# 			writer.writerow(i)
			
#get the party started
loginInit()	

