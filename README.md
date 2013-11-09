This is a little project to scrape weekly scores from my CBS Sportsline office pool
and produce graphs of the weekly results. 

TODO: 

* ~~login to the the CBS Sportsline website and to league page~~
* ~~pull down the data that is needed~~
* figure out how to handle players with the same name
* ~~format the data~~
* ~~export to a csv~~
* graphing using [dimpleJS](http://dimplejs.org/), matplotlib, Vincent?
* filter on player name(s)
* write test cases
* organize scripts and eliminate manual switches


## User Variables

You must create a file called private.py and in it declare the following:

	redirectURL = 'http://www.cbssports.com/login?xurl=http://leaguename.football.cbssports.com/office-pool/standings/live/'
	poolURL = 'http://leaguename.football.cbssports.com/office-pool/standings/live/'
	userid = 'username'
	password = 'password'

save the file in the same directory as getscores.py

I'm sure there is a better way to handle this - suggestions welcome!

## Current Status

The code is just a collection of scripts right now...no test cases, manual switching. 