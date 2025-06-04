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

@app.route("/addData", methods=["POST"])
def addData():
    data = request.get_json()
    con = sqlite3.connect("tasks.db")
    cursor = con.cursor()
    cursor.execute(f"INSERT INTO tasks (Task, Status) VALUES ('{data["value"]}', 'Incomplete')")
    cursor.close()
    con.close()
    return jsonify()



if __name__=="__main__":
    app.run()