from fuzzywuzzy import process
import logging, os, discord, asyncio,sys,csv,traceback
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

FIREFOX_PATH = r'C:\Program Files\Mozilla Firefox\firefox.exe'
GECKODRIVER_PATH = r'C:\geckodriver.exe'
cachefolder = os.getcwd() + '\cache\\'
cachetrigger = True;
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

dbUrl = 'https://classicdb.ch/?item='
dbQuestUrl = 'https://classicdb.ch/?quest='
dbNpcUrl = 'https://classicdb.ch/?npc='

def takeimage(itemID):
	#setup browser for running in background
	os.environ['MOZ_HEADLESS'] = '1'
	binary = FirefoxBinary(FIREFOX_PATH, log_file=sys.stdout)
	binary.add_command_line_options('-headless')
	browser = webdriver.Firefox(executable_path=GECKODRIVER_PATH,firefox_binary=binary)
	#request item url
	browser.get(dbUrl + itemID)

	try:
		browser.find_element_by_class_name('tooltip').screenshot(cachefolder + str(itemID) + '.png')
		print('Tooltip for item id : %s found at %s\nSaved at %s' % (itemID, str(dbUrl + str(itemID)), str(cachefolder+ str(itemID) + '.png')))
	except:
		print('Tooltip for item id : %s not found at %s' % (itemID, str(dbUrl + str(itemID))))
	browser.close()


def initItemsDict():
	items = {}
	with open('items.csv', 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			items[row['name']] = row['entry']
	return items

def findimagefromcache(itemID):
	filename = itemID + '.png'
	print('Trying to find ' + filename)
	for files in os.walk(cachefolder):
		for file in files:
			if filename in file:
				print('Item found in cache folder')
				return True
	print('Item not found in cache folder')
	return False

items = initItemsDict()
print(items)
for i in items:
    if not (findimagefromcache(items[i])):
        print('Downloading File for ' + items[i])
        takeimage(items[i])