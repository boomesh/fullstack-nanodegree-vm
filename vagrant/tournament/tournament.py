#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def clearTable(tableName):
    DB = connect()
    cursor = DB.cursor()
    cursor.execute('delete from ' + tableName + ';')
    DB.commit()
    cursor.close()
    DB.close()


def deleteMatches():
    """Remove all the match records from the database."""
    clearTable('Match')


def deletePlayers():
    """Remove all the player records from the database."""
    clearTable('Player')


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute('select count(id) from Player;')
    totalPlayers = cursor.fetchone()[0]
    cursor.close()
    DB.close()
    return totalPlayers


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cursor = DB.cursor()
    name = bleach.clean(name)
    cursor.execute('insert into Player (name) values (%s);', (name,))
    DB.commit()
    playerID = cursor.execute('select id from Player where name = %s', (name,))
    cursor.close()
    DB.close()
    return playerID


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
    DB = connect()
    cursor = DB.cursor()
    result = cursor.execute(
        'select playerid, winners.name, wins, matches from (select Player.id, name, count(*) as matches from Match JOIN Player ON Player.id = Match.playerOneID OR Player.id = Match.playerTwoID GROUP BY Player.id, name) as match JOIN (select playerid, name, count(playerid) as wins from Win JOIN Player ON Win.playerid = Player.id  GROUP BY Win.playerid, name) as winners ON playerid = id ORDER BY wins DESC;')
    # select * from (select playertwoid as id, count(playertwoid) as matches from Match group by playertwoid) as player_2 JOIN (select playeroneid as id, count(playeroneid) as matches from Match group by playeroneid) as player_1 ON player_2.id = player_1.id;
    # WINS
    # select playerid, name, count(playerid) as wins from Win JOIN Player ON Win.playerid = Player.id  GROUP BY Win.playerid, name;
    # TOTAL MATCHES
    # select Player.id, name, count(*) as matches from Match JOIN Player ON Player.id = Match.playerOneID OR Player.id = Match.playerTwoID GROUP BY Player.id, name;
    # FULL QUERY
    # select playerid, winners.name, wins, matches from (select Player.id, name, count(*) as matches from Match JOIN Player ON Player.id = Match.playerOneID OR Player.id = Match.playerTwoID GROUP BY Player.id, name) as match JOIN (select playerid, name, count(playerid) as wins from Win JOIN Player ON Win.playerid = Player.id  GROUP BY Win.playerid, name) as winners ON playerid = id ORDER BY wins DESC;

    print result
    players = []
    if result is not None:
        players = result.fetchall()
        print '=='
        print str(players)
        print '=='

    cursor.close()
    DB.close()
    return players


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """


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
