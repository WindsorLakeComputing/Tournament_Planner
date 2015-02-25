
CREATE TABLE player ( player_name NAME,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL PRIMARY KEY );

CREATE TABLE match ( winner INTEGER,
                     loser INTEGER,
		     id SERIAL PRIMARY KEY);
