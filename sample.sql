-- 1st Query
SELECT DISTINCT C.first_name,A.year, count(A.id) from movies A, movies_directors B, directors C 
where A.id = B.movie_id
and B.director_id = C.id 
and A.year > 1930
group by C.first_name, A.year
having count(B.movie_id) > 5;

EXPLAIN ANALYZE SELECT DISTINCT C.first_name,A.year, count(A.id) from movies A, movies_directors B, directors C 
where A.id = B.movie_id
and B.director_id = C.id 
and A.year > 1930
group by C.first_name, A.year
having count(B.movie_id) > 5;

CREATE INDEX test ON movies(id, year);
CREATE INDEX test1 ON directors(id,first_name);

drop index test;
drop index test1;

-- 2nd Query
EXPLAIN ANALYZE UPDATE movies SET availability = 'False', rating = 2.5 WHERE id = 13334;

CREATE INDEX test2 ON movies(id, availability);
CREATE INDEX test3 ON movies(id, rating);

drop index test2;
drop index test3;


-- 3rd Query
Explain Analyze select B.movie_id, c.name, c.rating, c.availability,c.year, A.last_name, A.gender from actors A
                    inner join roles B on A.id = B.actor_id
                    inner join movies c on B.movie_id = c.id
					where B.movie_id in (select movie_id from movies_genres where genre = 'Crime')
					and A.id in (select id from actors where gender = 'M');


CREATE INDEX test4 ON movies(id, name);
CREATE INDEX test5 ON movies(id, rating);
CREATE INDEX test6 ON movies(id, availability);
CREATE INDEX test7 ON movies(id, year);
CREATE INDEX test8 ON actors(id, gender);
CREATE INDEX test8 ON actors(id, last_name);



-- joining movies and actors
select B.movie_id, c.name, c.rating, d.genre, c.availability,c.year from actors A
                    inner join roles B on A.id = B.actor_id
                    inner join movies c on B.movie_id = c.id
                    inner join movies_genres d on b.movie_id = d.movie_id
                    where a.last_name = 'Adamyan'
					

-- List all indexes
select *
from pg_indexes
where tablename not like 'pg%';
