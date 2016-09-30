#!/usr/bin/env python3

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.select import Select
import os
import time
import shutil
import sys
import argparse
import scrapeWoS

# set up the virtual display
display = Display(visible=0, size=(800, 600))
display.start()

# Parse the arguments
parser = argparse.ArgumentParser(description='Scrape more than 500 records from WoS')
parser.add_argument('query',type=str,help='name of .txt file containing an advanced WoS Query')
parser.add_argument('-b',dest='browser',default="chrome",type=str,help='first record to download (default=1)')

args=parser.parse_args()

# the directory is a new folder with the same name as the query file
cwd = os.getcwd()
d = cwd+'/'+args.query.replace('.txt','')

if (os.path.isdir(d)):
	if scrapeWoS.query_yes_no("directory already exists and would be overwritten. Are you sure you want to do this?"):
		shutil.rmtree(d)
	else:
		exit()

os.mkdir(d) # make the directory

#read query
with open(args.query, 'r') as myfile:
    query=myfile.read().replace('\n', '')
print(query)

#set up browser (return browser)

#browser = scrapeWoS.profile(d,args.browser)
browser = scrapeWoS.profile(d,args.browser)


# go to adv search page 
link = "http://apps.webofknowledge.com/"
browser.get(link)

# change search type
browser.find_element_by_xpath('//i[@class="icon-dd-active-block-search"]').click()
browser.find_element_by_xpath('//a[@title="Advanced Search"]').click()

# search for query
search_box = browser.find_element_by_id('value(input1)')
search_box.send_keys(query)
browser.find_element_by_id('searchButton').click()

# click the first result link
browser.find_element_by_xpath('//div[@class="historyResults"]').click()

# how many results are there?
q = browser.find_element_by_id("hitCount.top").get_attribute('innerHTML')
q = int(q.replace(",",""))
# here's a link to the results page
qlink = browser.current_url

# Check we haven't got too many results..
if q > 100000:
	print("This search generates more than 100,000 results. WoS won't let you download past the 100,001st result. Consider splitting your search up into subsections by year and combining later...")
	print("exiting...")
	exit()


# download query results 
print("This search generates "+str(q)+" results. We'll download them in blocks of 500...")
scrapes = int(q // 500 + 1) # find out how many times we need to click

t0 = time.time() # start timing
for i in range(1,scrapes+1):
	pcnti = float(500)/float(q)*100
	f = (i-1)*500+1 # f is the first result to download
	t = i*500 # t is the last
	if t > q: # if the last is bigger than the total, set it to the total
	    t = q
	pcnt = round(float(t)/float(q)*100,1) # how far through are we

	t00 = time.time() # start timing for each scrape
	scrapeWoS.downloadChunk( qlink, browser, f, t, i ) # scrape
	t1 = time.time() # stop timer
	print(str(i) + ". downloading records from " + str(f) + " to " + str(t) + ": " + str(pcnt) + "%")
	total = t1-t0
	it = t1-t00
	tstate = "took " + str(int(round(it,0))) + " seconds, "

	remaining = round((it/pcnti)*(100-pcnt),0)

	rm = int(remaining//60)
	rs = int(remaining-(rm*60))

	tstate += "approx. " + str(rm) + " minutes and " + str(rs) + " seconds remaining"
	print(tstate)


time.sleep(5)

try :
    close = browser.find_element_by_xpath("//a[@class='quickoutput-cancel-action']") # close previous download box
    close.click()
except :
    pass

browser.quit()

display.stop()

totalTime = time.time() - t0

tm = int(totalTime//60)
ts = int(totalTime-(tm*60))

print("done! total time: " + str(tm) + " minutes and " + str(ts) + " seconds")

# go through results files and put into one big file / put in mysql database
with open(d+'/results.txt','w') as res:
	for f in os.listdir(d):
		if "savedrecs" in str(f):
			with open(d+"/"+f,'r') as recs:
				res.write(recs.read())
			os.remove(f)
		



