DROP SEQUENCE IF EXISTS actors_id_seq CASCADE;
DROP SEQUENCE IF EXISTS directors_id_seq CASCADE;
DROP SEQUENCE IF EXISTS movies_id_seq CASCADE;

DROP TABLE IF EXISTS actors CASCADE;
CREATE TABLE actors (
  id SERIAL NOT NULL,
  first_name varchar(100) NOT NULL,
  last_name varchar(100) NOT NULL,
  gender char(1) DEFAULT NULL,
  PRIMARY KEY (id) 
);
 
DROP TABLE IF EXISTS directors CASCADE;
CREATE TABLE directors (
  id SERIAL NOT NULL,
  first_name varchar(100) NOT NULL,
  last_name varchar(100) NOT NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS directors_genres CASCADE;
CREATE TABLE directors_genres (
  director_id int NOT NULL,
  genre varchar(100) NOT NULL,
  prob double precision DEFAULT NULL,
  PRIMARY KEY (director_id,genre),
  CONSTRAINT directors_genres_ibfk_1 FOREIGN KEY (director_id) 
  REFERENCES directors (id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS movies CASCADE;
CREATE TABLE movies (
  id SERIAL NOT NULL,
  name varchar(100) NOT NULL,
  year int DEFAULT NULL,
  rating float default NULL,
  availability boolean DEFAULT FALSE,
  price int default NULL,
  PRIMARY KEY (id)
);

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

DROP TABLE IF EXISTS movies_genres CASCADE;
CREATE TABLE movies_genres (
  movie_id int NOT NULL,
  genre varchar(100) NOT NULL,
  PRIMARY KEY (movie_id,genre),
  CONSTRAINT movies_genres_ibfk_1 FOREIGN KEY (movie_id) 
  REFERENCES movies (id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS roles CASCADE;
CREATE TABLE roles (
  actor_id int NOT NULL,
  movie_id int NOT NULL,
  role varchar(100) NOT NULL,
  PRIMARY KEY (actor_id,movie_id,role)
 ,
  CONSTRAINT roles_ibfk_1 FOREIGN KEY (actor_id) REFERENCES actors (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT roles_ibfk_2 FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- SEQUENCES

-- DROP SEQUENCE IF EXISTS actors_id_seq CASCADE;
-- DROP SEQUENCE IF EXISTS directors_id_seq CASCADE;
-- DROP SEQUENCE IF EXISTS movies_id_seq CASCADE;

-- CREATE SEQUENCE actors_id_seq
-- START 1
-- INCREMENT 1
-- MINVALUE 1
-- OWNED BY actors.id;

-- CREATE SEQUENCE directors_id_seq
-- START 1
-- INCREMENT 1
-- MINVALUE 1
-- OWNED BY directors.id;

-- CREATE SEQUENCE movies_id_seq
-- START 1
-- INCREMENT 1
-- MINVALUE 1
-- OWNED BY movies.id;