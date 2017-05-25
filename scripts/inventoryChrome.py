# install selenium and bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
import json, re
# import csv

chrome_options = Options()
# mobile_emulation = {
#     'deviceMetrics': { 
#     	'width': 360, 
#     	'height': 640, 
#     	'pixelRatio': 1.0 
#     },
#     'userAgent': 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/_BuildID_) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36' 
# }
preferences = {
    'credentials_enable_service': False,
    'profile': {
        'password_manager_enabled': False
    }
}
# chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
chrome_options.add_experimental_option('prefs', preferences)
driver = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)
driver.set_window_size(1024, 768)

driver.get('http://na.finalfantasyxiv.com/lodestone/account/login/')

while('my' not in driver.current_url):
	sleep(5)

data = {}
data['inventory'] = []
itemCount = 0
characterId = 0

driver.get('http://na.finalfantasyxiv.com/lodestone/character/4348521/item/')
page = BeautifulSoup(driver.page_source, 'lxml')
pages = int(re.search(r'(\d+)$', page.find('li', class_='btn__pager__current').get_text()).group(0))
print('Number of pages set to ' + str(pages))

if (characterId < 1):
	characterId = str(re.search(r'(\/)(\d+)(\/)', driver.current_url).group(0).replace('/', ''))
	print('Character ID set to ' + characterId)

for p in range(1, pages+1):
	# Mobile Mode URL
	# driver.get('http://na.finalfantasyxiv.com/lodestone/character/4348521/item/more/?category1=&q=&hq=&page='+ str(p))

	driver.get('http://na.finalfantasyxiv.com/lodestone/character/4348521/item/?q=&category1=&hq=&page='+ str(p))
	page = BeautifulSoup(driver.page_source, 'lxml')

	# Loop for Mobile Mode
	# for t in page.findAll('div', 'retainer__content__list'):
	# 	linkToInventory = t.find('a', class_='retainer__content__list__inner')['href']
	# 	iconImage = t.find('img', class_='item-icon__image')['src']
	# 	nameAndQuantity = t.find('p', class_= 'retainer__content__list--item_name').contents
	# 	# retainerName = t.find('p', class_='retainer__content__list--char').contents
	# 	item = [linkToInventory, iconImage, nameAndQuantity]
	# 	items.append(item)

	for t in page.findAll('li', 'item-list__list'):

		itemCount += 1
		itemLink = t.find('div', class_='item-list__name').find('a', href=True)['href']
		itemNameAndQuantity = t.find('div', class_='item-list__name').find('a', href=True).get_text().replace('\n', '').replace('\t', '')
		retainerName = t.find('div', 'item-list__cell--md').find('a', href=True).get_text()
		
		# replace this with the inventory slot data from Mobile Mode
		retainerLink = t.find('div', 'item-list__cell--md').find('a', href=True)['href']

		itemId = re.search(r'(\/)(\w+)(\/$)', itemLink).group(0).replace('/', '')
		itemQuantity = int(re.search(r'(\()(\d?)(,?)(\d+)(\)$)', itemNameAndQuantity).group(0).replace('(', '').replace(')', '').replace(',', ''))
		itemName = re.sub(r'(\()(\d+)(\)$)', '', itemNameAndQuantity)

		data['inventory'].append({
			'id': itemId,
			'name': itemName,
			'quantity': itemQuantity,
			'retainer': retainerName,
			'slot': 0
		})
		print('Added item named ' + itemName)

# print(data)

with open('inventory_'+ str(characterId) +'.json', 'w') as output:  
    json.dump(data, output, sort_keys=True, indent=4,  ensure_ascii=False)
    print('Updated inventory_' + str(characterId) + '.json with ' + str(itemCount) + ' entries')

driver.quit()