
CREATE TABLE player ( content NAME,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL );

CREATE TABLE match ( WINNER character(1),
                     LOSER character(1),
		     id SERIAL );
