from fuzzywuzzy import process
import logging, os, discord, asyncio,sys,csv,traceback
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

cachefolder = os.getcwd() + '/cache/'
cachetrigger = True
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

dbUrl = 'https://classicdb.ch/?item='
dbQuestUrl = 'https://classicdb.ch/?quest='
dbNpcUrl = 'https://classicdb.ch/?npc='

@client.event
async def on_ready():
	print('logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-------')

@client.event
async def on_message(message):
	if message.content.startswith('!help'):
		await message.channel.send('Find item\'s tooltip :\n- "!finditem <NAME/ID>" or "!fi <NAME/ID>" - Example -> !finditem thunderfury\n- "!finditem #VANILLAGAMINGITEMID" - Example -> !finditem 18402')
		await message.channel.send('Finding Player :\n- "!findplayer <NAME>" or "!fp <NAME>"')
		await message.channel.send('Finding Quest :\n- "!findquest <NAME/ID>" or "!fq <NAME/ID>"')
		await message.channel.send('Finding NPC :\n- "!findnpc <NAME/ID>" or "!fn <NAME/ID>"')
	elif (message.content.startswith(('!finditem', '!fi', '!i', '!item'))):
		await message.channel.send('Looking for item...')
		foundFile = False
		delete = True
		try:
			newArgs = message.content.split(' ')
			print (newArgs)
			if (len(newArgs) >= 2):
				if (len(newArgs) == 2):
					if newArgs[1].isdigit():
						itemid = newArgs[1]
					else:
						itemid = findItemIDFromName(newArgs[1])
				else:
					itemid = findItemIDFromName(rebuildName(newArgs))
				await message.channel.send(str(dbUrl + str(itemid)))
				if findimagefromcache(itemid):
					delete = False
				else:
					print('Downloading File')
					takeimage(itemid)
				try:
					with open(cachefolder + itemid + '.png', 'rb') as f:
						await message.channel.send(file=discord.File(cachefolder + itemid + '.png'))
						foundFile = True
				except:
                                        print(traceback.format_exc())
                                        await message.channel.send('Error Finding Item, make sure you pass the right item ID')
			else:
				await message.channel.send('Command Error')
		except ValueError:
			print(traceback.format_exc())
			await message.channel.send('Error Finding Item, make sure you passed the right parameters')
		#If cache argument has not passed, delete the item after sending it to Discord
		if delete and foundFile and cachetrigger is False:
			os.remove(cachefolder + str(itemid) + '.png')
			print(str(itemid) + '.png removed ')
	elif (message.content.startswith(('!findplayer', '!fp', '!p', '!player'))):
		await message.channel.send('Looking for Player...')
		try:
			newArgs = message.content.split(' ')
			if (len(newArgs) == 2):
				try:
					await message.channel.send(findplayer(newArgs[1]))
				except:
					await message.channel.send("Couldn't find player")
		except:
			await message.channel.send('Command Error')
	elif (message.content.startswith(('!findquest', '!fq', '!q', '!quest'))):
		await message.channel.send('Looking for Quest...')
		try:
			newArgs = message.content.split(' ')
			if (len(newArgs) == 2):
				if newArgs[1].isdigit():
					itemid = newArgs[1]
				else:
					itemid = findQuestIDFromName(newArgs[1])
			else:
				itemid = findQuestIDFromName(rebuildName(newArgs))
			if (itemid):
				await message.channel.send(str(dbQuestUrl + str(itemid)))
			else:
				await message.channel.send("Couldn't find quest")
		except Exception:
			print(traceback.format_exc())
			await message.channel.send("Couldn't find quest")
	elif (message.content.startswith(('!findnpc', '!fn', '!n', '!npc'))):
		await message.channel.send('Looking for NPC...')
		try:
			newArgs = message.content.split(' ')
			if (len(newArgs) == 2):
				if newArgs[1].isdigit():
					itemid = newArgs[1]
				else:
					itemid = findNpcIDFromName(newArgs[1])
			else:
				itemid = findNpcIDFromName(rebuildName(newArgs))
			if (itemid):
				await message.channel.send(str(dbNpcUrl + str(itemid)))
			else:
				await message.channel.send("Couldn't find npc")
		except Exception:
			print(traceback.format_exc())
			await message.channel.send("Couldn't find npc")

def takeimage(itemID):
    #setup browser for running in background
    os.environ['MOZ_HEADLESS'] = '1'
    browser = webdriver.Firefox()
    browser.get(dbUrl + itemID)
    try:
        browser.find_element_by_class_name('tooltip').screenshot(cachefolder + str(itemID) + '.png')
        print('Tooltip for item id : %s found at %s\nSaved at %s' % (itemID, str(dbUrl + str(itemID)), str(cachefolder+ str(itemID) + '.png')))
    except:
        print('Tooltip for item id : %s not found at %s' % (itemID, str(dbUrl + str(itemID))))
    browser.close()


def findplayer(playerName):
	realmPlayers = 'https://legacyplayers.com/Search/?search='
	return (realmPlayers + playerName)

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

def findItemIDFromName(name):
	global items
	if not bool(items):
		items = initItemsDict()
	return items[process.extractOne(name, items.keys())[0]]

def findQuestIDFromName(name):
	global quests
	if not bool(quests):
		quests = initQuestsDict()
	data = process.extractOne(name, quests.keys())
	return quests[data[0]]

def findNpcIDFromName(name):
	global npcs
	if not bool(npcs):
		npcs = initNpcsDict()
	data = process.extractOne(name, npcs.keys())
	return npcs[data[0]]


def initQuestsDict():
	quests = {}
	with open('quests.csv', 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			quests[row['Title']] = row['entry']
	return quests

def initItemsDict():
	items = {}
	with open('items.csv', 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			items[row['name']] = row['entry']
	return items

def initNpcDict():
	npcs = {}
	with open('creature.csv', 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			npcs[row['name']] = row['entry']
	return npcs

def rebuildName(args):
	name = ''
	for i in range(1, len(args)):
		name += args[i]
		if i  != len(args):
			name += ' '
	return name

if __name__ == '__main__':
	myargs = sys.argv
	if '-nc' in myargs:
            cachetrigger = False
	if not os.path.exists(os.path.dirname(cachefolder)):
	    try:
	        os.makedirs(os.path.dirname(cachefolder))
	    except:
	        print('Error while creating the cache folder')
	print('Cache is {0}'.format(cachetrigger))
	print(myargs)
	global items, quests, npcs
	items = initItemsDict()
	quests = initQuestsDict()
	npcs = initNpcDict()


client.run('MzkwOTk1MjY2OTg5MzI2MzQ2.DRSORg.-e_aMd2pSRO3Mqh5rHdul5u39nE')
