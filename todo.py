from flask import Flask, redirect, render_template, request, jsonify
import sqlite3
import re
from werkzeug.exceptions import BadRequest

app = Flask(__name__, static_url_path='', static_folder='static')
con = sqlite3.connect("tasks.db")

cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (Pos INTEGER, Task TEXT, Status TEXT)")
cursor.close()
con.close()

def isPositiveInt(val):
    return (isinstance(val,int) and val>0 and not isinstance(val,bool))

def getJsonData():
    if not request.is_json:
        return None, (jsonify({"error": "Content-Type must be application/json"}), 415)

    try:
        data = request.get_json()
    
    except BadRequest:
        return None, (jsonify({"error": "Invalid JSON"}), 400)

    return data, None

@app.route("/")
def appgoeshere():
    return render_template("index.html")

#TODO RESTful APIs
@app.route("/data", methods=["POST"])
def addData():
    data, error = getJsonData()
    if error:
        return error

    taskname = data.get("value")

    if not isinstance(taskname, str):
        return jsonify({"error": "Task name must be a string"}), 400

    taskname = taskname.strip()

    if not taskname:
        return jsonify({"error": "Task cannot be empty"}), 400

    if len(taskname) >= 150:
        return jsonify({"error": "Task must be less than 150 characters"}), 400

    if not (re.fullmatch("[a-zA-ZäöåÄÖÅ0-9!?,. ]+", taskname)):
        return jsonify({"error": "Task must consist of only standard letters and symbols"}), 400
    
    con = sqlite3.connect("tasks.db")
    
    try:
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM tasks")
        itemcount = cursor.fetchone()[0]

        pos = itemcount + 1
        cursor.execute("INSERT INTO tasks (Pos, Task, Status) VALUES (?,?,?)",
            (pos, taskname, "not_started")
        )

        con.commit()
    
        return jsonify({
            "pos": itemcount+1,
            "taskname": taskname,
            "status": "not_started"
        }), 201
    finally:
        con.close()


@app.route("/data", methods=["DELETE"])
def removeData():
    data, error = getJsonData()
    if error:
        return error

    taskPos = data.get("pos")
    if not isPositiveInt(taskPos):
        return jsonify({"error": "Task position must be positive"}), 400
    
    con = sqlite3.connect("tasks.db")
    try:
        cursor = con.cursor()
        cursor.execute(
            "Delete FROM tasks WHERE Pos=?", 
            (taskPos,)
        ) #Sqlite3.execute requires a sequence of parameters, single item tuple required

        cursor.execute(
            "UPDATE tasks SET Pos = Pos - 1 WHERE Pos > ?",
            (taskPos,)
        )
        con.commit()

        return jsonify()
    finally:
        con.close()

validStatuses = {"not_started", "in_progress", "completed"}

@app.route("/cycleStatus", methods=["POST"])
def cycleStatus():
    data, error = getJsonData()
    if error:
        return error

    taskPos = data.get("pos")
    status = data.get("status")

    if not isPositiveInt(taskPos):
        return jsonify({"error": "Task position must be positive"}), 400

    if not isinstance(status, str) or status not in validStatuses:
        return jsonify({
            "error": "Invalid status",
            "allowed": list(validStatuses) #Can't process python sets, typecast into a list
        }), 400
    
    con = sqlite3.connect("tasks.db")
    try:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE tasks SET Status = ? WHERE Pos=?",
            (status, taskPos)
        )

        con.commit()
        return jsonify({"message": "Status updated"}), 200
    finally:
        con.close()
    

@app.route("/getData", methods=["GET"]) #Route for getting data from the db, returns everything in the database
def getData():
    con = sqlite3.connect("tasks.db")   
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY Pos")
    DBData = cursor.fetchall()
    con.close()
    return jsonify(DBData)

@app.route("/moveTask", methods=["POST"]) #Route for reordering a task
def moveTask():
    data, error = getJsonData()
    if error:
        return error

    direction = data.get("direction")
    taskPos = data.get("pos")
    if not isPositiveInt(taskPos):
        return jsonify({"error": "Task position must be positive"}), 400

    if direction not in ("up", "down"):
        return jsonify({
            "error": "direction must be up or down"
        }), 400
    
    con = sqlite3.connect("tasks.db")
    try:
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM tasks")
        itemcount = cursor.fetchone()[0]

        if taskPos > itemcount:
            return jsonify({"error": "Task not found"}), 404

        if (direction == "up" and taskPos == 1) or (direction == "down" and taskPos == itemcount):
            return jsonify({"error": "Task is already at boundary"}), 200

        cursor.execute("UPDATE tasks SET Pos = 0 WHERE Pos = ?", (taskPos,)) #Temporarily move task to pos 0 to avoid a seperate check


        if direction == "down":
            cursor.execute("UPDATE tasks SET Pos = ? WHERE Pos = ?",
            (taskPos, taskPos+1))

            cursor.execute("UPDATE tasks SET Pos = ? WHERE Pos = 0",
                (taskPos+1,))
            
        else:
            cursor.execute("UPDATE tasks SET Pos = ? WHERE Pos = ?",
            (taskPos, taskPos-1))

            cursor.execute("UPDATE tasks SET Pos = ? WHERE Pos = 0",
            (taskPos-1,))
        
        con.commit()
        return jsonify({"message": "Task reordered"}), 200
    finally:
        con.close()


if __name__=="__main__":
    app.run()