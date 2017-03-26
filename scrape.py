''' 

this is the webscraping portion of our alexa hackathon project.
this can be used as a module for the alexa interface, or the interface can be coded directly
into this file.

'''

import urllib.request
import bs4 as bs

SERVICEHISTORY = 'service-records'
NOACCIDENTS = 'no-accidents'
CARFAXOWNER = 'one-owner'
PERSONALUSE = 'personal-lease-use'
CERTIFIEDPREOWNED = 'certified'

def neccInfo():

    ## This gets the information from the user for the URL. This is not in the
    ## later function because some of the parameters of the URL needed to be
    ## specifically formatted, so thery required a seperate function. Eventually
    ## this will need to be replaced with question / answers from Alexa and the user

    info = []
    USED = input('would you like the car new or used? (enter "new" or "used"): ')
    info.append(USED)

    MAKE = input('enter the make of your car: ')
    info.append(MAKE)

    MODEL = input('enter the model of your car: ')
    info.append(MODEL)

    ZIP = input('please enter your zipcode (5 digits please): ')
    info.append(ZIP)

    return info

def getCarStats():

    ## This is the information for the URL that required no special formatting.
    ## Eventually this will need to be replaced with questions / answers from Alexa
    ## and the user. 

    statsList = []

    service = input('would you like to know the service records? (y / n) ')
    if service == 'y':
        statsList.append(SERVICEHISTORY)

    accidents = input('would you like the car to never have been in an accident? (y / n) ')
    if accidents == 'y':
        statsList.append(NOACCIDENTS)

    carfax = input('do you care if the previous owner was a carfax member? (y / n) ')
    if carfax == 'y':
        statsList.append(CARFAXOWNER)

    personal = input('will this car be for personal use? (y / n) ')
    if personal == 'y':
        statsList.append(PERSONALUSE)

    certified = input('would you like the car to be a certified pre-owned? (y / n) ')
    if certified == 'y':
        statsList.append(CERTIFIEDPREOWNED)

    return statsList

def findprices(baseUrl):

    ## Retrieves the listed price for the car

    pricesList = []

    for cardiv in soup.find_all('div', {'class':'other'}):
        priceclass = cardiv.find('div', {'class':'price-normal'})
        price = priceclass.find('span', {'itemprop':'price'}).text
        pricesList.append(price)

    return pricesList

def findmiles(soup):

    ## Retrieves the current milage of the car

    milesList = []

    for milediv in soup.find_all('div', {'class':'other'}):
        mileclass = milediv.find('p', {'class':'miles'})
        milage = mileclass.find('strong').text
        milesList.append(milage)

    return milesList

def findColor(soup):

    ## Retrieves the color of the car

    colorList = []

    for colordiv in soup.find_all('div', {'class':'other'}):
        colorClass = colordiv.find('div', {'class':'special-features group2'})
        color = colorClass.find('span', {'class': 'special-features--value'}).text
        colorList.append(color)

    return colorList

def findTitle(soup):

    ## Retrieves the specific title of the car.

    titleList = []

    for titleDiv in soup.find_all('div', {'class':'basic-detail'}):
        titleClass = titleDiv.find('a', {'class':'j-singlepage'})
        title = titleClass.find('span', {'class': 'title'}).text
        titleList.append(title)

    return colorList

def findEngineInfo(soup):

    ## Retrieves the color of the car

    engineList = []

    for engineDiv in soup.find_all('div', {'class':'other'}):
        engineClass = engineDiv.find('div', {'class':'special-features group2'})

        detailList = engineClass.find_all('span', {'class': 'special-features--value'})
        engine = detailList[1].text
        transmission = detailList[2].text
        engineList.append([engine, transmission])

    return engineList


def getUrl():

    ## This gets formats the url with the users information

    info = neccInfo()
    statsList = getCarStats()
    baseUrl = 'https://www.carfax.com/vehicles/{0}-{1}-{2}--{3}'.format(info[0], info[1], info[2], info[3])
    for stat in statsList:
        baseUrl += '/' + stat

    return baseUrl

def generateCars(priceList,milesList,colorList,titleList,engineList):

    ## This just combines all of the lists of the information about the car into
    ## one giant list. It also forms everything into a dictionary since that it
    ## does not be iterated over and the key values make more sense

    carList = []
    for index in range(len(priceList)):
        carList.append({

        'title': titleList[index],
        'miles': milesList[index],
        'price': priceList[index],
        'color': colorList[index],
        'engineSize': engineList[index][0],
        'transmissionType': engineList[index][1]

        })
    print('we found {} cars that fit your description!\n'.format(len(carList)))
    return carList

def printCars(carList):

    ## This just prints the cars to the screen. Eventually this is what we will replace with
    ## Alexa telling the person about the cars.

    for car in carList:
        print('the exact title of the car is: {}'.format(car['title']))
        print('the exact milage on the car is: {} miles'.format(car['miles']))
        print('the exact price on the car is: ${}'.format(car['price']))
        print('the exact color of the car is: {}'.format(car['color']))
        print('the engine size of the car is: {}'.format(car['engineSize']))
        print('the transmission type of the car is: {}'.format(car['transmissionType']))

        print('\n\n\n')



## This ensures that the page only gets loaded once
baseUrl = getUrl()

print('\nPlease wait while we search for cars that fit your description...\n')

page = urllib.request.urlopen(baseUrl).read()
soup = bs.BeautifulSoup(page, 'lxml')

priceList = findprices(soup)
milesList = findmiles(soup)
colorList = findColor(soup)
titleList = findTitle(soup)
engineList = findEngineInfo(soup)

carList = generateCars(priceList,milesList,colorList,titleList,engineList)

printCars(carList)




