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
    if request.method == 'POST':
        name = request.form['actor']
        return redirect(url_for('query', name=name))

    conn = connectdb()
    cur = conn.cursor()
    cur.execute('SELECT distinct last_name from actors')

    results = cur.fetchall()
    print(results)

    QueryDetails = []
    for i in results:
        QueryDetails.append(i[0])

    return render_template('index.html', QueryDetails=QueryDetails)
    # return "success"

@app.route("/query/<name>")
def query(name):
    conn = connectdb()
    cur = conn.cursor()
    cur.execute("SELECT * from actors  where last_name = '%s'" % name)
    final_results = cur.fetchall()

    return render_template('results.html', final_results=final_results)

@app.route("/select1", methods=['POST'])
def select1():
    if request.method == 'POST':
        querynum = list(request.form.to_dict().keys())[0]
        if querynum == 'query_1':
            conn = connectdb()
            cur = conn.cursor() 
            cur.execute("SELECT * from actors  where last_name = 'Parrish' and gender = 'F'")
            Query1_results = cur.fetchall()
            print(Query1_results)

            return render_template('query1.html', Query1_results=Query1_results)
        else:
            return("hello")

@app.route("/insert", methods=['POST'])
def insert():
    if request.method == 'POST':

        actorID = request.form['actorID']
        actorfname = request.form['actorfname']
        actorlname = request.form['actorlname']
        actorgender = request.form['actorgender']

        directorID = request.form['directorID']
        directorfname = request.form['directorfname']
        directorlname = request.form['directorlname']
    
        conn = connectdb()
        cur = conn.cursor()
        # cur.execute("INSERT INTO actors (actorID, actorfname, actorlname, id) VALUES (%s, %s, %s, %s)")

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
    
        conn = connectdb()
        cur = conn.cursor()
        # cur.execute("INSERT INTO actors (actorID, actorfname, actorlname, id) VALUES (%s, %s, %s, %s)")

        sql1 = "UPDATE actors SET first_name = %s WHERE id = %s"
        val1 = (actorfname, actorID)
        cur.execute(sql1, val1)

        sql2 = "UPDATE directors SET last_name = %s WHERE id = %s"
        val2 = (directorlname, directorID)
        cur.execute(sql2, val2)

        conn.commit()

    return "Success"

@app.route("/delete", methods=['POST'])
def delete():
    if request.method == 'POST':

        actorID = request.form['actorID']    
        conn = connectdb()
        cur = conn.cursor()
        # cur.execute("INSERT INTO actors (actorID, actorfname, actorlname, id) VALUES (%s, %s, %s, %s)")

        sql = "DELETE FROM actors WHERE id = %s"
        val = (actorID,)
        cur.execute(sql, val)
        conn.commit()

    return "Success"


if __name__ == "__main__":
  app.run(debug=True)