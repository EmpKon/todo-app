from flask import Flask, redirect, render_template, request, jsonify
import sqlite3

app = Flask(__name__, static_url_path='', static_folder='static')
con = sqlite3.connect("tasks.db")

cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (Pos INTEGER, Task TEXT, Status TEXT)")
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
    cursor.execute(f"SELECT COUNT(*) FROM tasks") #Gets the amount of items in the database
    itemcount = cursor.fetchone()[0]
    cursor.execute(f"INSERT INTO tasks (Pos, Task, Status) VALUES (?,?,?)",
    (itemcount + 1, taskname, "not_started")
    )
    cursor.close()
    con.commit()
    con.close()
    getData()
    return jsonify()


@app.route("/removeData", methods=["POST"]) #Route for removing tasks from the database
def removeData():
    data = request.get_json()
    taskPos = data["pos"]
    con = sqlite3.connect("tasks.db")
    cursor = con.cursor()
    cursor.execute(f"Delete FROM tasks WHERE Pos=?",
    (taskPos))
    cursor.execute(f"UPDATE tasks SET Pos = Pos - 1 WHERE Pos > ?",
    (taskPos))
    cursor.close()
    con.commit()
    con.close()
    getData()
    return jsonify()

@app.route("/cycleStatus", methods=["POST"]) #Route for changing the status of the task
def cycleStatus():
    data = request.get_json()
    taskPos = data["Pos"]
    status = data["status"]
    con = sqlite3.connect("tasks.db")
    cursor = con.cursor()
    cursor.execute(f"UPDATE tasks SET Status = '?' WHERE Pos=?",
    (status, taskPos))
    cursor.close()
    con.commit()
    con.close()
    getData()
    return jsonify()
    

@app.route("/getData", methods=["GET"]) #Route for getting data from the db, returns everything in the database
def getData():
    con = sqlite3.connect("tasks.db")   
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY Pos")
    DBData = cursor.fetchall()
    return jsonify(DBData)

@app.route("/moveTask", methods=["POST"]) #Route for reordering a task
def moveTask():
    data = request.get_json()
    direction = data["direction"]
    pos = data["pos"]
    con = sqlite3.connect("tasks.db")
    cursor = con.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM tasks")
    itemcount = cursor.fetchone()[0]
    if direction == "down" and pos == itemcount or direction == "up" and pos == 1:
        pass
    else:
        cursor.execute(f"UPDATE tasks SET Pos = '0' WHERE Pos={pos}")
        if direction == "down":
            cursor.execute(f"UPDATE tasks SET Pos = '{pos}' WHERE Pos={pos+1}")
            cursor.execute(f"UPDATE tasks SET Pos = '{pos+1}' WHERE Pos=0")
        else:
            cursor.execute(f"UPDATE tasks SET Pos = '{pos}' WHERE Pos={pos-1}")
            cursor.execute(f"UPDATE tasks SET Pos = '{pos-1}' WHERE Pos=0")
    cursor.close()
    con.commit()
    con.close()
    getData()
    return jsonify()


if __name__=="__main__":
    app.run()