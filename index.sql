CREATE OR REPLACE FUNCTION movie_price()
RETURNS TRIGGER LANGUAGE plpgsql STRICT STABLE AS $$
BEGIN
  IF (
   NEW.price >= 0 or NEW.price is null
  ) THEN
    RETURN NEW;
  ELSE
    RAISE EXCEPTION 'Movie price cannot be negative (%)', NEW.price;
  END IF;
END;
$$;

CREATE OR REPLACE TRIGGER valid_movie_price
  BEFORE INSERT OR UPDATE
  ON movies
  FOR EACH ROW EXECUTE PROCEDURE movie_price();


CREATE OR REPLACE FUNCTION movie_rating()
RETURNS TRIGGER LANGUAGE plpgsql STRICT STABLE AS $$
BEGIN
  IF (
   NEW.rating >= 0 and NEW.rating <=10 or NEW.rating is null
  ) THEN
    RETURN NEW;
  ELSE
    RAISE EXCEPTION 'Movie rating should be between 0 to 10';
  END IF;
END;
$$;

CREATE OR REPLACE TRIGGER valid_movie_rating
  BEFORE INSERT OR UPDATE
  ON movies
  FOR EACH ROW EXECUTE PROCEDURE movie_rating();



CREATE OR REPLACE FUNCTION actor_gender()
RETURNS TRIGGER LANGUAGE plpgsql STRICT STABLE AS $$
BEGIN
  IF (
   NEW.gender in ('M','F','NB')
  ) THEN
    RETURN NEW;
  ELSE
    RAISE EXCEPTION 'Actor gender not in the database';
  END IF;
END;
$$;

CREATE OR REPLACE TRIGGER valid_actor_gender
  BEFORE INSERT OR UPDATE
  ON actors
  FOR EACH ROW EXECUTE PROCEDURE actor_gender();