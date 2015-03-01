DROP TABLE IF EXISTS player;
CREATE TABLE IF NOT EXISTS player ( player_name NAME,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL PRIMARY KEY);

DROP TABLE IF EXISTS match;
CREATE TABLE IF NOT EXISTS match ( winner INTEGER,
                     loser INTEGER,
		     id SERIAL PRIMARY KEY);
