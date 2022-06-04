from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

db_connection = db.connect_to_database()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_woolleyw'
app.config['MYSQL_PASSWORD'] = '4911' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_woolleyw'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)

# Routes
@app.route('/')
def root():
    return render_template("main.j2")

# route for pokemon page
@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    # Create
    if request.method == "POST":
        name = request.form["name"]
        type_1 = request.form["type_1"]
        type_2 = request.form["type_2"]
        region = request.form["region_ID"]
        evolution = request.form["evolution_ID"]

        # account for null type_2 and null evolution
        if type_2 == "" and evolution == "":
            query = "INSERT INTO Pokemon (name, type_1, region_ID) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, type_1, region))
            mysql.connection.commit()

        # account for null type_2
        elif type_2 == "":
            query = "INSERT INTO Pokemon (name, type_1, region_ID, evolution_ID) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, type_1, region, evolution))
            mysql.connection.commit()

        # account for null evolution
        elif evolution == "":
            query = "INSERT INTO Pokemon (name, type_1, type_2, region_ID) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, type_1, type_2, region))
            mysql.connection.commit()

        # no null inputs
        else:
            query = "INSERT INTO Pokemon (name, type_1, type_2, region_ID, evolution_ID) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, type_1, type_2, region, evolution))
            mysql.connection.commit()

        return redirect("/pokemon")

    # Read
    if request.method == "GET":    
        query = "SELECT * FROM Pokemon;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("pokemon.j2", Pokemon=results)

# route for evolutions page
@app.route('/evolutions', methods=['GET', 'POST'])
def evolutions():
    # Create
    if request.method == "POST":
        name = request.form["name"]
        lvl = request.form["lvl"]
        item = request.form["item"]

        # account for null lvl and null item
        if lvl == "" and item == "":
            query = "INSERT INTO Evolutions (name) VALUES (%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name,))
            mysql.connection.commit()
        
        # account for null lvl
        elif lvl == "":
            query = "INSERT INTO Evolutions (name, item) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, item))
            mysql.connection.commit()

        # account for null item
        elif item == "":
            query = "INSERT INTO Evolutions (name, lvl) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, lvl))
            mysql.connection.commit()

        # no null inputs
        else:
            query = "INSERT INTO Evolutions (name, lvl, item) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, lvl, item))
            mysql.connection.commit()

        return redirect("/evolutions")

    # Read
    if request.method == "GET":
        query = "SELECT * FROM Evolutions;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("evolutions.j2", Evolutions=results)

# route for trainers page
@app.route('/trainers', methods=['GET', 'POST'])
def trainers():
    # Create
    if request.method == "POST":
        name = request.form["trainer_name"]
        region_ID = request.form["trainer_region"]
        trainer_type = request.form["trainer_type"]
        pokemon = request.form["num_pokemon"]

        query = "INSERT INTO Trainers (name, region_ID, type, pokemon) VALUES (%s, %s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (name, region_ID, trainer_type, pokemon))
        mysql.connection.commit()

        return redirect("/trainers")

    # Read
    if request.method == "GET":
        query = "SELECT * FROM Trainers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("trainers.j2", Trainers=results)

# route for regions page
@app.route('/regions', methods=['GET', 'POST'])
def regions():
    # Create
    if request.method == "POST":
        name = request.form["region_name"]
        climate = request.form["region_climate"]

        query = "INSERT INTO Regions (name, climate) VALUES (%s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (name, climate))
        mysql.connection.commit()

        return redirect("/regions")

    # Read
    if request.method == "GET":
        query = "SELECT * FROM Regions;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("regions.j2", Regions=results)

# route for pokemon_trainers page
@app.route('/pokemon_trainers', methods=['GET', 'POST'])
def pokemon_trainers():
    # Create
    if request.method == "POST":
        pokemon_ID = request.form["pokemon_ID"]
        trainer_ID = request.form["trainer_ID"]

        query = "INSERT INTO Pokemon_Trainers (pokemon_ID, trainer_ID) VALUES (%s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (pokemon_ID, trainer_ID))
        mysql.connection.commit()

        return redirect("/pokemon_trainers")

    #Read
    if request.method == "GET":
        query = "SELECT * FROM Pokemon_Trainers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("pokemon_trainers.j2", Pokemon_Trainers=results)

# Listener
if __name__ == "__main__":

    #Start the app on port 42813, it will be different once hosted
    app.run(port=41813, debug=True)