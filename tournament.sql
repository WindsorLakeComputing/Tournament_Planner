DROP TABLE IF EXISTS player;
CREATE TABLE IF NOT EXISTS player ( player_name NAME,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL PRIMARY KEY);

DROP TABLE IF EXISTS match;
CREATE TABLE IF NOT EXISTS match ( winner INTEGER,
                     loser INTEGER,
		     id SERIAL PRIMARY KEY);

CREATE VIEW view_total_wins AS
SELECT match.winner, count(match.winner) as wins 
FROM match 
GROUP BY match.winner 
ORDER BY wins desc;

CREATE VIEW view_total_loses AS
SELECT match.loser, count(match.loser) as loses 
FROM match 
GROUP BY match.loser 
ORDER BY loses desc;

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
