''' 
This will be a practice webscraper to get whatever we need for our recycling database or
whatever else we might decide to do.

hopefully we can easily transfer this code to node js lol.
'''

import bs4 as bs
import urllib.request

def listHandler(source):
	for listItem in soup.find_all('li'):
		if listItem.find('p'):
			recycleData.append(listItem.find('p').text.strip())
		else:
			pass


def rowHandler(source):
	evenCount = 0

	for listItem in soup.find_all('td'):
		if listItem.find('p'):
			if evenCount % 2 == 0:
				recycleData.append(listItem.find('p').text.strip())
				evenCount += 1
			else:
				nonrecycleData.append(listItem.find('p').text.strip())
				evenCount += 1
		else:
			pass


recycleData = []
nonrecycleData = []
sourcesList = [

['http://www.cleanscapes.com/shoreline/recycling_guidelines/recycling/recyclable_materials_list/','li'], 
['http://www.lindoncity.org/recyclable-materials-list.htm', 'td']

]

for source in sourcesList:
	page = urllib.request.urlopen(source[0]).read()
	soup = bs.BeautifulSoup(page, 'lxml')

	if source[1] == "li":
		listHandler(soup)
	elif source[1] == "td":
		rowHandler(soup)

#TODO!! turn this from printing out the recyclables to saving them to a text file
for recyclable in recycleData:
	print(recyclable)

print("\n\n now entering scary zone of unrecyclables \n\n")

#TODO!! turn this from printing out the non-recyclables to saving them to a text file
for nonrecyclable in nonrecycleData:
	print(nonrecyclable)



