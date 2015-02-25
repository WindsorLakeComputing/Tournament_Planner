
CREATE TABLE player ( content NAME,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL );

CREATE TABLE match ( winner INTEGER,
                     loser INTEGER,
		     id SERIAL );
