-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE Player (
  id   SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

INSERT INTO Player (name) VALUES ('Michael');
INSERT INTO Player (name) VALUES ('Lindsay');
INSERT INTO Player (name) VALUES ('Gavin');
INSERT INTO Player (name) VALUES ('Ryan');
INSERT INTO Player (name) VALUES ('Geoff');
INSERT INTO Player (name) VALUES ('Jack');

CREATE TABLE Match (
  id          SERIAL PRIMARY KEY,
  playerOneID INT REFERENCES Player (id) NOT NULL,
  playerTwoID INT REFERENCES Player (id) NOT NULL
);

CREATE TABLE Win (
  id       SERIAL PRIMARY KEY,
  matchID  INT REFERENCES Match (id) ON DELETE CASCADE  NOT NULL,
  playerID INT REFERENCES Player (id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE Lose (
  id       SERIAL PRIMARY KEY,
  matchID  INT REFERENCES Match (id)  ON DELETE CASCADE NOT NULL,
  playerID INT REFERENCES Player (id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE Draw (
  id          SERIAL PRIMARY KEY,
  matchID     INT REFERENCES Match (id)  ON DELETE CASCADE NOT NULL,
  playerOneID INT REFERENCES Player (id) ON DELETE CASCADE NOT NULL,
  playerTwoID INT REFERENCES Player (id) ON DELETE CASCADE NOT NULL
);

INSERT INTO Match (playerOneID, playerTwoID) VALUES (1, 2);
INSERT INTO Match (playerOneID, playerTwoID) VALUES (1, 2);
INSERT INTO Match (playerOneID, playerTwoID) VALUES (1, 2);
INSERT INTO Match (playerOneID, playerTwoID) VALUES (2, 3);
INSERT INTO Match (playerOneID, playerTwoID) VALUES (1, 2);
INSERT INTO Match (playerOneID, playerTwoID) VALUES (1, 2);
INSERT INTO Match (playerOneID, playerTwoID) VALUES (1, 2);

INSERT INTO Win (matchID, playerID) VALUES (2, 1);
INSERT INTO Win (matchID, playerID) VALUES (3, 2);
INSERT INTO Win (matchID, playerID) VALUES (4, 3);
INSERT INTO Win (matchID, playerID) VALUES (5, 1);
INSERT INTO Win (matchID, playerID) VALUES (6, 1);
INSERT INTO Win (matchID, playerID) VALUES (7, 2);

INSERT INTO Lose (matchID, playerID) VALUES (2, 2);
INSERT INTO Lose (matchID, playerID) VALUES (3, 1);
INSERT INTO Lose (matchID, playerID) VALUES (4, 2);

INSERT INTO Draw (matchID, playerOneID, playerTwoID) VALUES (1, 1, 2);



