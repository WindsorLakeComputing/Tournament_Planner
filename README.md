# Tournament_Planner
The game tournament uses the Swiss system for pairing up players in each round: players are not eliminated, and each player is paired with another player with the same number of wins, or as close as possible.

The core of the database schema is the function playerStandings() found inside of tournament.sql. This function returns a list of the players and their win records, sorted by wins. Each row returned contains: id, name, number of wins, and number of matches played.
