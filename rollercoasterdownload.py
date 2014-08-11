from bs4 import BeautifulSoup
import praw # simple interface to the reddit API, also handles rate limiting of requests
from random import randint
import time
import urllib2

randnum = randint(0, 12250)

link = 'http://rcdb.com/' + str(randnum) + '.htm'

response = urllib2.urlopen(link)

textOfLink = '[Link](' + link + ')'

print textOfLink

soup = BeautifulSoup(response)

# extract ride/park name
allH1Tags = soup.findAll('h1')
rideParkName = str(allH1Tags[0])
rideParkName = rideParkName[4:]
rideParkName = rideParkName[:-5]

title = 'Random Ride/Park of the Day: ' + rideParkName

USERNAME  = ""
PASSWORD  = ""
USERAGENT = "A bot for /r/rollercoasters"
SUBREDDIT = "rollercoasters"

WAIT = 60*60*24 # 1 day

WAITS = str(WAIT) 
try:
    import bot 
    USERNAME = bot.getu()
    PASSWORD = bot.getp()
    USERAGENT = bot.geta()
except ImportError:
    pass

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD) 

def runSubmission():
    subreddit = r.get_subreddit(SUBREDDIT)
    r.submit(subreddit, title, url=link)


while True:
    try:
        runSubmission()
    except Exception as e:
        print('An error has occured:', e)
    print('Running again in ' + WAITS + ' seconds \n')
    time.sleep(WAIT)