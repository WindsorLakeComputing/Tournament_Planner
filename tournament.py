#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")
   
def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    sql = truncateSQL("match") 
    c.execute(sql)
    db.commit()
    db.close() 

def truncateSQL(tableName):
    """Create the SQL to truncate a table"""
    sql = "TRUNCATE TABLE %s RESTART IDENTITY CASCADE; " % tableName
    return sql

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    sql = truncateSQL("player")
    c.execute(sql)
    db.commit()
    db.close() 

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    sql = "select count(*) from player"  
    c.execute(sql)
    result = c.fetchone()
    db.commit()
    db.close()
    return result[0] 

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    attrs = {
    '*': ['style']
    }
    tags = ['p', 'em', 'strong']
    styles = ['color', 'font-weight'] 
    cleaned_text = bleach.clean(name, tags, attrs, styles)
    db = connect()
    c = db.cursor()
    sql = "insert into player (player_name) values (%s)"
    args = (cleaned_text,)
    c.execute(sql, args)
    db.commit()
    db.close()    
     

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    sql =('SELECT * from playerStandings(); ')
    c.execute(sql)
    results = c.fetchall()
    db.commit()
    db.close()
    return results 

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    if isinstance(winner, int) and isinstance(loser, int):
    	db = connect()
    	c = db.cursor()
    	sql = ('INSERT INTO match (winner, loser) values (%s, %s); ')
    	c.execute(sql, (winner, loser))
    	db.commit()
    	db.close()
    else:
	raise Exception("winner and loser must both be of type int")
 
def totalOpponents():
    """Returns a Dict of players and every opponent faced.
 
       Returns: 
        A Dict consisting of a player's id as the key, and
       a list of player id's of the opponents the player has faced as the value.
    """
    tot_opponents = {}  
    db = connect()
    c = db.cursor()
    sql = ('SELECT * FROM view_total_opponents;')	
    c.execute(sql)
    r = c.fetchall()
    db.commit()
    db.close()

    for i in r:
        plyr = i[0]
        opp = i[1]
        if tot_opponents.get(plyr):
		#Add to the list of opponents already faced
		opps = tot_opponents.get(plyr)
                opps.append(opp)
	else:
		tot_opponents[plyr] = [opp]
    return tot_opponents

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairs = []
    results = playerStandings()
    tot_opponents = totalOpponents()    

    for i in xrange(0, (len(results) / 2)):
	opps = tot_opponents.get(results[i][0])
	#if true then player results[i+ 1][0] has already played with results[i]
        #will check next playeys in standings until find one haven't played yet. 
 	if (results[i + 1][0] in opps):
		for inner in range(i + 2, len(results)):
			#if true, then found a player who hasn't played current one.
			if results[inner][0] not in opps:
				pairs.append((results[i][0],results[i][1], results[inner][0], results[inner][1]))
				#delete player that has just been matched to avoid scheduling 2 matches with
				#same player
				del[results[inner]]
				break
	else:
       		pairs.append((results[i][0],results[i][1], results[i +1][0], results[i + 1][1]))
		del[results[i + 1]] 
    return pairs
