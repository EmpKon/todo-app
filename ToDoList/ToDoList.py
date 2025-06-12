from flask import Flask, redirect, render_template, request, jsonify
import sqlite3

app = Flask(__name__, static_url_path='', static_folder='static')
con = sqlite3.connect("tasks.db")

cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, Task TEXT, Status TEXT)")
cursor.close()


@app.route("/")
def appgoeshere():
    return render_template("index.html")

@app.route("/addData", methods=["POST"]) #Route for adding tasks into the database
def addData():
    data = request.get_json()
    con = sqlite3.connect("tasks.db")
    cursor = con.cursor()
    taskname = data["value"]
    print(cursor.execute(f"INSERT INTO tasks (Task, Status) VALUES ('{taskname}', 'Incomplete')"))
    cursor.close()
    con.commit()
    con.close()
    getData()
    return jsonify()

@app.route("/getData", methods=["GET"]) #Route for getting data from the db, returns everything in the database
def getData():
    con = sqlite3.connect("tasks.db")   
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tasks")
    DBData = cursor.fetchall()
    print(DBData)
    return jsonify(DBData)




if __name__=="__main__":
    app.run()