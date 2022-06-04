from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

db_connection = db.connect_to_database()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_solimanj'
app.config['MYSQL_PASSWORD'] = '7937' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_solimanj'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)

# Routes
@app.route('/')
def root():
    return render_template("main.j2")

# route for pokemon page
@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    if request.method == "POST":
        name = request.form["name"]
        type_1 = request.form["type_1"]
        type_2 = request.form["type_2"]
        region = request.form["region"]
        evolution = request.form["evolution"]
        # account for null type_2 and null evolution
        if type_2 == "" and evolution == "":
            query = "INSERT INTO Pokemon (name, type_1, region) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, type_1, region))
            mysql.connection.commit()

        # account for null type_2
        elif type_2 == "":
            query = "INSERT INTO Pokemon (name, type_1, region, evolution) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, type_1, region, evolution))
            mysql.connection.commit()

        # account for null evolution
        elif evolution == "":
            query = "INSERT INTO Pokemon (name, type_1, type_2, region) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, type_1, type_2, region))
            mysql.connection.commit()

        # no null inputs
        else:
            query = "INSERT INTO Pokemon (name, type_1, type_2, region, evolution) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, type_1, type_2, region, evolution))
            mysql.connection.commit()

        return redirect("/pokemon")

    if request.method == "GET":    
        query = "SELECT * FROM Pokemon;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("pokemon.j2", Pokemon=results)

# route for evolutions page
@app.route('/evolutions')
def evolutions():
    query = "SELECT * FROM Evolutions;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("evolutions.j2", Evolutions=results)

# route for trainers page
@app.route('/trainers')
def trainers():
    query = "SELECT * FROM Trainers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("trainers.j2", Trainers=results)

# route for regions page
@app.route('/Regions')
def regions():
    query = "SELECT * FROM Regions;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("regions.j2", Regions=results)

# route for pokemon_trainers page
@app.route('/Pokemon_Trainers')
def pokemon_trainers():
    query = "SELECT * FROM Pokemon_Trainers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("pokemon_trainers.j2", Pokemon_Trainers=results)

# Listener
if __name__ == "__main__":

    #Start the app on port 42813, it will be different once hosted
    app.run(port=42813, debug=True)