DROP TABLE IF EXISTS player;
CREATE TABLE IF NOT EXISTS player ( player_name NAME,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL PRIMARY KEY);

DROP TABLE IF EXISTS match;
CREATE TABLE IF NOT EXISTS match ( winner INTEGER references player(id),
                     loser INTEGER references player(id),
		     id SERIAL PRIMARY KEY);

CREATE VIEW view_defeats AS
SELECT p.id, coalesce(m.loser, 0)
FROM player p
LEFT JOIN match m
on p.id=m.winner
ORDER BY p.id;

--The following view was created by a Udacity coach:
CREATE VIEW standing AS
SELECT p.id as id, p.player_name as name, sum(case when p.id=m.winner then 1 else 0 end) as wins, count(m.winner) as matches
FROM player p
LEFT JOIN match m
ON p.id=m.winner OR p.id=m.loser
GROUP BY p.id
ORDER BY wins DESC, matches DESC;

--View every opponent that a player has competed against
CREATE VIEW view_total_opponents AS
--right column will only show the competitor regardless if he/she won or lost
SELECT p.id, (CASE WHEN (m.loser != p.id) THEN m.loser ELSE m.winner END) as opponent 
FROM player p
LEFT JOIN match m
on p.id=m.winner or p.id=m.loser
ORDER BY p.id ASC, opponent ASC;

--view the total amount of matches a player has played
CREATE VIEW view_total_matches AS
SELECT player, count(*) total_matches
from
(
	SELECT winner as player 
	FROM match
	--perform a union to obtain all values from the winner and loser columns
	UNION ALL
	SELECT loser
	FROM match
) a
GROUP BY player
ORDER BY player desc;

--list of tuples, each of which contain: player: the player's unique id (assigned by the database)
--name: the player's full name (as registered)
--wins: the number of matches the player has won
--total_matches: the number of matches the player has played
CREATE OR REPLACE FUNCTION playerStandings() 
         RETURNS TABLE (player integer, player_name name, wins bigint, total_matches bigint) AS $$
         BEGIN
	 --if a game has been played calc player stats, otherwise return 0 for # of wins and games played
         IF (SELECT count(*) FROM match) > 1 THEN
           	RETURN QUERY SELECT tm.player, p.player_name, coalesce(m.wins, 0), tm.total_matches
           	FROM ( 
                	SELECT winner, count(*) as wins
                	FROM match 
                	GROUP BY match.winner 
                      ) m RIGHT JOIN view_total_matches tm ON m.winner = tm.player 
		--get player name's
                JOIN player p on tm.player = p.id
                ORDER BY m.wins DESC NULLs LAST; 
        ELSE 
                RETURN QUERY SELECT player.id, player.player_name, CAST(0 AS BIGINT), CAST(0 AS BIGINT)  FROM player; 
        END IF; 
END
$$ LANGUAGE plpgsql; 
