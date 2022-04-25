-- Creating Tables

DROP TABLE IF EXISTS actors CASCADE;
CREATE TABLE actors (
  id int NOT NULL DEFAULT 0,
  first_name varchar(100) DEFAULT NULL,
  last_name varchar(100) DEFAULT NULL,
  gender char(1) DEFAULT NULL,
  PRIMARY KEY (id)
);
CREATE INDEX actors_first_name ON actors (first_name);
CREATE INDEX actors_last_name ON actors (last_name);

DROP TABLE IF EXISTS directors CASCADE;
CREATE TABLE directors (
  id int NOT NULL DEFAULT 0,
  first_name varchar(100) DEFAULT NULL,
  last_name varchar(100) DEFAULT NULL,
  PRIMARY KEY (id)
);
CREATE INDEX directors_first_name ON directors (first_name);
CREATE INDEX directors_last_name ON directors (last_name);

DROP TABLE IF EXISTS directors_genres CASCADE;
CREATE TABLE directors_genres (
  director_id int NOT NULL,
  genre varchar(100) NOT NULL,
  prob double precision DEFAULT NULL,
  PRIMARY KEY (director_id,genre)
 ,
  CONSTRAINT directors_genres_ibfk_1 FOREIGN KEY (director_id) 
  REFERENCES directors (id) ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS movies CASCADE;
CREATE TABLE movies (
  id int NOT NULL DEFAULT 0,
  name varchar(100) DEFAULT NULL,
  year int DEFAULT NULL,
  rating varchar(100) default NULL,
	availability varchar(100) default NULL,
  PRIMARY KEY (id)
);
CREATE INDEX movies_name ON movies (name);

DROP TABLE IF EXISTS movies_directors CASCADE;
CREATE TABLE movies_directors (
  director_id int NOT NULL,
  movie_id int NOT NULL,
  PRIMARY KEY (director_id,movie_id)
 ,
  CONSTRAINT movies_directors_ibfk_1 FOREIGN KEY (director_id) 
  REFERENCES directors (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT movies_directors_ibfk_2 FOREIGN KEY (movie_id) 
  REFERENCES movies (id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE INDEX movies_directors_director_id ON movies_directors (director_id);
CREATE INDEX movies_directors_movie_id ON movies_directors (movie_id);

DROP TABLE IF EXISTS movies_genres CASCADE;
CREATE TABLE movies_genres (
  movie_id int NOT NULL,
  genre varchar(100) NOT NULL,
  PRIMARY KEY (movie_id,genre)
 ,
  CONSTRAINT movies_genres_ibfk_1 FOREIGN KEY (movie_id) 
  REFERENCES movies (id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE INDEX movies_genres_movie_id ON movies_genres (movie_id);

DROP TABLE IF EXISTS roles CASCADE;
CREATE TABLE roles (
  actor_id int NOT NULL,
  movie_id int NOT NULL,
  role varchar(100),
  PRIMARY KEY (actor_id,movie_id)
 ,
  CONSTRAINT roles_ibfk_1 FOREIGN KEY (actor_id) REFERENCES actors (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT roles_ibfk_2 FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE INDEX actor_id ON roles (actor_id);
CREATE INDEX movie_id ON roles (movie_id);


-- Inseting Sample Records

INSERT INTO actors 
VALUES (524655,'1st Lt. Donald W.','Zautcke','M'),(745996,'Amy','Paisley','F'),(746143,'Amy','Palant','F'),
(746250,'Amy','Paliganoff','F'),(746397,'Amy','Palmer','F'),(748052,'Amy','Parks','F'),
(748112,'Amy','Parlow','F'),(748251,'Amy','Parrish','F'),(749772,'Amy','Pawlukiewicz','F'),
(750029,'Amy','Pearce','F'),(750122,'Amy','Pearson','F'),(750238,'Amy','Peck','F'),
(750303,'Amy','Peden','F'),(750843,'Amy','Pemberton','F'),(751460,'Amy','Perez','F'),
(751764,'Amy','Perna','F'),(751981,'Amy','Perry','F'),(752432,'Amy','Peters','F'),
(753275,'Amy','Pettigrew','F'),(753753,'Amy','Phillips','F'),(754060,'Amy','Piantaggini','F'),
(754225,'Amy','Pickering','F'),(754363,'Amy','Pierce','F'),(754573,'Amy','Pietz','F');

INSERT INTO directors
VALUES (1114,'A.','Aleksandrov'),(3728,'A.','Babes'),(4175,'A.','Balakrishnan'),
(4871,'A.','Barr-Smith'),(6779,'A.','Berry'),(7125,'A.','Bhimsingh'),(7494,'A.','Bistritsky'),
(8026,'A.','Bobrov'),(13355,'A.','Champeaux'),(13475,'A.','Chandrasekaran'),(17209,'A.','Cyran'),
(17424,'A.','Da'),(17332,'A.','Armentières'),(20602,'A.','Dolinov'),(20852,'A.','Dormenko'),
(21004,'A.','Douson'),(21880,'A.','Dvoretsky'),(26919,'A.','Galai'),(29797,'A.','Gosling'),
(30451,'A.','Gregorio'),(32103,'A.','Hameed'),(34552,'A.','Hingo'),(36125,'A.','Hussein'),
(36457,'A.','Ignatenko'),(37035,'A.','Ivonin'),(37343,'A.','Jagannathan');

-- Copying data from CSV Files
\copy movies FROM 'data/movies.csv' CSV header;
\copy actors FROM 'data/actors.csv' CSV header;
\copy directors FROM 'data/directors.csv' CSV header;
\copy directors_genres FROM 'data/directors_genres.csv' CSV header;
\copy movies_genres FROM 'data/movies_genres.csv' CSV header;


\copy movies_directors FROM 'data/movies_directors.csv' CSV header;
\copy roles FROM 'data/roles.csv' CSV header;

ALTER TABLE roles ALTER COLUMN role DROP NOT NULL;


select count(*) from movies;
select count(*) from directors;
select count(*) from actors;

select * from movies;