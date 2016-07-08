from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.select import Select
import os
import time
import shutil
import sys
import argparse

# parse the arguments
parser = argparse.ArgumentParser(description='Scrape more than 500 records from WoS')
parser.add_argument('link',type=str,help='link of results to scrape (this needs to be refreshed')
parser.add_argument('--dis',dest='dis',action='store_const',const=True,default=False,
                    help='display scraping on the screen (default: do it invisibly)')

args=parser.parse_args()

link = args.link

if args.dis==False: # unless --dis option is used, set up virtual display
    display = Display(visible=0, size=(800, 600)) 
    display.start()

d = "WoSResults"

try:
    shutil.rmtree(d) #remove directory if it already exists
except:
    pass

os.mkdir(d) # make the directory

def profile( d ): # initialise browser with profile
    fp = webdriver.FirefoxProfile()

    #set up proxy
    fp.set_preference("network.proxy.type",1)
    fp.set_preference("network.proxy.socks","127.0.0.1")
    fp.set_preference("network.proxy.socks_port", 1080)
    fp.set_preference("network.proxy.socks_version", 4)

    #qj = "/home/max/.mozilla/firefox/tbcljxua.default/extensions//{E6C1199F-E687-42da-8C24-E7770CC3AE66}.xpi"

    #fp.add_extension(qj)
    #fp.set_preference("thatoneguydotnet.QuickJava.curVersion", "2.0.6.1")
    #fp.set_preference("thatoneguydotnet.QuickJava.startupStatus.Images", 2)
    #fp.set_preference("thatoneguydotnet.QuickJava.startupStatus.AnimatedImage", 2)

    # set rules for downloading without asking
    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.dir", os.getcwd()+"/"+d)
    fp.set_preference("browser.altClickSave",True)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")

    browser = webdriver.Firefox(firefox_profile=fp)
    return browser
   
def scrapeWoS( link, browser, rFrom, rTo, i ):

    try :
        close = browser.find_element_by_xpath("//a[@class='quickoutput-cancel-action']") # close previous download box 
        close.click()
    except :
        pass

    fFrom = str(rFrom)
    rTo = str(rTo)

    browser.find_element_by_xpath("//div[@id='s2id_saveToMenu']//b").click() # save to arrow

    if i == 1:
        browser.find_element_by_id('select2-result-label-12').click() # save to other formats
    else :
        browser.find_element_by_id('select2-chosen-1').click() # save to other formats

    browser.find_element_by_id('numberOfRecordsRange').click() # select records range
    browser.find_element_by_id('markFrom').click() # click on from box
    browser.find_element_by_id('markFrom').send_keys(fFrom) # enter keys in from box
    browser.find_element_by_id('markTo').click() # click on to box
    browser.find_element_by_id('markTo').send_keys(rTo) # enter keys in to box

    dropdown = browser.find_element_by_id('bib_fields') # find fields dropdown
    select_box = Select(dropdown) 
    select_box.select_by_index(3) # select option 3 (all records and refs

    browser.find_element_by_xpath("//span[@class='quickoutput-action']").click() # click send

    #browser.quit()

def getQuery ( link, browser ):

    browser.get(link) # take the initialised browser to the link

    q = browser.find_element_by_id("hitCount.top").get_attribute('innerHTML') # find out how many results there are

    q = int(q.replace(',','')) # parse that as a number
    
    return q # return that number


browser = profile(d) # initialise the browser

q = getQuery(link,browser) # find out how many queries there are

scrapes = q / 500 + 1 # find out how many times we need to click

t0 = time.time() # start timing
for i in range(1,scrapes+1):
    pcnti = float(500)/float(q)*100
    f = (i-1)*500+1 # f is the first result to download
    t = i*500 # t is the last
    if t > q: # if the last is bigger than the total, set it to the total
        t = q
    pcnt = round(float(t)/float(q)*100,1) # how far through are we
    
    t00 = time.time() # start timing for each scrape
    scrapeWoS( link, browser, f, t, i ) # scrape
    t1 = time.time() # stop timer
    print str(i) + ". downloading records from " + str(f) + " to " + str(t) + ": " + str(pcnt) + "%"
    total = t1-t0
    it = t1-t00
    tstate = "took " + str(int(round(it,0))) + " seconds, "
    
    remaining = round((it/pcnti)*(100-pcnt),0)

    rm = int(remaining)/60
    rs = int(remaining-(rm*60))

    tstate += "approx. " + str(rm) + " minutes and " + str(rs) + " seconds remaining"
    print tstate
    

time.sleep(5)

try :
    close = browser.find_element_by_xpath("//a[@class='quickoutput-cancel-action']") # close previous download box 
    close.click()
except :
    pass

if args.dis==False:
    display.stop()

totalTime = time.time() - t0

tm = int(totalTime)/60
ts = int(totalTime-(tm*60))

print "done! total time: " + str(tm) + " minutes and " + str(ts) + " seconds"


