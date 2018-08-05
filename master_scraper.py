#!/usr/bin/python3
"""This script contains two functions that work together to scrape the action 
network for sports odds data. The first function returns the data for a 
specific sport in the form of a list of dicts, each dict contain info about a 
single game. The second function simply loops through the different sports 
while calling the first function to get data on each sport. The second function 
returns a single dict with each entry being the list of dicts on all sports. 
The drivers for these functions are controlled by the controller, and passed 
to the functions as an argument."""
"""
File name: master_scraper.py
Author: Matt Thimsen
Date Created: 7/10/2018
Python Version: 3.5.2
Selenium Version: 3.11.0
Geckodriver Version: 0.21.0
FireFox Version: 61.0.1
"""
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

#this function scrapes odds for whichever sport on the sports tab is selected
def sport_scrape(driver):

    #click the moneyline tab
    xpath='//*[@id="__next"]/div/main/div/div/div[2]/ul[1]/li[4]/a'
    driver.find_element_by_xpath(xpath).click()

    #this list will hold dicts (one for each game) with the following keys:
    """home_team,    away_team,       home_moneyline,    away_moneyline,    
       home_spread,  away_spread ,    home_spread_odds,  away_spread_odds,    
       line,         line_over_odds,  line_under_odds
    """
    sport_odds=[]

    #----------GET TEAM NAMES-------------------------------------------------#
    #get each card with team names
    xpath="//*[starts-with(@class, 'border-top pt')]"
    gameCards = driver.find_elements_by_xpath(xpath)

    #go through each card and get the team abbreviations, game state, and score
    for card in gameCards:
        xpath=".//*[starts-with(@class, 'font-weight-semi')]"
        teamAbs=card.find_elements_by_xpath(xpath)
        #here we add both team names to each game dict
        game={}
        count=1
        for teamAb in teamAbs:
            if count==1:
                game['away_team']=teamAb.text
            else:
                game['home_team']=teamAb.text
            count=count+1

        game_state_elements=[]
        #try to get score (doesnt always exist because games not always on)
        try:
            #get the score elements

            xpath=".//*[starts-with(@class, 'font-weight-bold ml')]"
            score_elements=card.find_elements_by_xpath(xpath)
            #update the dict with the score
            game['away_score']=score_elements[0].text
            game['home_score']=score_elements[1].text
        #if we can't get score just feed empty strings
        except:
            game['away_score']=''
            game['home_score']=''

        #----------BUILD THE GAME STATE---------------------------------------#
        #try to get the start time
        try:
            #find element(s) containing the time (can be one or two, or 0)
            xpath=".//*[starts-with(@class, 'd-inline-block mr-')]"
            time_elements=card.find_elements_by_xpath(xpath)
            time_string=''
            for elem in time_elements:
                if time_string=='':
                    time_string=time_string + elem.text
                else:
                    time_string=time_string + ' ' + elem.text
            #if we didnt get any time string intentionally trigger except 
            if time_string=='':
                a=1/0
            #if its a fine time, update the game state
            game['game_state']=time_string
        #if i can't get the start time, try to get that the game if final
        except:
            try:
                #find element showing game is final
                xpath=".//*[starts-with(@class, 'd-block fz-1 fz-md-2 pt-')]"
                final_element=card.find_element_by_xpath(xpath)
                game['game_state']=final_element.text
            #if neither of these work, game is in progress
            except:
                game['game_state']='In Progress'

        #append the results to sport_odds
        sport_odds.append(game)


    #----------GET DATA FROM MONEYLINE TAB------------------------------------#
    #  xpath samples for infoCards:
    #
    #/html/body/div[1]/div/main/div/div/div[3]/div/table/tbody/tr[1]
    #/html/body/div[1]/div/main/div/div/div[3]/div/table/tbody/tr[2]
    #/html/body/div[1]/div/main/div/div/div[3]/div/table/tbody/tr[10]
    game_count=0

    #go through each infoCard containing info from each game and extract stuff
    for num in range(1,len(gameCards)+1):
        #build each xpath
        xpath=("/html/body/div[1]/div/main/div/div/div[3]/div/table/tbody/tr[" 
               + str(num) + "]")

        #get the infocard
        infoCard=driver.find_element_by_xpath(xpath)
        #select the 'current' card and get numbers from it
        xpath="(.//*[@class='text-right'])[2]"
        currentCard=infoCard.find_element_by_xpath(xpath)
        xpath=".//*[starts-with(@class, 'd-block ')]"
        currentNums=currentCard.find_elements_by_xpath(xpath)
        #predefine a dict to hold the moneyline data we get
        moneyline_nums={}
        """go through two current nums (one for each team) and add the data to 
        our spread dict"""
        count=1
        for num in currentNums:
            if count==1:
                moneyline_nums['away_moneyline']=num.text
            else:
                moneyline_nums['home_moneyline']=num.text
            count=count+1

        #add new entries from spread to each game by combining the dicts
        sport_odds[game_count]={**sport_odds[game_count], **moneyline_nums}
        #increment game count
        game_count=game_count+1

    #----------GET DATA FROM SPREAD TAB---------------------------------------#
    game_count=0
    #change to spread tab
    driver.find_element_by_xpath("/html/body/div[1]/div/main/div/"
                                 "div/div[2]/ul[1]/li[2]/a").click()

    #go through each infoCard containing info from each game and extract stuff
    for num in range(1,len(gameCards)+1):
        infoCard=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/"
                                              "div/div[3]/div/table/tbody/tr[" 
                                              + str(num) + "]")
        #select the 'current' card and get numbers from it
        currentCard=infoCard.find_element_by_xpath("(.//*[@class="
                                                   "'text-right'])[2]")
        currentNums=currentCard.find_elements_by_xpath(".//*[starts-with"
                                                       "(@class, 'd-block ')]")

        #predefine a dict to hold the spread data we get
        spread_nums={}

        """go through two current nums (one for each team) and add the 
        home_spread and away_spread to our spread dict"""
        count=1
        for num in currentNums:
            if count==1:
                spread_nums['away_spread']=num.text.split(' ')[0]
                spread_nums['away_spread_odds']=num.text.split(' ')[1]
            else:
                spread_nums['home_spread']=num.text.split(' ')[0]
                spread_nums['home_spread_odds']=num.text.split(' ')[1]
            count+=1

        #add new entries from spread to each game by combining the dicts
        sport_odds[game_count]={**sport_odds[game_count], **spread_nums}
        #increment game count
        game_count=game_count+1


    #this logic here is when the action network has no hosted odds
    no_odds=[{'home_spread': '--', 
              'home_spread_odds': '--', 
              'away_team': 'STL', 
              'home_team': 'CHC', 
              'home_moneyline': '--', 
              'away_moneyline': '--', 
              'away_spread': '--', 
              'away_spread_odds': '--'}]

    if sport_odds==no_odds:
        #return empty list to clear sql TABLE
        """TODO: might be better to trigger a scrape somewhere else, this could
        be a problem"""
        return []

    #----------GET DATA FROM TOTAL TAB----------------------------------------#
    #click the total tab
    driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[2]/"
                                 "ul[1]/li[3]/a").click()
    game_count=0
    #go through each infoCard containing info from each game and extract stuff
    for num in range(1,len(gameCards)+1):
        infoCard=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/"
                                              "div/div[3]/div/table/tbody/tr[" 
                                              + str(num) + "]")

        #select the 'current' card and get numbers from it
        currentCard=infoCard.find_element_by_xpath("(.//*[@class"
                                                   "='text-right'])[2]")
        currentNums=currentCard.find_elements_by_xpath(".//*[starts-with"
                                                       "(@class, 'd-block ')]")
        #predefine a dict to hold the total data we get
        total_nums={}
        #first number in currentNums is line
        total_nums['line']=currentNums[0].text.split(' ')[0]

        """go through two current nums (one for each team) and add the 
        line_over_odds and line_under_odds to our total dict"""
        count=1
        for num in currentNums:
            try:
                if count ==1:
                    total_nums['line_over_odds']=num.text.split(' ')[1]
                else:
                    total_nums['line_under_odds']=num.text
                count+=1
            # this exception is needed because an index error will be 
            # triggered if there are no displayed odds here
            except IndexError:
                if count ==1:
                    total_nums['line_over_odds']='--'
                else:
                    total_nums['line_under_odds']='--'
                count+=1


        #add new entries from spread to each game by combining the dicts
        sport_odds[game_count]={**sport_odds[game_count], **total_nums}
        #increment game count
        game_count=game_count+1

    print(sport_odds)
    return sport_odds

"""this function calls the sports_scrape function in a manner that retrieves 
all data from the action network"""
def masterScrape(driver):
    #predifine a dict to contain all action network odds
    all_odds={}
    #----

    #start the driver by scraping the first page that pops up (mlb odds)
    all_odds['mlb_odds']=sport_scrape(driver)
    #find the menu of sports and get the link to each one
    sport_menu=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/"
                                            "div/div[1]/ul")
    sport_links=sport_menu.find_elements_by_xpath(".//*[starts-with(@class, "
                                                  "'pointer text-muted ')]")
    """using the opened driver go through each link, get the odds and put them 
    into the dict in a labled manner"""
    count=1
    for link in sport_links:
        link.click()
        if count==1:
            all_odds['ncaab_odds']=sport_scrape(driver)
        if count==2:
            all_odds['nfl_odds']=sport_scrape(driver)
        if count==3:
            all_odds['nba_odds']=sport_scrape(driver)
        if count==4:
            all_odds['nhl_odds']=sport_scrape(driver)
        count+=1

    return all_odds
