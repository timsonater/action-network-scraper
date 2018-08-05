#!/usr/bin/python3
"""This script controls the use of both the webscraper and the CRUD 
applications that update the SQL database. The driver_start and exit_handler 
functions ensure that the driver starts up and shuts down correctly. 
exit_handler also ensures that mysql connections are closed appropriatly. The 
primary while True loop controls scrapes theactionnetwork.com at a randomly 
generated interval, handling any errors that occur along the way. Errors and 
success's are logged in files named error_log.txt and success_log.txt 
respectively."""
"""
File name: controller.py
Author: Matt Thimsen
Date Created: 7/16/2018
Python Version: 3.5.2
Selenium Version: 3.11.0
Geckodriver Version: 0.21.0
FireFox Version: 61.0.1
MySQL Version: 5.6.39
MySQL connector Version: 8.0
"""

import atexit
import traceback
from datetime import datetime
from random import randint
import time
import mysql.connector
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import master_scraper
import sql_odds_sync
master_scraper
#----------SET MYSQL CONNECTER LOGIN AND TARGET DATABASE----------------------#
cnx = mysql.connector.connect(user='', password='',
                            host= '',
                            database='')
cursor=cnx.cursor()

#----------CONFIGURE FIREFOX--------------------------------------------------#
#these variables controll the way firefox is launced
headless=True
img_load=False

#make a function that starts the drivers
def driver_start(headless, img_load):
    #setup options so that we can run firefox headless if needed
    options = Options()
    if headless==True:
        options.set_headless(headless=True)
    if img_load == False:
        #get a speed increase by not downloading images
        flash_permission='dom.ipc.plugins.enabled.libflashplayer.so'
        img_permission='permissions.default.image'
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference(img_permission, 2)
        firefox_profile.set_preference(flash_permission, 'false')
        driver=webdriver.Firefox(firefox_options=options,
                                 firefox_profile=firefox_profile)
        return driver
    else:
        driver=webdriver.Firefox(firefox_options=options)
        return driver

#start the drivers
driver=driver_start(headless, img_load)

#----------ENSURE PROPER SHUTDOWN ON EXIT-------------------------------------#
#ensures cursure, cnx, and driver close on script termination 
"""(this function is often redundent and will error as a result but exists as 
a precautionary measure)"""
def exit_handler(cursor, cnx, driver):
    cursor.close()
    cnx.close()
    driver.close()
#pass function and its arguments to atexit
atexit.register(exit_handler, cursor=cursor, cnx=cnx, driver=driver)

#----------SCRAPE AND PUSH ODDS TO THE DATABASE-------------------------------#

#this function sets an appropriate random wait period between paige reloads
def smart_sleep():
    sleep_time=randint(15,32)
    time.sleep(sleep_time)


while True:
    try:
        #go to the action network
        driver.get('https://www.actionnetwork.com/mlb/live-odds')
        #scrape all odds and dump into a database
        odds=master_scraper.masterScrape(driver)
        sql_odds_sync.mlb_sync(odds['mlb_odds'], cnx, cursor)
        sql_odds_sync.ncaab_sync(odds['ncaab_odds'], cnx, cursor)
        sql_odds_sync.nfl_sync(odds['nfl_odds'], cnx, cursor)
        sql_odds_sync.nba_sync(odds['nba_odds'], cnx, cursor)
        sql_odds_sync.nhl_sync(odds['nhl_odds'], cnx, cursor)
        #log successful scrape
        with open('success_log.txt', 'a') as f:
            f.write('Scrape errorless\n')
            f.write(str(datetime.now())+'\n')
        #sleep
        smart_sleep()

    
    # due to a bug in current version of selenium & geckodriver, broken pipe 
    # errors are intermittent, ignore them
    except BrokenPipeError:
        pass

    #in case the browser closes for whatever reason we need to restart it 
    except selenium.common.exceptions.SessionNotCreatedException:
        print('error')
        driver=driver_start(headless, img_load)
    except selenium.common.exceptions.NoSuchWindowException:
        print('error')
        driver=driver_start(headless, img_load)

    #all other exceptions are logged
    except Exception as e:
        """
        TODO: selenium.common.exceptions.WebDriverException: Message: Failed to 
        decode response from marionette 

        that error requires a full wait before a reload to fix, can be done 
        quicker but exception needs to reference specific error message as 
        WebDriverException does not nessecarily mean the browser has closed. 
        Extremely rare anyway.

        TODO: implement a timeout (seleniums built in is 300 sec and that 
        doesnt cut it (too long))
        """
        print('error')
        #define odds to avoid reference error
        mlb_odds=None
        #log the error
        with open('error_log.txt', 'a') as f:
            f.write(str(datetime.now()))
            f.write(str(e))
            f.write(traceback.format_exc())
        #sleep
        smart_sleep()
        
            

    

