from unittest import result
import psycopg2
from flask import Flask, request, render_template, redirect, url_for
import os
import yaml

app = Flask(__name__)

def connectdb():
    conn = psycopg2.connect(
        host="localhost",
        database="IMDB_Milestone1",
        user='postgres',
        password='Srinivas@047')
    return conn

def get_movieDetails(sql, val):
    conn = connectdb()
    cur = conn.cursor()
    cur.execute(sql, val)

    details = cur.fetchall()

    return details

# Initialization
@app.route('/',methods=('GET', 'POST'))
def Initialize():
    conn = connectdb()
    cur = conn.cursor()
    cur.execute('SELECT distinct last_name from actors LIMIT 1000')
    actorslastnames = cur.fetchall()

    cur.execute('SELECT DISTINCT C.first_name from movies A, movies_directors B, directors C where A.id = B.movie_id and B.director_id = C.id group by C.first_name having count(B.movie_id) > 5 LIMIT 1000')
    directorslastnames = cur.fetchall()

    cur.execute("SELECT distinct year from movies where rating is not NULL LIMIT 1000")
    moviesyear = cur.fetchall()

    cur.execute('SELECT distinct genre from movies_genres LIMIT 1000')
    movies_genres = cur.fetchall()

    cur.execute("SELECT * from movies where rating is not NULL order by rating DESC LIMIT 100;")
    movies = cur.fetchall()
    # print(movies[:5])

    # print(actorslastnames[:5])

    actordetails = []
    for i in actorslastnames:
        actordetails.append(i[0])
    
    directordetails = []
    for i in directorslastnames:
        directordetails.append(i[0])
    
    movies_genresdetails = []
    for i in moviesyear:
        movies_genresdetails.append(i[0])
    
    genredetails = []
    for i in movies_genres:
        genredetails.append(i[0])

    return render_template('index.html', moviedetails=movies, actordetails=actordetails, directordetails=directordetails, movies_genresdetails=movies_genresdetails, genredetails=genredetails,)

# Renting a Movie
@app.route('/rent', methods=('GET', 'POST'))
def rent():
    if request.method == 'POST':
        movieID = request.form['movieID']
        conn = connectdb()
        cur = conn.cursor()
        sql = "UPDATE movies SET availability = 'False' WHERE id = %s"
        val = (movieID,)
        cur.execute(sql, val)
        conn.commit()

        return "Movie Rented Successfully!!"

# Getting Movie Details
@app.route('/getdetails', methods=('GET', 'POST'))
def getdetails():
    if request.method == 'POST':
        
        movieID = request.form['movieID']
        conn = connectdb()
        cur = conn.cursor()
        sql = "SELECT * from movies where id = %s" 
        val = (movieID,)
        cur.execute(sql, val)
        moviedetails = cur.fetchall()

        return render_template('GetDetails.html', moviedetails=moviedetails)

# Sell a Movie
@app.route("/sell", methods=['POST'])
def sell():
    if request.method == 'POST':

        moviename = request.form['moviename']
        year = request.form['year']
        # genre = request.form['genre']
        rating = request.form['rating']
        price = request.form['price']
        availability = 'True'

        # actorfname = request.form['actorfname']
        # actorlname = request.form['actorlname']
        # actorgender = request.form['actorgender']
        # actorrole = request.form['actorrole']
        # directorfname = request.form['directorfname']
        # directorlname = request.form['directorlname']
    
        conn = connectdb()
        cur = conn.cursor()
        # cur.execute("INSERT INTO actors (actorID, actorfname, actorlname, id) VALUES (%s, %s, %s, %s)")

        # Inserting Movie
        sql1 = "INSERT INTO movies (name, year, rating, availability, price) VALUES (%s, %s, %s, %s, %s)"
        val1 = (moviename, year, rating, availability, price)
        cur.execute(sql1, val1)

        conn.commit()


        # sql2 = "SELECT id from movies where name= %s and year = %s and rating = %s and availability = %s and price = %s"
        # val2 = (moviename, year, rating, availability, price)
        # cur.execute(sql2, val2)

        # conn.commit()

    return "Movie Added Successfully!!"

# Get Recommendations
# Need to Complete
@app.route('/recommendations', methods=('GET', 'POST'))
def recommendations():
    if request.method == 'POST':
        actor_name = request.form['actor']
        director_name = request.form['director']
        year = request.form['year']
        genre = request.form['genre']

        if actor_name == "" and director_name == "" and year == "" and genre == "":
            sql = "SELECT M.id, M.name, M.rating, G.genre, M.availability, M.year from movies M, movies_genres G where M.id = G.movie_id and rating is not NULL and rating >= '7.5' order by rating DESC LIMIT 5"  

            conn = connectdb()
            cur = conn.cursor()
            cur.execute(sql)
            TopMovies = cur.fetchall()
            return render_template('TopMovies.html', TopMovies=TopMovies)

        if actor_name != "" and director_name != "":
            sql = "select M.id, M.name, M.rating, G.genre, M.availability, M.year from movies M, movies_genres G,  where M.id = G.movie_id  and rating is not NULL and genre = %s and M.year = %s order by rating DESC LIMIT 5" 
            val = (genre,year)

            TopMovies = get_movieDetails(sql, val)
        return render_template('TopMovies.html', TopMovies=TopMovies)

# Get Top Five Directors
@app.route("/TopfiveDirectors", methods=['POST'])
def TopfiveDirectors():
    if request.method == 'POST':
        first_name = request.form['director']
        conn = connectdb()
        cur = conn.cursor() 
        sql = "SELECT A.*, B.director_id, C.first_name, C.last_name from movies A, movies_directors B, directors C where A.id = B.movie_id and B.director_id = C.id and rating is not NULL and C.first_name = %s order by A.rating DESC LIMIT 5"
        val = (first_name,)
        cur.execute(sql, val)
        TopfiveDirectors = cur.fetchall()
        # print(TopfiveDirectors[:5])

        return render_template('TopDirectors.html', TopfiveDirectors=TopfiveDirectors)

# Get Top Five Movies of a Genre
@app.route("/TopfiveMovies", methods=['POST'])
def TopfiveMovies():
    if request.method == 'POST':
        genre = request.form['genres']
        conn = connectdb()
        cur = conn.cursor() 

        sql = "select M.id, M.name, M.rating, G.genre, M.availability,M.year from movies M, movies_genres G where M.id = G.movie_id  and rating is not NULL and genre = %s order by rating DESC"
        val = (genre,)
        cur.execute(sql, val)
        TopMovies = cur.fetchall()
        TopMovies = TopMovies[:5]

        return render_template('TopMovies.html', TopMovies=TopMovies)

# Update tables
@app.route("/update", methods=['POST'])
def update():
    if request.method == 'POST':

        # actorID = request.form['actorID']
        # actorfname = request.form['actorfname']

        directorID = request.form['directorID']
        directorlname = request.form['directorlname']

        movieID = request.form['movieID']
        movieRating = request.form['movieRating']
    
        conn = connectdb()
        cur = conn.cursor()
        # cur.execute("INSERT INTO actors (actorID, actorfname, actorlname, id) VALUES (%s, %s, %s, %s)")

        # if actorID != "" or actorfname !="":
        #     sql1 = "UPDATE actors SET first_name = %s WHERE id = %s"
        #     val1 = (actorfname, actorID)
        #     cur.execute(sql1, val1)

        if directorID != "" or directorlname !="":
            sql2 = "UPDATE directors SET last_name = %s WHERE id = %s"
            val2 = (directorlname, directorID)
            cur.execute(sql2, val2)

        if movieID != "" or movieRating !="":
            sql3 = "UPDATE movies SET rating = %s WHERE id = %s"
            val3 = (movieRating, movieID)
            cur.execute(sql3, val3)

        conn.commit()

    return "Details Updated Successfully!!"

# Delete a Movie
@app.route("/delete", methods=['POST'])
def delete():
    if request.method == 'POST':

        movieID = request.form['movieID']    
        conn = connectdb()
        cur = conn.cursor()

        sql = "DELETE FROM movies WHERE id = %s"
        val = (movieID,)
        cur.execute(sql, val)
        conn.commit()

    return "Deleted Successfully!!"

if __name__ == "__main__":
  app.run('0.0.0.0', port=5001, debug=True)