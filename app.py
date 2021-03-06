from enum import unique
from unittest import result
import psycopg2
from flask import Flask, request, render_template, redirect, url_for
import os
import numpy as np
import yaml

app = Flask(__name__)

def connectdb():
    conn = psycopg2.connect(
        host="localhost",
        database="DMQL_Milestone2",
        user='postgres',
        password='Srinivas@047')
    return conn

def get_queryResults(sql, val):
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
    cur.execute(""" select A.last_name from actors A
                    inner join roles B on A.id = B.actor_id
                    inner join movies c on B.movie_id = c.id
                    inner join movies_genres d on b.movie_id = d.movie_id
                    inner join movies_directors e on b.movie_id = e.movie_id
                    inner join directors f on e.director_id = f.id
                    order by A.first_name ASC, f.first_name ASC, c.year DESC, d.genre ASC
                    LIMIT 1000 """)
    actorslastnames1 = cur.fetchall()

    actorslastnames = []
    for item in actorslastnames1:
         if item not in actorslastnames:
             actorslastnames.append(item)


    cur.execute(""" select f.last_name from actors A
                    inner join roles B on A.id = B.actor_id
                    inner join movies c on B.movie_id = c.id
                    inner join movies_genres d on b.movie_id = d.movie_id
                    inner join movies_directors e on b.movie_id = e.movie_id
                    inner join directors f on e.director_id = f.id
                    order by A.first_name ASC, f.first_name ASC, c.year DESC, d.genre ASC
                    LIMIT 1000 """)
    directorslastnames1 = cur.fetchall()

    directorslastnames = []
    for item in directorslastnames1:
         if item not in directorslastnames:
             directorslastnames.append(item)


    cur.execute("""SELECT DISTINCT C.first_name from movies A, movies_directors B, directors C 
                    where A.id = B.movie_id and B.director_id = C.id group by C.first_name 
                    having count(B.movie_id) > 5 LIMIT 1000""")
    Topdirectordetails1 = cur.fetchall()

    cur.execute("""select c.year from actors A
                    inner join roles B on A.id = B.actor_id
                    inner join movies c on B.movie_id = c.id
                    inner join movies_genres d on b.movie_id = d.movie_id
                    inner join movies_directors e on b.movie_id = e.movie_id
                    inner join directors f on e.director_id = f.id
                    order by A.first_name ASC, f.first_name ASC, c.year DESC, d.genre ASC
                    LIMIT 1000""")
    moviesyear1 = cur.fetchall()

    moviesyear = []
    for item in moviesyear1:
         if item not in moviesyear:
             moviesyear.append(item)

    cur.execute("""select d.genre from actors A
                    inner join roles B on A.id = B.actor_id
                    inner join movies c on B.movie_id = c.id
                    inner join movies_genres d on b.movie_id = d.movie_id
                    inner join movies_directors e on b.movie_id = e.movie_id
                    inner join directors f on e.director_id = f.id
                    order by A.first_name ASC, f.first_name ASC, c.year DESC, d.genre ASC
                    LIMIT 1000""")
    movies_genres1 = cur.fetchall()

    movies_genres = []
    for item in movies_genres1:
         if item not in movies_genres:
             movies_genres.append(item)

    cur.execute("SELECT * from movies where rating is not NULL and availability = 'True' order by rating DESC LIMIT 100;")
    movies = cur.fetchall()

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
    
    Topdirectordetails = []
    for i in Topdirectordetails1:
        Topdirectordetails.append(i[0])

    return render_template('index.html', moviedetails=movies, Topdirectordetails = Topdirectordetails, actordetails=actordetails, directordetails=directordetails, movies_genresdetails=movies_genresdetails, genredetails=genredetails,)

# Renting a Movie
@app.route('/rent', methods=('GET', 'POST'))
def rent():
    if request.method == 'POST':
        movieID = request.form['movieID']


        sql1 = "select availability from movies WHERE id = %s"
        val1 = (movieID,)
        availability =  get_queryResults(sql1, val1)[0][0]

        if availability == False:
            return "Movie is already rented!!"
        else:
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
        sql = "SELECT * from movies where id = %s" 
        val = (movieID,)
        moviedetails = get_queryResults(sql, val)
        return render_template('GetDetails.html', moviedetails=moviedetails)

@app.route('/purchaseHistory', methods=('GET', 'POST'))
def purchaseHistory():
    if request.method == 'POST':
        conn = connectdb()
        cur = conn.cursor()
        sql = "SELECT * from purchase_history" 
        cur.execute(sql)
        purchaseHistory = cur.fetchall()

        return render_template('purchaseHistory.html', purchaseHistory=purchaseHistory)

# Sell a Movie
@app.route("/sell", methods=['POST'])
def sell():
    if request.method == 'POST':
        moviename = request.form['moviename']
        year = request.form['year']
        rating = request.form['rating']
        price = request.form['price']
        availability = 'True'
    
        conn = connectdb()
        cur = conn.cursor()

        # Inserting Movie
        sql1 = "INSERT INTO movies (name, year, rating, availability, price) VALUES (%s, %s, %s, %s, %s)"
        val1 = (moviename, year, rating, availability, price)
        cur.execute(sql1, val1)
        conn.commit()

    return "Movie Added Successfully!!"

# Get Recommendations
@app.route('/recommendations', methods=('GET', 'POST'))
def recommendations():
    if request.method == 'POST':
        actor_name = request.form['actor']
        director_name = request.form['director']
        year = request.form['year']
        genre = request.form['genre']

        if actor_name == "" and director_name == "" and year == "" and genre == "":
            print("blank")
            sql = """SELECT M.id, M.name, M.rating, G.genre, M.availability, M.year 
            from movies M, movies_genres G where M.id = G.movie_id 
            and rating is not NULL and rating >= '7.5' order by rating DESC LIMIT 5""" 

            conn = connectdb()
            cur = conn.cursor()
            cur.execute(sql)
            TopMovies = cur.fetchall()
            return render_template('TopMovies.html', TopMovies=TopMovies)

        elif actor_name != "" and director_name != "" and year != "" and genre != "":
            print("All")
            sql = """select B.movie_id, c.name, c.rating, d.genre, c.availability,c.year from actors A
                    inner join roles B on A.id = B.actor_id
                    inner join movies c on B.movie_id = c.id
                    inner join movies_genres d on b.movie_id = d.movie_id
                    inner join movies_directors e on b.movie_id = e.movie_id
                    inner join directors f on e.director_id = f.id
                    where d.genre = %s
                    and a.last_name = %s
                    and c.year = %s
                    and f.last_name = %s """
            val = (genre, actor_name, year,director_name)
            TopMovies = get_queryResults(sql, val)

        elif actor_name != "" and director_name != "" and year == "" and genre == "":
            print("Actor Director")
            sql = """select B.movie_id, c.name, c.rating, d.genre, c.availability,c.year from actors A
                    inner join roles B on A.id = B.actor_id
                    inner join movies c on B.movie_id = c.id
                    inner join movies_genres d on b.movie_id = d.movie_id
                    inner join movies_directors e on b.movie_id = e.movie_id
                    inner join directors f on e.director_id = f.id
                    where a.last_name = %s
                    and f.last_name = %s """
            val = (actor_name, director_name)
            TopMovies = get_queryResults(sql, val)

        elif actor_name != "" and director_name == "" and year == "" and genre == "":
            print("Only Actor")
            sql = """select B.movie_id, c.name, c.rating, d.genre, c.availability,c.year from actors A
                    inner join roles B on A.id = B.actor_id
                    inner join movies c on B.movie_id = c.id
                    inner join movies_genres d on b.movie_id = d.movie_id
                    where a.last_name = %s"""
            val = (actor_name,)
            TopMovies = get_queryResults(sql, val)

        elif director_name != "" and actor_name == "" and year == "" and genre == "":
            print("Only Director")
            sql = """select c.id, c.name, c.rating, d.genre, c.availability,c.year from movies c
                    inner join movies_genres d on c.id = d.movie_id
                    inner join movies_directors e on c.id = e.movie_id
                    inner join directors f on e.director_id = f.id
                    where f.last_name = %s """
            val = (director_name,)
            TopMovies = get_queryResults(sql, val)
        
        elif director_name != "" and genre != "" and actor_name == "" and year == "":
            print("Director Genre")
            sql = """select c.id, c.name, c.rating, d.genre, c.availability,c.year from movies c
                    inner join movies_genres d on c.id = d.movie_id
                    inner join movies_directors e on c.id = e.movie_id
                    inner join directors f on e.director_id = f.id
                    where f.last_name = %s 
                    and genre = %s"""
            val = (director_name, genre)
            TopMovies = get_queryResults(sql, val)

        elif actor_name != "" and genre != "" and director_name == "" and year == "":
            print("Actor Genre")
            sql = """select B.movie_id, c.name, c.rating, d.genre, c.availability,c.year from actors A
                    inner join roles B on A.id = B.actor_id
                    inner join movies c on B.movie_id = c.id
                    inner join movies_genres d on b.movie_id = d.movie_id
                    where a.last_name = %s
                    and genre = %s"""
            val = (actor_name, genre)
            print('test')
            TopMovies = get_queryResults(sql, val)

        return render_template('TopMovies.html', TopMovies=TopMovies)

# Get Top Five Directors
@app.route("/TopfiveDirectors", methods=['POST'])
def TopfiveDirectors():
    if request.method == 'POST':
        first_name = request.form['director']
        sql = """SELECT A.*, B.director_id, C.first_name, C.last_name from movies A, movies_directors B, 
        directors C where A.id = B.movie_id and B.director_id = C.id and rating is not NULL and C.first_name = %s 
        order by A.rating DESC LIMIT 5"""
        val = (first_name,)
        TopfiveDirectors = get_queryResults(sql, val)

        return render_template('TopDirectors.html', TopfiveDirectors=TopfiveDirectors)

# Get Top Five Movies of a Genre
@app.route("/TopfiveMovies", methods=['POST'])
def TopfiveMovies():
    if request.method == 'POST':
        genre = request.form['genres']

        sql = """select M.id, M.name, M.rating, G.genre, M.availability,M.year from movies M, movies_genres G 
        where M.id = G.movie_id  and rating is not NULL and genre = %s order by rating DESC LIMIT 5"""
        val = (genre,)
        TopMovies = get_queryResults(sql, val)

        return render_template('TopMovies.html', TopMovies=TopMovies)

# Update tables
@app.route("/update", methods=['POST'])
def update():
    if request.method == 'POST':

        directorID = request.form['directorID']
        directorlname = request.form['directorlname']

        movieID = request.form['movieID']
        movieRating = request.form['movieRating']
        movieAvail = request.form['movieAvail']
    
        conn = connectdb()
        cur = conn.cursor()
        if directorID != "" and directorlname !="":
            sql2 = "UPDATE directors SET last_name = %s WHERE id = %s"
            val2 = (directorlname, directorID)
            cur.execute(sql2, val2)

        if movieID != "" and movieRating !="":
            sql3 = "UPDATE movies SET rating = %s WHERE id = %s"
            val3 = (movieRating, movieID)
            cur.execute(sql3, val3)
        
        if movieID != "" and movieAvail !="":
            sql4 = "UPDATE movies SET availability = %s WHERE id = %s"
            val4 = (movieAvail, movieID)
            cur.execute(sql4, val4)
        
        if movieID != "" and movieAvail !="" and movieRating !="":
            sql5 = "UPDATE movies SET availability = %s, rating = %s WHERE id = %s"
            val5 = (movieAvail, movieRating, movieID)
            cur.execute(sql5, val5)

        conn.commit()

    return "Details Updated Successfully!!"

# Delete a Movie
@app.route("/delete", methods=['POST'])
def delete():
    if request.method == 'POST':

        ID = request.form['ID']    
        req = request.form['req']  
        conn = connectdb()
        cur = conn.cursor()

        if req == 'movie':
            sql = "DELETE FROM movies WHERE id = %s"
        elif req == 'director':
            sql = "DELETE FROM directors WHERE id = %s"
        else:
            sql = "DELETE FROM actors WHERE id = %s"

        val = (ID,)
        cur.execute(sql, val)
        conn.commit()

    return "Deleted Successfully!!"

if __name__ == "__main__":
  app.run('0.0.0.0', port=5002, debug=True)