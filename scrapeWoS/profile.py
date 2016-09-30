from selenium import webdriver

############################################################
## function to set up a browser

def profile( d , b): # initialise browser [b] with profile, setting download directory to [d]
	###### firefox - Doesn't work since update ?!!
	if b=="firefox":
		fp = webdriver.FirefoxProfile()

		#set up proxy
		fp.set_preference("network.proxy.type",1)
		fp.set_preference("network.proxy.socks","127.0.0.1")
		fp.set_preference("network.proxy.socks_port", 1080)
		fp.set_preference("network.proxy.socks_version", 4)

		# set rules for downloading without asking
		fp.set_preference("browser.download.folderList",2)
		fp.set_preference("browser.download.manager.showWhenStarting",False)
		fp.set_preference("browser.download.dir", d)
		fp.set_preference("browser.altClickSave",True)
		fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")

		browser = webdriver.Firefox(firefox_profile=fp)

	####phantomjs can't download files!??
	if b=="phantomjs":

		service_args = [
			"--proxy=127.0.0.1:1080",
			"--proxy-type=socks4"
		]
		browser = webdriver.PhantomJS('phantomjs',service_args=service_args)


	if b=="chrome":
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:1080')
		chrome_options.add_argument('download.default_directory='+d)
		chrome_options.add_argument('--download.default_directory='+d)
		chrome_options.add_argument('directory_upgrade=true')

		prefs = {"download.default_directory" : d}
		chrome_options.add_experimental_option("prefs",prefs)

		browser = webdriver.Chrome(chrome_options=chrome_options)	

	browser.implicitly_wait(5)
		
	return browser
