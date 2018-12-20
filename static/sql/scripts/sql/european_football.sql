--
-- 1.0 Setup. Delete tables after every build iteration.
--
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS country, season, preferred_foot, player, league, player_attributes, 
  team, match_table, match_squad;
SET FOREIGN_KEY_CHECKS=1;

--
-- 2.0 ENTITIES
-- Serve as lookup tables
--

--
-- 2.1 country table
--
CREATE TABLE IF NOT EXISTS country (
  country_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  country_name VARCHAR(25) NOT NULL UNIQUE,
  PRIMARY KEY (country_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO country (country_name) VALUES
  ('Belgium'), ('England'), ('France'), ('Germany'), ('Italy'), 
  ('Netherlands'), ('Poland'), ('Portugal'), ('Scotland'), ('Spain'), ('Switzerland');

--
-- 2.2 season table
--
CREATE TABLE IF NOT EXISTS season (
  season_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  season_name VARCHAR(25) NOT NULL UNIQUE,
  PRIMARY KEY (season_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO season (season_name) VALUES
  ('2008/2009'), ('2009/2010'), ('2010/2011'), ('2011/2012'), ('2012/2013'), 
  ('2013/2014'), ('2014/2015'), ('2015/2016');

--
-- 2.3 preferred_foot table
--
CREATE TABLE IF NOT EXISTS preferred_foot (
  preferred_foot_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  preferred_foot_name VARCHAR(10) NOT NULL UNIQUE,
  PRIMARY KEY (preferred_foot_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO preferred_foot (preferred_foot_name) VALUES
  ('left'), ('right');

--
-- 2.4 player table
--
CREATE TABLE IF NOT EXISTS player (
  player_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  player_name VARCHAR(45) NOT NULL,
  birthday DATETIME NOT NULL,
  height FLOAT NOT NULL,
  weight FLOAT NOT NULL,
  api_id INTEGER NOT NULL UNIQUE,
  PRIMARY KEY (player_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/players_trimmed.csv'
INTO TABLE player
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (player_name, birthday, height, weight, api_id);

--
-- 2.5 league table
--
CREATE TABLE IF NOT EXISTS league
  (
    league_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    league_name VARCHAR(45) NOT NULL UNIQUE,
    country_id INTEGER NOT NULL,
    PRIMARY KEY (league_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id) ON DELETE RESTRICT ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Set FK variables and populate the sub_region table.
SET @fk_bel =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'Belgium'
  );
SET @fk_eng =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'England'
  );
SET @fk_fra =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'France'
  );
SET @fk_ger =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'Germany'
  );
SET @fk_ita =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'Italy'
  );
SET @fk_net =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'Netherlands'
  );
SET @fk_pol =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'Poland'
  );
SET @fk_por =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'Portugal'
  );
SET @fk_sco =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'Scotland'
  );
SET @fk_spa =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'Spain'
  );
SET @fk_swi =
  (
    SELECT country_id
    FROM country
    WHERE country_name = 'Switzerland'
  );

INSERT IGNORE INTO league (league_name, country_id) VALUES
  ('Belgium Jupiler League', @fk_bel),
  ('England Premier League', @fk_eng),
  ('France Ligue 1', @fk_fra),
  ('Germany 1. Bundesliga', @fk_ger),
  ('Italy Serie A', @fk_ita),
  ('Netherlands Eredivisie', @fk_net),
  ('Poland Ekstraklasa', @fk_pol),
  ('Portugal Liga ZON Sagres', @fk_por),
  ('Scotland Premier League', @fk_sco),
  ('Spain LIGA BBVA', @fk_spa),
  ('Switzerland Super League', @fk_swi);

--
-- 2.6 player_attributes table
--
CREATE TEMPORARY TABLE temp_player_attributes
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    api_id INTEGER NOT NULL,
    overall_rating INTEGER,
    potential INTEGER,
    preferred_foot VARCHAR(10),
    crossing INTEGER,
    finishing INTEGER,
    heading_accuracy INTEGER,
    short_passing INTEGER,
    volleys INTEGER,
    marking  INTEGER,
    standing_tackle INTEGER,
    sliding_tackle INTEGER,
    diving INTEGER,
    handling INTEGER,
    kicking INTEGER,
    positioning INTEGER,
    reflexes INTEGER,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/players_attrs_trimmed.csv'
INTO TABLE temp_player_attributes
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (api_id, overall_rating, potential, preferred_foot,
  crossing, finishing, heading_accuracy, short_passing, volleys,
  marking, standing_tackle, sliding_tackle, diving, handling, kicking,
  positioning, reflexes)

  SET overall_rating = IF(overall_rating = '', NULL, overall_rating),
  potential = IF(potential = '', NULL, potential),
  preferred_foot = IF(preferred_foot = '', NULL, preferred_foot),
  crossing = IF(crossing = '', NULL, crossing),
  finishing = IF(finishing = '', NULL, finishing),
  heading_accuracy = IF(heading_accuracy = '', NULL, TRIM(heading_accuracy)),
  short_passing = IF(short_passing = '', NULL, TRIM(short_passing)),
  volleys = IF(volleys = '', NULL, TRIM(volleys)),
  marking = IF(marking = '', NULL, TRIM(marking)),
  standing_tackle = IF(standing_tackle = '', NULL, TRIM(standing_tackle)),
  sliding_tackle = IF(sliding_tackle = '', NULL, TRIM(sliding_tackle)),
  diving = IF(diving = '', NULL, TRIM(diving)),
  handling = IF(handling = '', NULL, TRIM(handling)),
  kicking = IF(kicking = '', NULL, TRIM(kicking)),
  positioning = IF(positioning = '', NULL, TRIM(positioning)),
  reflexes = IF(reflexes = '', NULL, TRIM(reflexes));

CREATE TABLE IF NOT EXISTS player_attributes
  (
    player_attributes_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    player_id INTEGER NOT NULL,
    overall_rating INTEGER,
    potential INTEGER,
    preferred_foot_id INTEGER,
    crossing INTEGER,
    finishing INTEGER,
    heading_accuracy INTEGER,
    short_passing INTEGER,
    volleys INTEGER,
    marking INTEGER,
    standing_tackle INTEGER,
    sliding_tackle INTEGER,
    diving INTEGER,
    handling INTEGER,
    kicking INTEGER,
    positioning INTEGER,
    reflexes INTEGER,
    PRIMARY KEY (player_attributes_id), 
    FOREIGN KEY (player_id) REFERENCES player(player_id)
    ON DELETE RESTRICT ON UPDATE CASCADE, 
    FOREIGN KEY (preferred_foot_id) REFERENCES preferred_foot(preferred_foot_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO player_attributes (player_id, overall_rating, potential, preferred_foot_id,
       crossing, finishing, heading_accuracy, short_passing, volleys, marking, standing_tackle,
       sliding_tackle, diving, handling, kicking, positioning, reflexes)
SELECT p.player_id,
       tpa.overall_rating,
       tpa.potential,
       pf.preferred_foot_id,
       tpa.crossing,
       tpa.finishing,
       tpa.heading_accuracy,
       tpa.short_passing,
       tpa.volleys,
       tpa.marking,
       tpa.standing_tackle,
       tpa.sliding_tackle,
       tpa.diving,
       tpa.handling,
       tpa.kicking,
       tpa.positioning,
       tpa.reflexes
  FROM temp_player_attributes tpa
       LEFT JOIN player p
              ON tpa.api_id = p.api_id
       LEFT JOIN preferred_foot pf
              ON tpa.preferred_foot = pf.preferred_foot_name
 ORDER BY tpa.id;

DROP TEMPORARY TABLE temp_player_attributes;

--
-- 2.7 team table
--
CREATE TEMPORARY TABLE temp_team
  (
  	id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  	api_id INTEGER NOT NULL,
  	team_long_name VARCHAR(45) NOT NULL,
  	team_short_name VARCHAR(3) NOT NULL,
  	league_name VARCHAR(45) NOT NULL,
  	PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/teams_trimmed.csv'
INTO TABLE temp_team
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  (api_id, team_long_name, team_short_name, league_name);

CREATE TABLE IF NOT EXISTS team
  (
  	team_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  	team_long_name VARCHAR(45) NOT NULL UNIQUE,
  	team_short_name VARCHAR(3) NOT NULL UNIQUE,
  	league_id INTEGER NOT NULL, 
  	api_id INTEGER NOT NULL,
  	PRIMARY KEY (team_id), 
    FOREIGN KEY (league_id) REFERENCES league(league_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO team (team_long_name, team_short_name, league_id, api_id)
SELECT tt.team_long_name,
	   tt.team_short_name,
	   l.league_id, 
	   tt.api_id
  FROM temp_team tt
  	   LEFT JOIN league l
  	          ON tt.league_name = l.league_name
 ORDER BY tt.id;

 DROP TEMPORARY TABLE temp_team;

--
-- 2.8 team_attributes table
--
CREATE TEMPORARY TABLE temp_team_attributes
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    api_id INTEGER NOT NULL,
    play_speed INTEGER,
    play_passing INTEGER,
    chance_creation_passing INTEGER,
    chance_creation_crossing INTEGER,
    chance_creation_shooting INTEGER,
    defence_pressure INTEGER,
    defence_aggression INTEGER,
    defence_team_width INTEGER,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/team_attrs_trimmed.csv'
INTO TABLE temp_team_attributes
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (api_id, play_speed, play_passing, chance_creation_passing,
  chance_creation_crossing, chance_creation_shooting, defence_pressure, 
  defence_aggression, defence_team_width);

CREATE TABLE IF NOT EXISTS team_attributes
  (
    team_attributes_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    team_id INTEGER NOT NULL,
    play_speed INTEGER,
    play_passing INTEGER,
    chance_creation_passing INTEGER,
    chance_creation_crossing INTEGER,
    chance_creation_shooting INTEGER,
    defence_pressure INTEGER,
    defence_aggression INTEGER,
    defence_team_width INTEGER,
    PRIMARY KEY (team_attributes_id), 
    FOREIGN KEY (team_id) REFERENCES team(team_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO team_attributes (team_id, play_speed, play_passing, chance_creation_passing,
  chance_creation_crossing, chance_creation_shooting, defence_pressure, 
  defence_aggression, defence_team_width)
SELECT t.team_id,
       tta.play_speed,
       tta.play_passing,
       tta.chance_creation_passing,
       tta.chance_creation_crossing,
       tta.chance_creation_shooting,
       tta.defence_pressure,
       tta.defence_aggression,tta.defence_team_width
  FROM temp_team_attributes tta
       LEFT JOIN team t
              ON tta.api_id = t.api_id
 ORDER BY tta.id;

DROP TEMPORARY TABLE temp_team_attributes;

--
-- 2.7 match table
--
CREATE TEMPORARY TABLE temp_match
  (
  	id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  	season VARCHAR(25)  NOT NULL,
  	date DATETIME NOT NULL,
  	home_team_goal INTEGER NOT NULL,
  	away_team_goal INTEGER NOT NULL,
  	PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/match_trimmed.csv'
INTO TABLE temp_match
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (@dummy, season, date, home_team_goal, away_team_goal);

CREATE TABLE IF NOT EXISTS match_table
  (
  	match_table_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  	season_id INTEGER NOT NULL,
  	date DATETIME NOT NULL,
  	home_team_goal INTEGER NOT NULL,
  	away_team_goal INTEGER NOT NULL,
  	PRIMARY KEY (match_table_id), 
    FOREIGN KEY (season_id) REFERENCES season(season_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO match_table (season_id, date, home_team_goal, away_team_goal)
SELECT s.season_id,
	   tm.date,
	   tm.home_team_goal, 
	   tm.away_team_goal
  FROM temp_match tm
  	   LEFT JOIN season s
  	          ON tm.season = s.season_name
 ORDER BY tm.id;

DROP TEMPORARY TABLE temp_match;



CREATE TEMPORARY TABLE temp_match_squad
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    match_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    is_home_team TINYINT(1) NOT NULL,
    player_id INTEGER,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/match_squad_modified.csv'
INTO TABLE temp_match_squad
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  (match_id, team_id, is_home_team, player_id)

  SET player_id = IF(player_id = '', NULL, player_id);

CREATE TABLE IF NOT EXISTS match_squad
  (
  	match_squad_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  	match_id INTEGER NOT NULL,
  	team_id INTEGER NOT NULL,
  	is_home_team TINYINT(1) NOT NULL,
    player_id INTEGER,
    PRIMARY KEY (match_squad_id), 
    FOREIGN KEY (match_id) REFERENCES match_table(match_table_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (team_id) REFERENCES team(team_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (player_id) REFERENCES player(player_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO match_squad (match_id, team_id, is_home_team, player_id)
SELECT tms.match_id,
	   t.team_id,
	   tms.is_home_team, 
	   p.player_id
  FROM temp_match_squad tms
  	   LEFT JOIN team t
  	          ON tms.team_id = t.api_id
  	   LEFT JOIN player p
  	   		  ON tms.player_id = p.api_id
 ORDER BY tms.id;

DROP TEMPORARY TABLE temp_match_squad;

ALTER TABLE player
	DROP COLUMN api_id;

ALTER TABLE team
	DROP COLUMN api_id;