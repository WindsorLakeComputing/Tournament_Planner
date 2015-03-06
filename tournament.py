#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import re

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    sql = "truncate match; ALTER SEQUENCE id RESTART WITH 1; " 
    a_sql = ('TRUNCATE TABLE match '
            ' RESTART IDENTITY; ')
    c.execute(a_sql)
    db.commit()
    db.close() 

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    sql = ('truncate player; '
          'ALTER SEQUENCE player_id_seq RESTART WITH 1 '
          'OWNED BY player.id; ')
    a_sql = ('TRUNCATE TABLE player '
            ' RESTART IDENTITY; ')
    c.execute(a_sql)
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
    list_tups = []
    db = connect()
    c = db.cursor()
    sql = ('CREATE OR REPLACE FUNCTION playerStandings() '
           'RETURNS TABLE (player integer, player_name name, wins bigint, total_matches bigint) AS $$ '
           'BEGIN '
           'IF (SELECT count(*) FROM match) > 1 THEN '
           	'RETURN QUERY SELECT tm.player, p.player_name, m.wins, tm.total_matches '
           	'FROM ( '
                	'SELECT winner, count(*) as wins '
                	'FROM match '
                	'GROUP BY match.winner '
                	') m RIGHT JOIN view_total_matches tm ON m.winner = tm.player ' 
                'JOIN player p on tm.player = p.id '
                'ORDER BY m.wins DESC NULLs LAST; '
            'ELSE '
                  'RETURN QUERY SELECT player.id, player.player_name, CAST(0 AS BIGINT), CAST(0 AS BIGINT)  FROM player; '
            'END IF; '
            'END'
            '$$ LANGUAGE plpgsql; '
            'SELECT playerStandings(); ')
    a_sql=('SELECT tw.winner, sum(tw.wins + tl.loses) as total_games '
          'FROM view_total_wins tw, view_total_loses tl '
	  'WHERE tw.winner = tl.loser '
          'GROUP BY tw.winner; ')
    b_sql=('SELECT player, total_matches FROM view_total_matches;')
    c.execute(sql)
    results = c.fetchall()
    c_sql =('FETCH ALL IN \"<unnamed portal 1>\"; ')
    #results = c.execute(c_sql)
    print "results are ", results
    for result in results:
        print "the result has a length of ", len(result)
	tups = (str(result).split(",")[:4])
        print result
        print "tups len == ", len(tups)
        print "tups == ", tups
        list_tups.append(result)
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
	raise Exception("winner and loser must both be ints")
  
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
    calcPairs = []
    results = playerStandings()
    print "The results are ", results
    for i in xrange(0, len(results), 2):
	print(str(results[i]).split(',')[:2])
	
        calcPairs.append((removeChars(str(results[i])).split(',')[:2]))
	calcPairs.append((removeChars(str(results[i + 1])).split(',')[:2]))
	#d2, name2 = str(results[i + 1]).split(',')[:2]
	#pairs = (id1
        #print(results[i + 1])
    pairs = tuple(calcPairs)
    print "The pairs are ", pairs

def removeChars(aString):
    regex = re.compile('[^a-zA-Z0-9, ]')
    print "String being cleaned is ", aString
    cString = regex.sub('', aString)
    return cString


if __name__ == '__main__':
    registerPlayer("Ben Bush")
    registerPlayer("Calvin Hobbs")
    registerPlayer("Mister Rodgers")
    registerPlayer("Fred Penhar")
    #reportMatch(1,2)
    #reportMatch(3,4)
    #reportMatch(3,1)
    #playerStandings()
    swissPairings()
    deletePlayers()
    deleteMatches()
    print "player count is ", countPlayers()

