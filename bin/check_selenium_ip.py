#!/usr/bin/env python3

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.select import Select
import os
import time
import shutil
import sys
import argparse
from scrapeWoS import * 

print("hello world")




# parse the arguments
parser = argparse.ArgumentParser(description='Scrape more than 500 records from WoS')
parser.add_argument('-b',dest='browser',default="firefox",type=str,help='first record to download (default=1)')
args=parser.parse_args()

btype = args.browser

browser = profile("/tmp",btype)

browser.get("https://www.whatismyip.com/")

ipbox = browser.find_element_by_xpath("//div[@class='ip']")

print(ipbox.get_attribute('innerHTML'))


browser.quit()
