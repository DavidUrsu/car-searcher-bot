from asyncio.windows_events import NULL
from turtle import update
from numpy import size
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import telegram
import configparser

config = NULL
bot = telegram.Bot('5125366694:AAFtjN0dvbjMU5JDkWGaHfOwLt8KVAk6Sso')

def scrapMobileDe():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get( config.get("SITES", "mobile.de") )
    driver.implicitly_wait(20)

    listOfCars = driver.find_element(By.XPATH, "/html/body/div/div/div[3]/section/div[1]") #get the list of the Cars

    dataOfCars = listOfCars.get_attribute("innerHTML") #transform the html into text

    startOfPromotions = dataOfCars.find('<section class="list-entry g-row">') #finds the section where are the promotions
    endOfPromotions = dataOfCars.find('</section>', startOfPromotions) #finds the end of the section
    dataOfCars = dataOfCars[0: startOfPromotions] + dataOfCars[endOfPromotions: len(dataOfCars)-1] #deletes the section

    dataOfCars = dataOfCars.split('<article class="list-entry g-row">') #split every element by the HTML <article> atribute
    dataOfCars.pop(0) #the first element is a script

    myListOfCars = [] #creates the list of the cars

    #adds every car to a list
    for i in dataOfCars:
        currentCar = []
        
        #TITLE
        startOfTitle = i.find('<h3 class="vehicle-title g-col-s-11">')
        endOfTitle =  i.find('</h3>', startOfTitle)
        currentCar.append((i[startOfTitle + len('<h3 class="vehicle-title g-col-s-11">') :endOfTitle]))

        #YEAR AND KILOMETERS
        startOfKm = i.find('<p class="u-text-bold">')
        endOfKm = i.find('</p>', startOfKm)
        yearAndKm = i[startOfKm + len('<p class="u-text-bold">') :endOfKm]
        yearAndKm = yearAndKm.split(",") #splits the year and mileage

        yearAndKm[1] = ''.join([i for i in yearAndKm[1] if i>='0' and i<='9']) #creates a string from only the digits of the element

        currentCar.append(yearAndKm[0])
        currentCar.append(yearAndKm[1])

        #PRICE
        startOfPrice = i.find('<p class="seller-currency u-text-bold">')
        endOfPrice = i.find('</p>', startOfPrice)

        price = i[startOfPrice + len('<p class="seller-currency u-text-bold">') :endOfPrice]
        price = ''.join([i for i in price if i>='0' and i<='9']) #creates a string from only the digits of the element

        currentCar.append(price)

        #LINK
        startOfLink = i.find('href="')
        endOfLink = i.find('">', startOfLink)
        currentCar.append("https://www.mobile.de" + (i[startOfLink + len('href="'): endOfLink]))

        #appends to the list of Cars
        myListOfCars.append(currentCar)

    driver.quit()

    return myListOfCars

def scrapAutoScout24():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get( config.get("SITES", "autoscout24") )
    driver.implicitly_wait(20)

    listOfCars = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/div/div[4]/div[2]/main") #get the list of the Cars

    dataOfCars = listOfCars.get_attribute("innerHTML") #transform the html into text

    dataOfCars = dataOfCars.split('<article') #split every element by the HTML <article> atribute
    dataOfCars.pop(0) #the first element is the header of the search menu

    myListOfCars = [] #creates the list of the cars

    #adds every car to a list
    for i in dataOfCars:
        currentCar = []
        
        #TITLE
        startOfTitle = i.find('<h2 class="css-4u347z') #emtvtq424
        endOfTitle =  i.find('</span>', startOfTitle)
        title = i[startOfTitle + len('<h2 class="css-4u347z elv7w5p24">') :endOfTitle]
        title = title.replace('<!-- -->', '') #remove the html comments from the title
        title = title.replace('</h2><span>', '') #remove the html atributes from the title
        currentCar.append(title)
        
        #YEAR
        startOfYear = i.find('<span type="registration-date" class="css-mo69i0 e1hcrnma1">')
        endOfYear = i.find('</span>', startOfYear)
        if startOfYear == -1: #the car can have unposted details, so we are skipping it
            continue

        currentCar.append(i[startOfYear + len('<span type="registration-date" class="css-mo69i0 e1hcrnma1">') :endOfYear] )

        #MILEAGE
        startOfKm = i.find('<span type="mileage" class="css-mo69i0 e1hcrnma1">')
        endOfKm = i.find('</span>', startOfKm)
        if startOfKm == -1: #the car can have unposted details, so we are skipping it
            continue

        mileage = i[startOfKm + len('<span type="mileage" class="css-mo69i0 e1hcrnma1">') :endOfKm]
        mileage = ''.join([i for i in mileage if i>='0' and i<='9']) #creates a string from only the digits of the element

        currentCar.append(mileage)

        #PRICE
        startOfPrice = i.find('<div class="css-s5xdrg"><span class="css-113e8xo">')
        endOfPrice = i.find(',-', startOfPrice)

        price = i[startOfPrice + len('<div class="css-s5xdrg"><span class="css-113e8xo">') :endOfPrice]
        price = ''.join([i for i in price if i>='0' and i<='9']) #creates a string from only the digits of the element

        currentCar.append(price)

        #LINK
        startOfLink = i.find('css-5n6fy4 e1q3laaa0" href="')
        endOfLink = i.find('"><span>', startOfLink)
        currentCar.append("https://www.autoscout24.ro" + (i[startOfLink + len('css-5n6fy4 e1q3laaa0" href="'): endOfLink]))

        #appends to the list of Cars
        myListOfCars.append(currentCar)

    driver.quit()

    return myListOfCars

if __name__ == "__main__":

    config = configparser.RawConfigParser()
    config.read('config.ini')

    myListOfCars = []
    for i in scrapAutoScout24():
        myListOfCars.append(i)
    
    for i in scrapMobileDe():
        myListOfCars.append(i)

    #Checking if is the first time of running the app
    if os.path.getsize("cars.list")==0:
        with open("cars.list", "w") as fileOfCars:
            #writes the first cars in the list
            for i in myListOfCars:
                currentCar = '|'.join([j for j in i]) #the serialization of a string that containts all the data of the car
                fileOfCars.write(currentCar+"\n") #writes the line to the file
    else:
        carsInFile = [] #creates a list with all the cars in the file (already scanned)
        with open("cars.list", "r") as fileOfCars:
            for i in fileOfCars:
                carsInFile.append(i)

        #checking if a new car is found
        fileOfCars = open("cars.list", "a")
        for i in myListOfCars:
            ok=0
            carString = '|'.join([j for j in i]) #the serialization a string like the one in the file
            for j in carsInFile:
                if carString == j.rstrip("\n"): #checks every car in the file with the every car in the list returned from the website
                    ok=1
            if ok == 0 and int( config.getint("PARAMETERS", "alert-price") ) >= int(i[3]):
                message = "A new car was found! {0} \nAt the price of {1} euro \nNumber of kilometers: {2} \nYear of fabrication: {3} \n{4}".format(i[0], i[3], i[2], i[1], i[4])
                print(i)
                bot.send_message( config.getint("PARAMETERS", "telegram-id") ,message)
                fileOfCars.write('|'.join([j for j in i])+'\n')
        fileOfCars.close()