#!/usr/bin/python3
#initialize odds table for nfl on RDS mysql instance through EC2 instance
"""
File name: make_table_nfl.py
Author: Matt Thimsen
Date Created: 7/15/2018
Python Version: 3.5.2
MySQL Version: 5.6.39
MySQL connector Version: 8.0
"""

import mysql.connector

cnx = mysql.connector.connect(user='', password='',
                            host= '',
                            database='')


cursor=cnx.cursor()

make_table=(
	"CREATE TABLE nfl_odds_table "
	"("
 	 "game_id		INT NOT NULL AUTO_INCREMENT, "
	 "home_team             VARCHAR(150) NOT NULL, "
 	 "away_team             VARCHAR(150) NOT NULL, "
 	 "away_score            VARCHAR(150) NOT NULL, "
 	 "home_score            VARCHAR(150) NOT NULL, "
 	 "game_state            VARCHAR(150) NOT NULL, "
 	 "home_moneyline        VARCHAR(150) NOT NULL, "
 	 "away_moneyline        VARCHAR(150) NOT NULL, "
	 "home_spread	        VARCHAR(150) NOT NULL, "
	 "away_spread	        VARCHAR(150) NOT NULL, "
	 "home_spread_odds	    VARCHAR(150) NOT NULL, "
	 "away_spread_odds	    VARCHAR(150) NOT NULL, "
	 "line	                VARCHAR(150) NOT NULL, "
	 "line_over_odds	    VARCHAR(150) NOT NULL, "
	 "line_under_odds	    VARCHAR(150) NOT NULL, "
 	 "PRIMARY KEY     (game_id) "
	");"
	)

cursor.execute(make_table)

cnx.commit()
cursor.close()
cnx.close()
