from selenium import webdriver
from selenium.webdriver.support.select import Select

#load browser profile function
from .profile import profile

########################################
## Yes no function (from http://code.activestate.com/recipes/577058/)
def query_yes_no(question):
	reply = input(question+' (y/n): ').lower().strip()
	if reply[0] == 'y':
	  return True
	if reply[0] == 'n':
	  return False
	else:
		return query_yes_no("Uhhhh... please enter ")


################################################
## scraping function
def downloadChunk( link, browser, rFrom, rTo, i ):
    try :
        close = browser.find_element_by_xpath("//a[@class='quickoutput-cancel-action']")  #close previous download box
        close.click()
    except :
        pass

    fFrom = str(rFrom)
    rTo = str(rTo)

    browser.execute_script("window.scrollTo(0, 0);")
    #time.sleep(1)
    browser.find_element_by_xpath("//div[@id='s2id_saveToMenu']//b").click()  #save to arrow

    if i == 1:
        browser.find_element_by_id('select2-result-label-12').click()  #save to other formats
    else :
        browser.find_element_by_id('select2-chosen-1').click()  #save to other formats

    browser.find_element_by_id('numberOfRecordsRange').click()  #select records range
    browser.find_element_by_id('markFrom').click()  #click on from box
    browser.find_element_by_id('markFrom').send_keys(fFrom)  #enter keys in from box
    browser.find_element_by_id('markTo').click()  #click on to box
    browser.find_element_by_id('markTo').send_keys(rTo)  #enter keys in to box

    dropdown = browser.find_element_by_id('bib_fields')  #find fields dropdown
    select_box = Select(dropdown)
    select_box.select_by_index(3)  #select option 3 (all records and refs)

    browser.find_element_by_xpath("//span[@class='quickoutput-action']").click()  #click send
















