from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route("/")
def appgoeshere():
    return render_template("index.html")

@app.route("/addData", methods=["POST"])
def addData():
    data = request.get_json()
    #sql goes here




if __name__=="__main__":
    app.run()