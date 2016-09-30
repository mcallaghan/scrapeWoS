from setuptools import setup

setup(name='scrapeWoS',
      version='0.1',
      description='Scrape records from WoS',
      url='http://github.com/mcallaghan/scrapeWoS',
      author='Max Callaghan',
      author_email='callaghan@mcc-berlin.net',
      license='MIT',
      packages=['scrapeWoS'],
      install_requires=[
          'selenium',
			 'argparse'
      ],
		scripts=['bin/check_selenium_ip.py','bin/scrapeQuery.py'],
      zip_safe=False)
