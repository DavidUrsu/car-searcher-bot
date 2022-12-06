# Car searcher BOT
## Introduction

On average, in the European Union, [80,000 second-hand cars are sold everyday](https://www.prnewswire.com/news-releases/european-used-car-market-analysis-report-2022-featuring-key-online-platforms---auto1-group-autoscout24-cazoo-reezocar--carvago-301597842.html) and the “best deals” resist just some hours on the internet until someone buys them. To get an offer like this, you should be lucky or spend countless hours on websites. An app that can do this thing for you will be a game changer if you want to buy a used car. The app will notify the user on his phone if a suitable deal is found.

The bot presented in this project can find the deals for the user from two car websites: [mobile.de](https://www.mobile.de) and [autoscout24.com](https://www.autoscout24.com).

## How to use

### Structure

The main code of the bot is located in main.py and the run of this file updates the cars.list file in which the already registered deals are located.

### Configuration

The user needs to update the config.ini file.

#### Websites
In the configuration file, the user needs to paste the search links from mobile.de or autoscout24 according to his desires. 

**Example**: If you want to be notified about a Volvo XC90, from 2018, with an automatic gearbox and no damage, you need to access mobile.de and search for the car with these parameters. Then it is mandatory to **sort the list by price from low to high** if you want to get the best results. After these steps, you need to copy the link from the search and paste it into the corresponding area of the configuration file. 

eg. In the config.ini file, the row for mobile.de should look like this:

mobile.de = https://www.mobile.de/ro/automobil/volvo-xc90/vhc:car,srt:price,sro:asc,ms1:25100_37_,frn:2018,ger:automatic_gear,dmg:false

#### Telegram configuration

The user can receive messages from the bot by initializing the conversation on Telegram. In the Telegram app, it needs to search for the bot in the search box by username @car_searcher_eu_bot. 

The user Telegram id also needs to be updated in the config.ini file. The user can find its id by following the steps from this [website](https://bigone.zendesk.com/hc/en-us/articles/360008014894-How-to-get-the-Telegram-user-ID-). After getting the id, it needs to update it in the configuration.


#### Maximum price

The maximum price is easy to set. The user just needs to change the alert-price variable in the configuration.

### Running the program

The program is intended to run periodically for its best performance.
The first time when the program runs it is doing a list with all the available cars at the moment and it does not notify the user about the cars. 

## The documentation is not complete! - 6 december 2022


Whenever the user wants to change the car it is looking for, it needs to empty the cars.list file.


