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

@app.route('/',methods=('GET', 'POST'))
def Initialize():
    conn = connectdb()
    cur = conn.cursor()
    cur.execute('SELECT distinct last_name from actors')
    actorslastnames = cur.fetchall()

    cur.execute('SELECT distinct last_name from directors')
    directorslastnames = cur.fetchall()

    cur.execute('SELECT distinct year from movies')
    moviesyear = cur.fetchall()

    cur.execute('SELECT distinct genre from movies_genres')
    movies_genres = cur.fetchall()

    # print(actorslastnames[:5])

    actordetails = []
    for i in actorslastnames:
        actordetails.append(i[0])
    
    directordetails = []
    for i in directorslastnames:
        directordetails.append(i[0])
    
    moviesdetails = []
    for i in moviesyear:
        moviesdetails.append(i[0])
    
    genredetails = []
    for i in movies_genres:
        genredetails.append(i[0])

    return render_template('index.html', actordetails=actordetails, directordetails=directordetails, moviesdetails=moviesdetails, genredetails=genredetails,)
    # return "success"

@app.route('/recommendations', methods=('GET', 'POST'))
def recommendations():
    if request.method == 'POST':
        actor_name = request.form['actor']
        director_name = request.form['director']
        year = request.form['year']
        genre = request.form['genre']

        if actor_name == "" and director_name == "" and year == "" and genre == "":
            conn = connectdb()
            cur = conn.cursor()
            sql = "SELECT * from movies where rating != 'NULL' order by rating DESC" 
            val = (year, 7)
            cur.execute(sql, val)
            moviedetails = cur.fetchall()
            moviedetails = moviedetails[:5]

            return render_template('results.html', moviedetails=moviedetails)
            
        conn = connectdb()
        cur = conn.cursor()
        sql = "SELECT * from movies  where year = %s and rating >= '%s' and rating != 'NULL' order by rating DESC" 
        val = (year, 7)
        cur.execute(sql, val)
        moviedetails = cur.fetchall()
        moviedetails = moviedetails[:5]

        return render_template('results.html', moviedetails=moviedetails)

@app.route('/rent', methods=('GET', 'POST'))
def rent():
    if request.method == 'POST':
        
        print("hi")
        movieID = request.form['movieID']
        print(movieID)
        conn = connectdb()
        cur = conn.cursor()
        sql = "UPDATE movies SET availability = 'No' WHERE id = %s"
        val = (movieID,)
        cur.execute(sql, val)
        conn.commit()

        return "Success"

@app.route('/getdetails', methods=('GET', 'POST'))
def getdetails():
    if request.method == 'POST':
        
        movieID = request.form['movieID']
        print(movieID)
        conn = connectdb()
        cur = conn.cursor()
        sql = "SELECT * from movies where id = %s" 
        val = (movieID,)
        cur.execute(sql, val)
        moviedetails = cur.fetchall()

        return render_template('results.html', moviedetails=moviedetails)

@app.route("/insert", methods=['POST'])
def insert():
    if request.method == 'POST':

        movieID = request.form['movieID']
        moviename = request.form['moviename']
        year = request.form['year']
        genre = request.form['genre']
        rating = request.form['rating']
        actorID = request.form['actorID']
        actorfname = request.form['actorfname']
        actorlname = request.form['actorlname']
        actorgender = request.form['actorgender']
        actorrole = request.form['actorrole']
        directorID = request.form['directorID']
        directorfname = request.form['directorfname']
        directorlname = request.form['directorlname']
    
        conn = connectdb()
        cur = conn.cursor()
        # cur.execute("INSERT INTO actors (actorID, actorfname, actorlname, id) VALUES (%s, %s, %s, %s)")

        # Inserting Movie
        sql1 = "INSERT INTO actors (id, first_name, last_name, gender) VALUES (%s, %s, %s, %s)"
        val1 = (actorID, actorfname, actorlname, actorgender)
        cur.execute(sql1, val1)


        sql1 = "INSERT INTO actors (id, first_name, last_name, gender) VALUES (%s, %s, %s, %s)"
        val1 = (actorID, actorfname, actorlname, actorgender)
        cur.execute(sql1, val1)


        sql2 = "INSERT INTO directors (id, first_name, last_name) VALUES (%s, %s, %s)"
        val2 = (directorID, directorfname, directorlname)
        cur.execute(sql2, val2)

        conn.commit()

    return "Success"

@app.route("/update", methods=['POST'])
def update():
    if request.method == 'POST':

        actorID = request.form['actorID']
        actorfname = request.form['actorfname']

        directorID = request.form['directorID']
        directorlname = request.form['directorlname']

        movieID = request.form['movieID']
        movieRating = request.form['movieRating']
    
        conn = connectdb()
        cur = conn.cursor()
        # cur.execute("INSERT INTO actors (actorID, actorfname, actorlname, id) VALUES (%s, %s, %s, %s)")

        if actorID != "" or actorfname !="":
            sql1 = "UPDATE actors SET first_name = %s WHERE id = %s"
            val1 = (actorfname, actorID)
            cur.execute(sql1, val1)

        if directorID != "" or directorlname !="":
            sql2 = "UPDATE directors SET last_name = %s WHERE id = %s"
            val2 = (directorlname, directorID)
            cur.execute(sql2, val2)

        if movieID != "" or movieRating !="":
            sql3 = "UPDATE movies SET rating = %s WHERE id = %s"
            val3 = (movieRating, movieID)
            cur.execute(sql3, val3)

        conn.commit()

    return "Success"

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

    return "Success"


@app.route("/TopfiveDirectors", methods=['POST'])
def TopfiveDirectors():
    if request.method == 'POST':
        
        conn = connectdb()
        cur = conn.cursor() 
        cur.execute("")
        Query1_results = cur.fetchall()
        print(Query1_results)

        return render_template('results.html', Query1_results=Query1_results)

@app.route("/TopfiveMovies", methods=['POST'])
def TopfiveMovies():
    if request.method == 'POST':
        genre = request.form['genres']
        conn = connectdb()
        cur = conn.cursor() 

        sql = "select M.id, M.name, M.rating, G.genre, M.availability from movies M, movies_genres G where M.id = G.movie_id  and rating != 'NULL' and genre = %s order by rating DESC"
        val = (genre,)
        cur.execute(sql, val)
        TopMovies = cur.fetchall()
        TopMovies = TopMovies[:5]
        print(TopMovies)

        return render_template('TopMovies.html', TopMovies=TopMovies)

if __name__ == "__main__":
  app.run('0.0.0.0', port=5001, debug=True)