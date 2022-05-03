-- Get Number of rows
SELECT
    schemaname as table_schema, relname as table_name, n_live_tup as row_count
FROM
    pg_stat_user_tables
ORDER BY
    n_live_tup DESC;
	

-- Drop all tables
SELECT
  'DROP TABLE IF EXISTS "' || tablename || '" CASCADE;' 
from
  pg_tables WHERE schemaname = 'public';


EXPLAIN ANALYZE select B.movie_id, c.name, c.rating, d.genre, c.availability,c.year, A.last_name, f.last_name from actors A
inner join roles B on A.id = B.actor_id
inner join movies c on B.movie_id = c.id
inner join movies_genres d on b.movie_id = d.movie_id
inner join movies_directors e on b.movie_id = e.movie_id
inner join directors f on e.director_id = f.id
order by A.first_name ASC, f.first_name ASC, c.year DESC, d.genre ASC


CREATE INDEX movies_idx ON movies(id);
CREATE INDEX roles_movies_idx ON roles(movie_id);
CREATE INDEX roles_actors_idx ON roles(actor_id);
CREATE INDEX movies_genres_movies_idx ON movies_genres(movie_id);
CREATE INDEX movies_genres_genres_idx ON movies_genres(movie_id, genre);

drop index movies_genres_genres_idx;




select * from actors;