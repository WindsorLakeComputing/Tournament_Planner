DROP TABLE IF EXISTS player;
CREATE TABLE IF NOT EXISTS player ( player_name NAME,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL PRIMARY KEY);

DROP TABLE IF EXISTS match;
CREATE TABLE IF NOT EXISTS match ( winner INTEGER,
                     loser INTEGER,
		     id SERIAL PRIMARY KEY);

CREATE VIEW view_total_matches AS
SELECT player, count(*) total_matches
from
(
	SELECT winner as player 
	FROM match
	UNION ALL
	SELECT loser
	FROM match
) a
GROUP BY player
ORDER BY player desc;

CREATE OR REPLACE FUNCTION playerStandings() 
         RETURNS TABLE (player integer, player_name name, wins bigint, total_matches bigint) AS $$
         BEGIN
         IF (SELECT count(*) FROM match) > 1 THEN
           	RETURN QUERY SELECT tm.player, p.player_name, coalesce(m.wins, 0), tm.total_matches
           	FROM ( 
                	SELECT winner, count(*) as wins
                	FROM match 
                	GROUP BY match.winner 
                      ) m RIGHT JOIN view_total_matches tm ON m.winner = tm.player 
                JOIN player p on tm.player = p.id
                ORDER BY m.wins DESC NULLs LAST; 
        ELSE 
                RETURN QUERY SELECT player.id, player.player_name, CAST(0 AS BIGINT), CAST(0 AS BIGINT)  FROM player; 
        END IF; 
END
$$ LANGUAGE plpgsql; 
