#!/usr/bin/python3
"""This file containes a series of functions intended to be called on by the 
controller. There is one function for every sport. Each function takes in the 
data list generated by the scraper, and uses it to update the SQL database to 
reflect the inputted data. The database is updated in a specific way so that 
tables are never cleared (unless there is no data), rather deleted games are 
removed, new ones added and current ones updated."""
"""
File name: sql_odds_sync.py
Author: Matt Thimsen
Date Created: 7/16/2018
Python Version: 3.5.2
MySQL Version: 5.6.39
MySQL connector Version: 8.0
"""

import mysql.connector

#=============================================================================#
#==============================MLB SYNC=======================================#
#=============================================================================#
def mlb_sync(odds, cnx, cursor):

    #get all currently stored data in table in the form of a list
    cursor.execute("SELECT * FROM mlb_odds_table;")
    current_data = cursor.fetchall()

    #----------PREDIFINE SOME SQL COMMANDS------------------------------------#
    #command to update the table, everywhere both team names match
    update = ("UPDATE mlb_odds_table "
        "SET "
        "home_moneyline = '%s', "
        "away_moneyline = '%s', "
        "home_score = '%s', "
        "away_score = '%s', "
        "game_state = '%s', "
        "home_spread = '%s', "
        "away_spread = '%s', "
        "home_spread_odds = '%s', "
        "away_spread_odds = '%s', "
        "line = '%s', "
        "line_over_odds = '%s', "
        "line_under_odds = '%s' "
        "WHERE "
        "home_team = '%s' and away_team = '%s';"
        )
    #enter the game into table
    insert = ("INSERT INTO mlb_odds_table ( home_team, away_team, "
         "home_score, away_score, game_state, "
         "home_moneyline, away_moneyline, home_spread, "
         "away_spread, home_spread_odds, away_spread_odds, "
         "line, line_over_odds, line_under_odds) VALUES "
         "( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"
         )
    #delete a game

    delete = ("DELETE FROM mlb_odds_table WHERE "
              "home_team = '%s' and away_team = '%s';")

    #----------IF THE ODDS LIST IS EMPTY CLEAR THE TABLE----------------------#
    if odds == None:
        cursor.execute("TRUNCATE TABLE mlb_odds_table")
        cnx.commit()
        return

    #----------UPDATE CURRENT GAMES, DELETE GAMES THAT DON'T EXIST------------#

    """predefine list off all scraped games, which we will use to fund 
    unmatched games by removing those that are matched"""
    unmatched_games=odds

    for stored_game in current_data:
        #set a variable to signal game deletion
        delete_game=True
        for scraped_game in odds:
            #if the teams playing match
            if (
                stored_game[1]==scraped_game['home_team'] and 
                stored_game[2]==scraped_game['away_team']
                ):

                row_update=(update % (scraped_game['home_moneyline'],
                            scraped_game['away_moneyline'],
                            scraped_game['home_score'],
                            scraped_game['away_score'],
                            scraped_game['game_state'],
                            scraped_game['home_spread'],
                            scraped_game['away_spread'],
                            scraped_game['home_spread_odds'],
                            scraped_game['away_spread_odds'],
                            scraped_game['line'],
                            scraped_game['line_over_odds'],
                            scraped_game['line_under_odds'],
                            scraped_game['home_team'],
                            scraped_game['away_team']
                            ))
                cursor.execute(row_update)
                cnx.commit()
                #remove the game from unmatched_games
                unmatched_games.remove(scraped_game)
                #signal that deleting a stored game is not needed
                delete_game=False
                #break the loop
                break
        #delete the stored game if it does not exist in the scraped data.
        if delete_game==True:
            delete_attempt = (delete % (stored_game[1],stored_game[2]))

            cursor.execute(delete_attempt)
            cnx.commit()

    #----------ADDS GAMES THAT ARE NOT IN DATABASE----------------------------#
    #go through each unmatched game and add it to
    for game in unmatched_games:
        cursor.execute(insert, (game['home_team'],
                    game['away_team'],
                    game['home_score'],
                    game['away_score'],
                    game['game_state'],
                    game['home_moneyline'],
                    game['away_moneyline'],
                    game['home_spread'],
                    game['away_spread'],
                    game['home_spread_odds'],
                    game['away_spread_odds'],
                    game['line'],
                    game['line_over_odds'],
                    game['line_under_odds']
                    ))
        cnx.commit()


#=============================================================================#
#==============================NFL SYNC=======================================#
#=============================================================================#
def nfl_sync(odds, cnx, cursor):

    #get all currently stored data in table in the form of a list
    cursor.execute("SELECT * FROM nfl_odds_table;")
    current_data = cursor.fetchall()

    #----------PREDIFINE SOME SQL COMMANDS------------------------------------#
    #command to update the table, everywhere both team names match
    update = ("UPDATE nfl_odds_table "
        "SET "
        "home_moneyline = '%s', "
        "away_moneyline = '%s', "
        "home_score = '%s', "
        "away_score = '%s', "
        "game_state = '%s', "
        "home_spread = '%s', "
        "away_spread = '%s', "
        "home_spread_odds = '%s', "
        "away_spread_odds = '%s', "
        "line = '%s', "
        "line_over_odds = '%s', "
        "line_under_odds = '%s' "
        "WHERE "
        "home_team = '%s' and away_team = '%s';"
        )
    #enter the game into table
    insert = ("INSERT INTO nfl_odds_table ( home_team, away_team, "
         "home_score, away_score, game_state, "
         "home_moneyline, away_moneyline, home_spread, "
         "away_spread, home_spread_odds, away_spread_odds, "
         "line, line_over_odds, line_under_odds) VALUES "
         "( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"
         )
    #delete a game
    delete = ("DELETE FROM nfl_odds_table WHERE "
              "home_team = '%s' and away_team = '%s';")

    #----------IF THE ODDS LIST IS EMPTY CLEAR THE TABLE----------------------#
    if odds == None:
        cursor.execute("TRUNCATE TABLE nfl_odds_table")
        cnx.commit()
        return

    #----------UPDATE CURRENT GAMES, DELETE GAMES THAT DON'T EXIST------------#
    
    """predefine list off all scraped games, which we will use to fund 
    unmatched games by removing those that are matched"""
    unmatched_games=odds


    for stored_game in current_data:
        #set a variable to signal game deletion
        delete_game=True
        for scraped_game in odds:
            #if the teams playing match
            if (
                stored_game[1]==scraped_game['home_team'] and 
                stored_game[2]==scraped_game['away_team']
                ):
                
                row_update=(update % (scraped_game['home_moneyline'],
                            scraped_game['away_moneyline'],
                            scraped_game['home_score'],
                            scraped_game['away_score'],
                            scraped_game['game_state'],
                            scraped_game['home_spread'],
                            scraped_game['away_spread'],
                            scraped_game['home_spread_odds'],
                            scraped_game['away_spread_odds'],
                            scraped_game['line'],
                            scraped_game['line_over_odds'],
                            scraped_game['line_under_odds'],
                            scraped_game['home_team'],
                            scraped_game['away_team']
                            ))
                cursor.execute(row_update)
                cnx.commit()
                #remove the game from unmatched_games
                unmatched_games.remove(scraped_game)
                #signal that deleting a stored game is not needed 
                delete_game=False
                #break the loop
                break
        #delete the stored game if it does not exist in the scraped data.
        if delete_game==True:
            delete_attempt = (delete % (stored_game[1],stored_game[2]))
            cursor.execute(delete_attempt)
            cnx.commit()

    #----------ADDS GAMES THAT ARE NOT IN DATABASE----------------------------#
    #go through each unmatched game and add it to
    for game in unmatched_games:
        cursor.execute(insert, (game['home_team'],
                    game['away_team'],
                    game['home_score'],
                    game['away_score'],
                    game['game_state'],
                    game['home_moneyline'],
                    game['away_moneyline'],
                    game['home_spread'],
                    game['away_spread'],
                    game['home_spread_odds'],
                    game['away_spread_odds'],
                    game['line'],
                    game['line_over_odds'],
                    game['line_under_odds']
                    ))
        cnx.commit()


#=============================================================================#
#==============================NHL SYNC=======================================#
#=============================================================================#
def nhl_sync(odds, cnx, cursor):

    #get all currently stored data in table in the form of a list
    cursor.execute("SELECT * FROM nhl_odds_table;")
    current_data = cursor.fetchall()

    #----------PREDIFINE SOME SQL COMMANDS------------------------------------#
    #command to update the table, everywhere both team names match
    update = ("UPDATE nhl_odds_table "
        "SET "
        "home_moneyline = '%s', "
        "away_moneyline = '%s', "
        "home_score = '%s', "
        "away_score = '%s', "
        "game_state = '%s', "
        "home_spread = '%s', "
        "away_spread = '%s', "
        "home_spread_odds = '%s', "
        "away_spread_odds = '%s', "
        "line = '%s', "
        "line_over_odds = '%s', "
        "line_under_odds = '%s' "
        "WHERE "
        "home_team = '%s' and away_team = '%s';"
        )
    #enter the game into table
    insert = ("INSERT INTO nhl_odds_table ( home_team, away_team, "
         "home_score, away_score, game_state, "
         "home_moneyline, away_moneyline, home_spread, "
         "away_spread, home_spread_odds, away_spread_odds, "
         "line, line_over_odds, line_under_odds) VALUES "
         "( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"
         )
    #delete a game
    delete = ("DELETE FROM nhl_odds_table WHERE "
              "home_team = '%s' and away_team = '%s';")

    #----------IF THE ODDS LIST IS EMPTY CLEAR THE TABLE----------------------#
    if odds == None:
        cursor.execute("TRUNCATE TABLE nhl_odds_table")
        cnx.commit()
        return

    #----------UPDATE CURRENT GAMES, DELETE GAMES THAT DON'T EXIST------------#
    """predefine list off all scraped games, which we will use to fund 
    unmatched games by removing those that are matched"""
    unmatched_games=odds

    for stored_game in current_data:
        #set a variable to signal game deletion
        delete_game=True
        for scraped_game in odds:

            #if the teams playing match
            if (
                stored_game[1]==scraped_game['home_team'] and 
                stored_game[2]==scraped_game['away_team']
                ):

                row_update=(update % (scraped_game['home_moneyline'],
                            scraped_game['away_moneyline'],
                            scraped_game['home_score'],
                            scraped_game['away_score'],
                            scraped_game['game_state'],
                            scraped_game['home_spread'],
                            scraped_game['away_spread'],
                            scraped_game['home_spread_odds'],
                            scraped_game['away_spread_odds'],
                            scraped_game['line'],
                            scraped_game['line_over_odds'],
                            scraped_game['line_under_odds'],
                            scraped_game['home_team'],
                            scraped_game['away_team']
                            ))
                cursor.execute(row_update)
                cnx.commit()
                #remove the game from unmatched_games
                unmatched_games.remove(scraped_game)
                #signal that deleting a stored game is not needed
                delete_game=False
                #break the loop
                break
        #delete the stored game if it does not exist in the scraped data.
        if delete_game==True:
            delete_attempt = (delete % (stored_game[1],stored_game[2]))
            cursor.execute(delete_attempt)
            cnx.commit()

    #----------ADDS GAMES THAT ARE NOT IN DATABASE----------------------------#
    #go through each unmatched game and add it to
    for game in unmatched_games:
        cursor.execute(insert, (game['home_team'],
                    game['away_team'],
                    game['home_score'],
                    game['away_score'],
                    game['game_state'],
                    game['home_moneyline'],
                    game['away_moneyline'],
                    game['home_spread'],
                    game['away_spread'],
                    game['home_spread_odds'],
                    game['away_spread_odds'],
                    game['line'],
                    game['line_over_odds'],
                    game['line_under_odds']
                    ))
        cnx.commit()


#=============================================================================#
#==============================NBA SYNC=======================================#
#=============================================================================#
def nba_sync(odds, cnx, cursor):

    #get all currently stored data in table in the form of a list
    cursor.execute("SELECT * FROM nba_odds_table;")
    current_data = cursor.fetchall()

    #----------PREDIFINE SOME SQL COMMANDS------------------------------------#
    #command to update the table, everywhere both team names match
    update = ("UPDATE nba_odds_table "
        "SET "
        "home_moneyline = '%s', "
        "away_moneyline = '%s', "
        "home_score = '%s', "
        "away_score = '%s', "
        "game_state = '%s', "
        "home_spread = '%s', "
        "away_spread = '%s', "
        "home_spread_odds = '%s', "
        "away_spread_odds = '%s', "
        "line = '%s', "
        "line_over_odds = '%s', "
        "line_under_odds = '%s' "
        "WHERE "
        "home_team = '%s' and away_team = '%s';"
        )
    #enter the game into table
    insert = ("INSERT INTO nba_odds_table ( home_team, away_team, "
         "home_score, away_score, game_state, "
         "home_moneyline, away_moneyline, home_spread, "
         "away_spread, home_spread_odds, away_spread_odds, "
         "line, line_over_odds, line_under_odds) VALUES "
         "( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"
         )
    #delete a game
    delete = ("DELETE FROM nba_odds_table WHERE "
              "home_team = '%s' and away_team = '%s';")

    #----------IF THE ODDS LIST IS EMPTY CLEAR THE TABLE----------------------#
    if odds == None:
        cursor.execute("TRUNCATE TABLE nba_odds_table")
        cnx.commit()
        return

    #----------UPDATE CURRENT GAMES, DELETE GAMES THAT DON'T EXIST------------#
    """predefine list off all scraped games, which we will use to fund 
    unmatched games by removing those that are matched"""
    unmatched_games=odds


    for stored_game in current_data:
        #set a variable to signal game deletion
        delete_game=True
        for scraped_game in odds:
            #if the teams playing match
            if (
                stored_game[1]==scraped_game['home_team'] and 
                stored_game[2]==scraped_game['away_team']
                ):

                row_update=(update % (scraped_game['home_moneyline'],
                            scraped_game['away_moneyline'],
                            scraped_game['home_score'],
                            scraped_game['away_score'],
                            scraped_game['game_state'],
                            scraped_game['home_spread'],
                            scraped_game['away_spread'],
                            scraped_game['home_spread_odds'],
                            scraped_game['away_spread_odds'],
                            scraped_game['line'],
                            scraped_game['line_over_odds'],
                            scraped_game['line_under_odds'],
                            scraped_game['home_team'],
                            scraped_game['away_team']
        					))
                cursor.execute(row_update)
                cnx.commit()
                #remove the game from unmatched_games
                unmatched_games.remove(scraped_game)
                #signal that deleting a stored game is not needed
                delete_game=False
                #break the loop
                break
        #delete the stored game if it does not exist in the scraped data.
        if delete_game==True:
            delete_attempt = (delete % (stored_game[1],stored_game[2]))
            cursor.execute(delete_attempt)
            cnx.commit()

    #----------ADDS GAMES THAT ARE NOT IN DATABASE----------------------------#
    #go through each unmatched game and add it to
    for game in unmatched_games:
        cursor.execute(insert, (game['home_team'],
                    game['away_team'],
                    game['home_score'],
                    game['away_score'],
                    game['game_state'],
                    game['home_moneyline'],
                    game['away_moneyline'],
                    game['home_spread'],
                    game['away_spread'],
                    game['home_spread_odds'],
                    game['away_spread_odds'],
                    game['line'],
                    game['line_over_odds'],
                    game['line_under_odds']
                    ))
        cnx.commit()

#=============================================================================#
#============================NCAAB SYNC=======================================#
#=============================================================================#
def ncaab_sync(odds, cnx, cursor):

    #get all currently stored data in table in the form of a list
    cursor.execute("SELECT * FROM ncaab_odds_table;")
    current_data = cursor.fetchall()

    #----------PREDIFINE SOME SQL COMMANDS------------------------------------#
    #command to update the table, everywhere both team names match
    update = ("UPDATE ncaab_odds_table "
        "SET "
        "home_moneyline = '%s', "
        "away_moneyline = '%s', "
        "home_score = '%s', "
        "away_score = '%s', "
        "game_state = '%s', "
        "home_spread = '%s', "
        "away_spread = '%s', "
        "home_spread_odds = '%s', "
        "away_spread_odds = '%s', "
        "line = '%s', "
        "line_over_odds = '%s', "
        "line_under_odds = '%s' "
        "WHERE "
        "home_team = '%s' and away_team = '%s';"
        )
    #enter the game into table
    insert = ("INSERT INTO ncaab_odds_table ( home_team, away_team, "
         "home_score, away_score, game_state, "
         "home_moneyline, away_moneyline, home_spread, "
         "away_spread, home_spread_odds, away_spread_odds, "
         "line, line_over_odds, line_under_odds) VALUES "
         "( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"
         )
    #delete a game
    delete = ("DELETE FROM ncaab_odds_table WHERE "
              "home_team = '%s' and away_team = '%s';")

    #----------IF THE ODDS LIST IS EMPTY CLEAR THE TABLE----------------------#
    if odds == None:
        cursor.execute("TRUNCATE TABLE ncaab_odds_table")
        cnx.commit()
        return

    #----------UPDATE CURRENT GAMES, DELETE GAMES THAT DON'T EXIST------------#
    """predefine list off all scraped games, which we will use to fund 
    unmatched games by removing those that are matched"""
    unmatched_games=odds

    for stored_game in current_data:
        #set a variable to signal game deletion
        delete_game=True
        for scraped_game in odds:
            #if the teams playing match

            if (
                stored_game[1]==scraped_game['home_team'] and 
                stored_game[2]==scraped_game['away_team']
                ):

                row_update=(update % (scraped_game['home_moneyline'],
        					scraped_game['away_moneyline'],
                            scraped_game['home_score'],
                            scraped_game['away_score'],
                            scraped_game['game_state'],
        					scraped_game['home_spread'],
        					scraped_game['away_spread'],
        					scraped_game['home_spread_odds'],
        					scraped_game['away_spread_odds'],
        					scraped_game['line'],
        					scraped_game['line_over_odds'],
        					scraped_game['line_under_odds'],
        					scraped_game['home_team'],
                            scraped_game['away_team']
        					))
                cursor.execute(row_update)
                cnx.commit()
                #remove the game from unmatched_games
                unmatched_games.remove(scraped_game)
                #signal that deleting a stored game is not needed
                delete_game=False
                #break the loop
                break
        #delete the stored game if it does not exist in the scraped data.
        if delete_game==True:
            delete_attempt = (delete % (stored_game[1],stored_game[2]))
            cursor.execute(delete_attempt)
            cnx.commit()

    #----------ADDS GAMES THAT ARE NOT IN DATABASE----------------------------#
    #go through each unmatched game and add it to
    for game in unmatched_games:
        cursor.execute(insert, (game['home_team'],
                    game['away_team'],
                    game['home_score'],
                    game['away_score'],
                    game['game_state'],
                    game['home_moneyline'],
                    game['away_moneyline'],
                    game['home_spread'],
                    game['away_spread'],
                    game['home_spread_odds'],
                    game['away_spread_odds'],
                    game['line'],
                    game['line_over_odds'],
                    game['line_under_odds']
                    ))
        cnx.commit()
